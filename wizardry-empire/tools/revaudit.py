"""Audit of the v1.0 -> Rev 1 port: does every address in script/*.json and every byte range the build patches in the
original banks map to Rev 1 (tools/revmap.py)? Run after a build (needs build/wizardry_empire_en.gbc).
"""
import sys, json, re, os, glob
sys.path.insert(0,'tools'); import revmap
A=open('rom/wizardry_empire_j.gbc','rb').read(); B=open('rom/wizardry_empire_j_rev1.gbc','rb').read()
E=open('build/wizardry_empire_en.gbc','rb').read()
def off(b,a): return a if b==0 else b*0x4000+a-0x4000
rep={}
# 1. scripts
for f in sorted(glob.glob('script/*.json')):
    d=json.load(open(f,encoding='utf-8'))
    if not isinstance(d,list): continue
    ok=chg=moved=0; bad=[]
    for e in d:
        b=e.get('bank'); a=e.get('addr') or e.get('site')
        if b is None or a is None: continue
        a=int(a,16) if isinstance(a,str) else a
        n=2
        if 'w' in e: n=2+e['w']*e['h']
        m=revmap.map_addr(b,a,n)
        if m is None: chg+=1; bad.append('%02X:%04X'%(b,a))
        elif m==a: ok+=1
        else: moved+=1
    rep[f]=(ok,moved,chg,bad[:8])
for f,(o,m,c,b) in rep.items(): print('%-26s same %4d moved %4d changed %3d %s'%(os.path.basename(f),o,m,c,b))
# 2. patched ranges in original banks
diff=[i for i in range(0x100000) if A[i]!=E[i]]
ranges=[]
for i in diff:
    if ranges and i<=ranges[-1][1]+2: ranges[-1][1]=i
    else: ranges.append([i,i])
ok=moved=chg=0; badr=[]
for s,e in ranges:
    b=s//0x4000; a=s if b==0 else s%0x4000+0x4000; n=e-s+1
    m=revmap.map_addr(b,a,n)
    if m is None: chg+=1; badr.append('%02X:%04X+%d'%(b,a,n))
    elif m==a: ok+=1
    else: moved+=1
print('patched ranges: %d same %d moved %d changed %d'%(len(ranges),ok,moved,chg))
print(' changed:', badr[:60])
