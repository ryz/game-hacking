"""Platform registry: one entry per supported system. Everything platform-specific lives here, so another system
(SNES, GBA, ...) is added by writing one Backend subclass and one PLATFORMS entry; the tools above it
(emu.py, play.py, shoot.py, intake.py) only use the Backend interface.

Backend interface (what the tools rely on):
  keys                       set of button names usable in tokens
  extensions                 ROM file extensions
  native_size                (w, h) of a screenshot at scale 1 (default model)
  identify(data) -> dict     header facts for game.json (title, model guess, ...)
  open(rom, model, seed, turbo, sav) -> self      load the ROM, power on
  input(keys)                set held buttons (list, [] = release)
  frames(n)                  run n frames
  screen() -> bytes          PNG of the current frame, native size
  screen_png(path)           write it
  save_state(path) / load_state(path)
  peek(addr, n, bank=None) -> bytes, poke(addr, data)
  ram_search(expr) / ram_search_reset()   cheat-search style narrowing (optional)
  gameshark(code), apply_game_genie(rom, code), poke_bank()   the platform's cheat formats (optional)
  regs() -> dict             at least {"pc": "..."} for logs
  close()
"""
import os, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))


class Backend:
    keys = set()
    extensions = ()
    native_size = (0, 0)
    emulator = "emulator"      # named in saves/README.md: who can load the .state files

    def ram_search(self, expr, wide=False):
        raise NotImplementedError("RAM search is not available on this platform")

    def ram_search_reset(self):
        raise NotImplementedError("RAM search is not available on this platform")


# ------------------------------------------------------------------ Game Boy / Game Boy Color (gbemu-cli)
GB_CART = {0x00: "ROM", 0x01: "MBC1", 0x02: "MBC1+RAM", 0x03: "MBC1+RAM+BATTERY", 0x05: "MBC2",
           0x06: "MBC2+BATTERY", 0x0F: "MBC3+TIMER+BATTERY", 0x10: "MBC3+TIMER+RAM+BATTERY", 0x11: "MBC3",
           0x12: "MBC3+RAM", 0x13: "MBC3+RAM+BATTERY", 0x19: "MBC5", 0x1A: "MBC5+RAM", 0x1B: "MBC5+RAM+BATTERY",
           0x1C: "MBC5+RUMBLE", 0x1D: "MBC5+RUMBLE+RAM", 0x1E: "MBC5+RUMBLE+RAM+BATTERY", 0x20: "MBC6",
           0x22: "MBC7+SENSOR+RUMBLE+RAM+BATTERY", 0xFC: "POCKET CAMERA", 0xFE: "HuC3", 0xFF: "HuC1+RAM+BATTERY"}
GB_RAM = {0: 0, 1: 2, 2: 8, 3: 32, 4: 128, 5: 64}     # KiB


