#!/bin/sh
# Fetch and build the emulators into tools/ (pinned commits, both gitignored):
#   gbemu-cli  headless SameBoy with a JSON-lines API. Backend for gb/gbc.
#              tools/gbemu-linux.patch fixes the Linux link (macOS-only symbol).
#   mesen      Mesen as a libretro core (driven in-process by tools/lrcore.py). Backend for nes.
#              tools/mesen-debug.patch adds retro_mesen_peek/poke/pc (whole CPU address space, program counter).
#   mesen-s    Mesen-S as a libretro core (same driver). Backend for snes.
#              tools/mesen-s-debug.patch adds retro_mesen_peek/poke/pc (24-bit address space).
#   dosbox-pure  DOSBox Pure as a libretro core (same driver). Backend for dos (a game = a ZIP of its files).
#              tools/dosbox-pure-debug.patch adds retro_gamedb_set_time (emulated clock set by the driver, not
#              the host), retro_gamedb_sync (wait for the emulation thread at the frame end) and retro_gamedb_pc; it also makes a loaded savestate continue exactly like the run that made it,
#              and adds retro_gamedb_flush (write the save ZIP of changed files now).
#              Fetched from the libretro mirror: the author's GitHub repository is only a pointer to Codeberg.
# sh tools/setup_emu.sh [gb|nes|snes|dos]   (default: all)
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
if [ "$want" = all ] || [ "$want" = dos ]; then
  if [ ! -d dosbox-pure ]; then
    mkdir dosbox-pure
    (cd dosbox-pure && git init -q && git remote add origin https://github.com/libretro/dosbox-pure.git &&
      git fetch -q --depth 1 origin e39497e7c2a32c67c26e6598dd14f6d58c384bfd && git checkout -q FETCH_HEAD &&
      git apply ../dosbox-pure-debug.patch)
  fi
  make -C dosbox-pure -j"$(nproc 2>/dev/null || echo 2)"
fi
