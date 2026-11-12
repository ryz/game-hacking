"""Persistent play session: one emulator kept running in the background, driven by short commands.
No re-boot or state reload between steps, so manual and agent play is a command per action.

  python3 tools/play.py start [--rom ROM] [--state S | --seq "boot,PARTY"] [--name NAME]
  python3 tools/play.py do "up,a,w30"      play tokens (tools/emu.py syntax incl. PARTY, poke:ADDR=HEX,
                                           KEY>KEY), wait until the screen settles, write the screenshot
  python3 tools/play.py shot [PATH]        screenshot only (default work/play/NAME/last.png, 3x)
  python3 tools/play.py status             party (name, HP, status), maze position, PC/bank, frame counter
  python3 tools/play.py peek ADDR [N]      hex dump (WRAM bank of the moment; bank-3 buffers: peek3)
  python3 tools/play.py peek3 ADDR [N]     read from WRAM bank 3 (screen buffers $D000/$D800, attributes +$400)
  python3 tools/play.py poke ADDR HEX      write bytes
  python3 tools/play.py save NAME          state -> work/play/states/NAME.state     load NAME: back to it
  python3 tools/play.py log                the commands played since start (replayable token list)
  python3 tools/play.py stop

Several sessions: --name NAME on every command (default 'main'); each has its own server and work/play/NAME/.
Every `do` appends to work/play/NAME/log.txt with the screenshot path, so a session can be reviewed afterwards.
The ROM is the one given at start (default build/wizardry_empire_en.gbc); rebuilding does not change a running
session (stop + start).
"""
import json, os, socket, socketserver, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
PLAY = os.path.join(ROOT, "work", "play")
STATUS = {0: "OK", 1: "Afraid", 2: "Asleep", 3: "Paralyzed", 4: "Stoned", 5: "Dead", 6: "Ashes"}


def sdir(name):
    return os.path.join(PLAY, name)


def sock_path(name):
    return os.path.join("/tmp", "wizplay_%s_%d.sock" % (name, os.getuid()))


