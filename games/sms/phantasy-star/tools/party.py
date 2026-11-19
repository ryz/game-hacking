# Phantasy Star (SMS) ROM helper, run from the repo root (capture part 2, 2026-11-19).
rom=open('rom/phantasy-star.sms','rb').read()
POW=rom[0x183a:0x183a+0x21]
BASE={0:0xf8af,1:0xf8af+240,2:0xf8af+480,3:0xf8af+720}
def lv(c,l):
    o=BASE[c]+8*(l-1); r=rom[o:o+8]
    return dict(hp=r[0],atk=r[1],dfn=r[2],mp=r[3],exp=r[4]|r[5]<<8,bs=r[6],fs=r[7])
def rec(c,l,w,a,s,hp=None,mp=None,expfrac=0.4):
    L=lv(c,l); N=lv(c,l+1) if l<30 else L
    exp=int(L['exp']+(N['exp']-L['exp'])*expfrac)
    hp=L['hp'] if hp is None else hp; mp=L['mp'] if mp is None else mp
    atk=L['atk']+POW[w]; dfn=L['dfn']+POW[a]+POW[s]
    b=[1,hp,mp,exp&255,exp>>8,l,L['hp'],L['mp'],min(atk,255),min(dfn,255),w,a,s,0,0,0]
    return 'poke:%04X=%s'%(0xC400+16*c, ''.join('%02X'%x for x in b))
if __name__=='__main__':
    for c in range(4):
        print(c,[ (l,lv(c,l)['hp'],lv(c,l)['atk'],lv(c,l)['dfn'],lv(c,l)['mp'],lv(c,l)['exp']) for l in (1,5,10,15,20,25,30)])
