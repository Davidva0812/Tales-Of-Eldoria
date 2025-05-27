from locations import *
from utils import resource_path


pygame.init()
pygame.mixer.init()


infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

clock = pygame.time.Clock()
pygame.display.set_caption("Fantasy RPG Game")
pygame.mouse.set_visible(False)  # Hide mouse button


# Sounds
volume_level = 0.7  # Starter volume
# Town music
pygame.mixer.music.load(resource_path("assets/sounds/Exploration.mp3"))
pygame.mixer.music.set_volume(volume_level)  # sound volume 0.1-1
pygame.mixer.music.play(-1)  # Infinite repeat
# Map music
adventure_channel = pygame.mixer.Channel(1)
adventure_theme = pygame.mixer.Sound(resource_path("assets/sounds/New_sunrise.wav"))
adventure_theme.set_volume(volume_level)
# Music for the different locations
location_channel = pygame.mixer.Channel(2)
cemetery_theme = pygame.mixer.Sound(resource_path("assets/sounds/rpgcavespooky.ogg"))
cemetery_theme.set_volume(volume_level)
dark_forest_theme = pygame.mixer.Sound(resource_path("assets/sounds/GameMusic_ForestTheme_24.mp3"))
dark_forest_theme.set_volume(volume_level)
haunted_ruin_theme = pygame.mixer.Sound(resource_path("assets/sounds/Kokopelli's Graveyard.mp3"))
haunted_ruin_theme.set_volume(volume_level)
enchanted_forest_theme = pygame.mixer.Sound(resource_path("assets/sounds/beautiful_forest_16bit_44.1khz.ogg"))
enchanted_forest_theme.set_volume(volume_level)
frostfang_peak_theme = pygame.mixer.Sound(resource_path("assets/sounds/cold_hands.ogg"))
frostfang_peak_theme.set_volume(volume_level)
sunken_temple_theme = pygame.mixer.Sound(resource_path("assets/sounds/Mysterious.mp3"))
sunken_temple_theme.set_volume(volume_level)
# Battle music
battle_channel = pygame.mixer.Channel(3)
battle_theme = pygame.mixer.Sound(resource_path("assets/sounds/battle_theme.mp3"))
battle_theme.set_volume(volume_level)
# Chapel music
chapel_channel = pygame.mixer.Channel(4)
chapel_theme = pygame.mixer.Sound(resource_path("assets/sounds/cathedral.wav"))
chapel_theme.set_volume(volume_level)
# Die sound
die_channel = pygame.mixer.Channel(5)
die_theme = pygame.mixer.Sound(resource_path("assets/sounds/ghost.wav"))
die_theme.set_volume(volume_level)
# Mouse clicking sound
click_sound = pygame.mixer.Sound(resource_path("assets/sounds/mouseclick.wav"))
click_sound.set_volume(volume_level)


music_tracks = {
    CEMETERY: cemetery_theme,
    DARK_FOREST: dark_forest_theme,
    HAUNTED_RUIN: haunted_ruin_theme,
    ENCHANTED_FOREST: enchanted_forest_theme,
    FROSTFANG_PEAK: frostfang_peak_theme,
    SUNKEN_TEMPLE: sunken_temple_theme
}


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 7, 179)
LIGHT_BLUE = (0, 79, 153)
GRAY = (181, 181, 181)
DARK_GREY = (135, 132, 132)
GREEN = (0, 135, 27)
DARK_GREEN = (1, 79, 16)
RED = (181, 2, 17)
BROWN = (163, 83, 8)
IVORY = (255,248,220)
GOLD = (181, 146, 31)
DARK_BROWN = (107, 4, 27)
LIGHT_BROWN = (200, 150, 50)
DARKER_GREY = (96, 99, 95)
ORANGE = (252, 114, 0)
MESSAGE_LIFETIME = 2500  # 2.5 sec
MAX_NAME_LENGTH = 12
# Grid options
GRID_SIZE = 3  #3x3
CELL_SIZE = 65  # Width and height
CELL_PADDING = 5  # Distance between cells


# Fonts and textures
title_font = pygame.font.Font(resource_path(
    "assets/fonts/MedievalSharp-Regular.ttf"), 82)
depiction_font = pygame.font.SysFont("arial", 33, italic=True)
font = pygame.font.Font(resource_path(
    "assets/fonts/MedievalSharp-Regular.ttf"), 60)
