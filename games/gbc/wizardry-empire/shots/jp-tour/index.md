# Reference screenshots - set `jp-tour` (commit `1737042`)

File names: `NAME` = `wizardry-empire_gbc_jp_<category>_<id>.jp-tour` (`docs/capture-guide.md` at the repo root, "File names"). Native 160x144 PNGs (`NAME.<rom>.png`); 3x nearest in `3x/`: JP|EN (`3x/NAME.compare.png`).

| id | category | description | settled | tokens |
|---|---|---|---|---|
| logo_publisher | boot | Publisher logo after power-on | jp:yes | `pow,w300` |
| copyright | boot | Copyright/licence screen | jp:yes | `pow,w600` |
| title | title | Title screen | jp:yes | `pow,w760` |
| mode_select | options | Mode settings (BGM, sound, map, ...) | jp:yes | `pow,w750,start,w60,start,w60,start,w60,start,w60` |
| town_edge | menu | Town map, Edge of Town info | jp:no | `boot` |
| town_training | menu | Town map, Training Grounds info | jp:no | `boot,right` |
| town_museum | menu | Town map, Museum info | jp:no | `boot,right*2` |
| town_tavern | menu | Town map, Rose's Tavern info | jp:no | `boot,right*3` |
| town_notice | menu | Town map, Notice Board info | jp:no | `boot,right*4` |
| town_shop | menu | Town map, Lorelei's Shop info | jp:no | `boot,right*5` |
| town_temple | menu | Town map, Samsara Temple info | jp:no | `boot,right*6` |
| town_inn | menu | Town map, Aries Inn info | jp:no | `boot,right*7` |
| tavern_menu | menu | Tavern menu | jp:yes | `boot,right*3,a,w60` |
| tavern_add | menu | Add member: roster with character card | jp:yes | `boot,right*3,a,w60,a,w40` |
| party_town | menu | Town with the full party panel | jp:no | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60` |
| training_menu | menu | Training Grounds menu | jp:yes | `boot,right,a,w60` |
| shop_menu | shop | Shop: welcome and Buy/Sell menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60` |
| shop_buy | shop | Shop: Buy, item categories | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40` |
| temple_menu | shop | Samsara Temple menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60` |
| inn_rooms | menu | Aries Inn room list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60` |
| outskirts_menu | menu | Edge of Town: explore / resume / end | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60` |
| camp | menu | Camp menu on entering the maze | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150` |
| character_sheet | inventory | Character sheet from Camp | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60` |
| maze_view | gameplay | First-person maze view, Camp closed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60` |
| maze_menu | menu | Maze menu (Search, Pick a lock, ...) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,a,w40` |
| stairs_prompt | dialogue | Stairs up prompt at the entrance | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60` |
| tavern_remove_prompt | menu | Remove: who to remove? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down,a,w40` |
| tavern_removed | menu | Remove: member removed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down,a,w40,a,w60` |
| tavern_inspect_prompt | menu | Inspect: who? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40` |
| tavern_sheet_fighter | inventory | Character sheet (fighter) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60` |
| tavern_sheet_mage | inventory | Character sheet (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60` |
| tavern_sheet_spells | inventory | Character sheet: spells page (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60,a,w60` |
| tavern_sheet_items | inventory | Character sheet: items + action menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60` |
| tavern_item_equip | inventory | Items: equip, choose main weapon | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,a,w60` |
| tavern_item_give | inventory | Items: give to whom | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down,` |
| tavern_item_drop | inventory | Items: discard | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down*` |
| tavern_item_use | inventory | Items: use | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down*` |
| tavern_sheet_pool | menu | Character sheet: pool gold (gold 600) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60,down*2,a,` |
| tavern_divide | menu | Divide gold message | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*3,a,w60` |
| tavern_full | menu | Add with full party: party is full | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,a,w60` |
| tavern_empty_remove | menu | Remove with no party | jp:yes | `boot,right*3,a,w60,down,a,w60` |
| shop_noparty | shop | Shop without a party | jp:yes | `boot,right*5,a,w60` |
| training_create_name_hira | system | Name entry, hiragana page | jp:yes | `boot,right,a,w60,a,w60` |
| training_create_name_kata | system | Name entry, katakana page | jp:yes | `boot,right,a,w60,a,w60,select,w40` |
| training_create_name_abc | system | Name entry, alphanumeric page | jp:yes | `boot,right,a,w60,a,w60,select,w40,select,w40` |
| training_create_name_typed | system | Name entry, a name typed | jp:yes | `boot,right,a,w60,a,w60,a,w40,a,w40` |
| training_create_gender | system | Choose sex | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60` |
| training_create_race | system | Choose race | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60` |
| training_create_align | system | Choose alignment | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60` |
| training_create_bonus | system | Distribute bonus points | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60` |
| training_create_bonusleft | system | Bonus points remain message | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,a,w60` |
| training_create_class | system | Choose class (bonus spent) | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,right*20,down,right*20,down,right*20,down,right*20,down,right*2` |
| training_create_confirm | system | Use this character? | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,right*20,down,right*20,down,right*20,down,right*20,down,right*2` |
| training_view_list | menu | View character: roster | jp:yes | `boot,right,a,w60,down,a,w60` |
| training_view_sheet | inventory | View character: sheet | jp:yes | `boot,right,a,w60,down,a,w60,a,w60` |
| training_view_spells | inventory | View character: spells (mage) | jp:yes | `boot,right,a,w60,down,a,w60,down*4,a,w60,a,w60` |
| training_delete_list | menu | Delete character: roster | jp:yes | `boot,right,a,w60,down*2,a,w60` |
| training_delete_confirm | menu | Delete character: confirm | jp:yes | `boot,right,a,w60,down*2,a,w60,a,w60` |
| training_rename | menu | Rename: roster | jp:yes | `boot,right,a,w60,down*3,a,w60` |
| training_rename_entry | system | Rename: name entry | jp:yes | `boot,right,a,w60,down*3,a,w60,a,w60` |
| training_class_list | menu | Change class: roster | jp:yes | `boot,right,a,w60,down*4,a,w60` |
| training_class_pick | menu | Change class: classes | jp:yes | `boot,right,a,w60,down*4,a,w60,a,w60` |
| training_order | menu | Reorder roster | jp:yes | `boot,right,a,w60,down*5,a,w60` |
| training_order_pick | menu | Reorder roster: one picked | jp:yes | `boot,right,a,w60,down*5,a,w60,a,w60` |
| training_transfer | menu | Character transfer | jp:yes | `boot,right,a,w60,down*6,a,w60` |
| training_transfer_start | menu | Character transfer after START (no link partner) | jp:yes | `boot,right,a,w60,down*6,a,w60,start,w180` |
| shop_who | shop | Shop entry: who enters? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60` |
| shop_buy_weapons | shop | Buy: weapon list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60` |
| shop_buy_confirm | shop | Buy: confirm purchase | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60,a,w60` |
| shop_buy_armor | shop | Buy: armour list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,down,a,w60` |
| shop_buy_other | shop | Buy: other items list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,down*5,a,w60` |
| shop_sell | shop | Sell: item list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,down,a,w60` |
| shop_sell_confirm | shop | Sell: confirm | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,down,a,w60,a,w60` |
| shop_uncurse | shop | Uncurse | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,down*2,a,w60` |
| shop_identify | shop | Identify | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,down*3,a,w60` |
| shop_pool | shop | Pool gold | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,down*4,a,w60` |
| temple_help | shop | Help (cure) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,a,w60` |
| temple_pickup | shop | Pick up | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,down,a,w60` |
| temple_deposit | shop | Deposit | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,down*2,a,w60` |
| inn_who | menu | Inn entry | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60` |
| inn_stable | system | Stables (free) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,a,w60` |
| inn_stable_3 | system | Stables, after 2 | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,a,w60,a,w60,a,w60` |
| inn_cot | system | Cot room | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down,a,w60` |
| inn_royal | system | Royal suite | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down*4,a,w60` |
| inn_pool | menu | Pool gold | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down*5,a,w60` |
| notice_board | dialogue | Notice board text (one page; A returns to town) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right,a,w60` |
| museum_menu | menu | Museum: item room / monster room | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60` |
| outskirts_resume | menu | Edge of Town: resume adventure | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,down,a,w60` |
| outskirts_quit | menu | Edge of Town: quit adventure | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,down*2,a,w60` |
| outskirts_noparty | menu | Edge of Town without a party | jp:yes | `boot,a,w60` |
| camp_inspect_prompt | menu | Camp: inspect, who? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40` |
| camp_sheet_mage | inventory | Camp: character sheet (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60` |
| camp_spells_mage | inventory | Camp: mage spells page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60,a,` |
| camp_spell_cast | inventory | Camp: mage spells, A on spell | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60,a,` |
| camp_spells_priest | inventory | Camp: priest spells page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*3,a,w60,a,` |
| camp_items | inventory | Camp: items + action menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down,a,w6` |
| camp_item_use | inventory | Camp: use item | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down,a,w6` |
| camp_pool | menu | Camp: pool gold | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down*2,a,` |
| camp_reorder | menu | Camp: reorder, empty slots | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down,a,w60` |
| camp_reorder_pick | menu | Camp: reorder, first placed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down,a,w60,a,w40` |
| camp_equip | inventory | Camp: equip | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60` |
| camp_equip_2 | inventory | Camp: equip, next | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60,a,w60` |
| camp_equip_3 | inventory | Camp: equip, next 2 | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60,a,w60,a,` |
| maze_reopen_camp | menu | B in the maze reopens Camp | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,b,w60` |
| maze_turn_left | gameplay | Maze view after turning left | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,left,w40` |
| maze_turn_right | gameplay | Maze view after turning right | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,right,w40` |
| maze_dmenu | menu | Dungeon menu (SELECT) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40` |
| maze_search | system | Dungeon menu: search, nothing found | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,a,w6` |
| maze_picklock | system | Dungeon menu: pick lock, no door | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| maze_findparty_none | system | Dungeon menu: search for party, nobody | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| maze_settings | options | Dungeon menu: settings | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| shop_buy_yes | shop | Buy: Yes - item bought | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60,a,w60,up,` |
| shop_buy_tooexpensive | shop | Buy: item the character cannot afford | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60,down,a,w6` |
| inn_sleep | system | Inn: character sleeping (cot) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down,a` |
| museum_item_room | system | Museum: item room, categories and found/unfound counts | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60` |
| museum_item_list | system | Museum: weapon list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,a,w60` |
| museum_item_info | system | Museum: item data page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,a,w60,a,w60` |
| museum_item_other | system | Museum: other items list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,down*5,a,w60` |
| museum_monster_none | system | Museum: monster room selected, no monsters met yet (A does nothing) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,down,w20,a,w60` |
| stairs_up_prompt | dialogue | Stairs up prompt (step back onto the entrance stairs) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60,down,w60` |
| stairs_up_climb | gameplay | Stairs climbed: back in town | jp:no | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60,down,w60` |

## State-based shots (`states/`)

Not reproducible from power-on (random encounter / chest), so not in the shot list. Original ROM only; native 160x144 `states/NAME.jp.png` + `states/3x/NAME.jp.png` (file names in `states/index.json`). Start state (gitignored, under `work/`) then the tokens (tools/emu.py syntax), then wait for a stable frame (same rule as shoot.py); a trailing `!` means captured right after the inputs (animated screen).
The states were made from power-on: `boot,PARTY,left*3,a,w60,a,w150` (camp) -> `b,w60` (mzbase) -> `work/triage/battle1/explore.py` seed 3 (encounter b1) -> fight -> chest.

| id | category | description | settled | state | tokens |
|---|---|---|---|---|---|
| maze_findparty_busy | system | Dungeon menu: search for party, searching... (animated) | timed | `work/shots/jp_tour/explore/mzbase.state` | `select,w40,down*2,a!` |
| battle_encounter_unid | battle | Encounter with an unidentified monster (やつれたすがた), party panel | yes | `work/shots/jp_tour/explore/b1.state` | `w1` |
| battle_cmd_fighter | battle | Command menu, fighter (front row) | yes | `work/shots/jp_tour/explore/b1.state` | `a,w30` |
| battle_run_escaped | battle | Run chosen: party escaped, back in the maze | yes | `work/shots/jp_tour/explore/b1.state` | `a,w30,down*3,a,w60` |
| battle_encounter | battle | Encounter: 3 Crawling Claws (identified), monster panel | yes | `work/shots/jp_tour/explore/bt.state` | `w1` |
| battle_fight_modes | battle | Fight sub-menu: Normal / Aim to hit / Aim for damage | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30` |
| battle_cmd_thief | battle | Command menu, thief (Hide) | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30` |
| battle_cmd_archer | battle | Command menu, archer | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30` |
| battle_fight_modes_hit | battle | Fight sub-menu, cursor on Aim to hit | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30` |
| battle_cmd_priest | battle | Command menu, priest (back row: Defend/Spell/Dispel/Item/Run) | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30` |
| battle_cmd_mage | battle | Command menu, mage | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30,a,w30` |
| battle_spell_list | battle | Spell sub-menu: mage spell list | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30,a,w30,down,w30,a,w40` |
| battle_spell_info | battle | Spell sub-menu: spell details (Call Fear) | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30,a,w30,down,w30,a,w40,a,w40` |
| battle_cmd_bishop | battle | Command menu, bishop | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30,a,w30,down,w30,a,w40,a,w40,a,w40` |
| battle_item_menu | battle | Item sub-menu (bishop) | yes | `work/shots/jp_tour/explore/bt.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w30,down,w30,a,w30,a,w30,down,w30,a,w40,a,w40,a,w40,w30,down*2,w30,a,w40` |
| battle_confirm | battle | Round confirm: Fight / Back, with everyone's orders | yes | `work/shots/jp_tour/explore/bconfirm.state` | `w1` |
| battle_msg_cast | battle | Message: mage casts Call Fear | yes | `work/shots/jp_tour/explore/bconfirm.state` | `a,w60` |
| battle_msg_noeffect | battle | Message: spell had no effect | yes | `work/shots/jp_tour/explore/b6.state` | `a,w30` |
| battle_msg_attacks | battle | Message: attacks without damage | yes | `work/shots/jp_tour/explore/b6.state` | `a,w30,a,w30,a,w30,a,w30` |
| battle_msg_damage | battle | Message: monster deals damage | yes | `work/shots/jp_tour/explore/b6.state` | `a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,w1` |
| battle_msg_kill | battle | Message: damage and monster killed | yes | `work/shots/jp_tour/explore/bpre.state` | `a,w30` |
| battle_victory_exp | battle | Victory: experience message, chest appears | yes | `work/shots/jp_tour/explore/bchest.state` | `w1` |
| chest_menu | battle | Chest menu (inspect/cast/disarm/open/leave) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60` |
| chest_inspect_who | battle | Chest: who inspects? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,a,w40` |
| chest_inspect_result | battle | Chest: inspect result (trap guess) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,a,w40,a,w60` |
| chest_cast_who | battle | Chest: who casts? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down,w30,a,w40` |
| chest_cast_list | battle | Chest: spell list of the caster | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down,w30,a,w40,a,w60` |
| chest_disarm_who | battle | Chest: who disarms? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40` |
| chest_disarm_traps | battle | Chest: trap name list | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40,a,w60` |
| chest_disarm_result | battle | Chest: disarm result (no trap, item found) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40,a,w60,a,w60` |
| chest_open_who | battle | Chest: who opens? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*3,w30,a,w40` |
| chest_open_result | battle | Chest: opened, gold shared | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*3,w30,a,w40,a,w60` |
| chest_leave | battle | Chest: leave without opening | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*4,w30,a,w60` |
