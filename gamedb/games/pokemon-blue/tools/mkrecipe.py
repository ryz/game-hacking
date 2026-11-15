"""Pokemon Blue RAM recipe generator (macros LATE / MID in game.json).

Builds emu.py poke tokens for a realistic party / bag / money / badges / Pokedex from a preset, using
pret/pokered constants (downloaded to PRET dir) for ids and the local ROM for base stats.

  python3 -I mkrecipe.py PRET_DIR ROM PRESET > tokens.txt
PRET_DIR: a checkout/download of github.com/pret/pokered (constants/, data/); ROM: rom/pokemon-blue.gb.
2026-11-15: growth groups fixed (3 = medium slow, 5 = slow, per pret data/growth_rates.asm) and the in-level EXP
fraction kept below 100% (was 109%/132% for slots 5/6: "741376 to L53").
"""
import math, re, sys

PRET, ROM, PRESET = sys.argv[1], sys.argv[2], sys.argv[3]
rom = open(ROM, "rb").read()


def consts(path):
    out, v = {}, 0
    for line in open(path, encoding="utf-8"):
        line = line.split(";")[0].strip()
        m = re.match(r"const_def\s*(\S+)?", line)
        if m:
            v = int(m.group(1).replace("$", "0x"), 0) if m.group(1) else 0
            continue
        m = re.match(r"const_next\s+(.+)", line)
        if m:
            v = eval(m.group(1).replace("$", "0x"))
            continue
        m = re.match(r"const_skip\s*(\d+)?", line)
        if m:
            v += int(m.group(1) or 1)
            continue
        m = re.match(r"const\s+(\w+)", line)
        if m:
            out[m.group(1)] = v
            v += 1
    return out


MON = consts(PRET + "/constants/pokemon_constants.asm")      # internal species id
DEX = consts(PRET + "/constants/pokedex_constants.asm")      # DEX_NAME -> dex no
MOVE = consts(PRET + "/constants/move_constants.asm")
ITEM = consts(PRET + "/constants/item_constants.asm")
EVENT = consts(PRET + "/constants/event_constants.asm")
for i in range(5):
    ITEM["HM%02d" % (i + 1)] = 0xC4 + i
for i in range(50):
    ITEM["TM%02d" % (i + 1)] = 0xC9 + i
PP = {}
for line in open(PRET + "/data/moves/moves.asm", encoding="utf-8"):
    m = re.match(r"\s*move\s+(\w+),.*,\s*(\d+)\s*$", line.split(";")[0])
    if m:
        PP[m.group(1)] = int(m.group(2))

BASE = 0x383DE  # BaseStats (bank $0E), 28 bytes per dex no (Mew is elsewhere)


def base(name):
    d = DEX["DEX_" + name]
    o = BASE + (d - 1) * 28
    b = rom[o:o + 28]
    assert b[0] == d, (name, b[0], d)
    return dict(hp=b[1], atk=b[2], df=b[3], spd=b[4], spc=b[5], t1=b[6], t2=b[7], catch=b[8], growth=b[19])