dialogue_font = pygame.font.Font(resource_path(
    "assets/fonts/MedievalSharp-Regular.ttf"), 30)
button_font = pygame.font.Font(None, 36)
stats_font = pygame.font.Font(None, 30)
wood_texture = pygame.image.load(resource_path("assets/images/other/wooden_pattern.jpg")).convert_alpha()
wood_texture = pygame.transform.scale(wood_texture, (200, 50))
item_font = pygame.font.Font(None, 20)
item_stat_font = pygame.font.Font(None, 25)
inventory_surf = dialogue_font.render("Inventory", True, IVORY)
inventory_rect = inventory_surf.get_rect(center=(100, 180))
profile_title_surf = font.render("Character", True, IVORY)
profile_title_rect = profile_title_surf.get_rect(center=(SCREEN_WIDTH // 2 + 45, 50))


# Images
icon = pygame.image.load(resource_path("assets/images/icon.png"))
pygame.display.set_icon(icon)
paladin_img = pygame.image.load(resource_path("assets/images/other/paladin.jpg")).convert_alpha()
paladin_img = pygame.transform.smoothscale(paladin_img, (250, 260))
paladin_rect = paladin_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))
barbarian_img = pygame.image.load(resource_path("assets/images/other/barbarian.jpg")).convert_alpha()
barbarian_img = pygame.transform.smoothscale(barbarian_img, (250, 260))
barbarian_rect = barbarian_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))
necromancer_img = pygame.image.load(resource_path("assets/images/other/necromancer.jpg")).convert_alpha()
necromancer_img = pygame.transform.smoothscale(necromancer_img, (250, 260))
necromancer_rect = necromancer_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))
rogue_img = pygame.image.load(resource_path("assets/images/other/rogue.jpg")).convert_alpha()
rogue_img = pygame.transform.smoothscale(rogue_img, (250, 260))
rogue_rect = rogue_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))
wizard_img = pygame.image.load(resource_path("assets/images/other/wizard.jpg")).convert_alpha()
wizard_img = pygame.transform.smoothscale(wizard_img, (250, 260))
wizard_rect = wizard_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))
druid_img = pygame.image.load(resource_path("assets/images/other/druid.jpg")).convert_alpha()
druid_img = pygame.transform.smoothscale(druid_img, (250, 260))
druid_rect = wizard_img.get_rect(center=(SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2))

