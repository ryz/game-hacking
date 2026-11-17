#!/bin/sh
# Fetch and build the emulators into tools/ (pinned commits, both gitignored):
#   gbemu-cli  headless SameBoy with a JSON-lines API. Backend for gb/gbc.
#              tools/gbemu-linux.patch fixes the Linux link (macOS-only symbol).
#   mesen      Mesen as a libretro core (driven in-process by tools/lrcore.py). Backend for nes.
#              tools/mesen-debug.patch adds retro_mesen_peek/poke/pc (whole CPU address space, program counter).
#   mesen-s    Mesen-S as a libretro core (same driver). Backend for snes.
#              tools/mesen-s-debug.patch adds retro_mesen_peek/poke/pc (24-bit address space).
# sh tools/setup_emu.sh [gb|nes|snes]   (default: all)
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
