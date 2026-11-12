# Wizardry Empire: all 224 items (generated)

Generated from the original Rev 1 ROM (`rom/wizardry_empire_j.gbc`), bank 40 `$4000` (40-byte records), by
`tools/designtables/items.py`. Field meanings, formulas and how each was established: `docs/tech/items.md`.
English names from `script/items.json`; use/special texts are the museum descriptions (`41:6378` / `41:63B6`, English
from `script/rects.json`).

Columns: **Damage** = min-max per hit (dice form `NdS+B`, rolled per swing); **Swings+** = extra swings per round;
**Hit+** = subtracted from the miss threshold (see items.md, values 47-50 = always max hit chance); **AC** = added to
the wearer's AC (negative = better); **Range** S/M/L/- (bits 2-3 of byte 31); **Throw** = item can be thrown, number =
% chance to keep it after the throw; **Classes** Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Ave Mus Kun Sum; **Align**
G/N/E who may equip it without it sticking; **Sell** = ceil(price/2) (also the Identify and Uncurse fee);
**Use** = effect when used, [where, spell level] and % chance the item is used up; class-change items show the % chance
the item vanishes instead of changing; **HP/step** = HP regained (or lost) per step while equipped; **Lv** = item
level (identification difficulty); **Shop** = stock at the start of a new game (unlimited = never runs out).