coin_img = pygame.image.load(resource_path("assets/images/other/coin.png")).convert_alpha()
coin_img = pygame.transform.scale(coin_img, (55, 55))
coin_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 185, 55, 55)
level_icon = pygame.image.load(resource_path("assets/images/other/level_arrow.png")).convert_alpha()
level_icon = pygame.transform.scale(level_icon, (55, 55))
level_icon_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 245, 55, 55)
heal_img = pygame.image.load(resource_path("assets/images/other/heal.png")).convert_alpha()
heal_img = pygame.transform.scale(heal_img, (55, 55))
heal_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
berserk_img = pygame.image.load(resource_path("assets/images/other/berserk.png")).convert_alpha()
berserk_img = pygame.transform.scale(berserk_img, (55, 55))
berserk_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
fireball_img = pygame.image.load(resource_path("assets/images/other/fireball.jpg")).convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (55, 55))
fireball_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
reanimate_img = pygame.image.load(resource_path("assets/images/other/reanimate.png")).convert_alpha()
reanimate_img = pygame.transform.scale(reanimate_img, (55, 55))
reanimate_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
stab_img = pygame.image.load(resource_path("assets/images/other/stab.png")).convert_alpha()
stab_img = pygame.transform.scale(stab_img, (55, 55))
stab_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
hive_img = pygame.image.load(resource_path("assets/images/other/hive.jpg")).convert_alpha()
hive_img = pygame.transform.scale(hive_img, (55, 55))
hive_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 305, 55, 55)
xp_img = pygame.image.load(resource_path("assets/images/other/XP1.png")).convert_alpha()
xp_img = pygame.transform.scale(xp_img, (55, 55))
xp_rect = pygame.Rect(SCREEN_WIDTH // 2 + 180, 365, 55, 55)
battle_icon = pygame.image.load(resource_path("assets/images/other/battle_icon.png")).convert_alpha()
battle_icon = pygame.transform.scale(battle_icon, (40, 40))
gate_icon = pygame.image.load(resource_path("assets/images/other/gate.png")).convert_alpha()
gate_icon = pygame.transform.scale(gate_icon, (35, 35))
cross_icon = pygame.image.load(resource_path("assets/images/other/heal.png")).convert_alpha()
cross_icon = pygame.transform.scale(cross_icon, (35, 35))
bag_icon = pygame.image.load(resource_path("assets/images/other/bag.png")).convert_alpha()
bag_icon = pygame.transform.scale(bag_icon, (50, 50))

battle_icon_rect = pygame.Rect(SCREEN_WIDTH // 2 + 135, 2, 50, 50)
#health_potion = pygame.image.load(resource_path("assets/images/h_potion.png")).convert_alpha()
#health_potion = pygame.transform.scale(health_potion, (64, 64))
#mana_potion = pygame.image.load(resource_path("assets/images/m_potion.png")).convert_alpha()
#mana_potion = pygame.transform.scale(mana_potion, (64, 64))
#stamina_potion = pygame.image.load(resource_path("assets/images/stam_potion.png")).convert_alpha()
#stamina_potion = pygame.transform.scale(stamina_potion, (64, 64))

# Different backgrounds
char_select_bg = pygame.image.load(resource_path("assets/images/bg/castle_background.jpg")).convert()
char_select_bg = pygame.transform.smoothscale(char_select_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
town_bg = pygame.image.load(resource_path("assets/images/bg/town_background.jpg")).convert()
town_bg = pygame.transform.smoothscale(town_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
lab = pygame.image.load(resource_path("assets/images/bg/lab.jpg")).convert()
lab = pygame.transform.smoothscale(lab, (SCREEN_WIDTH, SCREEN_HEIGHT))
forge = pygame.image.load(resource_path("assets/images/bg/forge.jpg")).convert()
forge = pygame.transform.smoothscale(forge, (SCREEN_WIDTH, SCREEN_HEIGHT))
tavern = pygame.image.load(resource_path("assets/images/bg/tavern.jpg")).convert()
tavern = pygame.transform.smoothscale(tavern, (SCREEN_WIDTH, SCREEN_HEIGHT))
map_img = pygame.image.load(resource_path("assets/images/bg/Tales of Eldoria.png")).convert()
map_img = pygame.transform.smoothscale(map_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
enchanted_img = pygame.image.load(resource_path("assets/images/bg/enchanted_forest.jpg")).convert()
enchanted_img = pygame.transform.smoothscale(enchanted_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
dark_forest_img = pygame.image.load(resource_path("assets/images/bg/dark_forest.jpg")).convert()
dark_forest_img = pygame.transform.smoothscale(dark_forest_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cemetery_img = pygame.image.load(resource_path("assets/images/bg/cemetery.jpg")).convert()
cemetery_img = pygame.transform.smoothscale(cemetery_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
ruin_img = pygame.image.load(resource_path("assets/images/bg/haunted_ruin.jpg")).convert()
ruin_img = pygame.transform.smoothscale(ruin_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
frost_peak_img = pygame.image.load(resource_path("assets/images/bg/frost_peaks.jpg")).convert()
frost_peak_img = pygame.transform.smoothscale(frost_peak_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
sunken_temple_img = pygame.image.load(resource_path("assets/images/bg/sunken_temple.jpg")).convert()
sunken_temple_img = pygame.transform.smoothscale(sunken_temple_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
chapel_img =  pygame.image.load(resource_path("assets/images/bg/chapel.jpg")).convert()
chapel_img = pygame.transform.smoothscale(chapel_img, (800, 600))
battle_img = pygame.image.load(resource_path("assets/images/bg/battle.jpg"))
battle_img = pygame.transform.smoothscale(battle_img, (800, 600)).convert()


def increase_volume():
    global volume_level
    if volume_level < 1.0:
        volume_level = round(volume_level + 0.1, 1)
        pygame.mixer.music.set_volume(volume_level)
        adventure_theme.set_volume(volume_level)
        battle_theme.set_volume(volume_level)
        chapel_theme.set_volume(volume_level)


def decrease_volume():
    global volume_level
    if volume_level > 0.0:
        volume_level = round(volume_level - 0.1, 1)
        pygame.mixer.music.set_volume(volume_level)
        adventure_theme.set_volume(volume_level)
        battle_theme.set_volume(volume_level)
        chapel_theme.set_volume(volume_level)