def exp_at(growth, n):
    return {0: n ** 3, 1: 3 * n ** 3 // 4 + 10 * n * n - 30, 2: 3 * n ** 3 // 4 + 20 * n * n - 70,
            3: 6 * n ** 3 // 5 - 15 * n * n + 100 * n - 140, 4: 4 * n ** 3 // 5, 5: 5 * n ** 3 // 4}[growth]


def stat(b, dv, sexp, lvl, hp=False):
    s = ((b + dv) * 2 + math.ceil(math.sqrt(sexp)) // 4) * lvl // 100
    return s + lvl + 10 if hp else s + 5


CHARS = {" ": 0x7F, ".": 0xE8, "-": 0xE3}


def text(s, n=11):
    out = []
    for c in s:
        if "A" <= c <= "Z":
            out.append(0x80 + ord(c) - 65)
        elif "a" <= c <= "z":
            out.append(0xA0 + ord(c) - 97)
        elif "0" <= c <= "9":
            out.append(0xF6 + ord(c) - 48)
        else:
            out.append(CHARS[c])
    out.append(0x50)
    return out + [0x50] * (n - len(out))


def bcd(v, n):
    s = "%0*d" % (2 * n, v)
    return [int(s[i:i + 2], 16) for i in range(0, 2 * n, 2)]


# preset: party (species, level, moves, DVs atk/def/spd/spc, stat exp per stat, hp missing), bag, money, badges,
# dex owned/seen counts (the party is always owned; the rest are filled in dex order, skipping legendaries)
PRESETS = {
    "late": dict(
        party=[
            ("BLASTOISE", 52, ["SURF", "ICE_BEAM", "BITE", "STRENGTH"], (12, 9, 14, 11), 31800, 0),
            ("PIDGEOT", 47, ["FLY", "WING_ATTACK", "QUICK_ATTACK", "SAND_ATTACK"], (10, 13, 15, 6), 27400, 0),
            ("RAICHU", 45, ["THUNDERBOLT", "THUNDER_WAVE", "FLASH", "QUICK_ATTACK"], (14, 7, 12, 13), 24100, 0),
            ("SNORLAX", 46, ["BODY_SLAM", "REST", "AMNESIA", "HYPER_BEAM"], (9, 11, 5, 12), 19800, 23),
            ("VICTREEBEL", 44, ["RAZOR_LEAF", "CUT", "SLEEP_POWDER", "ACID"], (11, 12, 9, 15), 22700, 0),
            ("KADABRA", 42, ["PSYCHIC_M", "RECOVER", "PSYBEAM", "REFLECT"], (13, 6, 11, 14), 17300, 0),
        ],
        bag=[("BICYCLE", 1), ("TOWN_MAP", 1), ("HYPER_POTION", 7), ("SUPER_POTION", 4), ("FULL_HEAL", 5),
             ("REVIVE", 3), ("ULTRA_BALL", 11), ("GREAT_BALL", 6), ("SUPER_REPEL", 4), ("ESCAPE_ROPE", 2),
             ("SUPER_ROD", 1), ("POKE_FLUTE", 1), ("SILPH_SCOPE", 1), ("ITEMFINDER", 1), ("RARE_CANDY", 2),
             ("HM01", 1), ("HM02", 1), ("HM03", 1), ("HM04", 1)],
        money=48215, badges=0xFF, owned=71, seen=104),
    "mid": dict(
        party=[
            ("WARTORTLE", 27, ["BITE", "WATER_GUN", "TAIL_WHIP", "BUBBLE"], (12, 9, 14, 11), 6100, 0),
            ("PIDGEOTTO", 24, ["GUST", "QUICK_ATTACK", "SAND_ATTACK", "TACKLE"], (10, 13, 15, 6), 4900, 0),
            ("PIKACHU", 22, ["THUNDERSHOCK", "THUNDER_WAVE", "QUICK_ATTACK", "GROWL"], (14, 7, 12, 13), 3300, 4),
            ("NIDORINO", 23, ["DOUBLE_KICK", "HORN_ATTACK", "POISON_STING", "LEER"], (9, 11, 5, 12), 2800, 0),
        ],
        bag=[("TOWN_MAP", 1), ("POTION", 6), ("ANTIDOTE", 3), ("PARLYZ_HEAL", 1), ("POKE_BALL", 9),
             ("ESCAPE_ROPE", 1), ("HM01", 1), ("TM28", 1)],
        money=3172, badges=0x07, owned=19, seen=31),
}
LEGEND = {"ARTICUNO", "ZAPDOS", "MOLTRES", "MEWTWO", "MEW"}

p = PRESETS[PRESET]
toks = []


def poke(addr, data):
    toks.append("poke:%04X=%s" % (addr, "".join("%02X" % x for x in data)))


ot_id = None  # copied from wPlayerID by the route (D359): use a fixed id written to both places
OTID = [0x4E, 0x31]  # trainer ID 20017
poke(0xD359, OTID)
party = p["party"]
poke(0xD163, [len(party)] + [MON[s] for s, *_ in party] + [0xFF])
for i, (sp, lvl, moves, dvs, sexp, hurt) in enumerate(party):
    b = base(sp)
    a, d, s, c = dvs
    hpdv = (a & 1) << 3 | (d & 1) << 2 | (s & 1) << 1 | (c & 1)
    # vary the stat exp a little between stats so the numbers do not look generated
    se = [sexp, int(sexp * 0.91), int(sexp * 1.07), int(sexp * 0.84), int(sexp * 0.97)]
    mhp = stat(b["hp"], hpdv, se[0], lvl, True)
    st = [stat(b["atk"], a, se[1], lvl), stat(b["df"], d, se[2], lvl), stat(b["spd"], s, se[3], lvl),
          stat(b["spc"], c, se[4], lvl)]
    e0, e1 = exp_at(b["growth"], lvl), exp_at(b["growth"], lvl + 1)
    exp = e0 + (e1 - e0) * (17 + 13 * i) // 100     # 17%..82% of the way to the next level
    mv = [MOVE[m] for m in moves] + [0] * (4 - len(moves))
    pp = [PP[m] for m in moves] + [0] * (4 - len(moves))
    rec = [MON[sp]] + list((mhp - hurt).to_bytes(2, "big")) + [lvl, 0, b["t1"], b["t2"], b["catch"]] + mv + OTID
    rec += list(exp.to_bytes(3, "big"))
    for v in se:
        rec += list(min(v, 65535).to_bytes(2, "big"))
    rec += [a << 4 | d, s << 4 | c] + pp + [lvl] + list(mhp.to_bytes(2, "big"))
    for v in st:
        rec += list(v.to_bytes(2, "big"))
    assert len(rec) == 44
    poke(0xD16B + 44 * i, rec)
    poke(0xD273 + 11 * i, text("ryz"))
    poke(0xD2B5 + 11 * i, text(sp))
    print("# %s L%d HP %d atk/def/spd/spc %s exp %d" % (sp, lvl, mhp, st, exp), file=sys.stderr)
# Pokedex: party species + others in dex order
own = {DEX["DEX_" + s] for s, *_ in party}
pre_evos = {"BLASTOISE": ["SQUIRTLE", "WARTORTLE"], "PIDGEOT": ["PIDGEY", "PIDGEOTTO"], "RAICHU": ["PIKACHU"],
            "VICTREEBEL": ["BELLSPROUT", "WEEPINBELL"], "KADABRA": ["ABRA"], "WARTORTLE": ["SQUIRTLE"],
            "PIDGEOTTO": ["PIDGEY"], "NIDORINO": ["NIDORAN_M"]}
for s, *_ in party:
    own |= {DEX["DEX_" + x] for x in pre_evos.get(s, [])}
names = sorted(DEX, key=DEX.get)
skip = {DEX["DEX_" + x] for x in LEGEND}
# not owned in a Blue game with a Squirtle start: other starters, Red-only species (they may be seen)
NOT_OWNED = {"BULBASAUR", "IVYSAUR", "VENUSAUR", "CHARMANDER", "CHARMELEON", "CHARIZARD", "EKANS", "ARBOK",
             "ODDISH", "GLOOM", "VILEPLUME", "MANKEY", "PRIMEAPE", "GROWLITHE", "ARCANINE", "SCYTHER", "ELECTABUZZ"}
pool = [DEX[n] for n in names if DEX[n] not in skip and DEX[n] <= 151]
pool_own = [d for d in pool if not any(DEX["DEX_" + x] == d for x in NOT_OWNED)]
k = 0
while len(own) < p["owned"]:
    own.add(pool_own[(k * 7) % len(pool_own)]); k += 1
seen = set(own)
k = 0
while len(seen) < p["seen"]:
    seen.add(pool[(k * 5 + 3) % len(pool)]); k += 1


def flags(nums):
    a = [0] * 19
    for n in nums:
        a[(n - 1) // 8] |= 1 << ((n - 1) % 8)
    return a


poke(0xD2F7, flags(own))
poke(0xD30A, flags(seen))
bag = p["bag"]
poke(0xD31D, [len(bag)] + sum([[ITEM[n], q] for n, q in bag], []) + [0xFF])
poke(0xD347, bcd(p["money"], 3))
poke(0xD356, [p["badges"]])
# event flags: got starter, Pokedex, Oak's parcel delivered (start menu shows POKEDEX)
ev = {}
for e in ["EVENT_GOT_STARTER", "EVENT_GOT_POKEDEX", "EVENT_OAK_GOT_PARCEL", "EVENT_GOT_OAKS_PARCEL",
          "EVENT_BATTLED_RIVAL_IN_OAKS_LAB", "EVENT_GOT_TOWN_MAP"]:
    n = EVENT[e]
    ev.setdefault(0xD747 + n // 8, 0)
    ev[0xD747 + n // 8] |= 1 << (n % 8)
    print("# %s = %d -> %04X bit %d" % (e, n, 0xD747 + n // 8, n % 8), file=sys.stderr)
for addr, v in sorted(ev.items()):
    toks.append("poke:%04X=%02X" % (addr, v))  # fresh game: these bytes are 0
print(",".join(toks))
