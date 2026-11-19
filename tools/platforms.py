"""Platform registry: one entry per supported system. Everything platform-specific lives here, so another system
(GBA, Mega Drive, ...) is added by writing one Backend subclass and one PLATFORMS entry; the tools above it
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


# ------------------------------------------------------------------ libretro cores (in-process, tools/lrcore.py)
class Libretro(Backend):
    """Shared part of the backends that run a Mesen libretro core patched with retro_mesen_peek/poke/pc
    (tools/mesen-debug.patch, tools/mesen-s-debug.patch). Subclasses set SO, ADDR_MASK, PC_FORMAT, SEARCH and
    call _open() with the core options."""
    SO = None
    ADDR_MASK = 0xFFFF
    PC_FORMAT = "%04x"
    SEARCH = []                 # RAM search ranges (addr, size)

    def _open(self, rom, options, sav):
        import ctypes, tempfile
        import lrcore
        if not os.path.exists(self.SO):
            raise SystemExit("%s missing: run sh tools/setup_emu.sh" % self.emulator)
        # A private empty save directory: the core must never pick up a battery file from an earlier run.
        self.tmp = tempfile.mkdtemp(prefix="gamedb-core")
        self.c = lrcore.Core(self.SO, os.path.abspath(rom), system_dir=self.tmp, save_dir=self.tmp, options=options)
        L = self.c.L
        L.retro_mesen_peek.restype, L.retro_mesen_peek.argtypes = ctypes.c_uint8, [ctypes.c_uint32]
        L.retro_mesen_poke.restype, L.retro_mesen_poke.argtypes = None, [ctypes.c_uint32, ctypes.c_uint8]
        L.retro_mesen_pc.restype = ctypes.c_uint32
        if sav:
            data = open(sav, "rb").read()
            ram = self.c.memory(lrcore.MEM_SAVE_RAM)
            if ram is None:
                raise SystemExit("this cartridge has no battery RAM; %s cannot be loaded" % sav)
            ctypes.memmove(ram, data, min(len(data), len(ram)))
        self.c.size = self.native_size
        self._search = None
        return self

    def input(self, keys):
        self.c.keys = set(keys)

    def frames(self, n):
        if n > 0:
            self.c.run(n)

    def image(self):
        """The current frame as a PIL image (subclasses crop or convert here)."""
        return self.c.image()

    def screen(self):
        import io
        b = io.BytesIO()
        self.image().save(b, "PNG")
        return b.getvalue()

    def screen_png(self, path):
        self.image().save(os.path.abspath(path), "PNG")

    def save_state(self, path):
        open(os.path.abspath(path), "wb").write(self.c.serialize())

    def load_state(self, path):
        self.c.unserialize(open(os.path.abspath(path), "rb").read())

    def peek(self, addr, n, bank=None):
        if bank is not None:
            raise NotImplementedError("peek reads the mapped address space only (no bank argument)")
        return bytes(self.c.L.retro_mesen_peek((addr + i) & self.ADDR_MASK) for i in range(n))

    def poke(self, addr, data):
        for i, b in enumerate(bytes(data)):
            self.c.L.retro_mesen_poke((addr + i) & self.ADDR_MASK, b)

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
            base = getattr(self, "_base", None)          # snapshot from ram_search_reset, else start here
            self._search = (wide, dict(base[wide]) if base else dict(now))
        old = self._search[1]
        keep = {a: v for a, v in now.items()
                if a in old and eval(code, {"__builtins__": {}}, {"new": v, "old": old[a]})}
        self._search = (wide, keep)
        rows = [{"addr": self.PC_FORMAT % a, "value": v} for a, v in sorted(keep.items())[:max_results]]
        return {"count": len(keep), "results": rows}

    def ram_search_reset(self):
        """Start a new search from the RAM as it is now (the next find compares against this)."""
        self._search = None
        self._base = {False: self._snapshot(False), True: self._snapshot(True)}

    def regs(self):
        return {"pc": self.PC_FORMAT % self.c.L.retro_mesen_pc()}

    def close(self):
        import shutil
        self.c.close()
        shutil.rmtree(self.tmp, ignore_errors=True)


# ------------------------------------------------------------------ NES / Famicom (Mesen libretro core)
NES_GG = "APZLGITYEOXUKSVN"


class Nes(Libretro):
    """Mesen (libretro core, in-process through tools/lrcore.py). Models: ntsc (NES/Famicom, 60 Hz), pal, dendy.
    Cartridge games (.nes, iNES/NES 2.0 header); Famicom Disk System images are not set up (they need the BIOS).
    Memory is the CPU address space: 0000-07FF RAM, 6000-7FFF cartridge RAM (battery save), 8000-FFFF the PRG
    banks mapped right now. peek has no side effects; poke writes RAM and cartridge RAM (not PRG ROM, not I/O registers)."""
    keys = {"a", "b", "start", "select", "up", "down", "left", "right"}
    extensions = (".nes",)
    native_size = (256, 240)
    emulator = "Mesen libretro core"
    SO = os.path.join(HERE, "mesen", "Libretro", "mesen_libretro.so")
    MODELS = {"ntsc": "NTSC", "pal": "PAL", "dendy": "Dendy"}
    SEARCH = [(0x0000, 0x0800), (0x6000, 0x2000)]

    def _wram(self, addr, n):
        """The core's battery RAM for 6000-7FFF (8 KiB carts), or None. Read/written directly so that peeks and
        pokes work while the game keeps the cartridge RAM disabled (MMC3 does; the bus then reads open bus and
        drops writes - found with Wizardry II, 2026-11-18)."""
        if not (0x6000 <= addr and addr + n <= 0x8000):
            return None
        import lrcore
        ram = self.c.memory(lrcore.MEM_SAVE_RAM)
        return ram if ram is not None and len(ram) == 0x2000 else None

    def peek(self, addr, n, bank=None):
        ram = self._wram(addr, n) if bank is None else None
        if ram is not None:
            return bytes(ram[addr - 0x6000:addr - 0x6000 + n])
        return Libretro.peek(self, addr, n, bank)

    def poke(self, addr, data):
        data = bytes(data)
        ram = self._wram(addr, len(data))
        if ram is None:
            return Libretro.poke(self, addr, data)
        for i, v in enumerate(data):
            ram[addr - 0x6000 + i] = v

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
        if (model or "ntsc") not in self.MODELS:
            raise SystemExit("NES model %r unknown (have: %s)" % (model, ", ".join(sorted(self.MODELS))))
        # fixed power-on state: RAM all zeros (Mesen default, set explicitly), no overscan crop, default palette
        return self._open(rom, {
            "mesen_region": self.MODELS[model or "ntsc"], "mesen_ramstate": "All 0s (Default)",
            "mesen_overscan_left": "None", "mesen_overscan_right": "None", "mesen_overscan_up": "None",
            "mesen_overscan_down": "None", "mesen_palette": "Default", "mesen_ntsc_filter": "Disabled",
            "mesen_nospritelimit": "disabled", "mesen_overclock": "None"}, sav)

# ------------------------------------------------------------------ SNES / Super Famicom (Mesen-S libretro core)
SNES_GG = "DF4709156BC8A23E"
SNES_REGION = {0: "Japan", 1: "North America", 2: "Europe", 3: "Sweden/Scandinavia", 4: "Finland", 5: "Denmark",
               6: "France", 7: "Netherlands", 8: "Spain", 9: "Germany", 10: "Italy", 11: "China", 12: "Indonesia",
               13: "South Korea", 15: "Canada", 16: "Brazil", 17: "Australia"}
SNES_CHIP = {0x00: "ROM", 0x01: "ROM+RAM", 0x02: "ROM+RAM+BATTERY", 0x03: "DSP", 0x04: "DSP+RAM",
             0x05: "DSP+RAM+BATTERY", 0x13: "SuperFX", 0x14: "SuperFX+RAM", 0x15: "SuperFX+RAM+BATTERY",
             0x1A: "SuperFX+RAM+BATTERY", 0x25: "OBC1+RAM+BATTERY", 0x32: "SA-1+RAM", 0x34: "SA-1+RAM",
             0x35: "SA-1+RAM+BATTERY", 0x43: "S-DD1", 0x45: "S-DD1+RAM+BATTERY", 0x55: "S-RTC+RAM+BATTERY",
             0xE3: "Super Game Boy", 0xE5: "BS-X", 0xF3: "CX4", 0xF5: "ST018/SPC7110+RAM+BATTERY",
             0xF6: "ST010/ST011+BATTERY", 0xF9: "SPC7110+RTC+RAM+BATTERY"}


class Snes(Libretro):
    """Mesen-S (libretro core, in-process through tools/lrcore.py). Models: ntsc (SNES/Super Famicom, 60 Hz), pal.
    Cartridge games (.sfc; .smc with or without the 512-byte copier header), special chips included.
    Memory is the 24-bit CPU address space BB:AAAA written as six hex digits: 7E0000-7FFFFF work RAM (the first
    8 KiB also at 00:0000-1FFF), ROM and battery RAM where the cartridge maps them (LoROM RAM 70:0000-,
    HiROM RAM 30:6000-). peek has no side effects; poke writes work RAM, battery RAM and ROM, never registers."""
    keys = {"a", "b", "x", "y", "l", "r", "start", "select", "up", "down", "left", "right"}
    extensions = (".sfc", ".smc")
    native_size = (256, 224)
    emulator = "Mesen-S libretro core"
    SO = os.path.join(HERE, "mesen-s", "Libretro", "mesen-s_libretro.so")
    MODELS = {"ntsc": "NTSC", "pal": "PAL"}
    ADDR_MASK = 0xFFFFFF
    PC_FORMAT = "%06x"
    SEARCH = [(0x7E0000, 0x20000)]

    @staticmethod
    def header(data):
        """(file offset of the internal header at xxFFC0, copier header size) by the best checksum/plausibility
        score among LoROM, HiROM and ExHiROM."""
        skip = 512 if len(data) % 1024 == 512 else 0
        best = (-1, None)
        for base in (0x7FC0, 0xFFC0, 0x40FFC0):
            o = skip + base
            if o + 0x40 > len(data):
                continue
            h = data[o:o + 0x40]
            score = 0
            chk, comp = h[0x1E] | h[0x1F] << 8, h[0x1C] | h[0x1D] << 8
            if chk ^ comp == 0xFFFF and chk + comp == 0xFFFF:
                score += 8
            mode = h[0x15] & 0x2F
            if (base == 0x7FC0 and mode in (0x20, 0x22, 0x23)) or (base == 0xFFC0 and mode == 0x21) or \
                    (base == 0x40FFC0 and mode == 0x25):
                score += 4
            if all(0x20 <= c < 0x7F or c >= 0xA0 for c in h[:21]):
                score += 2
            if h[0x3D] >= 0x80:                         # reset vector points into ROM
                score += 2
            if h[0x17] < 0x0E and h[0x18] < 0x09:
                score += 1
            if score > best[0]:
                best = (score, o)
        if best[1] is None:
            raise SystemExit("too small for a SNES ROM")
        return best[1], skip

    @classmethod
    def identify(cls, data):
        o, skip = cls.header(data)
        h = data[o:o + 0x40]
        title = bytes(h[:21]).decode("shift_jis", "replace").strip()
        mode = h[0x15]
        chk, comp = h[0x1E] | h[0x1F] << 8, h[0x1C] | h[0x1D] << 8
        body, p2 = data[skip:], 1
        while p2 * 2 <= len(body):
            p2 *= 2
        total = sum(body[:p2])                          # sizes that are not a power of two: the rest is mirrored
        if len(body) > p2:
            total += sum(body[p2:]) * (p2 // (len(body) - p2))
        total &= 0xFFFF
        region = SNES_REGION.get(h[0x19], "0x%02X" % h[0x19])
        pal = 2 <= h[0x19] <= 12 or h[0x19] == 17
        return {
            "header_title": title,
            "mapping": {0: "LoROM", 1: "HiROM", 2: "LoROM (S-DD1)", 3: "LoROM (SA-1)", 5: "ExHiROM"}.get(
                mode & 0x0F, "0x%02X" % mode),
            "fast_rom": bool(mode & 0x10),
            "cart_type": SNES_CHIP.get(h[0x16], "0x%02X" % h[0x16]),
            "rom_kib": 1 << h[0x17] if h[0x17] < 0x10 else None,
            "ram_kib": (1 << h[0x18]) if 0 < h[0x18] < 0x10 else 0,
            "region": region,
            "version": h[0x1B],
            "copier_header": bool(skip),
            "header_checksum_ok": chk ^ comp == 0xFFFF and chk == total,
            "platform": "snes",
            "model": "pal" if pal else "ntsc",
        }

    # ---- cheat formats (SNES). Pro Action Replay AAAAAAVV: RAM codes are held like the device (gs: token);
    # Game Genie XXXX-XXXX and ROM-address PAR codes are ROM patches.
    @staticmethod
    def gameshark(code):
        """Pro Action Replay 'AAAAAAVV' -> (None, addr, value), for the gs: token (written every frame)."""
        c = code.replace("-", "").replace(":", "").strip()
        if len(c) != 8:
            raise ValueError("Pro Action Replay code must be 8 hex digits AAAAAAVV: %r" % code)
        return None, int(c[:6], 16), int(c[6:], 16)

    @staticmethod
    def game_genie(code):
        """'XXXX-XXXX' -> (24-bit CPU address, value, None). Same decoding as Mesen-S Core/CheatManager.cpp."""
        c = code.replace("-", "").strip().upper()
        if len(c) != 8 or any(ch not in SNES_GG for ch in c):
            raise ValueError("SNES Game Genie code must be XXXX-XXXX with letters of %s: %r" % (SNES_GG, code))
        raw = 0
        for ch in c:
            raw = raw << 4 | SNES_GG.index(ch)
        addr = ((raw & 0x3C00) << 10) | ((raw & 0x3C) << 14) | ((raw & 0xF00000) >> 8) | ((raw & 0x03) << 10) | \
            ((raw & 0xC000) >> 6) | ((raw & 0xF0000) >> 12) | ((raw & 0x3C0) >> 6)
        return addr, raw >> 24, None

    @classmethod
    def rom_offset(cls, rom, addr):
        """File offset of a CPU address that maps to ROM, by the cartridge's mapping (LoROM / HiROM / ExHiROM)."""
        o, skip = cls.header(rom)
        mode = rom[o + 0x15] & 0x0F
        bank, a = addr >> 16, addr & 0xFFFF
        if mode in (1, 5):                              # HiROM / ExHiROM: banks C0-FF (and 40-7D), 8000+ in 00-3F
            if a < 0x8000 and not (0x40 <= bank <= 0x7D or bank >= 0xC0):
                raise ValueError("%06X is not ROM" % addr)
            off = (bank & 0x3F) << 16 | a
            if mode == 5 and bank < 0x80:
                off += 0x400000
        else:                                           # LoROM: 32 KiB per bank at 8000-FFFF
            if a < 0x8000:
                raise ValueError("%06X is not ROM" % addr)
            off = (bank & 0x7F) << 15 | (a & 0x7FFF)
        if off >= len(rom) - skip:
            off %= len(rom) - skip                      # mirrored
        return skip + off

    @classmethod
    def apply_game_genie(cls, rom, code):
        """Patch a ROM bytearray at the code's address (no compare byte on this console). Returns the offset."""
        addr, value, _ = cls.game_genie(code)
        off = cls.rom_offset(rom, addr)
        rom[off] = value
        return [off]

    def image(self):
        """The core always sends 239 lines (478 in hi-res/interlace). Nearly every game shows 224 lines, at rows
        7-230 with black above and below: those frames are cropped to 256x224 (512x448). A game that really
        uses the 239-line overscan mode has picture in the margins and keeps the full frame."""
        im = self.c.image()
        k = im.height // 239
        if im.height == 239 * k and k in (1, 2):
            top, bottom = im.crop((0, 0, im.width, 7 * k)), im.crop((0, 231 * k, im.width, im.height))
            if not top.getbbox() and not bottom.getbbox():
                im = im.crop((0, 7 * k, im.width, 231 * k))
        return im

    def open(self, rom, model="ntsc", seed=1, turbo=True, sav=None):
        if (model or "ntsc") not in self.MODELS:
            raise SystemExit("SNES model %r unknown (have: %s)" % (model, ", ".join(sorted(self.MODELS))))
        # fixed power-on state: RAM all zeros (the core's default is random), no overscan crop, no filters
        return self._open(rom, {
            "mesen-s_region": self.MODELS[model or "ntsc"], "mesen-s_ramstate": "All 0s",
            "mesen-s_overscan_vertical": "None", "mesen-s_overscan_horizontal": "None",
            "mesen-s_ntsc_filter": "Disabled", "mesen-s_blend_high_res": "disabled",
            "mesen-s_overclock": "None", "mesen-s_superfx_overclock": "100%"}, sav)


