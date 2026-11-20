#!/bin/sh
# Fetch and build the emulators into tools/ (pinned commits, both gitignored):
#   gbemu-cli  headless SameBoy with a JSON-lines API. Backend for gb/gbc.
#              tools/gbemu-linux.patch fixes the Linux link (macOS-only symbol).
#   mesen      Mesen as a libretro core (driven in-process by tools/lrcore.py). Backend for nes.
#              tools/mesen-debug.patch adds retro_mesen_peek/poke/pc (whole CPU address space, program counter).
#   mesen-s    Mesen-S as a libretro core (same driver). Backend for snes.
#              tools/mesen-s-debug.patch adds retro_mesen_peek/poke/pc (24-bit address space).
#   gpgx       Genesis Plus GX as a libretro core (same driver). Backend for sms (Master System / Mark III) and
#              md (Mega Drive / Genesis): `sms` and `md` build the same core.
#              tools/gpgx-debug.patch adds retro_gamedb_peek/poke/pc (Z80 address space, program counter) and
#              retro_gamedb_sram (the whole cartridge RAM), and silences the core's info-level log;
#              retro_gamedb_peek68k/poke68k/pc68k do the same for the 68000 (Mega Drive address space).
#   dosbox-pure  DOSBox Pure as a libretro core (same driver). Backend for dos (a game = a ZIP of its files).
#              tools/dosbox-pure-debug.patch adds retro_gamedb_set_time (emulated clock set by the driver, not
#              the host), retro_gamedb_sync (wait for the emulation thread at the frame end) and retro_gamedb_pc; it also makes a loaded savestate continue exactly like the run that made it,
#              and adds retro_gamedb_flush (write the save ZIP of changed files now).
#              Fetched from the libretro mirror: the author's GitHub repository is only a pointer to Codeberg.
#   applewin   AppleWin (Linux port by audetto) as a libretro core (same driver). Backend for apple2 (a game = a
#              disk image or a ZIP of disk images). Needs cmake. tools/applewin-debug.patch makes the machine
#              independent of the host (power-on RAM, clock, random numbers, frame length counted in emulated
#              cycles so a loaded savestate continues exactly), turns the type-ahead queue into the real
#              one-key latch, and adds retro_gamedb_insert/flush/peek/poke/pc and retro_gamedb_set_time; it also
#              drops a font resource only the SDL frontend needs (it lives in a git submodule).
#              The build embeds the firmware with `xxd -i`; without xxd, tools/xxd_i.py stands in.
#   puae       PUAE (libretro-uae) as a libretro core (same driver). Backend for amiga (a game = an ADF or a ZIP of
#              ADFs; real Kickstart ROMs go into rom/kickstart/, the core also has the free AROS one built in).
#              tools/puae-debug.patch: a loaded savestate continues exactly like the run that made it (the core
#              restores at the start of the next frame instead of emulating frames inside retro_unserialize),
#              the battery clock follows retro_gamedb_set_time, a restore takes its disks from the folder set
#              with retro_gamedb_disk_dir, retro_gamedb_peek/poke/pc/insert/flush; it also fixes the core's
#              fallback logger (it wrote to a NULL stderr and crashed without a frontend log interface).
# sh tools/setup_emu.sh [gb|nes|snes|sms|md|dos|apple2|amiga]   (default: all)
set -e
cd "$(dirname "$0")"
want=${1:-all}
if [ "$want" = all ] || [ "$want" = gb ]; then
  if [ ! -d gbemu-cli ]; then
    git clone https://github.com/gopherbone/gbemu-cli.git
    (cd gbemu-cli && git checkout 715f2506c34c1d14f4c644d249ab121b1411ab5c && git apply ../gbemu-linux.patch)
  fi
  make -C gbemu-cli
