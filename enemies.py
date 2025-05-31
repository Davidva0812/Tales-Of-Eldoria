from items import *
from utils import resource_path


screen = pygame.display.set_mode((800, 600))

class Enemy:
    def __init__(self, name, health, attack, img, gold_drop_range, xp_reward,
                 loot_table=None, bloodstone = 0):
        self.name = name
        self.health = health
        self.max_health = self.health
        self.attack = attack
        self.img = pygame.image.load(resource_path(f"assets/images/creatures/{img}")).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (175, 185))
        self.img_for_battle = pygame.transform.smoothscale(self.img, (250, 260))
        self.gold_drop_range = gold_drop_range
        self.loot_table = loot_table if loot_table else []
        self.bloodstone = bloodstone
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

    """def handle_equipment_loot(self, selected_character):
        if selected_character.name == "Paladin":
            selected_character.inventory.add_item(sword_2)
        else:
            pass"""


class TheCount(Enemy):
    def enemy_attack(self, player):
        if not self.enemy_alive:
            print(f"{self.name} is already dead and cannot attack!")
            player.gain_xp(self.xp_reward)
            print(f"Current XP: {player.xp}.")
            return
        print(f"{self.name} attacks {player.name}!")
        player.take_damage(self.attack)

        # Life drain: Count heals for 30% of the damage dealt
        life_steal = int(self.attack * 0.3)
        self.health += life_steal

        # Make sure health does not exceed max
        if self.health > self.max_health:
            self.health = self.max_health

        print(
            f"{self.name} healed for {life_steal} HP. Current HP: {self.health}/{self.max_health}")