# ------------------------------------------------------------------ DOS (DOSBox Pure libretro core)
def _retrok():
    k = {"backspace": 8, "tab": 9, "enter": 13, "esc": 27, "space": 32, "quote": 39, "comma": 44, "minus": 45,
         "period": 46, "slash": 47, "semicolon": 59, "equals": 61, "leftbracket": 91, "backslash": 92,
         "rightbracket": 93, "backquote": 96, "delete": 127, "kpperiod": 266, "kpdivide": 267, "kpmultiply": 268,
         "kpminus": 269, "kpplus": 270, "kpenter": 271, "up": 273, "down": 274, "right": 275, "left": 276,
         "insert": 277, "home": 278, "end": 279, "pageup": 280, "pagedown": 281, "rshift": 303, "shift": 304,
         "rctrl": 305, "ctrl": 306, "ralt": 307, "alt": 308}
    k.update({chr(c): c for c in range(ord("a"), ord("z") + 1)})
    k.update({str(d): 48 + d for d in range(10)})
    k.update({"kp%d" % d: 256 + d for d in range(10)})
    k.update({"f%d" % d: 281 + d for d in range(1, 13)})
    return k


class Dos(Libretro):
    """DOSBox Pure (libretro core, in-process through tools/lrcore.py, patched with tools/dosbox-pure-debug.patch:
    settable clock, frame sync, program counter). A game is a ZIP of its DOS files (mounted as C:).
    Model: MACHINE[-CYCLES], machine one of svga vga ega cga tandy pcjr hercules, cycles = instructions per
    millisecond (fixed, so a route does not depend on the host); default svga-7800.
    Keys are keyboard keys (KEYS) plus mouse1/mouse2/mouse3; the mouse moves with emu.mouse(dx, dy).
    The emulated clock starts at EPOCH on every power-on and follows the emulated frames.
    Memory is the physical address space (segment * 16 + offset): 00000-9FFFF conventional, 100000+ extended.
    The size of the picture follows the video mode (text 640x400 or 720x400, 320x200 games as 320x200, ...)."""
    KEYS = _retrok()
    keys = set(KEYS) | {"mouse1", "mouse2", "mouse3"}
    extensions = (".zip",)
    native_size = (640, 400)
    emulator = "DOSBox Pure libretro core"
    SO = os.path.join(HERE, "dosbox-pure", "dosbox_pure_libretro.so")
    MACHINES = ("svga", "vga", "ega", "cga", "tandy", "pcjr", "hercules")
    EPOCH = 631152000           # 1990-01-01 00:00:00 UTC
    FRAME_USEC = 16667          # virtual host time per emulated frame
    PC_FORMAT = "%05x"
    SEARCH = [(0x00500, 0x9FB00)]
    SHIFTED = dict(zip('!@#$%^&*()_+{}|:"<>?~', "1234567890-=[]\\;',./`"))
    NAMES = {" ": "space", "\n": "enter", "'": "quote", ",": "comma", "-": "minus", ".": "period", "/": "slash",
             ";": "semicolon", "=": "equals", "[": "leftbracket", "\\": "backslash", "]": "rightbracket",
             "`": "backquote"}

    @staticmethod
    def identify(data):
        import io, zipfile
        try:
            names = zipfile.ZipFile(io.BytesIO(data)).namelist()
        except zipfile.BadZipFile:
            raise SystemExit("not a ZIP file: a DOS game is registered as a ZIP of its files")
        exe = sorted(n for n in names if n.lower().endswith((".exe", ".com", ".bat")))
        return {"platform": "dos", "model": "svga-7800", "files": len(names), "programs": exe[:40]}

    def open(self, rom, model=None, seed=1, turbo=True, sav=None):
        import ctypes, shutil, tempfile
        import lrcore
        if not os.path.exists(self.SO):
            raise SystemExit("%s missing: run sh tools/setup_emu.sh dos" % self.emulator)
        machine, _, cycles = (model or "svga-7800").partition("-")
        if machine not in self.MACHINES or not (cycles or "7800").isdigit():
            raise SystemExit("unknown DOS model %r (MACHINE[-CYCLES], machines: %s)" % (model, " ".join(self.MACHINES)))
        # A private save directory: DOSBox Pure keeps the files a game writes in <content name>.pure.zip there.
        self.tmp = tempfile.mkdtemp(prefix="gamedb-core")
        self.savezip = os.path.join(self.tmp, os.path.splitext(os.path.basename(rom))[0] + ".pure.zip")
        self._sav0 = open(sav, "rb").read() if sav else None       # the save ZIP this power-on starts with
        options = {"dosbox_pure_machine": machine, "dosbox_pure_cycles": cycles or "7800",
                   "dosbox_pure_savestate": "on", "dosbox_pure_conf": "false", "dosbox_pure_midi": "disabled"}
        self._boot = (os.path.abspath(rom), options)
        self._search = None
        self._power_on()
        return self

    @staticmethod
    def _files(zipbytes):
        """{name: content} of a save ZIP (None or empty = no files), for comparing two disks."""
        import io, zipfile
        if not zipbytes:
            return {}
        z = zipfile.ZipFile(io.BytesIO(zipbytes))
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}

    def _disk(self):
        """The files the game has written so far, as DOSBox Pure's save ZIP (None = nothing written)."""
        self.c.L.retro_gamedb_flush()           # the core itself writes the ZIP only a second after a change
        return open(self.savezip, "rb").read() if os.path.exists(self.savezip) else None

    def _power_on(self, disk=None):
        """Power on with `disk` as the save ZIP (None = the one this session was opened with)."""
        import ctypes
        import lrcore
        rom, options = self._boot
        disk = self._sav0 if disk is None else disk
        if disk:
            open(self.savezip, "wb").write(disk)
        elif os.path.exists(self.savezip):
            os.remove(self.savezip)
        self.c = lrcore.Core(self.SO, rom, system_dir=self.tmp, save_dir=self.tmp, options=options,
                             frame_usec=self.FRAME_USEC, epoch=self.EPOCH, private=True)
        self.c.L.retro_gamedb_pc.restype = ctypes.c_uint32
        self.c.L.retro_gamedb_readb.restype, self.c.L.retro_gamedb_readb.argtypes = ctypes.c_uint8, [ctypes.c_uint32]
        self.c.size = self.native_size
        # _log: everything done since power-on, kept until the core can make a real savestate (see save_state)
        self._down, self._ran, self._log, self._launch = set(), 0, [], None

    def input(self, keys):
        keys = set(keys)
        for k in sorted(self._down - keys):
            if k in self.KEYS:
                self.c.key(self.KEYS[k], False)
        for k in sorted(keys - self._down):
            if k in self.KEYS:
                self.c.key(self.KEYS[k], True)
        self._down = keys
        self.c.keys = {k for k in keys if k.startswith("mouse")}
        if self._log is not None:
            self._log.append(["i", sorted(keys)])

    def mouse(self, dx, dy):
        """Relative mouse motion, reported to the game during the next frame."""
        self.c.mouse = [dx, dy]
        if self._log is not None:
            self._log.append(["m", [dx, dy]])

    def type_text(self, text, hold=4, gap=4):
        """Type text on the US keyboard (shift for capitals and symbols)."""
        for ch in text:
            shift = ch.isupper() or ch in self.SHIFTED
            base = self.SHIFTED.get(ch, ch.lower())
            key = self.NAMES.get(base, base)
            if key not in self.KEYS:
                raise ValueError("cannot type %r" % ch)
            if shift:
                self.input(["shift"])
                self.frames(2)
            self.input(["shift", key] if shift else [key])
            self.frames(hold)
            self.input([])
            self.frames(gap)

    WARMUP = 4                  # frames a just-opened machine runs before its first state load

    def frames(self, n):
        # Until a program runs, everything is logged (_log) and run in steps of at most 10 frames: the log
        # stops at the first step that ends with a program running. From then on it is the "launch" stored
        # with every state. It must end there and not later: replaying more than the launch on load would
        # repeat what the route did to the disk (found 2026-11-18: a second copy of a created character).
        while n > 0 and self._log is not None:
            step = min(n, 10)
            self.c.run(step)
            self._ran += step
            self._log.append(["f", step])
            n -= step
            if self.c.L.retro_gamedb_running():
                self._launch, self._log = self._log, None
        if n > 0:
            self.c.run(n)
            self._ran += n

    BOOTLOG = b"GAMEDB-DOS-BOOTLOG-1\n"
    STATE = b"GAMEDB-DOS-STATE-3\n"

    def save_state(self, path):
        """The core saves and loads states only while a DOS program runs, not in DOSBox Pure's start menu or at
        the DOS prompt, and its state holds the machine but not the files the game wrote. Two file kinds:
        - before the first real state (BOOTLOG): the list of inputs since power-on. Loading it powers the machine
          on again and replays them (same route = same frames, so the result is the same).
        - a real state (STATE): the inputs that got the program running, the files written so far (DOSBox Pure's
          save ZIP) and the core's state. Loading it into a machine where no program runs, or whose written
          files differ, powers on with those files, replays the launch inputs and then loads the core's state.
          So a state made after an in-game save still has that save on disk wherever it is loaded."""
        import base64, json
        if self._log is not None:
            data = self.BOOTLOG + json.dumps(self._log).encode() + b"\n"
        else:
            try:
                raw = self.c.serialize()
            except RuntimeError:
                raise RuntimeError("no savestate here: the DOS program has ended (DOS prompt or start menu)")
            disk = self._disk()
            head = {"launch": self._launch, "disk": base64.b64encode(disk).decode() if disk else None}
            data = self.STATE + json.dumps(head).encode() + b"\n" + raw
        open(os.path.abspath(path), "wb").write(data)

    def _replay(self, log, disk=None):
        self.c.close()
        self._power_on(disk)
        for kind, v in log:
            {"i": self.input, "f": self.frames, "m": lambda m: self.mouse(*m)}[kind](v)

    def load_state(self, path):
        import base64, json
        data = open(os.path.abspath(path), "rb").read()
        if data.startswith(self.BOOTLOG):
            self._replay(json.loads(data[len(self.BOOTLOG):].split(b"\n", 1)[0]))
            return
        if not data.startswith(self.STATE):
            raise RuntimeError("not a DOS savestate of this tool version (delete work/cache): %s" % path)
        head, raw = data[len(self.STATE):].split(b"\n", 1)
        head = json.loads(head)
        launch, disk = head["launch"], base64.b64decode(head["disk"]) if head["disk"] else b""
        # A state loaded into a machine that has run fewer than 2 frames continues with different timing than
        # the run that made it (measured 2026-11-18: 0 and 1 frames differ, 2 and more are exact).
        if self._ran < self.WARMUP:
            self.frames(self.WARMUP - self._ran)
        for k in sorted(self._down):
            if k in self.KEYS:
                self.c.key(self.KEYS[k], False)
        self._down = set()
        same_disk = self._files(disk) == self._files(self._disk())
        try:
            if not same_disk:
                raise RuntimeError("other files on disk")
            if (self._log == [["f", self.WARMUP]] and launch and launch[0][0] == "f"
                    and launch[0][1] >= self.WARMUP):
                # a machine that was only just opened (nothing but the warm-up, no program yet): play the
                # launch on it instead of powering on a second time; same timing as a power-on replay
                for n, (kind, v) in enumerate(launch):
                    v = v - self.WARMUP if n == 0 else v
                    {"i": self.input, "f": self.frames, "m": lambda m: self.mouse(*m)}[kind](v)
                if self._log is not None:
                    raise RuntimeError("the state's launch inputs did not start a program")
            self.c.unserialize(raw)
        except RuntimeError:                # no program running here, or other files: start again the way the
            self._replay(launch, disk or b"")       # saving run did, on the state's disk (b"" = no written files)
            if self._log is not None:
                raise RuntimeError("the state's launch inputs did not start a program")
            self.c.unserialize(raw)
            if self._files(self._disk()) != self._files(disk):
                raise RuntimeError("the launch inputs changed the files on disk; state not usable")
        self._launch, self._log = launch, None

    FILE_SAVES = True
    SAVE_HELP = ("`.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their "
                 "DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: "
                 "`ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder.")

    def text(self):
        """The text-mode screen as a list of lines (characters only), or None in a graphics mode. Read from
        video memory through the core (retro_gamedb_readb); peek does not reach it."""
        mode = self.peek(0x449, 1)[0]
        if mode not in (0, 1, 2, 3, 7):
            return None
        cols, rows = self.peek(0x44A, 1)[0] or 80, (self.peek(0x484, 1)[0] or 24) + 1
        base = 0xB0000 if mode == 7 else 0xB8000
        rd = self.c.L.retro_gamedb_readb
        out = []
        for r in range(rows):
            raw = bytes(rd(base + (r * cols + c) * 2) for c in range(cols))
            out.append("".join(chr(b) if 32 <= b < 127 else " " if b in (0, 255) else "?" for b in raw).rstrip())
        return out

    def battery(self, size):
        """The files written by the game (save ZIP), b"" when it has written none."""
        return self._disk() or b""

    def _mem(self):
        """(pointer to physical address 0, size): the core announces program memory first while DOS runs."""
        maps = self.c.maps
        if not maps:
            raise SystemExit("the DOS machine has no memory yet (run a frame first)")
        base = min(ptr for _, _, ptr in maps)
        return base, sum(size for _, size, _ in maps)

    def peek(self, addr, n, bank=None):
        import ctypes
        if bank is not None:
            raise NotImplementedError("DOS memory has no banks: use the physical address (segment * 16 + offset)")
        base, size = self._mem()
        if addr < 0 or addr + n > size:
            raise ValueError("address %x..%x outside the %d KiB of the machine" % (addr, addr + n, size // 1024))
        return ctypes.string_at(base + addr, n)

    def poke(self, addr, data):
        import ctypes
        base, size = self._mem()
        data = bytes(data)
        if addr < 0 or addr + len(data) > size:
            raise ValueError("address %x outside the %d KiB of the machine" % (addr, size // 1024))
        ctypes.memmove(base + addr, data, len(data))

    def regs(self):
        v = self.c.L.retro_gamedb_pc()
        return {"pc": "%04x:%04x" % (v >> 16, v & 0xFFFF)}


# ------------------------------------------------------------------ Apple II (AppleWin libretro core)
class Apple2(Libretro):
    """AppleWin (Linux port by audetto, libretro core, in-process through tools/lrcore.py, patched with
    tools/applewin-debug.patch: fixed power-on RAM and clock, deterministic random numbers, one-key keyboard
    latch, disk insert/eject, peek/poke, program counter). A game is one disk image or a ZIP of its disk images
    (the sides in name order); disk 1 is in drive 1 at power-on, emu.disk(n, drive) changes disks.
    Model: MACHINE[-VIDEO][-joy][-wpN ...] (wpN = disk N write-protected). Machines: iie (enhanced //e, 128K, default), iieorig, iiplus, ii, iijplus.
    Video: tv (default), monitor, idealized, rgb, bwtv, mono, green, amber. joy = a joystick is plugged in.
    Keys are keyboard keys (KEYS; letters arrive as capitals, shift+letter as lowercase), openapple/solidapple
    (= joystick buttons 0/1, also button0/button1) and joyleft/joyright/joyup/joydown.
    Memory: 0000-FFFF is what the program reads right now (banking followed, ROM included, soft switches read
    0); 10000-1FFFF is the auxiliary 64K of a //e; 20000-2FFFF is the main 64K as stored, whatever is mapped
    (2C000-2CFFF = language card bank 1 of D000-DFFF, 2D000-2FFFF = bank 2 and E000-FFFF RAM): games keep data
    there while ROM is mapped. peek has no side effects; poke writes RAM only."""
    KEYS = {k: v for k, v in _retrok().items() if not k.startswith(("kp", "f")) and k not in (
        "insert", "home", "end", "pageup", "pagedown", "rshift", "rctrl", "alt", "ralt", "backquote")}
    KEYS.update({"f": 102, "openapple": 308, "solidapple": 307, "button0": 308, "button1": 307})
    JOY = {"joyup": "up", "joydown": "down", "joyleft": "left", "joyright": "right"}
    keys = set(KEYS) | set(JOY)
    extensions = (".dsk", ".do", ".po", ".nib", ".woz", ".2mg", ".hdv")
    native_size = (560, 384)
    emulator = "AppleWin libretro core"
    SO = os.path.join(HERE, "applewin", "build", "source", "frontends", "libretro", "applewin_libretro.so")
    MACHINES = {"iie": "Apple //e (enhanced)", "iieorig": "Apple //e (original)", "iiplus": "Apple II Plus",
                "ii": "Apple II (original)", "iijplus": "Apple II J-Plus"}
    VIDEO = {"tv": "Color TV", "monitor": "Color (Composite Monitor)", "idealized": "Color (Composite Idealized)",
             "rgb": "Color (RGB Card/Monitor)", "bwtv": "B&W TV", "mono": "Monochrome (White)",
             "green": "Monochrome (Green)", "amber": "Monochrome (Amber)"}
    EPOCH = 504921600           # 1986-01-01 00:00:00 UTC (clock cards)
    FRAME_USEC = 16667
    SEARCH = [(0x0000, 0xC000)]
    SHIFTED = Dos.SHIFTED
    NAMES = Dos.NAMES
    BLOCK = 4096                # changed parts of a disk image are kept in blocks of this size
    STATE = b"GAMEDB-APPLE2-STATE-1\n"
    FILE_SAVES = True
    SAVES_ARE_DUMPS = True      # play.py export keeps them in rom/saves/<platform>/<slug>/ (game data)
    SAVE_HELP = ("`.sav` = a ZIP of the disk images the game has written to (whole images, same names as in the "
                 "game's ZIP): unzip it and use those images in place of the originals in any Apple II emulator.")

    @staticmethod
    def zip_disks(data):
        """Names of the disk images in a ZIP, in play order (sorted by name, case ignored); [] if it is not a
        ZIP of disk images (any other kind of file inside = not ours, e.g. a DOS game)."""
        import io, zipfile
        try:
            names = [n for n in zipfile.ZipFile(io.BytesIO(data)).namelist() if not n.endswith("/")]
        except zipfile.BadZipFile:
            return []
        if not names or not all(os.path.splitext(n)[1].lower() in Apple2.extensions for n in names):
            return []
        if len({os.path.basename(n).lower() for n in names}) != len(names):
            raise SystemExit("two disk images in the ZIP have the same file name")
        return sorted(names, key=lambda n: os.path.basename(n).lower())

    @staticmethod
    def image_kind(data):
        if data[:4] in (b"WOZ1", b"WOZ2"):
            return "%s flux-level floppy image" % data[:4].decode()
        if data[:4] == b"2IMG":
            return "2IMG container, %d KiB" % (len(data) // 1024)
        return {143360: "5.25 inch floppy, 140 KiB sector image", 232960: "5.25 inch floppy, nibble image",
                819200: "3.5 inch disk / hard disk volume, 800 KiB"}.get(
                    len(data), "hard disk volume, %d KiB" % (len(data) // 1024))

    @classmethod
    def identify(cls, data):
        import io, zipfile
        names = cls.zip_disks(data)
        if names:
            z = zipfile.ZipFile(io.BytesIO(data))
            disks = [{"name": os.path.basename(n), "kind": cls.image_kind(z.read(n)),
                      "sha1": __import__("hashlib").sha1(z.read(n)).hexdigest()} for n in names]
        elif data[:2] == b"PK":
            raise SystemExit("this ZIP is not a set of Apple II disk images (%s)" % " ".join(cls.extensions))
        else:
            disks = [{"kind": cls.image_kind(data)}]
        return {"platform": "apple2", "model": "iie", "disks": disks}

    def open(self, rom, model=None, seed=1, turbo=True, sav=None):
        import ctypes, io, tempfile, zipfile
        import lrcore
        if not os.path.exists(self.SO):
            raise SystemExit("%s missing: run sh tools/setup_emu.sh apple2" % self.emulator)
        parts = (model or "iie").split("-")
        machine, video, joy, self.protect = parts[0], "tv", False, set()
        for p in parts[1:]:
            if p == "joy":
                joy = True
            elif p[:2] == "wp" and p[2:].isdigit():         # wpN: disk N is write-protected
                self.protect.add(int(p[2:]))
            elif p in self.VIDEO:
                video = p
            else:
                machine = None
        if machine not in self.MACHINES:
            raise SystemExit("unknown Apple II model %r (MACHINE[-VIDEO][-joy][-wpN]; machines: %s; video: %s)" % (
                model, " ".join(self.MACHINES), " ".join(self.VIDEO)))
        # Private copies of the disk images: the game writes to them, the registered dump is never touched.
        self.tmp = tempfile.mkdtemp(prefix="gamedb-core")
        self.dir = os.path.join(self.tmp, "disks")
        os.makedirs(self.dir)
        data = open(rom, "rb").read()
        names = self.zip_disks(data)
        if names:
            z = zipfile.ZipFile(io.BytesIO(data))
            self._orig = {os.path.basename(n): z.read(n) for n in names}
            self.disks = [os.path.basename(n) for n in names]
        else:
            self.disks = ["disk" + os.path.splitext(rom)[1].lower()]
            self._orig = {self.disks[0]: data}
        start = dict(self._orig)
        if sav:                                             # a save = ZIP of whole images: a game disk under
            z = zipfile.ZipFile(sav)                        # its own name replaces it; any other name is an
            for n in sorted(z.namelist(), key=str.lower):   # extra disk after the game's own (a character
                if n.endswith("/"):                         # disk of another game, a blank disk to format)
                    continue
                if os.path.splitext(n)[1].lower() not in self.extensions or "/" in n:
                    raise SystemExit("%s holds %s, which is not a disk image" % (sav, n))
                if n not in start:
                    self.disks.append(n)
                    self._orig[n] = z.read(n)
                start[n] = z.read(n)
        for n, d in start.items():
            open(os.path.join(self.dir, n), "wb").write(d)
        self.c = lrcore.Core(self.SO, None, system_dir=self.tmp, save_dir=self.tmp, options={
            "applewin_machine": self.MACHINES[machine], "applewin_video_mode": self.VIDEO[video],
            "applewin_video_style": "560 x 192"}, frame_usec=self.FRAME_USEC, epoch=self.EPOCH, private=True)
        L = self.c.L
        L.retro_gamedb_pc.restype = ctypes.c_uint
        L.retro_gamedb_peek.restype, L.retro_gamedb_peek.argtypes = ctypes.c_uint, [ctypes.c_uint]
        L.retro_gamedb_poke.restype, L.retro_gamedb_poke.argtypes = ctypes.c_int, [ctypes.c_uint, ctypes.c_uint]
        L.retro_gamedb_insert.restype = ctypes.c_int
        L.retro_gamedb_insert.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        if joy:
            L.retro_set_controller_port_device(0, lrcore.DEVICE_JOYPAD)
        self.c.size = self.native_size
        self.drives = [None, None, None]                    # floppy drive 1, floppy drive 2, hard disk 1
        self._down, self._search = set(), None
        self.disk(1)
        return self

    # ---- disks
    def _put(self, slot, name):
        path = os.path.join(self.dir, name).encode() if name else None
        if not self.c.L.retro_gamedb_insert(slot, path, 0):
            return False
        self.drives[slot] = name
        self._protect()
        return True

    def _protect(self):
        """Tell the core which drives hold a write-protected disk (model wpN); after every insert and state load."""
        for slot in (0, 1):
            n = self.drives[slot]
            if n:
                self.c.L.retro_gamedb_protect(slot, 1 if self.disks.index(n) + 1 in self.protect else 0)

    def disk(self, n, drive=1):
        """Put disk n (1 = first image of the game; 0 = none) into floppy drive 1 or 2. An image that is not a
        floppy (hard disk volume) goes to the hard disk in slot 7 instead; only as drive 1."""
        if drive not in (1, 2) or not 0 <= n <= len(self.disks):
            raise ValueError("disk:%d in drive %d: this game has disks 1-%d (%s), drives 1-2" % (
                n, drive, len(self.disks), ", ".join(self.disks)))
        name = self.disks[n - 1] if n else None
        for slot in range(3):                               # a disk is in one drive at a time
            if name and self.drives[slot] == name and slot != drive - 1:
                self._put(slot, None)
        if self._put(drive - 1, name):
            return
        if drive == 1 and self._put(2, name):
            return
        raise ValueError("the emulator refused the disk image %s" % name)

    def _changed(self):
        """{name: {"size": n, "blocks": [offsets]}}, payload: the parts of the images that differ from the dump."""
        head, blob = {}, []
        for n in self.disks:
            cur, orig = open(os.path.join(self.dir, n), "rb").read(), self._orig[n]
            if cur == orig:
                continue
            offs = [o for o in range(0, len(cur), self.BLOCK) if cur[o:o + self.BLOCK] != orig[o:o + self.BLOCK]]
            head[n] = {"size": len(cur), "blocks": offs}
            blob += [cur[o:o + self.BLOCK] for o in offs]
        return head, b"".join(blob)

    def save_state(self, path):
        """The core's state names the disk images in the drives and keeps the track under the head; what the
        game wrote to the images so far is stored next to it (the changed blocks), so a state made after an
        in-game save still has that save on disk wherever it is loaded."""
        import json
        raw = zlib.compress(self.c.serialize(), 1)
        head, blob = self._changed()
        head = json.dumps({"drives": self.drives, "disks": head, "blob": len(blob)}).encode()
        open(os.path.abspath(path), "wb").write(self.STATE + head + b"\n" + blob + raw)

    def load_state(self, path):
        import json
        data = open(os.path.abspath(path), "rb").read()
        if not data.startswith(self.STATE):
            raise RuntimeError("not an Apple II savestate of this tool version (delete work/cache): %s" % path)
        head, rest = data[len(self.STATE):].split(b"\n", 1)
        head = json.loads(head)
        blob, raw = rest[:head["blob"]], rest[head["blob"]:]
        for slot in range(3):                   # empty the drives first: taking a disk out writes its last
            if self.drives[slot]:               # track to the image, which must not hit the restored files
                self._put(slot, None)
        pos = 0
        for n in self.disks:
            img = bytearray(self._orig[n])
            if n in head["disks"]:
                d = head["disks"][n]
                img = img[:d["size"]] + bytes(max(0, d["size"] - len(img)))
                for o in d["blocks"]:
                    k = min(self.BLOCK, d["size"] - o)
                    img[o:o + k] = blob[pos:pos + k]
                    pos += k
            p = os.path.join(self.dir, n)
            if open(p, "rb").read() != img:
                open(p, "wb").write(img)
        self.c.L.retro_gamedb_insert(0, os.path.join(self.dir, self.disks[0]).encode(), 0)   # names the folder
        self.c.L.retro_gamedb_insert(0, None, 0)
        self.c.unserialize(zlib.decompress(raw))
        self.drives = head["drives"]
        self._protect()

    def battery(self, size):
        """The disk images the game has written to, whole, as a ZIP (b"" when it has written nothing)."""
        import io, zipfile
        self.c.L.retro_gamedb_flush()
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for n in self.disks:
                cur = open(os.path.join(self.dir, n), "rb").read()
                if cur != self._orig[n]:
                    info = zipfile.ZipInfo(n, (1986, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(info, cur)
            count = len(z.namelist())
        return out.getvalue() if count else b""

    # ---- keyboard
    def _event(self, key, down, mods):
        code = self.KEYS[key]
        char = 0
        if len(key) == 1 and not key.isalpha() or key in self.NAMES.values():
            base = key if len(key) == 1 else {v: k for k, v in self.NAMES.items()}[key]
            if base != "\n" and not mods & 2:                # ctrl: the core's own table by key code
                shifted = {v: k for k, v in self.SHIFTED.items()}
                char = ord(shifted.get(base, base) if mods & 1 else base)
        self.c.key(code, down, char, mods)

    def input(self, keys):
        keys = set(keys)
        mods = (1 if "shift" in keys else 0) | (2 if "ctrl" in keys else 0)
        for k in sorted(self._down - keys):
            if k in self.KEYS and k not in ("shift", "ctrl"):
                self._event(k, False, mods)
        for k in sorted(keys - self._down):
            if k in self.KEYS and k not in ("shift", "ctrl"):
                self._event(k, True, mods)
        self._down = keys
        self.c.keys = {self.JOY[k] for k in keys if k in self.JOY}

    def type_text(self, text, hold=4, gap=4):
        """Type text as written: capitals are the plain letter keys, small letters need a //e."""
        for ch in text:
            if ch == "\n":
                code, char, mods = 13, 0, 0
            elif ch.isalpha() and ch.isascii():
                code, char, mods = ord(ch.lower()), 0, 0 if ch.isupper() else 1
            elif 0x20 <= ord(ch) < 0x7F:
                code, char, mods = 0, ord(ch), 0
            else:
                raise ValueError("cannot type %r" % ch)
            self.c.key(code, True, char, mods)
            self.frames(hold)
            self.c.key(code, False, char, mods)
            self.frames(gap)

    # ---- memory
    def peek(self, addr, n, bank=None):
        if bank is not None:                                # the 64K behind the banking: 0 main, 1 auxiliary
            if bank not in (0, 1) or addr + n > 0x10000:
                raise ValueError("bank 0 = main 64K, 1 = auxiliary 64K")
            return self.c.peek_map(bank * 0x10000 + addr, n)
        if addr >= 0x20000:
            return self.c.peek_map(addr - 0x20000, n)
        if addr >= 0x10000:
            return self.c.peek_map(addr, n)
        f = self.c.L.retro_gamedb_peek
        return bytes(f((addr + i) & 0xFFFF) for i in range(n))

    def poke(self, addr, data):
        data = bytes(data)
        if addr >= 0x20000:
            for i, b in enumerate(data):
                self.c.L.retro_gamedb_poke_main((addr + i) & 0xFFFF, b)
            return
        if addr >= 0x10000:
            return self.c.poke_map(addr, data)
        for i, b in enumerate(data):
            if not self.c.L.retro_gamedb_poke((addr + i) & 0xFFFF, b):
                raise ValueError("%04X is not RAM right now (ROM or I/O)" % ((addr + i) & 0xFFFF))

    def regs(self):
        return {"pc": "%04x" % self.c.L.retro_gamedb_pc()}


PLATFORMS = {"gb": GameBoy, "gbc": GameBoy, "nes": Nes, "snes": Snes, "dos": Dos, "apple2": Apple2}


def backend(platform):
    if platform not in PLATFORMS:
        raise SystemExit("platform %r not supported yet (have: %s)" % (platform, ", ".join(sorted(PLATFORMS))))
    return PLATFORMS[platform]()


def by_extension(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".zip" and os.path.exists(path) and Apple2.zip_disks(open(path, "rb").read()):
        return "apple2", Apple2                 # a ZIP of disk images; any other ZIP is a DOS game
    for name, cls in PLATFORMS.items():
        if ext in cls.extensions:
            return name, cls
    raise SystemExit("unknown ROM type %r (supported: %s)" % (
        ext, " ".join(sorted({e for c in PLATFORMS.values() for e in c.extensions}))))


def crc32(data):
    return "%08x" % (zlib.crc32(data) & 0xFFFFFFFF)
