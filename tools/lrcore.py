"""Minimal headless libretro frontend (ctypes): loads one core, feeds it a ROM and joypad input, collects frames.
No window, no audio, no SDL. Used by the NES, SNES, Master System, Mega Drive, DOS, Apple II, Amiga, C64 and PlayStation backends in platforms.py (cores built by tools/setup_emu.sh).

  c = Core("tools/mesen/Libretro/mesen_libretro.so", "rom/game.nes", options={"mesen_region": "NTSC"})
  c.keys = {"a", "right"}; c.run(60); c.png("x.png"); s = c.serialize(); c.unserialize(s); c.close()

A libretro core keeps its state in globals, so one loaded library = one running game. A second Core in the same
process loads a private copy of the .so (dlopen of the same path would share the globals).
"""
import atexit, ctypes as C, io, os, shutil, struct, tempfile, weakref

TRAILER = b"GAMEDB-FRAME-1"


class GameInfo(C.Structure):
    _fields_ = [("path", C.c_char_p), ("data", C.c_void_p), ("size", C.c_size_t), ("meta", C.c_char_p)]


class Variable(C.Structure):
    _fields_ = [("key", C.c_char_p), ("value", C.c_char_p)]


ENV = C.CFUNCTYPE(C.c_bool, C.c_uint, C.c_void_p)
VIDEO = C.CFUNCTYPE(None, C.c_void_p, C.c_uint, C.c_uint, C.c_size_t)
AUDIO = C.CFUNCTYPE(None, C.c_int16, C.c_int16)
AUDIO_BATCH = C.CFUNCTYPE(C.c_size_t, C.c_void_p, C.c_size_t)
POLL = C.CFUNCTYPE(None)
INPUT = C.CFUNCTYPE(C.c_int16, C.c_uint, C.c_uint, C.c_uint, C.c_uint)

# RETRO_DEVICE_ID_JOYPAD_*
JOYPAD = {"b": 0, "y": 1, "select": 2, "start": 3, "up": 4, "down": 5, "left": 6, "right": 7, "a": 8, "x": 9,
          "l": 10, "r": 11, "l2": 12, "r2": 13, "l3": 14, "r3": 15}
ENV_GET_SYSTEM_DIRECTORY, ENV_SET_PIXEL_FORMAT, ENV_GET_VARIABLE, ENV_SET_VARIABLES = 9, 10, 15, 16
ENV_GET_VARIABLE_UPDATE, ENV_GET_SAVE_DIRECTORY = 17, 31
ENV_SET_KEYBOARD_CALLBACK, ENV_GET_PERF_INTERFACE, ENV_SET_MEMORY_MAPS, ENV_GET_THROTTLE_STATE = 12, 28, 36, 71
DEVICE_JOYPAD, DEVICE_MOUSE, DEVICE_KEYBOARD = 1, 2, 3
MOUSE_BUTTONS = {"mouse1": 2, "mouse2": 3, "mouse3": 6}      # RETRO_DEVICE_ID_MOUSE_LEFT / RIGHT / MIDDLE
KEY_EVENT = C.CFUNCTYPE(None, C.c_bool, C.c_uint, C.c_uint32, C.c_uint16)
TIME_USEC = C.CFUNCTYPE(C.c_int64)


class MemDesc(C.Structure):
    _fields_ = [("flags", C.c_uint64), ("ptr", C.c_void_p), ("offset", C.c_size_t), ("start", C.c_size_t),
                ("select", C.c_size_t), ("disconnect", C.c_size_t), ("len", C.c_size_t), ("addrspace", C.c_char_p)]


class MemMap(C.Structure):
    _fields_ = [("descriptors", C.POINTER(MemDesc)), ("num", C.c_uint)]


class Throttle(C.Structure):
    _fields_ = [("mode", C.c_uint), ("rate", C.c_float)]
MEM_SAVE_RAM, MEM_SYSTEM_RAM = 0, 2
FMT_XRGB8888 = 1

_in_use = set()          # .so paths (originals) with a live Core
_copies = []             # temp dirs of private copies
_live = weakref.WeakSet()
_pending = []            # (library handle, temp dir) of the last private copy closed, unloaded one close later


