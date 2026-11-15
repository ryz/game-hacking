"""Platform registry: one entry per supported system. Everything platform-specific lives here, so another system
(NES, SNES, GBA, ...) is added by writing one Backend subclass and one PLATFORMS entry; the tools above it
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


PLATFORMS = {"gb": GameBoy, "gbc": GameBoy}


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
