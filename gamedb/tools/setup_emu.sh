#!/bin/sh
# Fetch and build gbemu-cli (headless SameBoy with a JSON-lines API) into tools/gbemu-cli. Backend for gb/gbc.
# Pinned commit; tools/gbemu-linux.patch fixes the Linux link (macOS-only symbol).
set -e
cd "$(dirname "$0")"
if [ ! -d gbemu-cli ]; then
  git clone https://github.com/gopherbone/gbemu-cli.git
  (cd gbemu-cli && git checkout 715f2506c34c1d14f4c644d249ab121b1411ab5c && git apply ../gbemu-linux.patch)
fi
make -C gbemu-cli