fi
if [ "$want" = all ] || [ "$want" = nes ]; then
  if [ ! -d mesen ]; then
    mkdir mesen
    (cd mesen && git init -q && git remote add origin https://github.com/libretro/Mesen.git &&
      git fetch -q --depth 1 origin 0102910c39ad1a62bc3f784466f3f67ca9eae335 && git checkout -q FETCH_HEAD &&
      git apply ../mesen-debug.patch)
  fi
  make -C mesen/Libretro -j"$(nproc 2>/dev/null || echo 2)"
fi
if [ "$want" = all ] || [ "$want" = snes ]; then
  if [ ! -d mesen-s ]; then
    mkdir mesen-s
    (cd mesen-s && git init -q && git remote add origin https://github.com/libretro/Mesen-S.git &&
      git fetch -q --depth 1 origin 9e4fdeb9b336470bc96beb8765b2e79c86a2da1e && git checkout -q FETCH_HEAD &&
      git apply ../mesen-s-debug.patch)
  fi
  make -C mesen-s/Libretro -j"$(nproc 2>/dev/null || echo 2)"
fi
if [ "$want" = all ] || [ "$want" = sms ] || [ "$want" = md ]; then
  if [ ! -d gpgx ]; then
    mkdir gpgx
    (cd gpgx && git init -q && git remote add origin https://github.com/libretro/Genesis-Plus-GX.git &&
      git fetch -q --depth 1 origin b9c2316441978d4015ba30e9a95d9b0e6f8ee981 && git checkout -q FETCH_HEAD &&
      git apply ../gpgx-debug.patch)
  fi
  make -C gpgx -f Makefile.libretro -j"$(nproc 2>/dev/null || echo 2)"
  [ "$want" = sms ] || python3 -c "import capstone" 2>/dev/null || pip install -q capstone   # tools/dis68k.py
fi
if [ "$want" = all ] || [ "$want" = dos ]; then
  if [ ! -d dosbox-pure ]; then
    mkdir dosbox-pure
    (cd dosbox-pure && git init -q && git remote add origin https://github.com/libretro/dosbox-pure.git &&
      git fetch -q --depth 1 origin e39497e7c2a32c67c26e6598dd14f6d58c384bfd && git checkout -q FETCH_HEAD &&
      git apply ../dosbox-pure-debug.patch)
  fi
  make -C dosbox-pure -j"$(nproc 2>/dev/null || echo 2)"
fi
if [ "$want" = all ] || [ "$want" = apple2 ]; then
  if [ ! -d applewin ]; then
    mkdir applewin
    (cd applewin && git init -q && git remote add origin https://github.com/audetto/AppleWin.git &&
      git fetch -q --depth 1 origin e9ebeb7c83b7ffe67d8604a3b79d34925d56aada && git checkout -q FETCH_HEAD &&
      git apply ../applewin-debug.patch)
  fi
  mkdir -p applewin/build/shim
  if ! command -v xxd >/dev/null 2>&1; then
    printf '#!/bin/sh\nexec python3 "%s/xxd_i.py" "$@"\n' "$PWD" > applewin/build/shim/xxd
    chmod +x applewin/build/shim/xxd
  fi
  (cd applewin/build && PATH="$PWD/shim:$PATH" &&
    cmake -DBUILD_LIBRETRO=ON -DENABLE_NETWORKING=OFF -DCMAKE_BUILD_TYPE=Release .. >/dev/null &&
    make -j"$(nproc 2>/dev/null || echo 2)" applewin_libretro)
fi
if [ "$want" = all ] || [ "$want" = amiga ]; then
  if [ ! -d puae ]; then
    mkdir puae
    (cd puae && git init -q && git remote add origin https://github.com/libretro/libretro-uae.git &&
      git fetch -q --depth 1 origin d366f77c60e5a5f059f129cc3773d3048306083b && git checkout -q FETCH_HEAD &&
      git apply ../puae-debug.patch)
  fi
  make -C puae -j"$(nproc 2>/dev/null || echo 2)"
fi
