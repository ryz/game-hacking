# Reference screenshots - set `jp_tour` (commit `1737042`)

Native 160x144 PNGs (`<id>.<rom>.png`), 3x nearest (`@3x`), JP|EN (`compare@3x`).

| id | category | description | settled | tokens |
|---|---|---|---|---|
| logo_publisher | boot | Publisher logo after power-on | jp:yes | `pow,w300` |
| copyright | boot | Copyright/licence screen | jp:yes | `pow,w600` |
| title | boot | Title screen | jp:yes | `pow,w760` |
| mode_select | options | Mode settings (BGM, sound, map, ...) | jp:yes | `pow,w750,start,w60,start,w60,start,w60,start,w60` |
| town_edge | town | Town map, Edge of Town info | jp:no | `boot` |
| town_training | town | Town map, Training Grounds info | jp:no | `boot,right` |
| town_museum | town | Town map, Museum info | jp:no | `boot,right*2` |
| town_tavern | town | Town map, Rose's Tavern info | jp:no | `boot,right*3` |
| town_notice | town | Town map, Notice Board info | jp:no | `boot,right*4` |
| town_shop | town | Town map, Lorelei's Shop info | jp:no | `boot,right*5` |
| town_temple | town | Town map, Samsara Temple info | jp:no | `boot,right*6` |
| town_inn | town | Town map, Aries Inn info | jp:no | `boot,right*7` |
| tavern_menu | tavern | Tavern menu | jp:yes | `boot,right*3,a,w60` |
| tavern_add | tavern | Add member: roster with character card | jp:yes | `boot,right*3,a,w60,a,w40` |
| party_town | town | Town with the full party panel | jp:no | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60` |
| training_menu | training | Training Grounds menu | jp:yes | `boot,right,a,w60` |
| shop_menu | shop | Shop: welcome and Buy/Sell menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60` |
| shop_buy | shop | Shop: Buy, item categories | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40` |
| temple_menu | temple | Samsara Temple menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60` |
| inn_rooms | inn | Aries Inn room list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60` |
| outskirts_menu | maze | Edge of Town: explore / resume / end | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60` |
| camp | maze | Camp menu on entering the maze | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150` |
| character_sheet | maze | Character sheet from Camp | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60` |
| maze_view | maze | First-person maze view, Camp closed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60` |
| maze_menu | maze | Maze menu (Search, Pick a lock, ...) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,a,w40` |
| stairs_prompt | maze | Stairs up prompt at the entrance | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60` |
| tavern_remove_prompt | tavern | Remove: who to remove? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down,a,w40` |
| tavern_removed | tavern | Remove: member removed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down,a,w40,a,w60` |
| tavern_inspect_prompt | tavern | Inspect: who? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40` |
| tavern_sheet_fighter | tavern | Character sheet (fighter) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60` |
| tavern_sheet_mage | tavern | Character sheet (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60` |
| tavern_sheet_spells | tavern | Character sheet: spells page (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60,a,w60` |
| tavern_sheet_items | tavern | Character sheet: items + action menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60` |
| tavern_item_equip | tavern | Items: equip, choose main weapon | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,a,w60` |
| tavern_item_give | tavern | Items: give to whom | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down,` |
| tavern_item_drop | tavern | Items: discard | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down*` |
| tavern_item_use | tavern | Items: use | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,a,w60,down,a,w60,down*` |
| tavern_sheet_pool | tavern | Character sheet: pool gold (gold 600) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*2,a,w40,down*4,a,w60,down*2,a,` |
| tavern_divide | tavern | Divide gold message | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,down*3,a,w60` |
| tavern_full | tavern | Add with full party: party is full | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,a,w60,a,w60` |
| tavern_empty_remove | tavern | Remove with no party | jp:yes | `boot,right*3,a,w60,down,a,w60` |
| shop_noparty | shop | Shop without a party | jp:yes | `boot,right*5,a,w60` |
| training_create_name_hira | training | Name entry, hiragana page | jp:yes | `boot,right,a,w60,a,w60` |
| training_create_name_kata | training | Name entry, katakana page | jp:yes | `boot,right,a,w60,a,w60,select,w40` |
| training_create_name_abc | training | Name entry, alphanumeric page | jp:yes | `boot,right,a,w60,a,w60,select,w40,select,w40` |
| training_create_name_typed | training | Name entry, a name typed | jp:yes | `boot,right,a,w60,a,w60,a,w40,a,w40` |
| training_create_gender | training | Choose sex | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60` |
| training_create_race | training | Choose race | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60` |
| training_create_align | training | Choose alignment | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60` |
| training_create_bonus | training | Distribute bonus points | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60` |
| training_create_bonusleft | training | Bonus points remain message | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,a,w60` |
| training_create_class | training | Choose class (bonus spent) | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,right*20,down,right*20,down,right*20,down,right*20,down,right*2` |
| training_create_confirm | training | Use this character? | jp:yes | `boot,right,a,w60,a,w60,a,w40,start,w60,a,w60,a,w60,a,w60,right*20,down,right*20,down,right*20,down,right*20,down,right*2` |
| training_view_list | training | View character: roster | jp:yes | `boot,right,a,w60,down,a,w60` |
| training_view_sheet | training | View character: sheet | jp:yes | `boot,right,a,w60,down,a,w60,a,w60` |
| training_view_spells | training | View character: spells (mage) | jp:yes | `boot,right,a,w60,down,a,w60,down*4,a,w60,a,w60` |
| training_delete_list | training | Delete character: roster | jp:yes | `boot,right,a,w60,down*2,a,w60` |
| training_delete_confirm | training | Delete character: confirm | jp:yes | `boot,right,a,w60,down*2,a,w60,a,w60` |
| training_rename | training | Rename: roster | jp:yes | `boot,right,a,w60,down*3,a,w60` |
| training_rename_entry | training | Rename: name entry | jp:yes | `boot,right,a,w60,down*3,a,w60,a,w60` |
| training_class_list | training | Change class: roster | jp:yes | `boot,right,a,w60,down*4,a,w60` |
| training_class_pick | training | Change class: classes | jp:yes | `boot,right,a,w60,down*4,a,w60,a,w60` |
| training_order | training | Reorder roster | jp:yes | `boot,right,a,w60,down*5,a,w60` |
| training_order_pick | training | Reorder roster: one picked | jp:yes | `boot,right,a,w60,down*5,a,w60,a,w60` |
| training_transfer | training | Character transfer | jp:yes | `boot,right,a,w60,down*6,a,w60` |
| training_transfer_start | training | Character transfer after START (no link partner) | jp:yes | `boot,right,a,w60,down*6,a,w60,start,w180` |
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
| temple_help | temple | Help (cure) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,a,w60` |
| temple_pickup | temple | Pick up | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,down,a,w60` |
| temple_deposit | temple | Deposit | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*3,a,w60,down*2,a,w60` |
| inn_who | inn | Inn entry | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60` |
| inn_stable | inn | Stables (free) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,a,w60` |
| inn_stable_3 | inn | Stables, after 2 | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,a,w60,a,w60,a,w60` |
| inn_cot | inn | Cot room | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down,a,w60` |
| inn_royal | inn | Royal suite | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down*4,a,w60` |
| inn_pool | inn | Pool gold | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down*5,a,w60` |
| notice_board | notice | Notice board text (one page; A returns to town) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right,a,w60` |
| museum_menu | museum | Museum: item room / monster room | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60` |
| outskirts_resume | maze | Edge of Town: resume adventure | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,down,a,w60` |
| outskirts_quit | maze | Edge of Town: quit adventure | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,down*2,a,w60` |
| outskirts_noparty | maze | Edge of Town without a party | jp:yes | `boot,a,w60` |
| camp_inspect_prompt | camp | Camp: inspect, who? | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40` |
| camp_sheet_mage | camp | Camp: character sheet (mage) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60` |
| camp_spells_mage | camp | Camp: mage spells page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60,a,` |
| camp_spell_cast | camp | Camp: mage spells, A on spell | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*4,a,w60,a,` |
| camp_spells_priest | camp | Camp: priest spells page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,down*3,a,w60,a,` |
| camp_items | camp | Camp: items + action menu | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down,a,w6` |
| camp_item_use | camp | Camp: use item | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down,a,w6` |
| camp_pool | camp | Camp: pool gold | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,a,w40,a,w60,down*2,a,` |
| camp_reorder | camp | Camp: reorder, empty slots | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down,a,w60` |
| camp_reorder_pick | camp | Camp: reorder, first placed | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down,a,w60,a,w40` |
| camp_equip | camp | Camp: equip | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60` |
| camp_equip_2 | camp | Camp: equip, next | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60,a,w60` |
| camp_equip_3 | camp | Camp: equip, next 2 | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,down*2,a,w60,a,w60,a,` |
| maze_reopen_camp | maze | B in the maze reopens Camp | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,b,w60` |
| maze_turn_left | maze | Maze view after turning left | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,left,w40` |
| maze_turn_right | maze | Maze view after turning right | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,right,w40` |
| maze_dmenu | maze | Dungeon menu (SELECT) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40` |
| maze_search | maze | Dungeon menu: search, nothing found | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,a,w6` |
| maze_picklock | maze | Dungeon menu: pick lock, no door | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| maze_findparty_none | maze | Dungeon menu: search for party, nobody | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| maze_settings | maze | Dungeon menu: settings | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,select,w40,down` |
| shop_buy_yes | shop | Buy: Yes - item bought | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60,a,w60,up,` |
| shop_buy_tooexpensive | shop | Buy: item the character cannot afford | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*2,a,w60,a,w60,a,w40,a,w60,down,a,w6` |
| inn_sleep | inn | Inn: character sleeping (cot) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60,down,a` |
| museum_item_room | museum | Museum: item room, categories and found/unfound counts | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60` |
| museum_item_list | museum | Museum: weapon list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,a,w60` |
| museum_item_info | museum | Museum: item data page | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,a,w60,a,w60` |
| museum_item_other | museum | Museum: other items list | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,a,w60,down*5,a,w60` |
| museum_monster_none | museum | Museum: monster room selected, no monsters met yet (A does nothing) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left,a,w60,down,w20,a,w60` |
| stairs_up_prompt | maze | Stairs up prompt (step back onto the entrance stairs) | jp:yes | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60,down,w60` |
| stairs_up_climb | maze | Stairs climbed: back in town | jp:no | `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,left*3,a,w60,a,w150,b,w60,up,w60,down,w60` |

## State-based shots (`states/`)

Not reproducible from power-on (random encounter / chest), so not in the shot list. Original ROM only; native 160x144 `states/<id>.jp.png` + `states/<id>.jp@3x.png`. Start state (gitignored, under `work/`) then the tokens (tools/emu.py syntax), then wait for a stable frame (same rule as shoot.py); a trailing `!` means captured right after the inputs (animated screen).
The states were made from power-on: `boot,PARTY,left*3,a,w60,a,w150` (camp) -> `b,w60` (mzbase) -> `work/triage/battle1/explore.py` seed 3 (encounter b1) -> fight -> chest.

| id | category | description | settled | state | tokens |
|---|---|---|---|---|---|
| maze_findparty_busy | maze | Dungeon menu: search for party, searching... (animated) | timed | `work/shots/jp_tour/explore/mzbase.state` | `select,w40,down*2,a!` |
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
| chest_menu | chest | Chest menu (inspect/cast/disarm/open/leave) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60` |
| chest_inspect_who | chest | Chest: who inspects? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,a,w40` |
| chest_inspect_result | chest | Chest: inspect result (trap guess) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,a,w40,a,w60` |
| chest_cast_who | chest | Chest: who casts? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down,w30,a,w40` |
| chest_cast_list | chest | Chest: spell list of the caster | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down,w30,a,w40,a,w60` |
| chest_disarm_who | chest | Chest: who disarms? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40` |
| chest_disarm_traps | chest | Chest: trap name list | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40,a,w60` |
| chest_disarm_result | chest | Chest: disarm result (no trap, item found) | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*2,w30,a,w40,a,w60,a,w60` |
| chest_open_who | chest | Chest: who opens? | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*3,w30,a,w40` |
| chest_open_result | chest | Chest: opened, gold shared | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*3,w30,a,w40,a,w60` |
| chest_leave | chest | Chest: leave without opening | yes | `work/shots/jp_tour/explore/bchest.state` | `a,w60,down*4,w30,a,w60` |
