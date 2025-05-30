import random
from enemies import Enemy, TheCount
from items import *


# Game statuses
MENU = "menu"
CHARACTER_SELECT = "character_select"
TOWN = "town"
CONFIRM_EXIT = "confirm_exit"
NAME_INPUT = "name_input"
PROFILE = "profile"
ALCHEMIST_LABORATORY = "alchemist_laboratory"
BLACKSMITH = "blacksmith"
TAVERN = "tavern"
EXPLORE = "explore"
AUDIO = "audio"
CEMETERY = "cemetery"
ENCHANTED_FOREST = "enchanted_forest"
HAUNTED_RUIN = "haunted_ruin"
DARK_FOREST = "dark_forest"
FROSTFANG_PEAK = "frostfang_peak"
SUNKEN_TEMPLE = "sunken_temple"
CHAPEL = "chapel"
BATTLE = "battle"


location_enemies = {
    CEMETERY: [
        Enemy("Skeleton", 100, 5, "skeleton.jpg",
              random.randint(1, 3), 60, [health_potion]),
        Enemy("Gravedigger", 10, 2, "gravedigger.jpg",
              random.randint(4, 7), 300, [mana_potion]),
        Enemy("Zombie", 10, 5, "zombie.jpg",
              random.randint(8, 10), 500),
        Enemy("Witch of the Ravens", 10, 5, "raven_witch.jpg",
              random.randint(20, 20), 1000),
    ],
    DARK_FOREST: [
        Enemy("Dark fairy", 10, 5, "dark_fairy.jpg",
              random.randint(15, 15), 800),
        Enemy("Assassin", 10, 5, "assassin.jpg",
              random.randint(16, 19), 900),
        Enemy("Werewolf", 10, 5, "werewolf.jpg",
              random.randint(20, 23), 1000),
        Enemy("Witch of Skulls", 10, 5, "dark_witch.jpg",
              random.randint(30, 30), 1500),
    ],
    HAUNTED_RUIN: [
        Enemy("Wraith", 100, 15, "wraith.jpg",
              random.randint(25, 28), 900),
        Enemy("Skeleton Sentinel", 80, 10, "skeleton_sentinel.jpg",
              random.randint(29, 32), 1200),
        Enemy("Death Knight", 90, 12, "death_knight.jpg",
              random.randint(33, 37), 1400),
        Enemy("Wraith Lord", 120, 18, "wraith_lord.jpg",
              random.randint(40, 40), 2000)
    ],
    ENCHANTED_FOREST: [
        Enemy("Fairy", 100, 15, "fairy.jpg",
              random.randint(35, 38), 1800),
        Enemy("Elk", 80, 10, "elk.jpg",
              random.randint(38, 41), 2200),
        Enemy("Dryad", 90, 12, "dryad.jpg",
              random.randint(42, 46), 2800),
        Enemy("Lady of the Forests", 120, 18, "fairy_druid.jpg",
              random.randint(50, 50), 3000)
    ],
    FROSTFANG_PEAK: [
        Enemy("Ice Wolf", 110, 16, "wolf.jpg",
              random.randint(45, 48), 2700),
        Enemy("Frost Wraith", 100, 14, "frost_wraith.jpg",
              random.randint(52, 55), 3200),
        Enemy("Ice Golem", 95, 13, "ice_golem.jpg",
              random.randint(55, 58), 3500),
        Enemy("Frost Dragon", 130, 20, "frost_dragon.jpg",
              random.randint(70, 70), 4000)
    ],
    SUNKEN_TEMPLE: [
        Enemy("Mermaid", 110, 16, "mermaid.jpg",
              random.randint(60, 65), 3700),
        Enemy("Coral Golem", 100, 14, "coral_golem.jpg",
              random.randint(66, 70), 4200),
        Enemy("Giant Squid", 95, 13, "squid.jpg",
              random.randint(72, 75), 4500),
        Enemy("Deepsea Horror", 130, 20, "deepsea_horror.jpg",
              random.randint(100, 100), 5000)
    ]
 }