def _unload_pending():
    import _ctypes
    while _pending:
        handle, d = _pending.pop()
        try:
            _ctypes.dlclose(handle)
        except OSError:
            pass
        shutil.rmtree(d, ignore_errors=True)
        if d in _copies:
            _copies.remove(d)


@atexit.register
def _close_all():
    """A core with its own emulation thread (DOSBox Pure) blocks the interpreter's exit while a game is loaded:
    unload whatever a failed script left open."""
    for c in list(_live):
        try:
            c.close()
        except Exception:
            pass


class Core:
    def __init__(self, so, rom, options=None, system_dir=None, save_dir=None, frame_usec=None, epoch=None,
                 private=False, defaults=False, av_info=False):
        """frame_usec: give the core a virtual clock that advances this many microseconds per run() frame
        (computer cores read the host clock for pacing; with the virtual one a route does not depend on how
        fast the host is). None = the core's own clock (consoles).
        epoch: Unix time of power-on for cores built with retro_gamedb_set_time (tools/dosbox-pure-debug.patch):
        the emulated machine's date and time start there and follow the virtual clock.
        private: always load a private copy of the library (cores that cannot load a second game after
        unloading the first: DOSBox Pure crashes on its first frame then; AppleWin keeps its cycle counter).
        rom None: start the core without content.
        defaults: answer options the backend does not set with the core's own default (the first value it
        announces with SET_VARIABLES), as a real frontend does; without it such options are left unanswered
        (the VICE core then sets the picture's brightness, contrast and gamma to 0: a black screen).
        av_info: ask the core for its audio/video timing after loading, as a real frontend does (VICE sets
        its sample rate and frame rate there)."""
        so = os.path.abspath(so)
        self.so = so
        if private or so in _in_use:            # second instance: private copy of the library
            d = tempfile.mkdtemp(prefix="lrcore")
            _copies.append(d)
            self._private_dir = d
            path = shutil.copy(so, d)
            self._shared = False
        else:
            path = so
            _in_use.add(so)
            self._shared = True
        self.L = L = C.CDLL(path)
        self.options = {k.encode(): v.encode() for k, v in (options or {}).items()}
        self._defaults = {} if defaults else None       # key -> c_char_p of the core's default value
        self._dirs = {ENV_GET_SYSTEM_DIRECTORY: (system_dir or tempfile.gettempdir()).encode(),
                      ENV_GET_SAVE_DIRECTORY: (save_dir or tempfile.gettempdir()).encode()}
        self.fmt, self.keys, self._held, self.frame, self.open = 0, set(), set(), None, False
        self._mheld, self._mouse, self._kheld = set(), [0, 0], set()
        self.size = None                        # (w, h) for the picture before the first frame
        self.frame_usec, self.clock = frame_usec, 0
        self._key_event, self.maps = None, []   # keyboard callback of the core; memory map [(start, len, ptr)]
        self.mouse = [0, 0]                     # relative motion reported during the next frame
        self._time = TIME_USEC(lambda: self.clock)
        self._cbs = (ENV(self._env), VIDEO(self._video), AUDIO(lambda l, r: None), AUDIO_BATCH(lambda d, n: n),
                     POLL(lambda: None), INPUT(self._input))       # keep references: ctypes callbacks
        L.retro_load_game.restype = C.c_bool
        L.retro_serialize_size.restype = C.c_size_t
        L.retro_serialize.restype = L.retro_unserialize.restype = C.c_bool
        L.retro_get_memory_data.restype = C.c_void_p
        L.retro_get_memory_size.restype = C.c_size_t
        self.epoch = epoch
        self._sync = getattr(L, "retro_gamedb_sync", None)
        if epoch is not None:
            L.retro_gamedb_set_time.argtypes = [C.c_int64]
            L.retro_gamedb_set_time(epoch * 1000000)
        L.retro_set_environment(self._cbs[0])
        L.retro_init()
        L.retro_set_video_refresh(self._cbs[1])
        L.retro_set_audio_sample(self._cbs[2])
        L.retro_set_audio_sample_batch(self._cbs[3])
        L.retro_set_input_poll(self._cbs[4])
        L.retro_set_input_state(self._cbs[5])
        if rom is None:                         # cores that start without content (the backend inserts disks)
            ok = L.retro_load_game(None)
        else:
            self._rom = open(rom, "rb").read()
            gi = GameInfo(os.path.abspath(rom).encode(), C.cast(C.c_char_p(self._rom), C.c_void_p), len(self._rom),
                          None)
            ok = L.retro_load_game(C.byref(gi))
        if not ok:
            self._release()
            raise RuntimeError("the core refused %s (unsupported mapper or bad dump?)" % rom)
        if av_info:
            self.av = C.create_string_buffer(64)        # struct retro_system_av_info (40 bytes)
            L.retro_get_system_av_info(self.av)
        self.open = True
        _live.add(self)

    # ---- callbacks
    def _env(self, cmd, data):
        cmd &= 0xFFFF
        if cmd == ENV_SET_PIXEL_FORMAT:
            self.fmt = C.cast(data, C.POINTER(C.c_int))[0]
            return True
        if cmd in self._dirs:
            C.cast(data, C.POINTER(C.c_char_p))[0] = self._dirs[cmd]
            return True
        if cmd == ENV_GET_VARIABLE:
            v = C.cast(data, C.POINTER(Variable))[0]
            if v.key in self.options:
                v.value = self.options[v.key]
                return True
            if self._defaults and v.key in self._defaults:
                v.value = self._defaults[v.key]
                return True
            v.value = None                      # the core keeps its default
            return False
        if cmd == ENV_SET_VARIABLES and self._defaults is not None:
            arr = C.cast(data, C.POINTER(Variable))
            i = 0
            while arr[i].key:
                desc = arr[i].value or b""
                if b"; " in desc:               # "Description; default|other|other"
                    self._defaults[arr[i].key] = desc.split(b"; ", 1)[1].split(b"|")[0]
                i += 1
            return True
        if cmd == ENV_SET_KEYBOARD_CALLBACK:
            self._key_event = KEY_EVENT(C.cast(data, C.POINTER(C.c_void_p))[0])
            return True
        if cmd == ENV_GET_PERF_INTERFACE and self.frame_usec:
            C.memset(data, 0, 7 * C.sizeof(C.c_void_p))             # retro_perf_callback: only get_time_usec
            C.cast(data, C.POINTER(C.c_void_p))[0] = C.cast(self._time, C.c_void_p).value
            return True
        if cmd == ENV_GET_THROTTLE_STATE and self.frame_usec:
            t = C.cast(data, C.POINTER(Throttle))[0]
            t.mode, t.rate = 0, 0.0             # RETRO_THROTTLE_NONE, rate unknown: the core never skips a frame
            return True
        if cmd == ENV_SET_MEMORY_MAPS:
            m = C.cast(data, C.POINTER(MemMap))[0]
            self.maps = [(d.start, d.len, d.ptr) for d in (m.descriptors[i] for i in range(m.num)) if d.ptr]
            return True
        if cmd == ENV_GET_VARIABLE_UPDATE:
            C.cast(data, C.POINTER(C.c_bool))[0] = False
            return True
        return False

    def _video(self, data, w, h, pitch):
        if data:
            self.frame = (w, h, pitch, C.string_at(data, pitch * h))

    def _input(self, port, device, index, ident):
        if port:
            return 0
        if device == DEVICE_JOYPAD:
            return 1 if ident in self._held else 0
        if device == DEVICE_KEYBOARD:           # cores poll this to release keys that are no longer held
            return 1 if ident in self._kheld else 0
        if device == DEVICE_MOUSE:
            return self._mouse[ident] if ident < 2 else (1 if ident in self._mheld else 0)
        return 0

    def key(self, code, down, char=0, mods=0):
        """Keyboard event (RETROK_* code) for cores that registered a keyboard callback."""
        if self._key_event is None:
            raise RuntimeError("this core takes no keyboard events")
        (self._kheld.add if down else self._kheld.discard)(code)
        self._key_event(down, code, char, mods)

    # ---- running
    def run(self, n=1):
        self._held = {JOYPAD[k] for k in self.keys if k in JOYPAD}
        self._mheld = {MOUSE_BUTTONS[k] for k in self.keys if k in MOUSE_BUTTONS}
        self._mouse, self.mouse = self.mouse, [0, 0]
        for _ in range(n):
            self.clock += self.frame_usec or 0
            if self.epoch is not None:
                self.L.retro_gamedb_set_time(self.epoch * 1000000 + self.clock)
            self.L.retro_run()
            if self._sync:
                self._sync()                    # threaded core: park the emulation thread at the frame end
            self._mouse = [0, 0]                # motion is relative: report it for one frame only

    def peek_map(self, addr, n):
        """n bytes at addr of the address space the core announced (SET_MEMORY_MAPS); unmapped bytes read 0."""
        out = bytearray(n)
        for start, size, ptr in self.maps:
            lo, hi = max(addr, start), min(addr + n, start + size)
            if lo < hi:
                out[lo - addr:hi - addr] = C.string_at(ptr + lo - start, hi - lo)
        return bytes(out)

    def poke_map(self, addr, data):
        for start, size, ptr in self.maps:
            lo, hi = max(addr, start), min(addr + len(data), start + size)
            if lo < hi:
                C.memmove(ptr + lo - start, bytes(data[lo - addr:hi - addr]), hi - lo)

    def image(self):
        from PIL import Image
        if self.frame is None:                  # nothing drawn yet (power-on): black, never advance emulation
            return Image.new("RGB", self.size or (256, 240))
        w, h, pitch, d = self.frame
        if self.fmt == FMT_XRGB8888:
            return Image.frombuffer("RGB", (w, h), d, "raw", "BGRX", pitch, 1)
        return Image.frombuffer("RGB", (w, h), d, "raw", "BGR;16", pitch, 1)      # RGB565

    def png_bytes(self):
        b = io.BytesIO()
        self.image().save(b, "PNG")
        return b.getvalue()

    def png(self, path):
        self.image().save(path, "PNG")

    # ---- state and memory
    # A savestate file is the core's own serialized state followed by a trailer with the frame on screen
    # (frame bytes, then w, h, pitch, pixel format, frame length, magic). A core does not keep the picture in
    # its state, so without the trailer a screenshot right after a load would need one more emulated frame and
    # a route would differ by a frame between "just played" and "loaded from the cache".
    def serialize(self):
        n = self.L.retro_serialize_size()
        buf = C.create_string_buffer(n)
        if not self.L.retro_serialize(buf, C.c_size_t(n)):
            raise RuntimeError("savestate failed")
        if self.frame is None:
            return buf.raw
        w, h, pitch, d = self.frame
        return buf.raw + d + struct.pack("<5I", w, h, pitch, self.fmt, len(d)) + TRAILER

    def unserialize(self, data):
        frame = None
        if data.endswith(TRAILER):
            w, h, pitch, fmt, n = struct.unpack("<5I", data[-len(TRAILER) - 20:-len(TRAILER)])
            end = len(data) - len(TRAILER) - 20
            frame, self.fmt = (w, h, pitch, data[end - n:end]), fmt
            data = data[:end - n]
        if not self.L.retro_unserialize(data, C.c_size_t(len(data))):
            raise RuntimeError("the core refused the savestate (made by another core version or ROM?)")
        self.frame = frame

    def memory(self, kind):
        """A live ctypes view of a libretro memory region (MEM_SYSTEM_RAM, MEM_SAVE_RAM), or None."""
        n, p = self.L.retro_get_memory_size(kind), self.L.retro_get_memory_data(kind)
        return (C.c_ubyte * n).from_address(p) if p and n else None

    def _release(self):
        self.L.retro_deinit()
        if self._shared:
            _in_use.discard(self.so)
        else:
            # A private copy is never used again: unload it and delete the file. Without this every game
            # opened kept its whole machine in memory (DOSBox Pure: about 40 MB each; a 250-shot verify was
            # killed for lack of memory, 2026-11-18). Not at once: a core with its own emulation thread may
            # still be leaving that thread when unload returns, and unmapping its code then crashes (seen as
            # a rare segfault in the tests). The copy closed before this one is unloaded now; this one waits.
            _unload_pending()
            _pending.append((self.L._handle, self._private_dir))

    def close(self):
        if self.open:
            self.open = False
            self.L.retro_unload_game()
            self._release()

    def __del__(self):
        """A core dropped without close() must not stay loaded until the process ends: AppleWin's own exit
        handlers then use freed memory (seen as a random abort at interpreter exit, 2026-11-18)."""
        try:
            self.close()
        except Exception:
            pass
