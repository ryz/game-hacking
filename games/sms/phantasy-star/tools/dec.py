# Phantasy Star (SMS) ROM helper, run from the repo root (capture part 2, 2026-11-19).
rom=open('rom/phantasy-star.sms','rb').read()
st=rom.index(b'ALIS\x65MYAU')
words=[];i=st;cur=b''
while len(words)<128:
    b=rom[i];i+=1
    if b==0x65: words.append(cur.decode('latin1')); cur=b''
    elif b==0xff: break
    else: cur+=bytes([b])
D={0x80+k:w for k,w in enumerate(words)}
def dec(a,n=4000):
    s='';i=a
    while i<a+n:
        b=rom[i];i+=1
        if b in D: s+=D[b]+('' if D[b].endswith(' ') else '')
        elif b==0x60: s+=' / '
        elif b==0x61: s+=' // '
        elif b==0x62: s+=' [Q] '
        elif b==0x63: s+=' [E] '
        elif b==0x65: s+=' [END]\n'
        elif b==0x40: s+="'"
        elif 0x20<=b<0x5b: s+=chr(b)
        else: s+='{%02x}'%b
    return s
if __name__=='__main__':
    import re
    out=[]
    # scan text regions: find runs with high ratio of letters/dict codes
    i=0
    while i<len(rom):
        j=i;good=0
        while j<len(rom) and (0x20<=rom[j]<0x5b or rom[j] in D or rom[j] in (0x60,0x61,0x62,0x63,0x65,0x5b,0x5c,0x5d,0x5e,0x5f)):
            j+=1
        if j-i>40:
            out.append('%05x: '%i+dec(i,j-i))
        i=j+1
    open('alltext.txt','w').write('\n'.join(out))
    print(len(words), len(out))