class GameBoy(Backend):
    """gbemu-cli (headless SameBoy). Models: dmg (grey), cgb, sgb (256x224 with border), agb."""
    keys = {"a", "b", "start", "select", "up", "down", "left", "right"}
    extensions = (".gb", ".gbc", ".sgb")
    native_size = (160, 144)
    emulator = "SameBoy"
    BIN = os.path.join(HERE, "gbemu-cli", "build", "gbemu")

    @staticmethod
    def identify(data):
        h = data[0x134:0x150]
        cgb = h[0x143 - 0x134]
        title_len = 11 if cgb in (0x80, 0xC0) else 16
        title = bytes(h[:title_len]).split(b"\x00")[0].decode("ascii", "replace").strip()
        chk = 0
        for b in data[0x134:0x14D]:
            chk = (chk - b - 1) & 0xFF
        sgb = data[0x146] == 0x03
        return {
            "header_title": title,
            "cgb_flag": "cgb_only" if cgb == 0xC0 else "cgb_enhanced" if cgb == 0x80 else "dmg",
            "sgb": sgb,
            "cart_type": GB_CART.get(data[0x147], "0x%02X" % data[0x147]),
            "rom_kib": 32 << data[0x148] if data[0x148] < 9 else None,
            "ram_kib": GB_RAM.get(data[0x149]),
            "region": "Japan" if data[0x14A] == 0 else "Overseas",
            "version": data[0x14C],
            "header_checksum_ok": chk == data[0x14D],
            "platform": "gbc" if cgb in (0x80, 0xC0) else "gb",
            # default capture model: colour for CGB games, the original grey DMG for the rest
            "model": "cgb" if cgb in (0x80, 0xC0) else "dmg",
        }

    # ---- cheat formats (GB/GBC). GameShark: write every frame; Game Genie: ROM patch.
    @staticmethod
    def gameshark(code):
        """'TTVVAAAA' -> (bank or None, addr, value). Type 01 = the mapped bank; 8n/9n = RAM bank n of the
        address's banked region (cart RAM A000-BFFF, CGB WRAM D000-DFFF). Address low byte first: 0109A2C0 =
        write 09 to C0A2. (EnHacklopedia "Hacking Gameboy"; SameBoy Core/cheats.c GB_import_cheat.)"""
        c = code.replace("-", "").strip()
        if len(c) != 8:
            raise ValueError("GameShark code must be 8 hex digits: %r" % code)
        t, v, lo, hi = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), int(c[6:8], 16)
        bank = None if t == 0x01 else (t & 0x0F)
        return bank, hi << 8 | lo, v

    @staticmethod
    def game_genie(code):
        """'ABC-DEF[-GHI]' -> (addr, value, compare or None). value = AB, addr = (F^F)CDE,
        compare = ror(GI, 2) ^ 0xBA (H unused). Same as SameBoy Core/cheats.c GB_import_cheat."""
        d = [int(x, 16) for x in code.replace("-", "").strip()]
        if len(d) not in (6, 9):
            raise ValueError("Game Genie code must be 6 or 9 hex digits: %r" % code)
        value = d[0] << 4 | d[1]
        addr = (d[5] ^ 0xF) << 12 | d[2] << 8 | d[3] << 4 | d[4]
        cmp_ = None
        if len(d) == 9:
            g = d[6] << 4 | d[8]
            cmp_ = (((g >> 2) | (g << 6)) & 0xFF) ^ 0xBA
        return addr, value, cmp_

    @classmethod
    def apply_game_genie(cls, rom, code):
        """Patch a ROM bytearray like the device would: the address in bank 0, or in every switchable bank (the
        device patches whatever bank is mapped), only where the compare byte matches. Returns patched offsets."""
        addr, value, cmp_ = cls.game_genie(code)
        if addr >= 0x8000:
            raise ValueError("Game Genie address %04X is not ROM" % addr)
        if addr < 0x4000:
            offs = [addr]
        else:
            offs = [b * 0x4000 + (addr - 0x4000) for b in range(1, max(2, len(rom) // 0x4000))]
        done = []
        for o in offs:
            if o < len(rom) and (cmp_ is None or rom[o] == cmp_):
                rom[o] = value
                done.append(o)
        return done

    def poke_bank(self, bank, addr, data):
        """Write RAM bank n of a banked region (GameShark 8n/9n): cart RAM A000-BFFF, WRAM D000-DFFF."""
        if 0xA000 <= addr < 0xC000:
            self.g.mem_write(None, list(data), region="cart_ram", offset=bank * 0x2000 + (addr - 0xA000))
        elif 0xD000 <= addr < 0xE000:
            self.g.mem_write(None, list(data), region="wram", offset=bank * 0x1000 + (addr - 0xD000))
        else:
            self.poke(addr, data)

    def open(self, rom, model="cgb", seed=1, turbo=True, sav=None):
        sys.path.insert(0, os.path.join(HERE, "gbemu-cli", "cli", "py"))
        from gbemu import GBEmu
        if not os.path.exists(self.BIN):
            raise SystemExit("gbemu-cli missing: run sh tools/setup_emu.sh")
        self.g = GBEmu(self.BIN)
        self.g.load_rom(os.path.abspath(rom), model=model, seed=seed, sav=sav and os.path.abspath(sav))
        if turbo:
            self.g.cmd("turbo", on=True)
        return self

    def input(self, keys):
        self.g.input_set(list(keys))

    def frames(self, n):
        if n > 0:
            self.g.run_frames(n)

    def screen(self):
        return self.g.screenshot()

    def screen_png(self, path):
        self.g.screenshot_png(os.path.abspath(path), scale=1)

    def save_state(self, path):
        self.g.snapshot_save(path=os.path.abspath(path))

    def load_state(self, path):
        self.g.snapshot_load(path=os.path.abspath(path))

    def peek(self, addr, n, bank=None):
        return bytes(self.g.mem_read(addr, n, bank=bank))

    def battery(self, size):
        """The cartridge RAM (battery save) as an emulator .sav file: `size` bytes from offset 0."""
        return bytes(self.g.mem_read(0, size, region="cart_ram", offset=0))

    def poke(self, addr, data):
        self.g.mem_write(addr, list(data))

    def ram_search(self, expr, wide=False):
        return self.g.mem_search(expr, wide=wide, max_results=64)

    def ram_search_reset(self):
        self.g.mem_search_reset()

    def regs(self):
        r = self.g.regs()
        return {"pc": r["pc"], "bank": r["banks"]["rom"]}

    def close(self):
        self.g.close()


# ------------------------------------------------------------------ NES / Famicom (Mesen libretro core)
NES_GG = "APZLGITYEOXUKSVN"


class Nes(Backend):
    """Mesen (libretro core, in-process through tools/lrcore.py). Models: ntsc (NES/Famicom, 60 Hz), pal, dendy.
    Cartridge games (.nes, iNES/NES 2.0 header); Famicom Disk System images are not set up (they need the BIOS).
    Memory is the CPU address space: 0000-07FF RAM, 6000-7FFF cartridge RAM (battery save), 8000-FFFF the PRG
    banks mapped right now. peek has no side effects; poke writes RAM and mapped PRG, never I/O registers."""
    keys = {"a", "b", "start", "select", "up", "down", "left", "right"}
    extensions = (".nes",)
    native_size = (256, 240)
    emulator = "Mesen libretro core"
    SO = os.path.join(HERE, "mesen", "Libretro", "mesen_libretro.so")
    MODELS = {"ntsc": "NTSC", "pal": "PAL", "dendy": "Dendy"}
    SEARCH = [(0x0000, 0x0800), (0x6000, 0x2000)]       # RAM search ranges (addr, size)

    @staticmethod
    def identify(data):
        if data[:4] != b"NES\x1a":
            raise SystemExit("not an iNES file (no 'NES\\x1a' header); headerless dumps need a header first")
        f6, f7 = data[6], data[7]
        nes2 = (f7 & 0x0C) == 0x08
        mapper = (f6 >> 4) | (f7 & 0xF0 if nes2 or not any(data[12:16]) else 0)
        prg, chr_ = data[4], data[5]
        region, ram_kib, submapper = "NTSC", 8 if f6 & 2 else 0, None
        if nes2:
            mapper |= (data[8] & 0x0F) << 8
            submapper = data[8] >> 4
            prg |= (data[9] & 0x0F) << 8
            chr_ |= (data[9] & 0xF0) << 4
            region = ("NTSC", "PAL", "Multi", "Dendy")[data[12] & 3]
            nv = data[10] >> 4
            ram_kib = (64 << nv) // 1024 if nv else 0
        elif data[9] & 1:
            region = "PAL"
        return {
            "format": "NES 2.0" if nes2 else "iNES",
            "mapper": mapper,
            "submapper": submapper,
            "prg_kib": prg * 16,
            "chr_kib": chr_ * 8,                      # 0 = CHR RAM
            "battery": bool(f6 & 2),
            "ram_kib": ram_kib,                       # battery RAM for play.py export (iNES: 8 KiB assumed)
            "mirroring": "four-screen" if f6 & 8 else "vertical" if f6 & 1 else "horizontal",
            "trainer": bool(f6 & 4),
            "region": region,
            "platform": "nes",
            "model": {"PAL": "pal", "Dendy": "dendy"}.get(region, "ntsc"),
        }

    # ---- cheat formats (NES). Game Genie: ROM patch; there is no GameShark, use freeze:ADDR=HEX for RAM.
    @staticmethod
    def gameshark(code):
        raise ValueError("no GameShark on the NES: hold a RAM value with freeze:ADDR=HEX instead of gs:%s" % code)

    @staticmethod
    def game_genie(code):
        """6 or 8 letters -> (addr 8000-FFFF, value, compare or None). (nesdev wiki "Game Genie".)"""
        c = code.replace("-", "").strip().upper()
        if len(c) not in (6, 8) or any(ch not in NES_GG for ch in c):
            raise ValueError("NES Game Genie code must be 6 or 8 letters of %s: %r" % (NES_GG, code))
        n = [NES_GG.index(ch) for ch in c]
        addr = 0x8000 | (n[3] & 7) << 12 | (n[5] & 7) << 8 | (n[4] & 8) << 8 | (n[2] & 7) << 4 | (n[1] & 8) << 4 \
            | (n[4] & 7) | (n[3] & 8)
        if len(c) == 6:
            return addr, (n[1] & 7) << 4 | (n[0] & 8) << 4 | (n[0] & 7) | (n[5] & 8), None
        value = (n[1] & 7) << 4 | (n[0] & 8) << 4 | (n[0] & 7) | (n[7] & 8)
        cmp_ = (n[7] & 7) << 4 | (n[6] & 8) << 4 | (n[6] & 7) | (n[5] & 8)
        return addr, value, cmp_

    @classmethod
    def apply_game_genie(cls, rom, code):
        """Patch a ROM bytearray. 8-letter codes: every 8 KiB PRG bank at that address where the compare byte
        matches (what the device does while that bank is mapped). 6-letter codes have no compare byte, so they
        are only exact without bank switching (PRG <= 32 KiB); for bigger games use the 8-letter form."""
        addr, value, cmp_ = cls.game_genie(code)
        head = 16 + (512 if rom[6] & 4 else 0)
        size = rom[4] * 0x4000
        if cmp_ is None:
            if size > 0x8000:
                raise ValueError("6-letter Game Genie code %s on a bank-switched game: the bank is unknown. Use "
                                 "the 8-letter code, or rom_variants \"bytes\" with the file offset" % code)
            offs = [(addr - 0x8000) % size]
        else:
            offs = [o for o in range(addr & 0x1FFF, size, 0x2000) if rom[head + o] == cmp_]
        for o in offs:
            rom[head + o] = value
        return [head + o for o in offs]

    def open(self, rom, model="ntsc", seed=1, turbo=True, sav=None):
        import shutil, tempfile
        import lrcore
        if not os.path.exists(self.SO):
            raise SystemExit("Mesen core missing: run sh tools/setup_emu.sh")
        if (model or "ntsc") not in self.MODELS:
            raise SystemExit("NES model %r unknown (have: %s)" % (model, ", ".join(sorted(self.MODELS))))
        # fixed power-on state: RAM all zeros (Mesen default, set explicitly), no overscan crop, default palette.
        # A private empty save directory: the core must never pick up a battery file from an earlier run.
        self.tmp = tempfile.mkdtemp(prefix="gamedb-nes")
        self.c = lrcore.Core(self.SO, os.path.abspath(rom), system_dir=self.tmp, save_dir=self.tmp, options={
            "mesen_region": self.MODELS[model or "ntsc"], "mesen_ramstate": "All 0s (Default)",
            "mesen_overscan_left": "None", "mesen_overscan_right": "None", "mesen_overscan_up": "None",
            "mesen_overscan_down": "None", "mesen_palette": "Default", "mesen_ntsc_filter": "Disabled",
            "mesen_nospritelimit": "disabled", "mesen_overclock": "None"})
        import ctypes
        L = self.c.L
        L.retro_mesen_peek.restype, L.retro_mesen_peek.argtypes = ctypes.c_uint8, [ctypes.c_uint16]
        L.retro_mesen_poke.restype, L.retro_mesen_poke.argtypes = None, [ctypes.c_uint16, ctypes.c_uint8]
        L.retro_mesen_pc.restype = ctypes.c_uint16
        if sav:
            data = open(sav, "rb").read()
            ram = self.c.memory(lrcore.MEM_SAVE_RAM)
            if ram is None:
                raise SystemExit("this cartridge has no battery RAM; %s cannot be loaded" % sav)
            n = min(len(data), len(ram))
            ctypes.memmove(ram, data, n)
        self.c.size = self.native_size
        self._search = None
        return self

    def input(self, keys):
        self.c.keys = set(keys)

    def frames(self, n):
        if n > 0:
            self.c.run(n)

    def screen(self):
        return self.c.png_bytes()

    def screen_png(self, path):
        self.c.png(os.path.abspath(path))

    def save_state(self, path):
        open(os.path.abspath(path), "wb").write(self.c.serialize())

    def load_state(self, path):
        self.c.unserialize(open(os.path.abspath(path), "rb").read())

    def peek(self, addr, n, bank=None):
        if bank is not None:
            raise NotImplementedError("NES peek reads the mapped address space only (no bank argument)")
        return bytes(self.c.L.retro_mesen_peek((addr + i) & 0xFFFF) for i in range(n))

    def poke(self, addr, data):
        for i, b in enumerate(bytes(data)):
            self.c.L.retro_mesen_poke((addr + i) & 0xFFFF, b)

    def battery(self, size):
        """The battery RAM as an emulator .sav file (the core's real size; `size` is only the header's guess)."""
        import lrcore
        ram = self.c.memory(lrcore.MEM_SAVE_RAM)
        if ram is None:
            raise SystemExit("this cartridge has no battery RAM")
        return bytes(ram)

    # ---- RAM search (cheat-search style): the first call takes a snapshot and applies the filter with
    # old == new; later calls keep the addresses where the expression holds. Names: new, old.
    def _snapshot(self, wide):
        out = {}
        for base, size in self.SEARCH:
            data = self.peek(base, size)
            for i in range(size - (1 if wide else 0)):
                out[base + i] = data[i] | (data[i + 1] << 8 if wide else 0)
        return out

    def ram_search(self, expr, wide=False, max_results=64):
        import re
        if not re.fullmatch(r"[\s\w+\-*/%<>=!&|^()~]+", expr) or "__" in expr:
            raise ValueError("search expression may only use new, old, numbers and operators: %r" % expr)
        code = compile(expr, "<search>", "eval")
        now = self._snapshot(wide)
        if self._search is None or self._search[0] != wide:
            self._search = (wide, dict(now))
        old = self._search[1]
        keep = {a: v for a, v in now.items()
                if a in old and eval(code, {"__builtins__": {}}, {"new": v, "old": old[a]})}
        self._search = (wide, keep)
        rows = [{"addr": "%04x" % a, "value": v} for a, v in sorted(keep.items())[:max_results]]
        return {"count": len(keep), "results": rows}

    def ram_search_reset(self):
        self._search = None

    def regs(self):
        return {"pc": "%04x" % self.c.L.retro_mesen_pc()}

    def close(self):
        import shutil
        self.c.close()
        shutil.rmtree(self.tmp, ignore_errors=True)


PLATFORMS = {"gb": GameBoy, "gbc": GameBoy, "nes": Nes}


def backend(platform):
    if platform not in PLATFORMS:
        raise SystemExit("platform %r not supported yet (have: %s)" % (platform, ", ".join(sorted(PLATFORMS))))
    return PLATFORMS[platform]()


def by_extension(path):
    ext = os.path.splitext(path)[1].lower()
    for name, cls in PLATFORMS.items():
        if ext in cls.extensions:
            return name, cls
    raise SystemExit("unknown ROM type %r (supported: %s)" % (
        ext, " ".join(sorted({e for c in PLATFORMS.values() for e in c.extensions}))))


def crc32(data):
    return "%08x" % (zlib.crc32(data) & 0xFFFFFFFF)
