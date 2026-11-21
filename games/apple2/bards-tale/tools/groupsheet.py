"""Sheet of the special groups that cityscan.py printed: python3 groupsheet.py SCANDIR SCANOUTPUT.txt OUT.png [MAXCOUNT]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
d, txt, out = sys.argv[1:4]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 100
ps, ls = [], []
for l in open(txt):
    p = l.split()
    if len(p) > 2 and len(p[0]) == 8 and int(p[1]) < mx:
        ps.append(os.path.join(d, "g_%s.png" % p[0])); ls.append("%s n%s %s" % (p[0][:4], p[1], " ".join(p[2:4])))
E.sheet(ps, out, cols=5, labels=ls)
