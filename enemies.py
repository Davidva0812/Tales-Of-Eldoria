#import random
#import pygame
from items import *
from utils import resource_path

#pygame.init()
screen = pygame.display.set_mode((800, 600))

class Enemy:
    def __init__(self, name, health, attack, img, gold_drop_range, xp_reward,
                 loot_table=None):
        self.name = name
        self.health = health
        self.max_health = self.health
        self.attack = attack
        self.img = pygame.image.load(resource_path(f"assets/images/creatures/{img}")).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (175, 185))
        self.img_for_battle = pygame.transform.smoothscale(self.img, (250, 260))
        self.gold_drop_range = gold_drop_range
        self.loot_table = loot_table if loot_table else []
        self.xp_reward = xp_reward
        self.enemy_alive = True

    def enemy_take_damage(self, damage):
        if not self.enemy_alive:
            print(f"{self.name} is already dead and cannot take damage!")
            return
        self.health -= damage
        if self.health <= 0:
            self.enemy_die()
            print(f"{self.name} has been defeated!")

    def enemy_attack(self, player):
        if not self.enemy_alive:
            print(f"{self.name} is already dead and cannot attack!")
            player.gain_xp(self.xp_reward)
            print(f"Current XP: {player.xp}.")
            return
        print(f"{self.name} attacks {player.name}!")
        player.take_damage(self.attack)

    def enemy_die(self):
        self.enemy_alive = False
        self.health = 0

    def handle_equipment_loot(self, selected_character):
        if selected_character.name == "Paladin":
            selected_character.inventory.add_item(sword_2)
        else:
            pass


"""pygame.init()
screen = pygame.display.set_mode((800, 600))

class Enemy:
    def __init__(self, name, health, attack, img, gold_drop_range, xp_reward,
                 loot_table=None):
        self.name = name
        self.health = health
        self.max_health = self.health
        self.attack = attack
        self.img = pygame.image.load(f"assets/images/creatures/{img}").convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (175, 185))
        self.img_for_battle = pygame.transform.smoothscale(self.img, (250, 260))
        self.gold_drop_range = gold_drop_range
        self.loot_table = loot_table if loot_table else []
        self.xp_reward = xp_reward
        self.enemy_alive = True

    def enemy_take_damage(self, damage):
        if not self.enemy_alive:
            print(f"{self.name} is already dead and cannot take damage!")
            return
        self.health -= damage
        if self.health <= 0:
            self.enemy_die()
            print(f"{self.name} has been defeated!")

    def enemy_attack(self, player):
        if not self.enemy_alive:
            print(f"{self.name} is already dead and cannot attack!")
            return
        print(f"{self.name} attacks {player.name}!")
        player.take_damage(self.attack)

    def enemy_die(self):
        self.enemy_alive = False
        self.health = 0


    def battle(self, player):
        while True:
            if self.enemy_alive and player.alive:
                player.attack(self)
                self.attack(player)
            else:
                break

battle_over = False  # Kezdetben nincs vége a harcnak
def battle(player, enemy):
    Egyetlen kör lejátszása, ha mindkét fél él még.
    global battle_over  # Hogy kívülről is kezeljük

    # Ha a harc már véget ért, ne történjen semmi
    if battle_over:
        return "⚠️ A harc már véget ért!"

    player_damage = random.randint(5, 15)
    enemy_damage = random.randint(3, 12)

    enemy.health -= player_damage
    player.health -= enemy_damage

    # Ha az ellenség meghalt
    if enemy.health <= 0:
        battle_over = True  # Lezárjuk a harcot
        return f"🏆 {player.name} legyőzte {enemy.name}-t!"

    # Ha a játékos meghalt
    if player.health <= 0:
        battle_over = True  # Lezárjuk a harcot
        return f"💀 {player.name} elbukott {enemy.name} ellen!"

    return (f"⚔️ {player.name} ütött {enemy.name}-re ({player_damage} sebzés),"
            f"de kapott is egy csapást ({enemy_damage} sebzés).")"""

