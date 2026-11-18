#!/bin/sh
# The emulator (gbemu-cli, a headless SameBoy) is shared by all games: built once into tools/gbemu-cli at the
# repo root. This wrapper only calls the shared setup.
set -e
exec sh "$(dirname "$0")/../../../../../tools/setup_emu.sh" gb
