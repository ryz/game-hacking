# Apple II

Platform notes for `apple2` games (Apple II, II Plus, //e). The general rules (routes, tokens, the working loop)
are in [README.md](README.md). Added 2026-11-18. First game: Might and Magic Book One
(`games/apple2/might-and-magic/`, four disk sides), played from power-on through two disk changes into the
wilderness, with an in-game save.

## Backend
AppleWin (the Linux port by audetto), built as a libretro core and run inside the Python process by
`tools/lrcore.py`. Built by `sh tools/setup_emu.sh apple2` at a pinned commit into `tools/applewin/` (needs
cmake; the firmware ROMs are part of the AppleWin source, nothing else to supply). `tools/applewin-debug.patch`:
- Power-on RAM, the clock (No-Slot clock, ThunderClock) and the emulator's random numbers (disk latch noise,
  weak bits, track-seam jitter of copy-protected images) no longer come from the host: RAM is the same on every
  power-on, the clock starts at 1986-01-01 00:00:00 and follows the emulated frames, the random numbers are a
  hash of the emulated cycle counter.
- One call runs exactly one video frame, counted on the cycle counter that a savestate keeps. Before, the length
  of a frame followed the host's sound buffer, and a run loaded from a state drifted from the run that made it.
- The keyboard is the real one-key latch (below).
- The colour tables are built from cleared filters every time. Before, a state load rebuilt them with leftover
  filter memory and some colours came out 1 off: a run from a cached checkpoint drew other pixels than the run
  that made it (found with Might and Magic's wilderness, test `test_apple2_colour_after_state_load`).
- `retro_gamedb_insert` (put an image into a drive or take it out), `retro_gamedb_flush` (write the track in
  memory to the image), `retro_gamedb_peek/poke/pc`, `retro_gamedb_set_time`; the core's log is silent unless
  `GAMEDB_CORE_LOG` is set.

Checked (tests `test_apple2_*`): two power-ons give the same frames and RAM; a run continued after a savestate
equals one loaded from it into a machine that has not run; states taken while the drive is reading are exact.

## A game is a disk image or a ZIP of disk images
`python3 tools/intake.py GAME.dsk --region na [--slug S --title "T"]` (the region of the release; a disk image does not say it), or `intake.py GAME.zip` for a game with several
disks or sides. Formats: `.dsk .do .po .nib .woz .2mg .hdv`. A ZIP that holds only such files is an Apple II
game (any other ZIP is a DOS game); its images are the disks in name order, listed in `game.json` "header" with
their SHA-1s. Name the files so that they sort in play order (`1 Boot.dsk`, `2 Scenario.dsk`). The game lands in
`games/apple2/<slug>/`, the dump in `rom/<slug>.<ext>` (never committed).
- Disk 1 is in drive 1 at power-on and boots. `disk:N` puts disk N into drive 1, `disk2:N` into drive 2,
  `disk:0` empties the drive. A disk is in one drive at a time.
- Images that are not 5.25 inch floppies (800 KiB and hard disk volumes) go to the hard disk controller in slot 7,
  which boots before the floppy. Not tried with a real game yet.
- The emulator works on private copies: the game can write to every disk, the registered dump never changes.
  Write protection is not offered yet (a game that wants a write-protected master would complain).
- A game asks for a side by letter ("INSERT DISK B AND PRESS 'RETURN'"): answer `disk:2,enter` and give it
  `w600` to load. Checked with Might and Magic: sides 2 and 3 swapped in mid-game, checkpoints after a swap
  rebuild and reload exactly.
- A sector image (`.dsk`) of a copy-protected original may hang at boot re-reading one track (Might and
  Magic's side 1, marked `[b]`); a `.nib` or `.woz` of the same side, or a cracked copy, is needed then.
- No reset key yet (Ctrl-Reset, Ctrl-Open Apple-Reset). A boot that ends in the monitor (`*`) continues with
  `6,ctrl+p,enter`; from BASIC (`]`) with `type:PR#6\n`.

## Models
`game.json` "model" is `MACHINE[-VIDEO][-joy]`:
- machine: `iie` (enhanced //e, 128K, 80 columns; default), `iieorig` (unenhanced //e), `iiplus`, `ii`, `iijplus`.
  Try `iiplus` when an old game misbehaves on the //e.
- video: `tv` (colour television, the emulator's default: colours blend), `monitor`, `idealized` (crisp solid
  colours), `rgb`, `bwtv`, `mono` (white), `green`, `amber`.
- `joy`: a joystick is plugged in (centred).
- `wpN` (repeatable): disk N is write-protected (`iiplus-wp1`). Wizardry's boot disk checks it: it writes to
  itself after the title and hangs on a black screen unless the write is refused.
- Apple Pascal programs (Wizardry) switch a //e to 80 columns, where every second text column is blank: use
  `iiplus` for them. Without it the paddle inputs read as not connected.
Slots: Disk II in 6, hard disk in 7, Mockingboard in 4 (the core's defaults). NTSC only.

## Screenshots
Always 560x384: the 280x192 screen with every pixel doubled, so 80-column text and double hi-res fit as well.
The text cursor blinks, so text screens rarely `settle`; capture anyway.

## Keys
`a`-`z`, `0`-`9`, `enter esc space tab backspace delete left right up down`, `minus equals comma period slash
semicolon quote leftbracket rightbracket backslash`, modifiers `shift` and `ctrl` (`ctrl+c`, `shift+1` = `!`),
`openapple` and `solidapple` (the same as joystick buttons 0 and 1: `button0`, `button1`), with `-joy` also
`joyleft joyright joyup joydown`.
- A letter key arrives as a capital (caps lock down, what almost every game expects); `shift+a` is a small `a`.
  `left` is also the backspace of the II Plus (it has no up/down arrows: games use I J K M or similar).
- `w30` is "wait 30 frames"; the W key is `w`.
- `type:SOME TEXT` types a string exactly as written (no comma inside, `\n` = Return). Write capitals: small
  letters are small letters.
- The Apple II keyboard is a latch for one key. A key pressed while the program is busy (loading, drawing)
  replaces the one before it: wait for the prompt, then press. A held key is one key press (no auto-repeat), so
  walk with `i*5`, not `i:60`.

## Memory
`peek`, `poke`, `find` and `dump` use the 64K the program sees right now: banking followed (auxiliary memory,
language card), ROM included, the soft switches `C000-C0FF` read as 0 (no side effects). `10000-1FFFF` is the
auxiliary 64K of a //e wherever it is mapped. `20000-2FFFF` is the main 64K as stored, mapped or not
(`2C000-2CFFF` = language card bank 1 of `D000`, `2D000-2FFFF` = bank 2 and the RAM under the ROM): games keep
data there while ROM is mapped (Might and Magic's character records are at `2C000`). `poke` writes RAM only (ROM and I/O are refused). `find` covers
`0000-BFFF`. Text page 1 is `0400-07FF` (screen codes: high bit set = normal), hi-res page 1 `2000-3FFF`.
`status` shows the program counter. 6502 code can be read with `tools/dis6502.py` only for NES files so far.

## Saves
Apple II games save to the floppy (often to a scenario or character disk). A savestate holds the machine, the
disk images are files, so the backend stores the changed parts of the images with every state and puts them back
on load: a state made before an in-game save has the old disk, one made after it has the save, in the same
process and in a new one (`test_apple2_state_carries_disk_writes`, with DOS 3.3 `SAVE`).
- `play.py export NAME "desc"` writes `games/apple2/<slug>/saves/NAME.sav`: a ZIP of the whole images the game
  has written to, under their names from the game's ZIP (`disk.<ext>` for a single-image game). For the owner:
  unzip and use those images in place of the originals in any Apple II emulator. `sav:NAME` powers on with them.
- An exported `.sav` holds whole disk images, so it is game data (program and maps, not only the save):
  `play.py export` writes it to `rom/saves/apple2/<slug>/` (uncommitted) and only its line in
  `games/apple2/<slug>/saves/README.md` is committed; `sav:NAME` finds it there. Open: an export that
  holds only the changed blocks.
- **Extra disks** (2026-11-19): an image in the `sav:` ZIP whose name is not one of the game's disks becomes
  an additional disk after the game's own, in name order (`disk:N` with the next numbers). Use it for a
  character disk of another game (Wizardry II takes the party from the Wizardry I scenario disk) or a blank
  disk a game wants to format. Make one from an export: unzip the `.sav`, zip the image again under a new
  name (`T Wizardry I.dsk`) into `rom/saves/<slug>/NAME.sav`. The same name as a game disk replaces that disk.
- Only this tool reads the `.state` files.

## Not supported yet
Reset keys, write-protected disks, PAL machines, the Apple IIc and IIgs, cassette, printer and serial cards,
Z80 card, mouse card, held keys (auto-repeat, the //e "any key down" flag), 13-sector disks (untested).
