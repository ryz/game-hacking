# Deep Dungeon III - towns, shops and services

## Overview
Each of the three towns (Dirige, Ail and an unnamed north town; map in [maps.md](maps.md) section 5) has the same
six kinds of building: item shop, weapon and armour shop, temple, information seller, inn and magic training hall
**(verified in Dirige; the others inferred from the building numbers)**. Buildings are entered by facing the door
and pressing A; each opens a menu with the shopkeeper's portrait and a sign (INN, SHOP, TEMPLE, MAGIC) **(verified)**.
Ail's building 7 is the way into the tower and the north town's building 8 the way into the castle **(verified)**.

## 1. Inn (INN)
| Choice | What it does | How sure |
|---|---|---|
| やどにとまる (stay) | heals; 4 gold for a level-5 party as for a level-1 party, asked with yes/no | verified (shot `inn_stay`; 643 -> 639 gold) |
| ぼうけんのきろく (adventure record) | saves the party to its slot: "recorded" | verified (shot `inn_save`, saves reload) |
| パーティーのくみかえ (reorder) | change the marching order | source: menu text |
| パーティーからはずす (remove) | dismiss a companion; the swordsman alone cannot be left ("this party is only you") | ROM text |
| そとにでる (go out) | back to the street | verified |

## 2. Weapon and armour shop (Dirige)
| Weapons | Price | Armour | Price |
|---|---|---|---|
| たんけん dagger | 5 | きぬのころも silk robe | 15 |
| こんぼう club | 8 | うでのたて arm shield | 20 |
| ておの hand axe | 10 | レザー leather | 25 |
| ダート dart | 10 | | |
| スリング sling | 20 | | |
**(verified: shots `shop_weapons_list`, `shop_armour_list`)**. Buying asks who will carry the item; the shop does
not equip it **(verified)**.

## 3. Item shop (SHOP, Dirige)
Buy or sell ("unwanted things are bought back"). Wares: くさのつゆ grass dew 20, しろきのこ white mushroom 40,
ランプ lamp 50, なわばしご rope ladder 250 **(verified: shot `item_shop_list`)**. The rope ladder opens the well on
cave floor 1 ([maps.md](maps.md) section 7) **(inferred from the well's message)**. The lamp probably lights the dark
cave **(inferred: the cave shows only scraps of wall, shot `area2_cave`)**.

## 4. Temple (TEMPLE)
いのりをささげる (pray), ししゃをよみがえらせる (revive the dead), じゅもんをおぼえる (learn spells), leave **(verified:
shot `temple_menu`)**. "Priests and hunters can learn spells here"; a level-1 character is sent away ("come back when
your level is higher") **(verified)**. At level 5 the lesson offered was キュアー (Cure) for 100 gold, learned at once
**(verified: shots `temple_spells`, `temple_learned`)**.

## 5. Magic training hall (MAGIC)
"Those who aim to be magicians learn spells here" - the magician's counterpart of the temple **(verified: shot
`magic_guild`)**. A new magician already knows スピアー (Spear) **(verified: shot `spell_menu`)**.

## 6. Information seller
Three tips for 1, 5 and 10 gold **(verified: shot `info_broker`)**. Dirige's tips (ROM text, first one verified):
other adventurers are in the dungeons and worth talking to; the seal was made of two stone tablets, one went
through "Hank's" wall; the castle cannot be entered from the front - find a back way; north of this town the stairs
lead down to an underground called Hank's (ハンクのちか); the gods left a great sword in the cave, stuck in a rock,
which only a swordsman recognised as a hero can draw; holy water cures the mad; the monster with the key is on
Hank's floor 2 beyond a door in the middle of a long corridor; from the cave stairs in this town walk 16 steps east
and push the south wall: a short cut to Ail **(ROM text)**.

## Open questions
- Prices and wares of the shops in Ail and the north town (not visited).
- What praying does; prices of revival; the magic hall's spell list and prices.
