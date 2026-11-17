"""Minimal headless libretro frontend (ctypes): loads one core, feeds it a ROM and joypad input, collects frames.
No window, no audio, no SDL. Used by the NES backend in platforms.py (Mesen core, built by tools/setup_emu.sh).

  c = Core("tools/mesen/Libretro/mesen_libretro.so", "rom/game.nes", options={"mesen_region": "NTSC"})
  c.keys = {"a", "right"}; c.run(60); c.png("x.png"); s = c.serialize(); c.unserialize(s); c.close()

A libretro core keeps its state in globals, so one loaded library = one running game. A second Core in the same
process loads a private copy of the .so (dlopen of the same path would share the globals).
"""
import ctypes as C, io, os, shutil, tempfile


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
          "l": 10, "r": 11}
ENV_GET_SYSTEM_DIRECTORY, ENV_SET_PIXEL_FORMAT, ENV_GET_VARIABLE = 9, 10, 15
ENV_GET_VARIABLE_UPDATE, ENV_GET_SAVE_DIRECTORY = 17, 31
MEM_SAVE_RAM, MEM_SYSTEM_RAM = 0, 2
FMT_XRGB8888 = 1

_in_use = set()          # .so paths (originals) with a live Core
_copies = []             # temp dirs of private copies


class Core:
    def __init__(self, so, rom, options=None, system_dir=None, save_dir=None):
        so = os.path.abspath(so)
        self.so = so
        if so in _in_use:                       # second instance: private copy of the library
            d = tempfile.mkdtemp(prefix="lrcore")
            _copies.append(d)
            path = shutil.copy(so, d)
            self._shared = False
        else:
            path = so
            _in_use.add(so)
            self._shared = True
        self.L = L = C.CDLL(path)
        self.options = {k: v.encode() for k, v in (options or {}).items()}
        self._dirs = {ENV_GET_SYSTEM_DIRECTORY: (system_dir or tempfile.gettempdir()).encode(),
                      ENV_GET_SAVE_DIRECTORY: (save_dir or tempfile.gettempdir()).encode()}
        self.fmt, self.keys, self._held, self.frame, self.open = 0, set(), set(), None, False
        self._cbs = (ENV(self._env), VIDEO(self._video), AUDIO(lambda l, r: None), AUDIO_BATCH(lambda d, n: n),
                     POLL(lambda: None), INPUT(self._input))       # keep references: ctypes callbacks
        L.retro_load_game.restype = C.c_bool
        L.retro_serialize_size.restype = C.c_size_t
        L.retro_serialize.restype = L.retro_unserialize.restype = C.c_bool
        L.retro_get_memory_data.restype = C.c_void_p
        L.retro_get_memory_size.restype = C.c_size_t
        L.retro_set_environment(self._cbs[0])
        L.retro_init()
        L.retro_set_video_refresh(self._cbs[1])
        L.retro_set_audio_sample(self._cbs[2])
        L.retro_set_audio_sample_batch(self._cbs[3])
        L.retro_set_input_poll(self._cbs[4])
        L.retro_set_input_state(self._cbs[5])
        self._rom = open(rom, "rb").read()
        gi = GameInfo(os.path.abspath(rom).encode(), C.cast(C.c_char_p(self._rom), C.c_void_p), len(self._rom), None)
        if not L.retro_load_game(C.byref(gi)):
            self._release()
            raise RuntimeError("the core refused %s (unsupported mapper or bad dump?)" % rom)
        self.open = True

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
            v.value = None                      # the core keeps its default
            return False
        if cmd == ENV_GET_VARIABLE_UPDATE:
            C.cast(data, C.POINTER(C.c_bool))[0] = False
            return True
        return False

    def _video(self, data, w, h, pitch):
        if data:
            self.frame = (w, h, pitch, C.string_at(data, pitch * h))

    def _input(self, port, device, index, ident):
        return 1 if port == 0 and device == 1 and ident in self._held else 0

    # ---- running
    def run(self, n=1):
        self._held = {JOYPAD[k] for k in self.keys}
        for _ in range(n):
            self.L.retro_run()

    def image(self):
        from PIL import Image
        if self.frame is None:
            self.run(1)
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
    def serialize(self):
        n = self.L.retro_serialize_size()
        buf = C.create_string_buffer(n)
        if not self.L.retro_serialize(buf, C.c_size_t(n)):
            raise RuntimeError("savestate failed")
        return buf.raw

    def unserialize(self, data):
        if not self.L.retro_unserialize(data, C.c_size_t(len(data))):
            raise RuntimeError("the core refused the savestate (made by another core version or ROM?)")

    def memory(self, kind):
        """A live ctypes view of a libretro memory region (MEM_SYSTEM_RAM, MEM_SAVE_RAM), or None."""
        n, p = self.L.retro_get_memory_size(kind), self.L.retro_get_memory_data(kind)
        return (C.c_ubyte * n).from_address(p) if p and n else None

    def _release(self):
        self.L.retro_deinit()
        if self._shared:
            _in_use.discard(self.so)

    def close(self):
        if self.open:
            self.open = False
            self.L.retro_unload_game()
            self._release()
