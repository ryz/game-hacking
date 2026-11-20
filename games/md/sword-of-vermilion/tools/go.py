import sys
# Overworld/cave walker: BFS over the 48x32 map window at FF9000 (0 = open), fights battles with SW and frozen HP,
# prints the route (ROUTE ...) to paste into play.py/checkpoints. Usage: go.py @CHECKPOINT OX OY TX TY (window coords; OX,OY = window offset of the current map, usually 16 16).
sys.path.insert(0, "tools")
import emu as E
from collections import deque
# go.py START OX OY TX TY [TX TY ...] -- OX,OY = window offset of the current map; targets in window coords
g = E.Game("sword-of-vermilion")
start=sys.argv[1]; ox,oy=int(sys.argv[2]),int(sys.argv[3]); tg=[int(v) for v in sys.argv[4:]]
emu, rest, _ = E.start(g, start); E.play(emu, g, E.expand(g, rest))
W=48; ram=emu.peek(0xFF9000,0x600)
open_=lambda x,y: 0<=x<W and 0<=y<32 and ram[y*W+x]==0
D={0:(0,-1),2:(-1,0),4:(0,1),6:(1,0)}
w=lambda a:int.from_bytes(emu.peek(a,2),"big")
route=[]
def play(toks):
    battles=0
    for t in toks:
        E.play(emu,g,E.expand(g,[t])); route.append(t)
        n=0
        while emu.peek(0xFFC550,1)[0]==0xFF and n<60:
            for t2 in ["freeze:FFC62C=00A2","SW","unfreeze"]: E.play(emu,g,E.expand(g,[t2])); route.append(t2)
            n+=1
        if n:
            battles+=1
            for t2 in ["w120","b","w40","b","w40"]: E.play(emu,g,E.expand(g,[t2])); route.append(t2)
    return battles
def bfs(s,t):
    prev={s:None}; q=deque([s])
    while q:
        p=q.popleft()
        if p==t: break
        for d,(dx,dy) in D.items():
            n=(p[0]+dx,p[1]+dy)
            if n not in prev and (open_(*n) or n==t): prev[n]=(p,d); q.append(n)
    if t not in prev: return None
    out=[]; p=t
    while prev[p]: p,d=prev[p]; out.append(d)
    return out[::-1]
x,y=w(0xFFC662)+ox,w(0xFFC664)+oy
for i in range(0,len(tg),2):
    t=(tg[i],tg[i+1]); path=bfs((x,y),t)
    if path is None: print("no path to",t); break
    for d in path:
        f=emu.peek(0xFFC60D,1)[0]
        while f!=d:
            play(["TL" if (f+2)%8==d else "TR"]); f=emu.peek(0xFFC60D,1)[0]
        want=((w(0xFFC662)+D[d][0])%16,(w(0xFFC664)+D[d][1])%16)
        for k in range(4):
            play(["FWD"])
            if (w(0xFFC662),w(0xFFC664))==want: break
            if emu.peek(0xFFC60D,1)[0]!=d: play(["TL" if (emu.peek(0xFFC60D,1)[0]+2)%8==d else "TR"])
        else:
            print("stuck at",(w(0xFFC662),w(0xFFC664)),"dir",d); break
        x,y=x+D[d][0],y+D[d][1]
    print("at target",t,"local",(w(0xFFC662),w(0xFFC664)))
print("ROUTE",start+","+",".join(route))
emu.screen_png("work/go.png")
open("work/go_ram.bin","wb").write(emu.peek(0xFF0000,0x10000))
