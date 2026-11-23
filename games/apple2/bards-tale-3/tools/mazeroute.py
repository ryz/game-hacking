"""Shortest key route (i/k forward, j/l turn) between squares of a decoded level map (design/maps/XX_name.txt):
python3 games/apple2/bards-tale-3/tools/mazeroute.py MAP.txt E,N E,N "E,N E,N ..." [FACING]
(start, goal, squares to avoid, start facing 0 N 1 E 2 S 3 W). Doors (D) are passed with k. Prints the path and
tokens, or the reachable squares when the goal cannot be reached."""
import sys, collections
txt=sys.argv[1]; start=tuple(map(int,sys.argv[2].split(','))); goal=tuple(map(int,sys.argv[3].split(',')))
avoid=set(tuple(map(int,a.split(','))) for a in sys.argv[4].split()) if len(sys.argv)>4 else set()
L=open(txt).read().split('\n')
rows={}; hw={}
lines=[l for l in L if l[:3].strip().isdigit() or l.startswith('   +')]
cur=None; first=True
for l in lines:
    if l.startswith('   +'):
        b=l[3:]
        if first: top=b; first=False
        else: hw[cur]=b  # wall below row cur
    else:
        cur=int(l[:3]); rows[cur]=l[3:]
W=(len(rows[0])-1)//4
def edge(e,n,d):  # d 0N 1E 2S 3W -> char
    if d==1: return rows[n][4*e+4]
    if d==3: return rows[n][4*e]
    if d==2: return hw[n][4*e+1:4*e+4]
    if d==0: return hw[n+1][4*e+1:4*e+4] if n+1 in hw else '---'
def passable(c): return c.strip()=='' or 'D' in c
mv={0:(0,1),1:(1,0),2:(0,-1),3:(-1,0)}
# state (e,n,facing) ; actions i (forward), j (left), l (right)
f0=int(sys.argv[5]) if len(sys.argv)>5 else 0
st=(start[0],start[1],f0); prev={st:None}; q=collections.deque([st])
while q:
    s=q.popleft(); e,n,f=s
    if (e,n)==goal: break
    nxt=[]
    c=edge(e,n,f)
    if passable(c):
        de,dn=mv[f]; t=(e+de,n+dn)
        if t not in avoid and 0<=t[0]<W and t[1] in rows: nxt.append(((t[0],t[1],f),('k' if 'D' in c else 'i')))
    nxt.append(((e,n,(f+3)%4),'j')); nxt.append(((e,n,(f+1)%4),'l'))
    for t,a in nxt:
        if t not in prev: prev[t]=(s,a); q.append(t)
path=[]
if (s[0],s[1])!=goal: print('UNREACHABLE; reachable:',sorted(set((a,b) for a,b,c in prev)))
while prev[s]: p,a=prev[s]; path.append((a,s)); s=p
path.reverse()
print(' '.join('%s>%d,%d,%d'%(a,*t) for a,t in path))
print('tokens:', ','.join(a[0]+',w60' for a,t in path))
