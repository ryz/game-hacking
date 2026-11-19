# Phantasy Star (SMS) ROM helper, run from the repo root (capture part 2, 2026-11-19).
rom=open('rom/phantasy-star.sms','rb').read()
import re
names='- WOODCANE SHT.SWD IRN.SWD WAND IRN.FANG IRN.AXE TIT.SWD CRC.SWD NEEDLGUN SIL.FANG HEAT.GUN LGT.SABR LASR.GUN LAC.SWD LAC.AXE LTH.ARMR WHT.MANT LGT.SUIT IRN.ARMR THCK.FUR ZIR.ARMR DMD.ARMR LAC.ARMR FRD.MANT LTH.SLD BRNZ.SLD IRN.SLD CRC.SLD GLOVE LASR.SLD MIRR.SLD LAC.SLD LANDROVR HOVRCRFT ICEDIGR COLA BURGER FLUTE FLASH ESCAPER TRANSER MAGCHAT ALSULIN POLYMTRL DUGNKEY SPHERE TORCH PRISM NUTS HAPSBY ROADPASS PASSPORT COMPASS CAKE LETTER LACPOT MAGLAMP AMBREYE GASSLD CRYSTAL MSYSTEM MRCLKEY ZILLION SECRETS'.split()
seg=rom[0xc69f:0xd400]
mons=['-']+[m.group().decode().replace('e',' ').strip() for m in re.finditer(rb'[A-Z][A-Z .e]{3,7}',seg)][:0x4a]
EV=[]
r=0xef5c
while r<0xf900:
    f,sq,fl,fh,t,v1,v2=rom[r:r+7]
    if fh not in (0xc5,0xc6): break
    EV.append((f,sq,(fh<<8)|fl,t,v1,v2)); r+=7
def desc(t,v1,v2):
    if t==0: return 'item '+(names[v1] if v1<len(names) else '%02x'%v1)+('' if v2==0 else ' %02x'%v2)
    if t==1: return 'meseta %d'%(v1|v2<<8)
    if t==2: return 'fight '+(mons[v1] if v1<len(mons) else '%02x'%v1)+(' + '+names[v2] if v2 and v2<len(names) else '')
    return 'type%02x %02x%02x'%(t,v2,v1)
if __name__=='__main__':
    print('end',hex(r),len(EV))
    for f,sq,fl,t,v1,v2 in EV: print('fl %02x sq %02x flag %04X  %s'%(f,sq,fl,desc(t,v1,v2)))