| # | English | Japanese | Slot | Unid. name | Damage | Swings+ | Hit+ | AC | Range | Throw (keep %) | Classes | Align | Curse | Price | Sell | Use (break %) | Special | HP/step | Lv | Shop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Hand Axe | ハンドアックス | 1H weapon | Axe | 2-7 (1d6+1) |  |  |  | S | 70 | Fig Sam Lor Nin Val Mus Kun | any |  | 60 | 30 |  |  |  | 1 | unlimited |
| 1 | Battle Axe | バトルアックス | 2H weapon | Axe | 4-12 (2d5+2) |  | 50 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 180 | 90 |  |  |  | 2 | unlimited |
| 2 | Great Axe | グレートアックス | 2H weapon | Axe | 6-14 (2d5+4) |  | 48 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 500 | 250 |  |  |  | 4 | 1 |
| 3 | Blood Axe | ブラッドアックス | 2H weapon | Axe | 9-18 (1d10+8) |  | 2 |  | S |  | Fig Sam Lor Nin Val Ave Kun | any | cursed | 25000 | 12500 |  |  | -3 | 10 |  |
| 4 | Axe of Death | アックス オブ デス | 2H weapon | Axe | 23-35 (2d7+21) |  | 4 |  | S |  | Fig Sam Lor Nin Val Ave Kun | any | cursed | 190000 | 95000 |  |  | -4 | 14 |  |
| 5 | Crescent Axe | アックス オブ クレッセント | 2H weapon | Axe | 24-42 (2d10+22) |  | 4 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 600000 | 300000 |  |  |  | 15 |  |
| 6 | Arrow | ノーマルアロー | Arrows | Arrow |  |  |  |  | - |  | Fig Thi Sam Lor Nin Arc Val Kun Sum | any |  | 10 | 5 |  |  |  | 1 | unlimited |
| 7 | Quarrel | クォーレル | Quarrels | Arrow |  |  |  |  | - |  | Fig Thi Sam Lor Nin Arc Val Kun | any |  | 30 | 15 |  |  |  | 1 | unlimited |
| 8 | Silver Quarrel | シルバークォーレル | Quarrels | Arrow |  |  |  |  | - |  | Fig Thi Sam Lor Nin Arc Val Kun | any |  | 15000 | 7500 |  | vs Demons: damage up |  | 9 |  |
| 9 | Exorcist Arrow | はまや | Arrows | Arrow |  |  |  |  | - |  | Fig Thi Sam Lor Nin Arc Val Kun Sum | any |  | 10000 | 5000 |  | vs Undead: damage up |  | 10 |  |
| 10 | Sling Stone | スリングストーン | Stones | Stone |  |  |  |  | - |  | Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 10 | 5 |  |  |  | 1 | unlimited |
| 11 | Chain Sickle | くさりがま | 2H weapon | Scythe | 1-6 (1d6) | 1 | 50 |  | M |  | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 70 | 35 |  |  |  | 1 | unlimited |
| 12 | Reaper's Scythe | しにがみのかま | 2H weapon | Scythe | 17-26 (1d10+16) |  | 3 |  | M |  | Fig Sam Lor Nin Val Ave Kun | any | cursed | 65000 | 32500 |  |  | -5 | 13 |  |
| 13 | Claws | かぎづめ | 1H weapon | Odd object | 1-2 (1d2) | 1 |  |  | S |  | Nin Kun | any |  | 70 | 35 |  |  |  | 1 | 2 |
| 14 | Shuriken | しゅりけん | 1H weapon | Odd object | 7-35 (4d8+3) |  | 3 |  | S | 95 | Nin Kun | any |  | 350000 | 175000 |  | Critical +5% |  | 13 |  |
| 15 | Fiend Shuriken | まじんのしゅりけん | 1H weapon | Odd object | 10-45 (5d8+5) |  | 5 |  | S | 95 | Nin Ave Kun | any | cursed | 815000 | 407500 |  |  | -5 | 15 |  |
| 16 | Quarterstaff | クォータースタッフ | 2H weapon | Staff | 1-4 (1d4) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 20 | 10 |  |  |  | 1 | unlimited |
| 17 | Staff of Pain | いたみのつえ | 2H weapon | Staff | 4-9 (1d6+3) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Ave Kun Sum | any | cursed | 200 | 100 |  |  |  | 2 |  |
| 18 | Staff of Healing | いやしのつえ | 2H weapon | Staff | 2-5 (1d4+1) |  | 1 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 1000 | 500 | Healing [battle+camp, Lv9] (breaks 25%) |  |  | 6 | 1 |
| 19 | Staff of Grace | しゅくふくのつえ | 2H weapon | Staff | 2-5 (1d4+1) |  | 1 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 1000 | 500 | Yell [battle, Lv10] (breaks 25%) |  |  | 6 |  |
| 20 | Rod of Flame | ロッド オブ フレイム | 1H weapon | Staff | 1-3 (1d3) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 10000 | 5000 | Fireball [battle, Lv6] (breaks 10%) |  |  | 9 |  |
| 21 | Rod of Frost | ロッド オブ フロスト | 1H weapon | Staff | 1-3 (1d3) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 10000 | 5000 | Ice Storm [battle, Lv6] (breaks 10%) |  |  | 9 |  |
| 22 | Rod of Lightning | ロッド オブ ライトニング | 1H weapon | Staff | 1-3 (1d3) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Kun Sum | any |  | 10000 | 5000 | Lightning Bolt [battle, Lv6] (breaks 10%) |  |  | 9 |  |
| 23 | Sinner's Staff | ざいにんのつえ | 2H weapon | Staff | 9-19 (2d6+7) |  | 50 |  | S |  | Fig Mag Pri Bis Sam Lor Nin Val Ave Kun Sum | any | cursed | 20000 | 10000 |  |  | -3 | 10 |  |
| 24 | Short Sword | ショートソード | 1H weapon | Sword | 1-4 (1d4) |  |  |  | S |  | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 10 | 5 |  |  |  | 1 | unlimited |
| 25 | Sword | ソード | 1H weapon | Sword | 1-5 (1d5) |  |  |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 20 | 10 |  |  |  | 1 | unlimited |
| 26 | Saber | サーベル | 1H weapon | Sword | 1-4 (1d4) |  |  |  | S |  | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 100 | 50 |  |  |  | 2 | unlimited |
| 27 | Rapier | レイピア | 1H weapon | Sword | 1-4 (1d4) | 1 |  |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 130 | 65 |  |  |  | 2 | unlimited |
| 28 | Gladius | グラディウス | 1H weapon | Sword | 2-5 (1d4+1) |  |  |  | S | 70 | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 80 | 40 |  |  |  | 1 | 1 |
| 29 | Katar | カタール | 1H weapon | Sword | 1-3 (1d3) | 1 |  |  | S |  | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 150 | 75 |  |  |  | 2 |  |
| 30 | Falchion | ファルシオン | 1H weapon | Sword | 1-7 (1d7) |  |  |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 90 | 45 |  |  |  | 1 | 1 |
| 31 | Ninja Blade | ニンジャとう | 1H weapon | Sword | 1-5 (1d5) |  |  |  | S |  | Sam Nin Mus Kun | any |  | 100 | 50 |  |  |  | 2 | unlimited |
| 32 | Long Sword | ロングソード | 1H weapon | Sword | 1-8 (1d8) |  |  |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 100 | 50 |  |  |  | 2 | unlimited |
| 33 | Katana | カタナ | 1H weapon | Sword | 1-7 (1d7) |  | 1 |  | S |  | Sam Mus | any |  | 600 | 300 |  |  |  | 4 | 1 |
| 34 | Shamshir | シャムシール | 1H weapon | Sword | 2-11 (1d10+1) |  | 50 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 250 | 125 |  |  |  | 2 | unlimited |
| 35 | Rune Sword | ルーンソード | 1H weapon | Sword | 3-10 (1d8+2) |  | 1 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 1500 | 750 |  |  |  | 5 |  |
| 36 | Bushido Blade | ブシドウブレード | 1H weapon | Sword | 4-16 (2d7+2) |  | 1 |  | S |  | Sam Nin Mus Kun | any |  | 5000 | 2500 |  |  |  | 6 |  |
| 37 | Chain Sword | チェーンソード | 1H weapon | Sword | 3-10 (1d8+2) |  | 2 |  | M |  | Fig Sam Lor Nin Val Mus Kun | any |  | 9500 | 4750 |  |  |  | 7 |  |
| 38 | Swift Sword | しんそくのけん | 1H weapon | Sword | 1-8 (1d8) | 7 | 2 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 15000 | 7500 |  |  |  | 8 |  |
| 39 | Dragonslayer | ドラゴンスレイヤー | 1H weapon | Sword | 1-11 (1d11) |  | 1 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 15000 | 7500 |  | vs Dragons: damage up |  | 8 |  |
| 40 | Drying Pole | ものほしざお | 1H weapon | Sword | 1-10 (1d10) |  | 1 |  | M |  | Sam Mus | any |  | 8000 | 4000 |  |  |  | 7 |  |
| 41 | Cursed Sword | のろわれたけん | 1H weapon | Sword | 2-10 (2d5) |  | 1 |  | S |  | Fig Sam Lor Nin Val Ave Mus Kun | any | cursed | 20000 | 10000 |  |  |  | 8 |  |
| 42 | Black Blade | ブラックブレード | 1H weapon | Sword | 4-15 (1d12+3) |  | 2 |  | S |  | Fig Sam Lor Nin Val Ave Mus Kun | any | cursed | 50000 | 25000 |  |  | -4 | 10 |  |
| 43 | Estoc de Olivia | エストック・デ・オリビア | 2H weapon | Sword | 5-20 (3d6+2) |  | 2 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 55000 | 27500 |  |  |  | 11 |  |
| 44 | Holy Cross Sword | クロスソード・ホーリー | 1H weapon | Sword | 2-20 (2d10) |  | 2 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 90000 | 45000 |  | vs Undead: damage up |  | 13 |  |
| 45 | Death Sword | デス・ソード | 1H weapon | Sword | 6-20 (2d8+4) |  | 3 |  | S |  | Fig Sam Lor Nin Val Ave Mus Kun | any | cursed | 125000 | 62500 |  |  | -5 | 13 |  |
| 46 | Blade Cusinart | カシナートのけん | 1H weapon | Sword | 10-22 (2d7+8) | 3 | 3 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 450000 | 225000 |  |  |  | 15 |  |
| 47 | Thundergod Blade | らいじんけん | 1H weapon | Sword | 3-25 (2d12+1) |  | 2 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 290000 | 145000 | Lightning Bolt [battle, Lv6] (breaks 25%) |  |  | 13 |  |
| 48 | Shadow Blade | シャドーブレード | 1H weapon | Sword | 4-26 (2d12+2) | 1 | 2 | -1 | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 330000 | 165000 |  |  |  | 14 |  |
| 49 | The Flamberge | ザ・フランベルジュ | 2H weapon | Sword | 5-33 (4d8+1) |  | 3 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 370000 | 185000 |  |  |  | 14 |  |
| 50 | Sword of Flash | ソード オブ フラッシュ | 1H weapon | Sword | 5-29 (4d7+1) |  | 2 |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 500000 | 250000 |  | vs Demons, Undead: damage up |  | 15 |  |
| 51 | Odin Sword | オーディンソード | 1H weapon | Sword | 5-38 (3d12+2) |  | 4 |  | S |  | Fig Lor Val | any |  | 500000 | 250000 |  | vs Demons, Spirits, Dragons: damage up |  | 15 |  |
| 52 | Excalibur | エクスカリバー | 2H weapon | Sword | 7-40 (3d12+4) |  | 4 |  | S |  | Val | G |  | 650000 | 325000 |  |  |  | 15 |  |
| 53 | Onikiri | オニキリ | 1H weapon | Sword | 3-30 (3d10) |  | 3 |  | S |  | Sam Nin Mus Kun | any |  | 700000 | 350000 |  |  |  | 15 |  |
| 54 | Siegfried Sword | ジークフリートのつるぎ | 2H weapon | Sword | 10-55 (5d10+5) |  | 5 |  | S |  | Fig Sam Lor Val Ave | any |  | 900000 | 450000 |  |  |  | 15 |  |
| 55 | Muramasa | むらまさ | 1H weapon | Sword | 8-80 (8d10) |  | 6 |  | S |  | Sam Mus | any |  | 1000000 | 500000 |  | Critical +5% |  | 15 |  |
| 56 | Dagger | ダガー | 1H weapon | Dagger | 1-4 (1d4) | 2 |  |  | S | 70 | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum | any |  | 20 | 10 |  |  |  | 1 | unlimited |
| 57 | Sacrifice Dagger | いけにえのダガー | 1H weapon | Dagger | 1-4 (1d4) | 3 |  |  | S | 95 | Fig Mag Thi Sam Lor Nin Arc Val Ave Mus Kun Sum | any | cursed | 100 | 50 |  |  |  | 2 |  |
| 58 | Silver Dagger | シルバーダガー | 1H weapon | Dagger | 1-4 (1d4) | 4 |  |  | S | 70 | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum | any |  | 250 | 125 |  |  |  | 2 | 3 |
| 59 | Kris | クリス | 1H weapon | Dagger | 1-4 (1d4) | 5 |  |  | S | 70 | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum | any |  | 500 | 250 |  | vs Demons: damage up |  | 3 | 3 |
| 60 | Main Gauche | マンゴーシュ | Parry dagger | Dagger | 1-4 (1d4) | 6 |  | -1 | S | 65 | Fig Thi Sam Lor Nin Val Mus Kun | any |  | 1500 | 750 |  |  |  | 5 | 1 |
| 61 | Dagger of Speed | ダガー オブ スピード | 1H weapon | Dagger | 1-4 (1d4) | 3 | 2 |  | S | 85 | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum | any |  | 10000 | 5000 |  |  |  | 8 |  |
| 62 | Thieves' Dagger | シーブズダガー | 1H weapon | Dagger | 2-5 (1d4+1) | 1 | 1 |  | S | 85 | Thi Nin Kun | any |  | 10000 | 5000 | A Thief using it becomes a Ninja (gone 100%) |  |  | 9 |  |
| 63 | Butterfly Knife | バタフライナイフ | 1H weapon | Dagger | 3-6 (1d4+2) | 1 | 2 |  | S | 85 | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum | any |  | 10000 | 5000 | Becomes a Ninja (gone 100%) |  |  | 9 |  |
| 64 | Kunai | くない | 1H weapon | Dagger | 3-7 (2d3+1) | 5 |  |  | S | 95 | Nin Kun | any |  | 500000 | 250000 |  | Critical +10% |  | 15 |  |
| 65 | War Hammer | ウォーハンマー | 1H weapon | Hammer | 3-7 (2d3+1) |  |  |  | S | 70 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 150 | 75 |  |  |  | 2 | unlimited |
| 66 | Thor's Hammer | トールハンマー | 1H weapon | Hammer | 10-16 (2d4+8) |  |  |  | S | 85 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 200000 | 100000 | Lightning Bolt [battle, Lv6] (breaks 25%) |  |  | 15 |  |
| 67 | Sling | スリング | Sling | Cord | 1-3 (1d3) |  |  |  | L |  | Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 20 | 10 |  |  |  | 1 | unlimited |
| 68 | Queen's Whip | じょおうのムチ | 1H weapon | Cord | 11-21 (2d6+9) |  | 50 |  | M |  | Fig Mag Pri Thi Bis Sam Lor Nin Val Ave Mus Kun Sum | any | cursed | 50000 | 25000 |  |  |  | 10 |  |
| 69 | Whip | ウィップ | 1H weapon | Cord | 2-3 (1d2+1) |  | 50 |  | M |  | Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 40 | 20 |  |  |  | 1 | unlimited |
| 70 | Flail | フレイル | 1H weapon | Long staff | 2-5 (1d4+1) |  |  |  | M | 70 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 70 | 35 |  |  |  | 1 | unlimited |
| 71 | Morning Star | モーニングスター | 1H weapon | Long staff | 2-7 (1d6+1) |  |  |  | M | 70 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 90 | 45 |  |  |  | 1 | 5 |
| 72 | Nunchaku | ヌンチャク | 2H weapon | Long staff | 1-3 (1d3) | 1 | 50 |  | S |  | Nin Kun | any |  | 100 | 50 |  |  |  | 2 | 5 |
| 73 | Cursed Flail | のろわれたフレイル | 1H weapon | Long staff | 3-6 (1d4+2) |  | 50 |  | M | 95 | Fig Pri Bis Sam Lor Nin Val Ave Mus Kun Sum | any | cursed | 200 | 100 |  |  |  | 2 |  |
| 74 | Holy Flail | せいなるフレイル | 1H weapon | Long staff | 3-8 (1d6+2) |  | 1 |  | M | 80 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 1000 | 500 |  | vs Demons: damage up |  | 5 |  |
| 75 | Sickle Spear | かまやり | 2H weapon | Long staff | 1-17 (1d17) |  | 49 |  | M |  | Fig Sam Lor Nin Val Kun | any |  | 1500 | 750 |  |  |  | 5 |  |
| 76 | Halberd | ハルバード | 2H weapon | Long staff | 1-24 (1d24) |  | 47 |  | M |  | Fig Sam Lor Nin Val Kun | any |  | 1500 | 750 |  |  |  | 5 |  |
| 77 | Windmill Glaive | ふうしゃなぎなた | 2H weapon | Long staff | 1-30 (1d30) |  | 48 |  | M |  | Fig Sam Lor Nin Val Kun | any |  | 170000 | 85000 |  |  |  | 13 |  |
| 78 | Vulcan Hammer | バルカンハンマー | 2H weapon | Long staff | 1-36 (1d36) |  | 1 |  | M |  | Fig Pri Bis Sam Lor Nin Val Kun | any |  | 444440 | 222220 | Fireball [battle, Lv6] (breaks 25%) |  |  | 15 |  |
| 79 | Faust Halberd | ファウストハルバード | 2H weapon | Long staff | 1-42 (1d42) |  | 2 |  | M |  | Fig Sam Lor Nin Val Kun | any |  | 666660 | 333330 |  | vs Demons: damage up |  | 15 |  |
| 80 | Mace | メイス | 1H weapon | Staff | 1-6 (1d6) |  |  |  | S | 70 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 60 | 30 |  |  |  | 1 | unlimited |
| 81 | Maul | モール | 2H weapon | Staff | 3-7 (2d3+1) |  |  |  | S |  | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 100 | 50 |  |  |  | 2 | unlimited |
| 82 | Unholy Mace | けがれたメイス | 1H weapon | Staff | 2-7 (1d6+1) |  | 50 |  | S | 95 | Fig Pri Bis Sam Lor Nin Val Ave Mus Kun Sum | any | cursed | 200 | 100 |  |  |  | 2 |  |
| 83 | Purified Mace | きよめたメイス | 1H weapon | Staff | 2-7 (1d6+1) |  | 1 |  | S | 80 | Fig Pri Bis Sam Lor Nin Val Mus Kun Sum | any |  | 1000 | 500 |  | vs Undead: damage up |  | 4 |  |
| 84 | Spear | スピア | 1H weapon | Spear | 1-6 (1d6) |  |  |  | S | 70 | Fig Sam Lor Nin Val Mus Kun | any |  | 50 | 25 |  |  |  | 1 | unlimited |
| 85 | Vermilion Spear | しゅぬりのやり | 1H weapon | Spear | 3-9 (2d4+1) |  |  |  | S | 70 | Fig Sam Lor Nin Val Mus Kun | any |  | 250 | 125 |  |  |  | 3 | 1 |
| 86 | Lance | ランサー | 2H weapon | Spear | 4-13 (3d4+1) |  | 50 |  | M |  | Fig Sam Lor Nin Val Kun | any |  | 300 | 150 |  |  |  | 3 | 1 |
| 87 | Demon Spear | あくまのやり | 2H weapon | Spear | 11-20 (1d10+10) |  | 2 |  | M |  | Fig Sam Lor Nin Val Ave Mus Kun | any | cursed | 35000 | 17500 |  |  | -5 | 10 |  |
| 88 | Naobi Spear | なおびのやり | 2H weapon | Spear | 12-26 (2d8+10) |  | 2 |  | M |  | Fig Sam Lor Nin Val Mus Kun | any |  | 90000 | 45000 |  |  |  | 12 |  |
| 89 | Valkyrie Javelin | ヴァルキリー・ジャベリン | 1H weapon | Spear | 19-40 (3d8+16) |  | 7 |  | S | 95 | Fig Sam Lor Nin Val Mus Kun | any |  | 100000 | 50000 |  |  |  | 13 |  |
| 90 | Jeanne's Spear | ジャンヌのやり | 1H weapon | Spear | 16-30 (2d8+14) | 1 | 3 |  | S | 95 | Fig Sam Lor Nin Val Mus Kun | any |  | 150000 | 75000 |  |  |  | 13 |  |
| 91 | Gungnir | グングニル | 2H weapon | Spear | 17-35 (2d10+15) |  | 4 |  | M | 95 | Fig Sam Lor Nin Val Kun | any |  | 500000 | 250000 |  |  |  | 14 |  |
| 92 | Longinus | ロンギヌス | 2H weapon | Spear | 20-38 (2d10+18) |  | 4 |  | M | 95 | Fig Sam Lor Nin Val Ave Kun | any | cursed | 520000 | 260000 |  |  |  | 15 |  |
| 93 | Short Bow | ショートボウ | Bow | Bow | 1-6 (1d6) |  |  |  | L |  | Fig Thi Sam Lor Nin Arc Val Kun Sum | any |  | 350 | 175 |  |  |  | 1 | unlimited |
| 94 | Long Bow | ロングボウ | Bow | Bow | 1-8 (1d8) |  |  |  | L |  | Fig Sam Lor Nin Arc Val Kun | any |  | 900 | 450 |  |  |  | 4 | 2 |
| 95 | Light Crossbow | ライトクロスボウ | Crossbow | Bow | 2-7 (1d6+1) |  |  |  | L |  | Fig Thi Sam Lor Nin Arc Val Kun | any |  | 2500 | 1250 |  |  |  | 4 |  |
| 96 | Composite Bow | コンポジットボウ | Bow | Bow | 2-10 (2d5) |  |  |  | L |  | Arc | any |  | 3000 | 1500 |  |  |  | 5 |  |
| 97 | Heavy Crossbow | ヘビークロスボウ | Crossbow | Bow | 5-10 (1d6+4) |  |  |  | L |  | Arc | any |  | 9000 | 4500 |  |  |  | 7 |  |
| 98 | Arbalest | アルバレスト | Crossbow | Bow | 7-15 (2d5+5) |  |  |  | L |  | Arc | any |  | 25000 | 12500 |  |  |  | 5 |  |
| 99 | Lloyd's Bow | ロイドのゆみ | Bow | Bow | 4-8 (1d5+3) | 1 |  |  | L |  | Arc | any |  | 30000 | 15000 |  |  |  | 8 |  |
| 100 | Rotten Leather | くさったレザーアーマー | Body armor | Armor |  |  |  |  | - |  | Fig Pri Thi Bis Sam Lor Nin Arc Val Ave Mus Kun Sum | any | cursed | 1500 | 750 |  |  |  | 4 |  |
| 101 | Leather Armor | レザーアーマー | Body armor | Armor |  |  |  | -2 | - |  | Fig Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 90 | 45 |  |  |  | 1 | unlimited |
| 102 | Studded Leather | スタデッドレザー | Body armor | Armor |  |  |  | -3 | - |  | Fig Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 350 | 175 |  |  |  | 2 | unlimited |
| 103 | Old Chain Mail | ふるいチェインメイル | Body armor | Armor |  |  |  | -4 | - |  | Fig Pri Bis Sam Lor Nin Val Ave Mus Kun | any | cursed | 10000 | 5000 |  |  |  | 7 |  |
| 104 | Scale Mail | スケイルメイル | Body armor | Armor |  |  |  | -5 | - |  | Fig Pri Bis Sam Lor Nin Val Mus Kun | any |  | 1000 | 500 |  |  |  | 5 | 5 |
| 105 | Chain Mail | チェインメイル | Body armor | Armor |  |  |  | -6 | - |  | Fig Pri Bis Sam Lor Nin Val Mus Kun | any |  | 1500 | 750 |  |  |  | 5 | 5 |
| 106 | Badick's Garb | バティックのしょうぞく | Body armor | Armor |  |  |  | -6 | - |  | Thi Nin Kun | E |  | 2000 | 1000 |  |  |  | 7 |  |
| 107 | Breastplate | ブレストプレート | Body armor | Armor |  |  |  | -7 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 2750 | 1375 |  |  |  | 6 |  |
| 108 | Rusted Armor | さびついたよろい | Body armor | Armor |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 13000 | 6500 |  |  |  | 8 |  |
| 109 | Banded Mail | バンデッドメイル | Body armor | Armor |  |  |  | -8 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 5250 | 2625 |  |  |  | 7 |  |
| 110 | Veteran's Armor | れきせんのよろい | Body armor | Armor |  |  |  | -6 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 10000 | 5000 |  |  |  | 8 |  |
| 111 | Plate Mail | プレートメイル | Body armor | Armor |  |  |  | -9 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 11500 | 5750 |  |  |  | 8 |  |
| 112 | Plate of Anguish | くるしみのむねあて | Body armor | Armor |  |  |  | -7 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 25000 | 12500 |  |  | -5 | 9 |  |
| 113 | Ninja Mail | しのびかたびら | Body armor | Armor |  |  |  | -10 | - |  | Nin Kun | any |  | 42500 | 21250 |  |  |  | 10 |  |
| 114 | Warrior's Armor | もののふのよろい | Body armor | Armor |  |  |  | -10 | - |  | Fig Sam Mus | any |  | 42500 | 21250 |  |  |  | 10 |  |
| 115 | Cursed Armor | のろわれたよろい | Body armor | Armor |  |  |  | -8 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 50000 | 25000 |  |  | -3 | 11 |  |
| 116 | Nobunaga's Armor | のぶながのよろい | Body armor | Armor |  |  |  | -9 | - |  | Fig Sam Mus | any | cursed | 80000 | 40000 |  |  |  | 11 |  |
| 117 | Black Lion Armor | くろじしおどし | Body armor | Armor |  |  |  | -11 | - |  | Fig Sam Mus | any |  | 80000 | 40000 |  |  |  | 11 |  |
| 118 | Armor of Love | あいのよろい | Body armor | Armor |  |  |  | -11 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | G |  | 100000 | 50000 |  |  |  | 12 |  |
| 119 | Armor of Life | いのちのよろい | Body armor | Armor |  |  |  | -11 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | N |  | 100000 | 50000 |  |  |  | 12 |  |
| 120 | Armor of Hate | にくしみのよろい | Body armor | Armor |  |  |  | -10 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | E |  | 120000 | 60000 |  |  |  | 12 |  |
| 121 | Demon Armor | あくまのよろい | Body armor | Armor |  |  |  | -12 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 200000 | 100000 |  |  | -4 | 13 |  |
| 122 | Kamui Garb | カムイのしょうぞく | Body armor | Armor |  |  |  | -12 | - |  | Nin Kun | any |  | 500000 | 250000 |  |  |  | 14 |  |
| 123 | Asura Armor | しゅらのよろい | Body armor | Armor |  |  |  | -12 | - |  | Sam Mus | any |  | 500000 | 250000 |  |  |  | 14 |  |
| 124 | Hero's Armor | ゆうしゃのよろい | Body armor | Armor |  |  |  | -12 | - |  | Val | any |  | 800000 | 400000 |  |  |  | 15 |  |
| 125 | Garb of Lords | ガーブ オブ ローズ | Body armor | Armor |  |  |  | -13 | - |  | Lor | any |  | 1000000 | 500000 |  |  | 3 | 15 |  |
| 126 | Moldy Robe | かびたローブ | Body armor | Robe |  |  |  | 1 | - |  | all | any | cursed | 400 | 200 |  |  |  | 2 |  |
| 127 | Robe | ローブ | Body armor | Robe |  |  |  | -1 | - |  | all | any |  | 20 | 10 |  |  |  | 1 | unlimited |
| 128 | Warnard's Robe | ワーナードのローブ | Body armor | Robe |  |  |  | -4 | - |  | Mag Pri Thi Bis Sam Lor Nin Arc Val Ave Mus Kun Sum | any |  | 55000 | 27500 |  |  |  | 11 |  |
| 129 | Phoenix Robe | ほうおうのローブ | Body armor | Robe |  |  |  | -8 | - |  | Pri Bis Sum | any |  | 60000 | 30000 |  |  |  | 11 |  |
| 130 | Buckler | バックラー | Shield | Shield |  |  |  | -1 | - |  | Fig Pri Thi Bis Lor Nin Val Kun Sum | any |  | 30 | 15 |  |  |  | 1 | unlimited |
| 131 | Warped Shield | ゆがんだたて | Shield | Shield |  |  |  | 1 | - |  | Fig Pri Lor Val Ave Kun | any | cursed | 3500 | 1750 |  |  |  | 3 |  |
| 132 | Old Shield | ふるいたて | Shield | Shield |  |  |  | -1 | - |  | Fig Pri Lor Val Ave Kun | any | cursed | 2300 | 1150 |  |  |  | 3 |  |
| 133 | Rusted Shield | さびついたたて | Shield | Shield |  |  |  | -2 | - |  | Fig Pri Lor Val Ave Kun | any | cursed | 2300 | 1150 |  |  |  | 3 |  |
| 134 | Round Shield | ラウンドシールド | Shield | Shield |  |  |  | -2 | - |  | Fig Pri Thi Bis Lor Nin Val Kun Sum | any |  | 500 | 250 |  |  |  | 2 | unlimited |
| 135 | Kite Shield | カイトシールド | Shield | Shield |  |  |  | -3 | - |  | Fig Pri Lor Val | any |  | 1500 | 750 |  |  |  | 3 | 5 |
| 136 | Spiked Shield | スパイクシールド | Shield | Shield | 1-4 (1d4) | 1 | 49 | -2 | S |  | Fig Lor Val | any |  | 2000 | 1000 |  |  |  | 4 | 1 |
| 137 | Heater Shield | ヒーターシールド | Shield | Shield |  |  |  | -4 | - |  | Fig Pri Lor Val | any |  | 3500 | 1750 |  |  |  | 4 |  |
| 138 | Tower Shield | タワーシールド | Shield | Shield |  |  |  | -5 | - |  | Fig Lor Val | any |  | 8000 | 4000 |  |  |  | 7 |  |
| 139 | Hollow Shield | うつろのたて | Shield | Shield |  |  |  | -4 | - |  | Fig Pri Lor Val Ave Kun | any | cursed | 50000 | 25000 |  |  | -4 | 12 |  |
| 140 | Shield of Trust | しんらいのたて | Shield | Shield |  |  |  | -5 | - |  | Fig Pri Lor Val Kun | G |  | 200000 | 100000 |  |  |  | 13 |  |
| 141 | Shield of Might | ちからのたて | Shield | Shield |  |  |  | -5 | - |  | Fig Pri Lor Val Kun | N |  | 200000 | 100000 |  |  |  | 13 |  |
| 142 | Murphy's Shield | マーフィー・シールド | Shield | Shield |  |  |  | -3 | - |  | Fig Lor Val | any |  | 1800 | 900 |  |  |  | 5 |  |
| 143 | Demon Shield | あくまのたて | Shield | Shield |  |  |  | -7 | - |  | Fig Pri Lor Val Ave Kun | any | cursed | 150000 | 75000 |  |  | -5 | 13 |  |
| 144 | Traitor's Shield | うらぎりのたて | Shield | Shield |  |  |  | -6 | - |  | Fig Pri Lor Val Ave Kun | E |  | 250000 | 125000 |  |  |  | 14 |  |
| 145 | Wizard's Hat | まほうつかいのぼうし | Helm | Helm |  |  |  | -1 | - |  | Mag Pri Bis Sum | any |  | 150 | 75 |  |  |  | 2 | unlimited |
| 146 | Leather Helm | レザーヘルム | Helm | Helm |  |  |  | -1 | - |  | Fig Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 250 | 125 |  |  |  | 2 | unlimited |
| 147 | Heavy Helm | おもいかぶと | Helm | Helm |  |  |  | 2 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 8000 | 4000 |  |  |  | 5 |  |
| 148 | Chain Coif | チェインコイフ | Helm | Helm |  |  |  | -2 | - |  | Fig Pri Bis Sam Lor Nin Val Mus Kun | any |  | 500 | 250 |  |  |  | 2 | unlimited |
| 149 | Louie's Hat | ルーイのぼうし | Helm | Helm |  |  |  | -2 | - |  | Pri Bis Val | G |  | 600 | 300 | Healing [battle+camp, Lv9] (breaks 30%) |  |  | 6 |  |
| 150 | Plate Helm | プレートヘルム | Helm | Helm |  |  |  | -3 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 1000 | 500 |  |  |  | 4 | 4 |
| 151 | Bascinet | バシネット | Helm | Helm |  |  |  | -4 | - |  | Fig Sam Lor Nin Val Mus Kun | any |  | 4000 | 2000 |  |  |  | 4 |  |
| 152 | Suit Helm | スーツヘルム | Helm | Helm |  |  |  | -5 | - |  | Fig Lor Val | any |  | 12500 | 6250 |  |  |  | 6 |  |
| 153 | Helm of Warping | てんいのかぶと | Helm | Helm |  |  |  | -2 | - |  | Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 25000 | 12500 |  | Teleport |  | 7 |  |
| 154 | Helm of Wisdom | ちえのかぶと | Helm | Helm |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | N |  | 50000 | 25000 |  |  |  | 8 |  |
| 155 | Helm of Joy | よろこびのかぶと | Helm | Helm |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | G |  | 50000 | 25000 |  |  |  | 8 |  |
| 156 | Hannya Mask | はんにゃのめん | Helm | Helm |  |  |  | -3 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 75000 | 37500 |  |  | -4 | 10 |  |
| 157 | Helm of Sorrow | かなしみのかぶと | Helm | Helm |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | E |  | 75000 | 37500 |  |  |  | 10 |  |
| 158 | Demon Helm | あくまのかぶと | Helm | Helm |  |  |  | -6 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 95000 | 47500 |  |  | -5 | 11 |  |
| 159 | Heavy Gloves | おもいグローブ | Gloves | Gloves |  |  |  | 1 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 7000 | 3500 |  |  |  | 6 |  |
| 160 | Leather Gloves | レザーグローブ | Gloves | Gloves |  |  |  | -1 | - |  | Fig Pri Thi Bis Sam Lor Nin Arc Val Mus Kun Sum | any |  | 500 | 250 |  |  |  | 2 | unlimited |
| 161 | Fingerless Glove | ゆびのないグローブ | Gloves | Gloves |  |  |  | 2 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 8000 | 4000 |  |  | -3 | 6 |  |
| 162 | Chain Gloves | チェイングローブ | Gloves | Gloves |  |  |  | -2 | - |  | Fig Pri Bis Sam Lor Nin Val Mus Kun | any |  | 2500 | 1250 |  |  |  | 2 | 3 |
| 163 | Copper Gloves | カッパーグローブ | Gloves | Gloves |  |  |  | -3 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 7500 | 3750 |  |  |  | 4 |  |
| 164 | Gauntlets | ガントレット | Gloves | Gloves |  |  |  | -4 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 30000 | 15000 |  |  |  | 7 |  |
| 165 | Silver Gloves | シルバーグローブ | Gloves | Gloves |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 75000 | 37500 |  |  |  | 10 |  |
| 166 | Winter Mittens | ウィンターミトン | Gloves | Gloves |  |  |  | -6 | - |  | Fig Lor Val | any |  | 125000 | 62500 |  | Water damage 1/2 |  | 12 |  |
| 167 | Gloves of Valor | ゆうきのこて | Gloves | Gloves |  |  |  | -6 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | N |  | 250000 | 125000 |  |  |  | 13 |  |
| 168 | Gloves of Amity | ゆうじょうのこて | Gloves | Gloves |  |  |  | -6 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | G |  | 250000 | 125000 |  |  |  | 13 |  |
| 169 | Gloves of Fury | いかりのこて | Gloves | Gloves |  |  |  | -7 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | E |  | 300000 | 150000 |  |  |  | 14 |  |
| 170 | Demon Gloves | あくまのこて | Gloves | Gloves |  |  |  | -7 | - |  | Fig Pri Sam Lor Nin Val Ave Mus Kun | any | cursed | 400000 | 200000 |  |  | -5 | 15 |  |
| 171 | Exorcism Charm | はじゃのごふ | Other | Odd object |  |  |  |  | - | 0 | none | any |  | 15000 | 7500 |  | Thrown: Sun Ray effect |  | 7 |  |
| 172 | Revival Charm | ふっかつのごふ | Other | Odd object |  |  |  |  | - |  | none | any |  | 1000000 | 500000 | Cures death, ashes and even Lost [battle+camp, Lv9] (breaks 100%) |  |  | 12 | unlimited |
| 173 | Fairy's Heart | ようせいのこころ | Other | Odd object |  |  |  |  | - |  | Fig Mag Pri Thi Bis Sam Lor Arc Val Mus Sum | any |  | 50 | 25 |  | Lets you meet the twin fairies |  | 10 |  |
| 174 | Laila's Beads | ライラのじゅず | Other | Odd object |  |  |  | -3 | - |  | Pri Bis Val | any |  | 4000 | 2000 |  |  |  | 9 |  |
| 175 | Jewel of Magic | ジュエル オブ マジック | Other | Odd object |  |  |  | -2 | - |  | Mag Pri Bis Sum | any |  | 3500 | 1750 |  |  |  | 6 |  |
| 176 | Shell Amulet | アミュレット オブ シェル | Other | Odd object |  |  |  |  | - |  | all | any |  | 300000 | 150000 |  | Magic evade 30% |  | 13 | 1 |
| 177 | Shell Amulet+1 | アミュレット オブ シェル+1 | Other | Odd object |  |  |  |  | - |  | all | any |  | 450000 | 225000 |  | Magic evade 50% |  | 14 |  |
| 178 | Shell Amulet+2 | アミュレット オブ シェル+2 | Other | Odd object |  |  |  |  | - |  | all | any |  | 600000 | 300000 |  | Magic evade 85% |  | 15 |  |
| 179 | Dreaming Stone | ゆめみのいし | Other | Stone |  |  |  |  | - |  | none | any |  | 1000 | 500 | Sleep on all foes [battle, Lv7] (breaks 25%) |  |  | 6 | 1 |
| 180 | Healing Stone | ヒーリングストーン | Other | Stone |  |  |  |  | - | 10 | none | any |  | 2000 | 1000 | Healing [battle+camp, Lv9] (breaks 40%) | Thrown at undead: 16-24 damage |  | 1 | unlimited |
| 181 | Exorcist Stone | エクソシストストーン | Other | Stone |  |  |  |  | - |  | none | any |  | 15000 | 7500 | Astral Gate [battle, Lv6] (breaks 100%) |  |  | 9 |  |
| 182 | Synthesis Stone | シンセサイズストーン | Other | Stone |  |  |  | -3 | - |  | all | any |  | 40000 | 20000 | Astral Gate [battle, Lv6] (breaks 100%) | Drain evade 50% |  | 10 |  |
| 183 | Youth Stone | わかがえりのいし | Other | Stone |  |  |  |  | - |  | all | any |  | 38000 | 19000 | Age -1 (gone 100%) |  |  | 10 |  |
| 184 | Rabbit's Foot | ウサギのあし | Other | Odd object |  |  |  |  | - |  | all | any |  | 50000 | 25000 | Luck +1 (gone 100%) |  |  | 11 |  |
| 185 | Clockwork Doll | からくりにんぎょう | Other | Odd object |  |  |  |  | - |  | Nin Kun | any |  | 20000 | 10000 |  | Equipped: hits deal double damage |  | 9 |  |
| 186 | Scroll of Sleep | スクロール オブ スリープ | Other | Scroll |  |  |  |  | - |  | none | any |  | 300 | 150 | Sleep [battle, Lv6] (breaks 100%) |  |  | 4 | 5 |
| 187 | Scroll of Light | スクロール オブ ライト | Other | Scroll |  |  |  |  | - |  | none | any |  | 80 | 40 | Light [camp, Lv0] (breaks 100%) |  |  | 1 | unlimited |
| 188 | Scroll of Flesh | スクロール オブ フレッシュ | Other | Scroll |  |  |  |  | - |  | none | any |  | 600 | 300 | Stone to Flesh [battle+camp, Lv9] (breaks 100%) |  |  | 4 |  |
| 189 | Scroll of Ice | スクロール オブ アイス | Other | Scroll |  |  |  |  | - |  | none | any |  | 1100 | 550 | Ice Storm [battle, Lv6] (breaks 100%) |  |  | 7 |  |
| 190 | Scroll of Bolt | スクロール オブ サンダー | Other | Scroll |  |  |  |  | - |  | none | any |  | 900 | 450 | Lightning Bolt [battle, Lv6] (breaks 100%) |  |  | 7 |  |
| 191 | Scroll of Fire | スクロール オブ ファイア | Other | Scroll |  |  |  |  | - |  | none | any |  | 1000 | 500 | Fireball [battle, Lv6] (breaks 100%) |  |  | 7 |  |
| 192 | Scroll of Guard | スクロール オブ プロテクション | Other | Scroll |  |  |  |  | - |  | none | any |  | 1100 | 550 | Force Field [battle, Lv10] (breaks 100%) |  |  | 7 |  |
| 193 | Map Record Sheet | マップきろくシート | Other | Scroll |  |  |  |  | - |  | none | any |  | 400 | 200 | Shows the map [camp, Lv0] (breaks 30%) |  |  | 1 | unlimited |
| 194 | Healing Potion | ヒーリングポーション | Other | Potion |  |  |  |  | - | 0 | none | any |  | 100 | 50 | Healing [battle+camp, Lv9] (breaks 100%) | Thrown at undead: 16-24 damage |  | 1 | unlimited |
| 195 | Antidote | アンチドート | Other | Potion |  |  |  |  | - |  | none | any |  | 250 | 125 | Cure Poison [battle+camp, Lv9] (breaks 100%) |  |  | 2 | unlimited |
| 196 | Cure Potion | キュアポーション | Other | Potion |  |  |  |  | - |  | none | any |  | 300 | 150 | Cures paralysis, sleep, fear, poison [battle+camp, Lv9] (breaks 100%) |  |  | 2 | unlimited |
| 197 | High Heal Potion | ハイヒーリングポーション | Other | Potion |  |  |  |  | - | 0 | none | any |  | 300 | 150 | Recovery [battle+camp, Lv9] (breaks 100%) | Thrown at undead: 32-48 damage |  | 2 | 15 |
| 198 | Potion of Poison | ポーション オブ ポイズン | Other | Potion |  |  |  |  | - | 0 | none | any |  | 300 | 150 |  | Thrown: poisons the foe |  | 2 |  |
| 199 | Elixir | エリクサー | Other | Potion |  |  |  |  | - | 0 | none | any |  | 500 | 250 | Cure All [battle+camp, Lv9] (breaks 100%) | Can destroy the undead |  | 3 | 3 |
| 200 | Cloak | クローク | Other | Cloth |  |  |  |  | - |  | all | any |  | 20 | 10 |  |  |  | 1 | 5 |
| 201 | Hider Cloak | ハイダークローク | Other | Cloth |  |  |  | -4 | - |  | Thi | any |  | 200000 | 100000 |  | "Hide" success +10% |  | 9 |  |
| 202 | Ring of Warping | てんいのゆびわ | Other | Ring |  |  |  |  | - |  | all | any |  | 25000 | 12500 | Teleport [camp, Lv10] (breaks 25%) |  |  | 11 |  |
| 203 | Ring of Guard | プロテクションリング | Other | Ring |  |  |  | -1 | - |  | all | any |  | 25000 | 12500 |  |  |  | 10 |  |
| 204 | Ring of Guard+1 | プロテクションリング+1 | Other | Ring |  |  |  | -2 | - |  | all | any |  | 50000 | 25000 |  |  |  | 11 |  |
| 205 | Ring of Ice | リング オブ アイス | Other | Ring |  |  |  |  | - |  | all | any |  | 50000 | 25000 |  | Fire damage 1/2 |  | 12 |  |
| 206 | Ring of Fire | リング オブ ファイア | Other | Ring |  |  |  |  | - |  | all | any |  | 50000 | 25000 |  | Water damage 1/2 |  | 12 |  |
| 207 | Ring of Healing | リング オブ ヒーリング | Other | Ring |  |  |  |  | - |  | all | any |  | 300000 | 150000 |  | Equipped: +5 HP per step | 5 | 13 |  |
| 208 | Holy Ring | ホーリーリング | Other | Ring |  |  |  |  | - |  | all | any |  | 400000 | 200000 |  | Drain evade 10% |  | 14 |  |
| 209 | Priest Ring | プリーストリング | Other | Ring |  |  |  |  | - |  | Pri Bis Lor Val | any |  | 500000 | 250000 |  | Healing and cure success +50% |  | 15 |  |
| 210 | Ring of Death | リング オブ デス | Other | Ring |  |  |  | -4 | - |  | all | any |  | 500000 | 250000 |  | Equipped: -5 HP per step | -5 | 15 |  |
| 211 | Ring of Life | リング オブ ライフ | Other | Ring |  |  |  | -2 | - |  | all | any |  | 500000 | 250000 |  | Equipped: +5 HP per step | 5 | 15 |  |
| 212 | Avenger Sword | アベンジャーソード | 1H weapon | Sword | 4-40 (4d10) |  | 4 |  | S |  | Ave | any | cursed | 700000 | 350000 |  |  |  | 14 |  |
| 213 | The Avenger | ジ・アベンジャー | 1H weapon | Sword | 6-42 (4d10+2) |  | 5 |  | S |  | Fig Thi Sam Lor Nin Ave Mus Kun | any |  | 800000 | 400000 | Becomes an Avenger The item changes (gone 30%) |  |  | 15 |  |
| 214 | Ura Muramasa | うら・むらまさ | 1H weapon | Sword | 15-105 (10d10+5) | 1 | 8 |  | S |  | Sam Mus | any |  | 5000000 | 2500000 |  | Critical +10% |  | 15 |  |
| 215 | Summoner's Robe | しょうかんしのローブ | Body armor | Robe |  |  |  | -6 | - |  | Sum | any |  | 50000 | 25000 |  |  |  | 12 |  |
| 216 | Magic Robe | まどうのローブ | Body armor | Robe |  |  |  | -7 | - |  | all | any |  | 80000 | 40000 | Becomes a Summoner The item changes (gone 30%) |  |  | 13 |  |
| 217 | Valiant Shield | ヴァリアントシールド | Shield | Shield |  |  |  | -5 | - |  | Val | any |  | 100000 | 50000 |  |  |  | 13 |  |
| 218 | Guardian Shield | かごのたて | Shield | Shield |  |  |  | -6 | - |  | Fig Pri Thi Bis Lor Nin Val Kun | any |  | 300000 | 150000 | Becomes a Valiant The item changes (gone 30%) |  |  | 14 |  |
| 219 | Musashi's Helm | ムサシのかぶと | Helm | Helm |  |  |  | -4 | - |  | Mus | any |  | 20000 | 10000 |  |  |  | 13 |  |
| 220 | Warrior's Helm | もののふのかぶと | Helm | Helm |  |  |  | -5 | - |  | Fig Sam Lor Val Mus | any |  | 65000 | 32500 | Becomes a Musashi The item changes (gone 30%) |  |  | 14 |  |
| 221 | Kunoichi Gloves | くのいちのこて | Gloves | Gloves |  |  |  | -4 | - |  | Kun | any |  | 10000 | 5000 |  |  |  | 13 |  |
| 222 | Charming Gloves | みわくのこて | Gloves | Gloves |  |  |  | -5 | - |  | Fig Pri Sam Lor Nin Val Mus Kun | any |  | 230000 | 115000 | Becomes a Kunoichi The item changes (gone 30%) |  |  | 14 |  |
| 223 | Key Card | キーカード | Other | Odd object |  |  |  |  | - |  | none | any |  | 50 | 25 |  | Lets you ride the elevator |  | 4 |  |