# ---------------------------------------------------------------- server
class Session:
    def __init__(self, rom, state, seq, name):
        import emu
        self.emu, self.name = emu, name
        self.dir = sdir(name)
        os.makedirs(self.dir, exist_ok=True)
        self.g, toks, skip = emu.start(rom, seq or "", state)
        emu.play(self.g, toks[skip:])
        self.history = list(toks)
        self.n = 0

    def settle(self, step=10, limit=600):
        prev = self.g.screenshot()
        for _ in range(limit // step):
            self.g.run_frames(step)
            cur = self.g.screenshot()
            if cur == prev:
                return True
            prev = cur
        return False

    def shot(self, path=None):
        from PIL import Image
        path = path or os.path.join(self.dir, "last.png")
        self.g.screenshot_png(path, scale=1)
        im = Image.open(path).convert("RGB")
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(path)
        return path

    def status(self):
        g = self.g
        out = []
        for i in range(6):
            r = bytes(g.mem_read(0xC880 + 0x80 * i, 0x80))
            name = r[:8].split(b"\x00")[0].decode("latin-1")
            if not name:
                continue
            st = r[0x0C]
            word = STATUS.get(st & 0x3F, "Lost") + (" +Poison" if st & 0x80 else "") + (" +Silenced" if st & 0x40 else "")
            out.append("%d %-8s HP %3d/%-3d %s" % (i + 1, name, r[0x64] | r[0x65] << 8, r[0x62] | r[0x63] << 8, word))
        x, y, f, d = g.mem_read(0xCB80, 4)
        rg = g.regs()
        out.append("maze x=%d y=%d floor=%d dir=%d   pc=%s bank=%02d   frame=%d" % (
            x, y, f, d, rg["pc"], rg["banks"]["rom"], g.mem_read(0xC00A, 1)[0]))
        return "\n".join(out)

    def handle(self, cmd, args):
        g = self.g
        if cmd == "do":
            seq = args[0]
            toks = self.emu.tokens(seq)
            self.emu.play(g, toks)
            settled = self.settle()
            self.history += toks
            self.n += 1
            p = self.shot(os.path.join(self.dir, "%03d.png" % self.n))
            self.shot()
            with open(os.path.join(self.dir, "log.txt"), "a") as f:
                f.write("%03d %s -> %s%s\n" % (self.n, seq, os.path.relpath(p, ROOT), "" if settled else " (not settled)"))
            return "%s%s\n%s" % (os.path.relpath(p, ROOT), "" if settled else "  (screen still changing)", self.status())
        if cmd == "shot":
            return os.path.relpath(self.shot(args[0] if args else None), ROOT)
        if cmd == "status":
            return self.status()
        if cmd in ("peek", "peek3"):
            a, n = int(args[0], 16), int(args[1], 0) if len(args) > 1 else 16
            data = bytes(g.mem_read(a, n, bank=3) if cmd == "peek3" else g.mem_read(a, n))
            return "\n".join("%04x  %s" % (a + i, data[i:i + 16].hex(" ")) for i in range(0, n, 16))
        if cmd == "poke":
            g.mem_write(int(args[0], 16), list(bytes.fromhex(args[1])))
            self.history.append("poke:%s=%s" % (args[0], args[1]))
            return "ok"
        if cmd == "save":
            os.makedirs(os.path.join(PLAY, "states"), exist_ok=True)
            p = os.path.join(PLAY, "states", args[0] + ".state")
            g.snapshot_save(path=p)
            return os.path.relpath(p, ROOT)
        if cmd == "load":
            g.snapshot_load(path=os.path.join(PLAY, "states", args[0] + ".state"))
            self.history.append("# load %s" % args[0])
            return self.status()
        if cmd == "log":
            return ",".join(self.history)
        if cmd == "ping":
            return "pong"
        return "unknown command %r" % cmd


def serve(name, rom, state, seq):
    path = sock_path(name)
    if os.path.exists(path):
        os.remove(path)
    sess = Session(rom, state, seq, name)

    class H(socketserver.StreamRequestHandler):
        def handle(self):
            req = json.loads(self.rfile.readline())
            if req["cmd"] == "stop":
                self.wfile.write(b'"stopped"\n')
                sess.g.close()
                os._exit(0)
            try:
                out = sess.handle(req["cmd"], req["args"])
            except Exception as e:      # keep the session alive on a bad command
                out = "error: %s" % e
            self.wfile.write((json.dumps(out) + "\n").encode())

    with socketserver.UnixStreamServer(path, H) as srv:
        open(os.path.join(sdir(name), "ready"), "w").write(str(os.getpid()))
        srv.serve_forever()


# ---------------------------------------------------------------- client
def call(name, cmd, args, timeout=600):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(sock_path(name))
    s.sendall((json.dumps({"cmd": cmd, "args": args}) + "\n").encode())
    data = b""
    while not data.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        data += chunk
    return json.loads(data)


def main(argv):
    name = "main"
    if "--name" in argv:
        i = argv.index("--name")
        name = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "_serve":
        serve(name, *[None if a == "-" else a for a in args])
        return 0
    if cmd == "start":
        import emu
        opt = {"--rom": emu.EN_ROM, "--state": "-", "--seq": "-"}
        for k in opt:
            if k in args:
                opt[k] = args[args.index(k) + 1]
        try:
            call(name, "stop", [], timeout=5)
        except OSError:
            pass
        d = sdir(name)
        os.makedirs(d, exist_ok=True)
        for f in ("ready", "log.txt"):
            if os.path.exists(os.path.join(d, f)):
                os.remove(os.path.join(d, f))
        log = open(os.path.join(d, "server.log"), "w")
        subprocess.Popen([sys.executable, __file__, "--name", name, "_serve", opt["--rom"], opt["--state"], opt["--seq"]],
                         stdout=log, stderr=log, start_new_session=True)
        for _ in range(1200):
            if os.path.exists(os.path.join(d, "ready")):
                print(call(name, "status", []))
                return 0
            time.sleep(0.25)
        print("server did not start; see", os.path.relpath(os.path.join(d, "server.log"), ROOT))
        return 1
    try:
        out = call(name, cmd, args)
    except OSError:
        print("no session %r running: python3 tools/play.py start [--seq boot,PARTY]" % name)
        return 1
    print(out)
    return 1 if isinstance(out, str) and out.startswith("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
