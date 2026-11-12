# Glossary - Wizardry Empire (GBC)

Binding names and terms. Use them exactly; add new rows when a new name is decided (with the Japanese).

## Rulings
- Classic Wizardry terminology where the series has an established English term (classes, statuses, spells,
  item and monster names from the English Wizardry games); otherwise translate the meaning.
- Stats abbreviations in tight fields: STR, IQ, PIE, VIT, AGI, LUK. Long form on the stat screen: Strength, I.Q.,
  Piety, Vitality, Agility, Luck.
- Currency: gold / "G" after numbers (`500G`).
- Japanese quotes 『』 -> "...". ・・・ -> `...` (or `…`, code $7E, where space is tight).
- No honorifics in this game's register (archaic speech is rendered as archaic English: "I am Lloyd", "Farewell").
- Fonts (owner's rule, 2026-11-11, widened the same day): use the small VWF font for as much as possible,
  numbers included; it leaves room for long names. The 8 px font stays only where it is a stylistic choice
  (e.g. a deliberately large display or a grid such as the name-entry chart); name each such case in
  docs/status.md so the owner can review it. When a screen still shows text or numbers in the 8 px font, hook
  its printer (route it through the VWF) rather than fitting the English to the fixed-width field. Numbers keep
  their alignment (right-aligned in their field, digits of equal width).
- Field limits are hard: items 16 chars, monsters 12 (abbreviate with "Gr." / "Mstr." / "Elem." only when needed),
  default character names 7.
- Battle narration: events in past tense ("attacked", "dealt", "took N damage", "cast"); states keep "is"
  ("is afraid!", "is paralyzed!"). (2026-11-12, editor review)
- One name per monster, never two monsters with the same name (しかく = Cutthroat, アサシン = Assassin).
  イフリート = Ifrit (spell and monster). ダンジョン in system messages = "maze".

## Places
| JP | EN |
|---|---|
| まちはずれ | Edge of Town / Outskirts (short header) |
| くんれんじょう | Training Grounds / Training (short) |
| はくぶつかん | Museum |
| ローズの さかば | Rose's Tavern |
| たてふだ | Notice Board |
| サンサーラじいん | Samsara Temple |
| しょうてん ローレライ | Lorelei's Shop |
| アリエスの やど | Aries Inn |
| まどう | the maze |
| まどうエレベータ | Maze Elevator |
| まかい | the abyss / netherworld |
| ちじょう | the surface / mortals (ちじょうのもの) |

## People
| JP | EN |
|---|---|
| マーフィー | Murphy |
| ロイド | Lloyd |
| ルーイ | Louie |
| ジークフリート | Siegfried |
| ライラ | Laila |
| こじろう | Kojiro |
| バディック | Badick |
| ワーナード | Warnard |
| デーモンアディッシュ | Demon Adish |
| こうてい | the Emperor (the surface Emperor; ときのこうてい = the reigning Emperor) |
| まかいのこうてい | the Emperor of the Abyss (the netherworld's ruler; never plain "the Emperor" where the two could be confused) |
| きょうおう | Mad Overlord (狂王, as in Wizardry I) |
| レイ / シア | Rei / Shia (fairy twins) |

## Classes, races, alignments
| JP | EN | | JP | EN |
|---|---|---|---|---|
| せんし | Fighter | | にんげん | Human |
| まほうつかい | Mage | | エルフ | Elf |
| そうりょ | Priest | | ドワーフ | Dwarf |
| とうぞく | Thief | | ノーム | Gnome |
| ビショップ | Bishop | | ホビット | Hobbit |
| サムライ | Samurai | | ぜん | Good |
| ロード | Lord | | ちゅうりつ | Neutral |
| ニンジャ | Ninja | | あく | Evil |
| ゆみつかい | Archer | | | |
| ヴァリアント / アベンジャー / ムサシ / くのいち / しょうかんし | Valiant / Avenger / Musashi / Kunoichi / Summoner | | | |

## Statuses
| JP | EN |
|---|---|
| せいじょう | OK |
| きょうふ | Afraid |
| すいみん | Asleep |
| まひ | Paralyzed |
| いし | Stoned |
| しぼう | Dead |
| はい | Ashes |
| ロスト | Lost |
| どく | Poisoned |
| まふうじ | Silenced |

## Menus and verbs
| JP | EN |
|---|---|
| かう / うる / のろいをとく / しきべつ | Buy / Sell / Uncurse / Identify |
| おかねを あつめる / やまわけ | Pool gold / Divide gold |
| そうび / わたす / すてる / つかう | Equip / Give / Drop / Use |
| キャンプ | Camp |
| じゅもん | spells |
| けいけんち | EXP |
| しょうごう | Title |
| みならい | Apprentice |
