"""Quake (DOS shareware): print map entities from ID1/PAK0.PAK in rom/quake.zip.

  python3 games/dos/quake/tools/ents.py MAP REGEX     e.g. e1m1 "secret|weapon|monster"

One dict per entity whose classname matches REGEX; brush entities get "box" (x y z ranges from the model lump)
instead of "model". spawnflags 256/512/1024 = not on Easy/Normal/Hard, 2048 = not in deathmatch.
"""
import zipfile,struct,sys,re
z=zipfile.ZipFile(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','..','..','..','rom','quake.zip'))
n=[x for x in z.namelist() if x.upper().endswith('PAK0.PAK')][0]
pak=z.read(n)
_,off,ln=struct.unpack('<4sii',pak[:12])
files={}
for i in range(ln//64):
    name,o,s=struct.unpack('<56sii',pak[off+i*64:off+i*64+64]); files[name.split(b'\0')[0].decode()]=(o,s)
o,s=files['maps/%s.bsp'%sys.argv[1]]; b=pak[o:o+s]
eo,el=struct.unpack('<ii',b[4:12]); ents=b[eo:eo+el].decode('latin1')
mo,ml=struct.unpack('<ii',b[4+14*8:4+14*8+8]); models=[struct.unpack('<9f',b[mo+i*64:mo+i*64+36]) for i in range(ml//64)]
for e in re.findall(r'\{([^}]*)\}',ents):
    d=dict(re.findall(r'"([^"]*)" "([^"]*)"',e))
    if 'model' in d and d['model'].startswith('*'):
        m=models[int(d['model'][1:])]; d['box']='%d..%d %d..%d %d..%d'%(m[0],m[3],m[1],m[4],m[2],m[5]); del d['model']
    if re.search(sys.argv[2],d.get('classname','')): print(d)
