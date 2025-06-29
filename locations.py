import random
from enemies import Enemy, TheCount, TheBride
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
CRIMSON_CASTLE = "crimson_castle"
CHAPEL = "chapel"
BATTLE = "battle"


location_enemies = {
    CEMETERY: [
        Enemy("Skeleton", 8, 2, "skeleton.jpg",
              random.randint(1, 2), 10),
        Enemy("Gravedigger", 9, 3, "gravedigger.jpg",
              random.randint(3, 5), 20),
        Enemy("Zombie", 10, 4, "zombie.jpg",
              random.randint(3, 5), 20, [health_potion]),
        Enemy("Witch of the Ravens", 12, 5, "raven_witch.jpg",
              random.randint(8, 10), 100, bloodstone=1),
    ],

    DARK_FOREST: [
        Enemy("Dark fairy", 20, 5, "dark_fairy.jpg",
              random.randint(5, 8), 80),
        Enemy("Assassin", 22, 6, "assassin.jpg",
              random.randint(5, 8), 100),
        Enemy("Werewolf", 25, 7, "werewolf.jpg",
              random.randint(8, 10), 120, [health_potion]),
        Enemy("Witch of Skulls", 30, 9, "dark_witch.jpg",
              random.randint(10, 15), 150, bloodstone=1),
    ],

    HAUNTED_RUIN: [
        Enemy("Wraith", 40, 8, "wraith.jpg",
              random.randint(8, 10), 120),
        Enemy("Skeleton Sentinel", 45, 9, "skeleton_sentinel.jpg",
              random.randint(10, 12), 150),
        Enemy("Death Knight", 50, 10, "death_knight.jpg",
              random.randint(10, 12), 180, [health_potion]),
        Enemy("Wraith Lord", 60, 12, "wraith_lord.jpg",
              random.randint(12, 15), 200, bloodstone=1)
    ],

    ENCHANTED_FOREST: [
        Enemy("Fairy", 70, 10, "fairy.jpg",
              random.randint(12, 15), 180),
        Enemy("Elk", 80, 12, "elk.jpg",
              random.randint(12, 15), 220),
        Enemy("Dryad", 90, 14, "dryad.jpg",
              random.randint(15, 18), 250, [health_potion]),
        Enemy("Lady of the Forests", 100, 16, "fairy_druid.jpg",
              random.randint(20, 25), 300, bloodstone=1)
    ],

    FROSTFANG_PEAK: [
        Enemy("Ice Wolf", 100, 15, "wolf.jpg",
              random.randint(15, 20), 270),
        Enemy("Frost Wraith", 110, 16, "frost_wraith.jpg",
              random.randint(15, 20), 320),
        Enemy("Ice Golem", 120, 18, "ice_golem.jpg",
              random.randint(18, 25), 350, [health_potion]),
        Enemy("Frost Dragon", 130, 20, "frost_dragon.jpg",
              random.randint(25, 30), 400, bloodstone=1)
    ],

    SUNKEN_TEMPLE: [
        Enemy("Mermaid", 130, 18, "mermaid.jpg",
              random.randint(20, 25), 370),
        Enemy("Coral Golem", 110, 20, "coral_golem.jpg",
              random.randint(20, 25), 420),
        Enemy("Giant Squid", 140, 23, "squid.jpg",
              random.randint(25, 30), 450, [health_potion]),
        Enemy("Deepsea Horror", 160, 25, "deepsea_horror.jpg",
              random.randint(35, 40), 500, bloodstone=1)
    ],

    CRIMSON_CASTLE: [
        Enemy("Sangromancer", 160, 22, "sangromancer.jpg",
              random.randint(25, 30), 450),
        Enemy("Vampire Knight", 170, 24, "vampire_knight.jpg",
              random.randint(30, 35), 500, [health_potion]),
        TheBride("Linda Nocturne", 180, 27, "bride.jpg",
              random.randint(50, 50), 700),
        TheCount("Victor Nocturne", 200, 30, "count.jpg",
              random.randint(100, 100), 1000)
    ]
 }


