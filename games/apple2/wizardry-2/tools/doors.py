# Door-kick encounter routes: for every door into a room (".") on floors 2-6, warp to the square outside,
# face the room and kick. Usage: python3 games/apple2/wizardry-2/tools/doors.py [SEED] [PER_FLOOR] > plan.txt
# then python3 tools/preview.py apple2/wizardry-2 plan.txt --crop 0,0,560,130
import re,random,sys
txt=open('games/apple2/wizardry-2/design/maps/floors.txt').read()
blocks=re.findall(r'Floor (\d)\n(.*?)Special squares',txt,re.S)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 5)
per=int(sys.argv[2]) if len(sys.argv)>2 else 5
out=[]
for fl,b in blocks:
    lines=[l for l in b.split('\n') if l.startswith(('|','+'))]
    cells={};doors=[]
    rowy=None
    for i,l in enumerate(lines):
        if l.startswith('|'):
            y=int(re.search(r'y=(\d+)',l).group(1)); rowy=y
            for x in range(20):
                cells[(x,y)]=l[1+3*x:3+3*x].strip()
                if x>0 and l[3*x]=='D': doors.append(((x-1,y),(x,y)))
        else:
            if rowy is None or rowy==0: continue
            for x in range(20):
                if l[1+3*x:3+3*x]=='DD': doors.append(((x,rowy),(x,rowy-1)))
    cand=[]
    for a,b in doors:
        for out_,in_ in ((a,b),(b,a)):
            if cells.get(in_)=='.' and cells.get(out_)!='.' :
                dx,dy=in_[0]-out_[0],in_[1]-out_[1]
                face={(0,1):0,(1,0):1,(0,-1):2,(-1,0):3}[(dx,dy)]
                cand.append((out_,face,in_))
    if fl=='1': continue
    for (o,face,i) in random.sample(cand,min(per,len(cand))):
        out.append(f"f{fl}_{i[0]}_{i[1]} | @gmaze,WARP:0{fl}:{o[0]:02X}:{o[1]:02X},poke:730E=0{face}00,l,w200,r,w200,k,w600,w900")
print('\n'.join(out))
