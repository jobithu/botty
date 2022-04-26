from d2r_image.data_models import ItemQuality, ItemQualityKeyword


NIP_RE_PATTERNS = {}
NIP_PATTERNS = {}

NTIP_ALIAS_QUALITY_MAP = {
    ItemQualityKeyword.LowQuality.value: 1,
    ItemQualityKeyword.Crude.value: 1,
    ItemQualityKeyword.Cracked.value: 1,
    ItemQuality.Gray.value: 2,
    ItemQuality.Normal.value: 2,
    ItemQualityKeyword.Superior.value: 3,
    ItemQuality.Magic.value: 4,
    ItemQuality.Set.value: 5,
    ItemQuality.Rare.value: 6,
    ItemQuality.Unique.value: 7,
    ItemQuality.Crafted.value: 8,
    ItemQuality.Runeword.value: 9,
    ItemQuality.Rune.value: 10,
}

NIP_ALIAS_STAT_PATTERNS = {
    "Adds {:d}-{:d} cold damage": [
        "54",
        "55"
    ],
    "Adds {:d}-{:d} damage": [
        "21",
        "22"
    ],
    "Adds {:d}-{:d} fire damage": [
        "48",
        "49"
    ],
    "Adds {:d}-{:d} lightning damage": [
        "50",
        "51"
    ],
    "Adds {:d}-{:d} magic damage": [
        "52",
        "53"
    ],
    "Adds {:d}-{:d} poison damage over {:d} seconds": [
        "57",
        "58",
		"59"
    ],
    "All Resistances {:d}": [
        ["39", "41", "43", "45"]
    ],
    "Attacker Takes Damage of {:d}": [
        "78"
    ],
    "Attacker Takes Damage of {:d} (Based on Character Level)": [
        "238"
    ],
    "Attacker Takes Lightning Damage of {:d}": [
        "128"
    ],
    "Cannot Be Frozen": [
        "153"
    ],
    "Cold Absorb {:d}": [
        "148",
    ],
    "Cold Resist {:d}": [
        "43"
    ],
    "Cold Resist {:d} (Based on Character Level)": [
        "230"
    ],
    "Damage Reduced by {:d}": [
        "34"
    ],
    "Damage Reduced by {:d}": [
        "36"
    ],
    "Damage {:d}": [
        "111"
    ],
    "Defense: {:d}": [
        "31"
    ],
    "Durability: {:d} of {:d}": [
        "72",
        "73"
    ],
    "Ethereal (Cannot be Repaired)": [
        "0x400000"
    ],
    "Extra Gold from Monsters {:d}": [
        "79"
    ],
    "Fire Absorb {:d}": [
        "142"
    ],
    "Fire Resist {:d}": [
        "39"
    ],
    "Fire Resist {:d} (Based on Character Level)": [
        "231"
    ],
    "Fires Explosive Arrows or Bolts": [
        "158"
    ],
    "Fires Magic Arrows": [
        "157"
    ],
    "Freezes target {:d}": [
        "134"
    ],
    "Half Freeze Duration": [
        "118"
    ],
    "Heal Stamina Plus {:d}": [
        "28"
    ],
    "Heal Stamina Plus {:d} (Based on Character Level)": [
        "241"
    ],
    "Hit Blinds Target {:d}": [
        "113"
    ],
    "Hit Causes Monster to Flee {:d}": [
        "112"
    ],
    "Ignore Target's Defense": [
        "116"
    ],
    "Increase Maximum Durability {:d}": [
        "75"
    ],
    "Increase Maximum Life {:d}": [
        "76"
    ],
    "Increase Maximum Mana {:d}": [
        "77"
    ],
    "Increased Stack Size": [
        "254"
    ],
    "Knockback": [
        "81"
    ],
    "Level {:d} {} ({:d}/{:d} Charges)": [
        "204"
    ],
    "Level {:d} {} Aura When Equipped": [
        "151"
    ],
    "Lightning Absorb {:d}": [
        "144"
    ],
    "Lightning Resist {:d}": [
        "41"
    ],
    "Lightning Resist {:d} (Based on Character Level)": [
        "232"
    ],
    "Magic Absorb {:d}": [
        "146"
    ],
    "Magic Damage Reduced by {:d}": [
        "35"
    ],
    "Magic Resist {:d}": [
        "37"
    ],
    "One-Hand Damage: {:d} to {:d}": [
        "21",
		"22"
    ],
    "{:d} Piercing Attack": [
        "156"
    ],
    "Poison Length Reduced by {:d}": [
        "110"
    ],
    "Poison Resist {:d}": [
        "45"
    ],
    "Poison Resist {:d} (Based on Character Level)": [
        "233"
    ],
    "Prevent Monster Heal": [
        "117"
    ],
    "Reduces all Vendor Prices {:d}": [
        "87"
    ],
    "Regenerate Mana {:d}": [
        "27"
    ],
    "Repairs {:d} durability {:d}": [
        "252"
    ],
    "Replenish Life {:d}": [
        "74"
    ],
    "Replenishes quantity": [
        "253"
    ],
    "Requirements {:d}": [
        "91"
    ],
    "Slain Monsters Rest in Peace": [
        "108"
    ],
    "Slows Target by {:d}": [
        "150"
    ],
    "Socketed ({:d})": [
        "194"
    ],
    "Throwable": [
        "125"
    ],
    "Two-Hand Damage: {:d} to {:d}": [
        "21",
		"22"
    ],
    "{:d} Absorbs Cold Damage": [
        "149",
    ],
    "{:d} Absorbs Cold Damage (Based on Character Level)": [
        "234"
    ],
    "{:d} Absorbs Fire Damage": [
        "143"
    ],
    "{:d} Absorbs Fire Damage (Based on Character Level)": [
        "235"
    ],
    "{:d} Absorbs Lightning Damage": [
        "145"
    ],
    "{:d} Absorbs Lightning Damage (Based on Character Level)": [
        "236"
    ],
    "{:d} Better Chance of Getting Magic Items": [
        "293"
    ],
    "{:d} Bonus to Attack Rating": [
        "279"
    ],
    "{:d} Chance of Crushing Blow": [
        "136"
    ],
    "{:d} Chance of Open Wounds": [
        "135"
    ],
    "{:d} Cold Absorb": [
        "149"
    ],
    "{:d} Damage to Demons": [
        "121"
    ],
    "{:d} Damage to Undead": [
        "122"
    ],
    "{:d} Deadly Strike": [
        "141"
    ],
    "{:d} Defense": [
        "31"
    ],
    "{:d} Defense (Based on Character Level)": [
        "214"
    ],
    "{:d} Defense vs. Melee": [
        "33"
    ],
    "{:d} Defense vs. Missile": [
        "32"
    ],
    "{:d} Enhanced Maximum Damage": [
        "219"
    ],
    "{:d} Fire Absorb": [
        "143"
    ],
    "{:d} Kick Damage": [
        "137"
    ],
    "{:d} Kick Damage (Based on Character Level)": [
        "249"
    ],
    "{:d} Life after each Demon Kill": [
        "139"
    ],
    "{:d} Life after each Kill": [
        "86"
    ],
    "{:d} Lightning Absorb": [
        "145"
    ],
    "{:d} Magic Absorb": [
        "147"
    ],
    "{:d} Maximum Stamina": [
        "11"
    ],
    "{:d} Maximum Stamina (Based on Character Level)": [
        "242"
    ],
    "{:d} cold damage": [
        "54"
    ],
    "{:d} damage": [
        "21"
    ],
    "{:d} fire damage": [
        "48"
    ],
    "{:d} lightning damage": [
        "50"
    ],
    "{:d} magic damage": [
        "52"
    ],
    "{:d} poison damage over {:d} seconds": [
        "57",
        "59"
    ],
    "{:d} to All Skills": [
        "127"
    ],
    "{:d} to Amazon Skill Levels": [
        "83,0"
    ],
    "{:d} to Assassin Skill Levels": [
        "83,6"
    ],
    "{:d} to Attack Rating": [
        "19"
    ],
    "{:d} to Attack Rating (Based on Character Level)": [
        "224"
    ],
    "{:d} to Attack Rating against Demons": [
        "123"
    ],
    "{:d} to Attack Rating against Demons (Based on Character Level)": [
        "245"
    ],
    "{:d} to Attack Rating against Undead": [
        "124"
    ],
    "{:d} to Attack Rating against Undead (Based on Character Level)": [
        "246"
    ],
    "{:d} to Attack Rating versus {}": [
        "180"
    ],
    "{:d} to Barbarian Skill Levels": [
        "83,4"
    ],
    "{:d} to Dexterity": [
        "2"
    ],
    "{:d} to Dexterity (Based on Character Level)": [
        "221"
    ],
    "{:d} to Druid Skill Levels": [
        "83,5"
    ],
    "{:d} to Energy": [
        "1"
    ],
    "{:d} to Energy (Based on Character Level)": [
        "222"
    ],
    "{:d} to Fire Skills": [
        "188"
    ],
    "{:d} to Life": [
        "7"
    ],
    "{:d} to Life (Based on Character Level)": [
        "216"
    ],
    "{:d} to Light Radius": [
        "89"
    ],
    "{:d} to Mana": [
        "9"
    ],
    "{:d} to Mana (Based on Character Level)": [
        "217"
    ],
    "{:d} to Mana after each Kill": [
        "138"
    ],
    "{:d} to Maximum Cold Damage": [
        "55"
    ],
    "{:d} to Maximum Cold Damage (Based on Character Level)": [
        "226"
    ],
    "{:d} to Maximum Damage": [
        "22"
    ],
    "{:d} to Maximum Damage (Based on Character Level)": [
        "218"
    ],
    "{:d} to Maximum Fire Damage": [
        "49"
    ],
    "{:d} to Maximum Fire Damage (Based on Character Level)": [
        "227"
    ],
    "{:d} to Maximum Lightning Damage": [
        "51"
    ],
    "{:d} to Maximum Lightning Damage (Based on Character Level)": [
        "228"
    ],
    "{:d} to Maximum Poison Damage": [
        "58"
    ],
    "{:d} to Maximum Poison Damage (Based on Character Level)": [
        "229"
    ],
    "{:d} to Minimum Cold Damage": [
        "54"
    ],
    "{:d} to Minimum Fire Damage": [
        "48"
    ],
    "{:d} to Minimum Lightning Damage": [
        "50"
    ],
    "{:d} to Minimum Poison Damage": [
        "57"
    ],
    "{:d} to Monster Defense Per Hit": [
        "120"
    ],
    "{:d} to Necromancer Skill Levels": [
        "83,2"
    ],
    "{:d} to Paladin Skill Levels": [
        "83,3"
    ],
    "{:d} to Sorceress Skill Levels": [
        "83,1"
    ],
    "{:d} to Strength": [
        "0"
    ],
    "{:d} to Strength (Based on Character Level)": [
        "220"
    ],
    "{:d} to Vitality": [
        "3"
    ],
    "{:d} to Vitality (Based on Character Level)": [
        "223"
    ],
    "{:d} to all Attributes": [
        ["0","1","2","3"]
    ],
    # "{:d} to {}": [
    #     "97"
    # ],
    "{:d} to Bow and Crossbow Skills (Amazon only)": [
        "188,0"
    ],
    "{:d} to Passive Skills (Amazon only)": [
        "188,1"
    ],
    "{:d} to Javelin and Spear Skills (Amazon only)": [
        "188,2"
    ],
    "{:d} to Fire Skills (Sorceress only)": [
        "188,8"
    ],
    "{:d} to Lightning Skills (Sorceress only)": [
        "188,9"
    ],
    "{:d} to Cold Skills (Sorceress only)": [
        "188,10"
    ],
    "{:d} to Curses (Necromancer only)": [
        "188,16"
    ],
    "{:d} to Poison and Bone Skills (Necromancer only)": [
        "188,17"
    ],
    "{:d} to Summoning Skills (Necromancer only)": [
        "188,18"
    ],
    "{:d} to Combat Skills (Paladin only)": [
        "188,24"
    ],
    "{:d} to Offensive Aura Skills (Paladin only)": [
        "188,25"
    ],
    "{:d} to Defensive Aura Skills (Paladin only)": [
        "188,26"
    ],
    "{:d} to Combat Skills (Barbarian only)": [
        "188,32"
    ],
    "{:d} to Masteries (Barbarian only)": [
        "188,33"
    ],
    "{:d} to Warcries (Barbarian only)": [
        "188,34"
    ],
    "{:d} to Summoning Skills (Druid only)": [
        "188,40"
    ],
    "{:d} to Shape Shifting Skills (Druid only)": [
        "188,41"
    ],
    "{:d} to Elemental Skills (Druid only)": [
        "188,42"
    ],
    

    "{:d} to Bash (Barbarian only)": [
    "107,126"
],
# "{:d} to Sword Mastery (Barbarian only)": [
#     "107,127" 
#],
# "{:d} to Axe Mastery (Barbarian only)": [
#     "107,128" 
#],
# "{:d} to Mace Mastery (Barbarian only)": [
#     "107,129" 
#],
#"{:d} to General Mastery (Barbarian only)": [],
"{:d} to Howl (Barbarian only)": [
    "107,130"
],
"{:d} to Find Potion (Barbarian only)": [
    "107,131"
],
"{:d} to Leap (Barbarian only)": [
    "107,132"
],
"{:d} to Double Swing (Barbarian only)": [
    "107,133"
],
"{:d} to Polearm and Spear Mastery (Barbarian only)": [
    "107,134"
],
#"{:d} to Throwing Mastery (Barbarian only)": [
#     "107,135"
#],
#"{:d} to Spear Mastery (Barbarian only)": [
#     "107,136"
"{:d} to Taunt (Barbarian only)": [
    "107,137"
],
"{:d} to Shout (Barbarian only)": [
    "107,138"
],
"{:d} to Stun (Barbarian only)": [
    "107,139"
],
"{:d} to Double Throw (Barbarian only)": [
    "107,140"
],
#"{:d} to Combat Reflexes (Barbarian only)": [],
#"{:d} to Increased Stamina (Barbarian only)": [
#     "107,141"
#],
"{:d} to Find Item (Barbarian only)": [
    "107,142"
],
"{:d} to Leap Attack (Barbarian only)": [
    "107,143"
],
"{:d} to Concentrate (Barbarian only)": [
    "107,144"
],
"{:d} to Iron Skin (Barbarian only)": [
    "107,145"
],
"{:d} to Battle Cry (Barbarian only)": [
    "107,146"
],
"{:d} to Frenzy (Barbarian only)": [
    "107,147"
],
"{:d} to Increased Speed (Barbarian only)": [
    "107,148"
],
"{:d} to Battle Orders (Barbarian only)": [
    "107,149"
],
"{:d} to Grim Ward (Barbarian only)": [
    "107,150"
],
"{:d} to Whirlwind (Barbarian only)": [
    "107,151"
],
"{:d} to Berserk (Barbarian only)": [
    "107,152"
],
"{:d} to Natural Resistance (Barbarian only)": [
    "107,153"
],
"{:d} to War Cry (Barbarian only)": [
    "107,154"
],
"{:d} to Battle Command (Barbarian only)": [
    "107,155"
],
"{:d} to Raven (Druid only)": [
    "107,221"
],
"{:d} to Poison Creeper (Druid only)": [
    "107,222"
],
"{:d} to Werewolf (Druid only)": [
    "107,223"
],
"{:d} to Lycanthropy (Druid only)": [
    "107,224"
],
"{:d} to Firestorm (Druid only)": [
    "107,225"
],
"{:d} to Oak Sage (Druid only)": [
    "107,226"
],
"{:d} to Summon Spirit Wolf (Druid only)": [
    "107,227"
],
"{:d} to Werebear (Druid only)": [
    "107,228"
],
"{:d} to Molten Boulder (Druid only)": [
    "107,229"
],
"{:d} to Arctic Blast (Druid only)": [
    "107,230"
],
"{:d} to Fissure (Druid only)": [
    "107,231"
],
"{:d} to Feral Rage (Druid only)": [
    "107,232"
],
"{:d} to Maul (Druid only)": [
    "107,233"
],
"{:d} to Carrion Vine (Druid only)": [ 
    "107,234"
],
"{:d} to Cyclone Armor (Druid only)": [ 
    "107,235"
],
"{:d} to Heart of Wolverine (Druid only)": [ 
    "107,236"
],
"{:d} to Summon Dire Wolf (Druid only)": [ 
    "107,237"
],
"{:d} to Rabies (Druid only)": [ 
    "107,238"
],
"{:d} to Fire Claws (Druid only)": [ 
    "107,239"
],
"{:d} to Twister (Druid only)": [ 
    "107,240"
],
"{:d} to Solar Creeper (Druid only)": [ 
    "107,241"
],
"{:d} to Hunger (Druid only)": [ 
    "107,242"
],
"{:d} to Shock Wave (Druid only)": [ 
    "107,243"
],
"{:d} to Volcano (Druid only)": [ 
    "107,244"
],
"{:d} to Tornado (Druid only)": [ 
    "107,245"
],
"{:d} to Spirit of Barbs (Druid only)": [ 
    "107,246"
],
"{:d} to Summon Grizzly (Druid only)": [ 
    "107,247"
],
"{:d} to Fury (Druid only)": [ 
    "107,248"
],
"{:d} to Armageddon (Druid only)": [ 
    "107,249"
],
"{:d} to Hurricane (Druid only)": [ 
    "107,250"
],
#"{:d} to Gust": [],
"{:d} to Fire Blast (Assassin only)": [ 
    "107,251"
],
"{:d} to Claw Mastery (Assassin only)": [ 
    "107,252"
],
"{:d} to Psychic Hammer (Assassin only)": [ 
    "107,253"
],
"{:d} to Tiger Strike (Assassin only)": [ 
    "107,254"
],
"{:d} to Dragon Talon (Assassin only)": [ 
    "107,255"
],
"{:d} to Shock Web (Assassin only)": [ 
    "107,256"
],
"{:d} to Blade Sentinel (Assassin only)": [ 
    "107,257"
],
"{:d} to Burst of Speed (Assassin only)": [ 
    "107,258"
],
"{:d} to Fists of Fire (Assassin only)": [ 
    "107,259"
],
"{:d} to Dragon Claw (Assassin only)": [ 
    "107,260"
],
"{:d} to Charged Bolt Sentry (Assassin only)": [ 
    "107,261"
],
"{:d} to Wake of Fire (Assassin only)": [ 
    "107,262"
],
"{:d} to Weapon Block (Assassin only)": [ 
    "107,263"
],
"{:d} to Cloak of Shadows (Assassin only)": [ 
    "107,264"
],
"{:d} to Cobra Strike (Assassin only)": [ 
    "107,265"
],
"{:d} to Blade Fury (Assassin only)": [ 
    "107,266"
],
"{:d} to Fade (Assassin only)": [ 
    "107,267"
],
"{:d} to Shadow Warrior (Assassin only)": [ 
    "107,268"
],
"{:d} to Claws of Thunder (Assassin only)": [ 
    "107,269"
],
"{:d} to Dragon Tail (Assassin only)": [ 
    "107,270"
],
"{:d} to Chain Lightning Sentry (Assassin only)": [ 
    "107,271"
],
"{:d} to Wake of Inferno (Assassin only)": [ 
    "107,272"
],
"{:d} to Mind Blast (Assassin only)": [ 
    "107,273"
],
"{:d} to Blades of Ice (Assassin only)": [ 
    "107,274"
],
"{:d} to Dragon Flight (Assassin only)": [ 
    "107,275"
],
"{:d} to Death Sentry (Assassin only)": [ 
    "107,276"
],
"{:d} to Blade Shield (Assassin only)": [ 
    "107,277"
],
"{:d} to Venom (Assassin only)": [ 
    "107,278"
],
"{:d} to Shadow Master (Assassin only)": [ 
    "107,279"
],
"{:d} to Phoenix Strike (Assassin only)": [ 
    "107,280"
],
#"{:d} to Lightning Sentry (Assassin only)": [],
#"{:d} to Wake Of Destruction Sentry (Assassin only)": [],
#"{:d} to Blink (Assassin only)": [],
#"{:d} to Inferno Sentry (Assassin only)": [],
#"{:d} to Death Sentry (Assassin only)": [],
#"{:d} to Sentry Lightning (Assassin only)": [],

    
    "{:d} to Traps (Assassin only)": [
        "188,48"
    ],
    "{:d} to Shadow Disciplines (Assassin only)": [
        "188,49"
    ],
    "{:d} to Martial Arts (Assassin only)": [
        "188,50"
    ],
    "{:d} to Amazon Skill Levels": [
        "83,0"
    ],
    "{:d} to Sorceress Skill Levels": [
        "83,1"
    ],
    "{:d} to Necromancer Skill Levels": [
        "83,2"
    ],
    "{:d} to Paladin Skill Levels": [
        "83,3"
    ],
    "{:d} to Barbarian Skill Levels": [
        "83,4"
    ],
    "{:d} to Druid Skill Levels": [
        "83,5"
    ],
    "{:d} to Assassin Skill Levels": [
        "83,6"
    ],
    "{:d} Better Chance of Getting Magic Items": [
        "80"
    ],
    "{:d} Better Chance of Getting Magic Items (Based on Character Level)": [
        "240"
    ],
    "{:d} Bonus to Attack Rating": [
        "119"
    ],
    "{:d} Bonus to Attack Rating (Based on Character Level)": [
        "225"
    ],
    "{:d} Chance of Crushing Blow": [
        "136"
    ],
    "{:d} Chance of Crushing Blow (Based on Character Level)": [
        "247"
    ],
    "{:d} Chance of Open Wounds": [
        "135"
    ],
    "{:d} Chance of Open Wounds (Based on Character Level)": [
        "248"
    ],
    "{:d} Chance to cast level {:d} {} on attack": [
        "195"
    ],
    "{:d} Chance to cast level {:d} {} on striking": [
        "196"
    ],
    "{:d} Chance to cast level {:d} {} when struck": [
        "201"
    ],
    "{:d} Chance to cast level {:d} {} when you Die": [
        "197"
    ],
    "{:d} Chance to cast level {:d} {} when you Kill an Enemy": [
        "196"
    ],
    "{:d} Chance to cast level {:d} {} when you Level-Up": [
        "199"
    ],
    "{:d} Damage Taken Goes To Mana": [
        "114"
    ],
    "{:d} Damage to Demons": [
        "121"
    ],
    "{:d} Damage to Demons (Based on Character Level)": [
        "dmg-dem/lvl",
        "item_damage_demon_perlevel",
        "243"
    ],
    "{:d} Damage to Undead": [
        "122"
    ],
    "{:d} Damage to Undead (Based on Character Level)": [
        "244"
    ],
    "{:d} Deadly Strike": [
        "141"
    ],
    "{:d} Deadly Strike (Based on Character Level)": [
        "250"
    ],
    "{:d} Enhanced Defense": [
        "16"
    ],
    "{:d} Enhanced Defense (Based on Character Level)": [
        "215"
    ],
    "{:d} Enhanced Maximum Damage (Based on Character Level)": [
        "219"
    ],
    "{:d} Enhanced damage": [
        "18"
    ],
    "{:d} Extra Gold from Monsters": [
        "79"
    ],
    "{:d} Extra Gold from Monsters (Based on Character Level)": [
        "239"
    ],
    "{:d} Faster Block Rate": [
        "102"
    ],
    "{:d} Faster Cast Rate": [
        "105"
    ],
    "{:d} Faster Hit Recovery": [
        "99"
    ],
    "{:d} Faster Run/Walk": [
        "96"
    ],
    "{:d} Increased Attack Speed": [
        "93"
    ],
    "{:d} Increased Chance of Blocking": [
        "20"
    ],
    "{:d} Life stolen per hit": [
        "60"
    ],
    "{:d} Mana stolen per hit": [
        "62"
    ],
    "{:d} Reanimate as: {}": [
        "155"
    ],
    "{:d} Slower Stamina Drain": [
        "154"
    ],
    "{:d} Target Defense": [
        "116"
    ],
    "{:d} to Cold Skill Damage": [
        "331"
    ],
    "{:d} to Enemy Cold Resistance": [
        "335"
    ],
    "{:d} to Enemy Fire Resistance": [
        "333"
    ],
    "{:d} to Enemy Lightning Resistance": [
        "334"
    ],
    "{:d} to Enemy Poison Resistance": [
        "336"
    ],
    "{:d} to Experience Gained": [
        "85"
    ],
    "{:d} to Fire Skill Damage": [
        "329"
    ],
    "{:d} to Lightning Skill Damage": [
        "330"
    ],
    "{:d} to Maximum Cold Resist": [
        "44"
    ],
    "{:d} to Maximum Fire Resist": [
        "40"
    ],
    "{:d} to Maximum Lightning Resist": [
        "42"
    ],
    "{:d} to Maximum Magic Resist": [
        "38"
    ],
    "{:d} to Maximum Poison Resist": [
        "46"
    ],
    "{:d} to Poison Skill Damage": [
        "332"
    ]
}