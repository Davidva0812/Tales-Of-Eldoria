import random
from items import *
from settings_images import die_channel, die_theme
import json


class Inventory:
    def __init__(self):
        self.items = []
        self.max_size = 8  #2

    def add_item(self, item):
        if len(self.items) <= self.max_size:
            self.items.append(item)
            print(f"{item} added to inventory!")
            return True
        else:
            print("Inventory is full!")
            return False

    def remove_item(self, item):
         if item in self.items:
            self.items.remove(item)
            print(f"{item.name} removed from inventory!")
            return True
         else:
            return False

    def show_inventory(self):
        return [item.name for item in self.items]

    # Inventory can be iterated
    def __iter__(self):
        return iter(self.items)


class Character:
    def __init__(self, name, health, attack, armor, mana, stamina=0, special_ability="",
                 special_ability_depiction="", depiction=""):
        self.name = name
        self.health = health
        self.max_health = self.health
        self.attack = attack
        self.armor = armor
        self.mana = mana
        self.max_mana = self.mana
        self.stamina = stamina
        self.max_stamina = self.stamina
        self.special_ability = special_ability
        self.special_ability_depiction = special_ability_depiction
        self.depiction = depiction
        self.alive = True
        self.inventory = Inventory()
        self.gold_amount = 10
        self.bloodstone_amount = 0
        self.max_bloodstone_amount = 6
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 50
        self.equipped_items = [None] * 4  # store the EQUIPPED items

    def take_damage(self, damage):
        if not self.alive:
            print(f"{self.name} is already dead and cannot take damage!")
            return

        reduced_damage = max(0, damage - (self.armor / 2))
        self.health -= reduced_damage
        print(f"{self.name} took {reduced_damage} damage. Remaining HP: {self.health}")

        if self.health <= 0:
            self.die()

    def attack_enemy(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot attack!")
            return
        print(f"{self.name} attacks {enemy.name}!")
        enemy.enemy_take_damage(self.attack)
        if enemy.health <= 0:
            self.enemy_is_dead(enemy)

    def enemy_is_dead(self, enemy):
        global is_victory
        is_victory = True
        self.gold_amount += enemy.gold_drop_range
        if self.bloodstone_amount < self.max_bloodstone_amount:
            self.bloodstone_amount =min(self.bloodstone_amount + enemy.bloodstone,
                                        self.max_bloodstone_amount)
        if not enemy.loot_table:
            print("No equipment loot!")
        elif len(enemy.loot_table) == 1:  # if 1 item in the list
            self.inventory.add_item(enemy.loot_table[0])
        else:
            self.inventory.add_item(
                enemy.loot_table[0])  # always add the first item
        # Character specific looting
        if isinstance(self, Barbarian) and len(enemy.loot_table) > 1:
            self.inventory.add_item(enemy.loot_table[1])
        elif isinstance(self, Wizard) and len(enemy.loot_table) > 2:
            self.inventory.add_item(enemy.loot_table[2])
        elif isinstance(self, Rogue) and len(enemy.loot_table) > 3:
            self.inventory.add_item(enemy.loot_table[3])
        elif isinstance(self, Paladin) and len(enemy.loot_table) > 4:
            self.inventory.add_item(enemy.loot_table[4])
        elif isinstance(self, Necromancer) and len(
                enemy.loot_table) > 5:
            self.inventory.add_item(enemy.loot_table[5])
        print("Victory detected!")

    def die(self):
        self.alive = False
        self.health = 0  # Ensure HP does not go below zero
        print(f"{self.name} has died.")
        die_channel.play(die_theme, loops=0)

    def equip(self, item):
        if item in self.equipped_items:
            print(f"{self.name} has already equipped {item.name}!")
            return
        if isinstance(item, Weapon):
            for equipped_item in self.equipped_items:
                if isinstance(equipped_item, Weapon):
                    print( f"{self.name} already has {equipped_item.name} equipped. Unequipping it first...")
                    self.unequip(equipped_item)
                    break
        elif isinstance(item, Helmet):
            for equipped_item in self.equipped_items:
                if isinstance(equipped_item, Helmet):
                    print( f"{self.name} already has {equipped_item.name} equipped. Unequipping it first...")
                    self.unequip(equipped_item)
                    break
        elif isinstance(item, Armor):
            for equipped_item in self.equipped_items:
                if isinstance(equipped_item, Armor):
                    print( f"{self.name} already has {equipped_item.name} equipped. Unequipping it first...")
                    self.unequip(equipped_item)
                    break
        elif isinstance(item, Object):
            for equipped_item in self.equipped_items:
                if isinstance(equipped_item, Object):
                    print( f"{self.name} already has {equipped_item.name} equipped. Unequipping it first...")
                    self.unequip(equipped_item)
                    break
        if item in self.inventory.items:
            self.inventory.remove_item(item)
        if isinstance(item, Weapon):
            if isinstance(self, Barbarian):
                self.base_attack += item.damage
            self.attack += item.damage
        elif isinstance(item, Helmet):
            if isinstance(self, Barbarian):
                self.base_armor += item.armor
            self.armor += item.armor
            print(f"{self.name} equips {item.name}, increasing damage by {item.armor}!")
        elif isinstance(item, Armor):
            if isinstance(self, Barbarian):
                self.base_armor += item.armor
            self.armor += item.armor
            print(f"{self.name} equips {item.name}, increasing damage by {item.armor}!")
        elif isinstance(item, Object):
            if isinstance(self, Barbarian) or isinstance(self, Rogue):
                ratio = self.stamina / self.max_stamina if self.max_stamina > 0 else 1
                self.max_stamina += item.bonus
                self.stamina = int(self.max_stamina * ratio)
            else:
                ratio = self.mana / self.max_mana if self.max_mana > 0 else 1
                self.max_mana += item.bonus
                self.mana = int(self.max_mana * ratio)
            print(f"{self.name} equips {item.name}, increasing damage by {item.bonus}!")
        self.equipped_items.append(item)

    def unequip(self, item):
        if item in self.equipped_items:
            self.equipped_items.remove(item)
            if item not in self.inventory.items:
                self.inventory.add_item(item)
            if isinstance(item, Weapon):
                if isinstance(self, Barbarian):
                    self.base_attack -= item.damage
                self.attack -= item.damage
            elif isinstance(item, Helmet):
                if isinstance(self, Barbarian):
                    self.base_armor -= item.armor
                self.armor -= item.armor
            elif isinstance(item, Armor):
                if isinstance(self, Barbarian):
                    self.base_armor -= item.armor
                self.armor -= item.armor
            elif isinstance(item, Object):
                if isinstance(self, Barbarian) or isinstance(self, Rogue):
                    ratio = self.stamina / self.max_stamina if self.max_stamina > 0 else 1
                    self.max_stamina -= item.bonus
                    self.stamina = int(self.max_stamina * ratio)
                else:
                    ratio = self.mana / self.max_mana if self.max_mana > 0 else 1
                    self.max_mana -= item.bonus
                    self.mana = int(self.max_mana * ratio)
            print(f"{self.name} unequipped {item.name}!")
        else:
            print(f"{self.name} does not have {item.name} equipped.")

    def gain_xp(self, xp_reward):
        """Gaining XP and checking level up"""
        if not self.alive:
            return f"{self.name} is dead and cannot gain XP."
        self.xp += xp_reward
        print(f"{self.name} got {xp_reward} XP!")

        while self.xp >= self.xp_to_next_level:
            self.level_up()
            print(f"{self.name} leveled up!")

    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # More XP needed for leveling up
        if isinstance(self, Paladin):
            self.max_health += 6
            self.attack += 1.5
        elif isinstance(self, Barbarian):
            self.max_health += 6
            self.base_attack += 1.5
            self.attack = self.base_attack
        elif isinstance(self, Wizard) or isinstance(self, Necromancer):
            self.max_health += 4
            self.attack += 2.5
        elif isinstance(self, Cryomancer) or isinstance(self, Bard):
            self.max_health += 5
            self.attack += 2
        else:
            self.max_health += 5
            self.attack += 2
        # full health, mana/stamina when levels up
        self.health = self.max_health
        if isinstance(self, Barbarian) or isinstance(self, Rogue):
            self.max_stamina += 5
            self.stamina = self.max_stamina
        else:
            self.max_mana += 5
            self.mana = self.max_mana
        return (f"{self.name} leveled up to level {self.level}! "
                f"XP needed for next level: {self.xp_to_next_level}")

    """def save_game(self, filename="save_game.json"):
        data = {
            "name": self.name,
            "class": self.__class__.__name__,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "armor": self.armor,
            "xp": self.xp,
            "gold_amount": self.gold_amount,
            "inventory": [item.name for item in character.inventory.items],
        "equipped_items": [item.name if item else None for item in character.equipped_items],
            "bloodstone_amount": self.bloodstone_amount
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Game saved successfully.")

    def load_game(self, filename="save_game.json"):
        with open(filename, "r") as f:
            data = json.load(f)

        # Characters
        if data["class"] == "Barbarian":
            character = Barbarian()

        elif data["class"] == "Wizard":
            character = Wizard()

        elif data["class"] == "Rogue":
            character = Rogue()

        elif data["class"] == "Paladin":
            character = Paladin()

        elif data["class"] == "Necromancer":
            character = Necromancer()

        elif data["class"] == "Druid":
            character = Druid()

        elif data["class"] == "Cryomancer":
            character = Cryomancer()

        elif data["class"] == "Bard":
            character = Bard()

        self.name = data["name"]
        self.level = data["level"]
        self.health = data["health"]
        self.max_health = data["max_health"]
        self.mana = data["mana"]
        self.max_mana = data["max_mana"]
        self.stamina = data["stamina"]
        self.max_stamina = data["max_stamina"]
        self.armor = data["armor"]
        self.xp = data["xp"]
        self.gold_amount = data["gold_amount"]
        self.inventory = data["inventory"]
        self.equipped_items = data ["equipped_items"]
        self.bloodstone_amount = data["bloodstone_amount"]

        return character"""


class Barbarian(Character):
    def __init__(self):
        super().__init__("Barbarian", health=45, attack=5, armor=0, mana=0,
                         stamina=20, special_ability="Berserk",
                         special_ability_depiction="Frenzy: increases attack, but lowers defense.",
                         depiction="Fueled by fury, unstoppable in the heart of battle.")
        #self.inventory.add_item(axe)
        self.berserk_active = False
        self.base_attack = self.attack
        self.base_armor = self.armor

    def enter_berserk(self):
        if self.stamina > 0 and not self.berserk_active:
            self.attack += self.level * 7
            self.armor -= self.level * 3
            self.berserk_active = True
            self.stamina = 0
            print("You enter berserk mode!")

    def exit_berserk(self):
        if self.berserk_active:
            self.attack = self.base_attack
            self.armor = self.base_armor
            self.berserk_active = False
            print("You calm down and return to normal.")


class Wizard(Character):
    def __init__(self):
        super().__init__("Wizard", health=42, attack=8, armor=0, mana=30,
                         special_ability="Fireball",
                         special_ability_depiction="Casts a blazing fireball that burns enemies.",
                         depiction="A master of arcane secrets, bending reality with powerful spells.")
        #self.inventory.add_item(spellbook)

    def fireball(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Fireball!")
            return
        if self.mana >= 15:
            #damage = 10 + self.level * 2
            damage = self.attack * 1.7
            self.mana -= 15
            print(f"{self.name} casts a fireball at {enemy.name}!")
            enemy.enemy_take_damage(damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough mana for the spell!")


class Rogue(Character):
    def __init__(self):
        super().__init__("Rogue", health=45, attack=5, armor=0, mana=0,
                         stamina=20,
                         special_ability="Stab",
                         special_ability_depiction="Strikes swiftly to deal critical hit.",
                         depiction=" A shadow in the night, striking swiftly and unseen.")
        #self.inventory.add_item(dagger)

    def stab(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Stab!")
            return
        if self.stamina >= 10:
            damage = self.attack * 1.5
            self.stamina -= 10
            print(f"{self.name} lands a critical hit on {enemy.name}!")
            enemy.enemy_take_damage(damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough stamina for Stab!")

    def take_damage(self, damage):
        if not self.alive:
            print(f"{self.name} is already dead and cannot take damage!")
            return
        # 25% chance to dodge the attack
        if random.random() < 0.25:
            print(f"{self.name} dodges the attack!")
            return True
        else:
            reduced_damage = max(0, damage - self.armor)
            self.health -= reduced_damage
            print(f"{self.name} took {reduced_damage} damage. Remaining HP: {self.health}")

        if self.health <= 0:
            self.die()


class Paladin(Character):
    def __init__(self):
        super().__init__("Paladin", health=47, attack=3, armor=0, mana=20,
                         special_ability="Heal",
                         special_ability_depiction="Restores health using divine energy.",
                         depiction="A holy warrior, wielding divine power and protect the weak.")
        #self.inventory.add_item(sword)

    def heal(self):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Heal!")
            return

        if self.mana >= 10:
            if self.health < self.max_health:
                self.health = min(self.health + self.level * 2, self.max_health)  # Prevent overhealing
                self.mana -= 10
                print(f"{self.name} heals himself! New HP: {self.health}")
            else:
                print(f"{self.name} is already at max HP!")
        else:
            print(f"{self.name} does not have enough mana to heal!")


class Necromancer(Character):
    def __init__(self):
        super().__init__("Necromancer", health=40, attack=10, armor=0, mana=30,
                        special_ability="Reanimate",
                         special_ability_depiction="Raises a skeleton to fight alongside you.",
                        depiction="A dark sorcerer, commanding the dead.")
        #self.inventory.add_item(grimoire)

    def reanimate(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Summon skeletons!")
            return

        if self.mana >= 10:
            self.mana -= 10
            skeleton_damage = self.attack // 2
            print(f"{self.name} summons a skeleton! It attacks {enemy.name} for {skeleton_damage} damage before vanishing.")
            enemy.enemy_take_damage(skeleton_damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough mana to summon a skeleton!")


class Druid(Character):
    def __init__(self):
        super().__init__("Swarmcaller", health=43, attack=7, armor=0, mana=30,
                        special_ability="Summon Swarm",
                         special_ability_depiction="Unleashes a stinging cloud of insects.",
                        depiction="A subtype of Druid, commands the insects.")
        #self.inventory.add_item(whip)

    def summon_swarm(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Summon Swarm!")
            return
        if self.mana >= 15:
            #damage = 8 + self.level * 2
            damage = self.attack * 1.3
            self.mana -= 15
            print(f"{self.name} casts Summon Swarm at {enemy.name}!")
            enemy.enemy_take_damage(damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough mana for the spell!")

    def nature_favor(self):
        """Returns the modified attack value based on Nature's Favor chance."""
        base_attack = self.attack
        if random.random() < 0.2:
            print(f"Nature's Favor! {self.name}'s attack is empowered!")
            return base_attack + (base_attack / 2)
        return base_attack


class Cryomancer(Character):
    def __init__(self):
        super().__init__("Cryomancer", health=44, attack=6, armor=0, mana=30,
                        special_ability="Ice Spikes",
                         special_ability_depiction="Rapid volley of ice spikes toward enemies.",
                        depiction="A Mage, specialized to Ice magic, master of frost.")
        #self.inventory.add_item(ice_wand)

    def ice_spikes(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Ice Spikes!")
            return
        if self.mana >= 15:
            damage = 10 + self.level * 3
            #damage = self.attack * 1.5
            self.mana -= 15
            print(f"{self.name} casts Ice Spikes at {enemy.name}!")
            enemy.enemy_take_damage(damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough mana for the spell!")


class Bard(Character):
    def __init__(self):
        super().__init__("Bard", health=40, attack=10, armor=0, mana=30,
                        special_ability="Metal Cards",
                         special_ability_depiction="Sharp volley of metal cards towards enemies.",
                        depiction="A performer, master of voice, magical melodies, illusion and perception.")
        #self.inventory.add_item(flute)

    def take_damage(self, damage):
        if not self.alive:
            print(f"{self.name} is already dead and cannot take damage!")
            return
        # 20% chance to avoid the attack
        if random.random() < 0.2:
            print(f"{self.name} avoids the attack!")
            return True
        else:
            reduced_damage = max(0, damage - self.armor)
            self.health -= reduced_damage
            print(f"{self.name} took {reduced_damage} damage. Remaining HP: {self.health}")

        if self.health <= 0:
            self.die()

    def metal_cards(self, enemy):
        if not self.alive:
            print(f"{self.name} is dead and cannot use Metal Cards!")
            return
        if self.mana >= 15:
            damage = 8 + self.level * 2.5
            self.mana -= 15
            print(f"{self.name} casts Metal cards at {enemy.name}!")
            enemy.enemy_take_damage(damage)
            if enemy.health <= 0:
                self.enemy_is_dead(enemy)
        else:
            print(f"{self.name} does not have enough mana for the spell!")