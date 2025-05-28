import pygame
from utils import resource_path

class Equipment:
    def __init__(self, name, equipment_type, icon, cost, required_class=None):
        self.name = name
        self.equipment_type = equipment_type
        self.icon = pygame.image.load(resource_path(icon))
        self.icon = pygame.transform.smoothscale(self.icon, (65, 65))
        self.cost = cost
        self.required_class = required_class  #if None, every class can use it

    def __str__(self):
        return self.name


class Weapon(Equipment):
    def __init__(self, name, damage, icon, cost, required_class):
        super().__init__(name, "Weapon", icon, cost, required_class)
        self.damage = damage

    def __repr__(self):
        return f"{self.name}, damage={self.damage}"


class Armor(Equipment):  #for Warrior
    def __init__(self, name, armor, icon, cost, required_class):
        super().__init__(name, "Armor", icon, cost, required_class)
        self.armor = armor

    def __repr__(self):
        return f"{self.name}, armor={self.armor}"


class Helmet(Equipment):  #for Warrior
    def __init__(self, name, armor, icon, cost, required_class):
        super().__init__(name, "Helmet", icon, cost, required_class)
        self.armor = armor

    def __repr__(self):
        return f"{self.name}, armor={self.armor}"


class Object(Equipment):
    def __init__(self, name, bonus, icon, cost, required_class):
        super().__init__(name, "Object", icon, cost, required_class)
        self.bonus = bonus

    def __repr__(self):
        return f"{self.name}, bonus={self.bonus}"


class OtherItem:
    def __init__(self, name, icon, cost):
        self.name = name
        self.icon = pygame.image.load(resource_path(icon))
        self.icon = pygame.transform.scale(self.icon, (65, 65))
        self.cost = cost

    def use_item(self, target):
        pass    #each item will define this itself

    def __str__(self):
        return self.name

    def pick_up_item(self, target):
        target.inventory.append(self)
        return f"{self.name} added to {target.name}'s inventory!"

    def sell_item(self, target):
        for item in target.inventory:
            if item.name == self.name:
                target.gold_amount += item.cost
                target.inventory.remove(item)
                return f"{target.name} sold {self.name}."
            return f"{self.name} is not in {target.name}'s inventory yet!"


class HealthPotion(OtherItem):
    def __init__(self, name, icon, cost, healing_point):
        super().__init__(name, icon, cost)
        self.healing_point = healing_point

    def __repr__(self):
        return (f"HealthPotion: name='{self.name}', cost={self.cost}, "
                f"healing_point={self.healing_point}")

    def use_item(self, target):
        try:
            if target.health == 0:
                print(f"{target.name} is already dead and cannot be healed!")
                return f"{target.name} is already dead and cannot be healed!"
            if target.health == target.max_health:
                print(f"{target.name} is already at max {target.max_health} HP!")
                return f"{target.name} is already at max {target.max_health} HP!"

            target.inventory.remove_item(self)
            healed_amount = min(self.healing_point, target.max_health - target.health)
            target.health += healed_amount
            print(f"{target.name} healed {healed_amount} HP!")
            return f"{target.name} healed {healed_amount} HP!"

        except ValueError:
            print(f"{self.name} is not in {target.name}'s inventory yet!")
            return f"{self.name} is not in {target.name}'s inventory yet!"


class ManaPotion(OtherItem):
    def __init__(self, name, icon, cost, mana_point):
        super().__init__(name, icon, cost)
        self.mana_point = mana_point

    def __repr__(self):
        return f"ManaPotion: name='{self.name}', cost={self.cost}, mana_point={self.mana_point}"

    def use_item(self, target):
        try:
            if target.health == 0:
                print(f"{target.name} is already dead and cannot be healed!")
                return f"{target.name} is already dead!"
            if target.mana == target.max_mana:
                print(f"{target.name} is already at max {target.max_mana} Mana!")
                return f"{target.name} is already at max {target.max_mana} Mana!"
            target.inventory.remove_item(self)
            healed_amount = min(self.mana_point, target.max_mana - target.mana)
            target.mana += healed_amount
            print(f"{target.name} healed {healed_amount} Mana!")
            return f"{target.name} healed {healed_amount} Mana!"
        except ValueError:
            print(f"{self.name} is not in {target.name}'s inventory yet!")
            return f"{self.name} is not in {target.name}'s inventory yet!"


class StaminaPotion(OtherItem):
    def __init__(self, name, icon, cost, stamina_point):
        super().__init__(name, icon, cost)
        self.stamina_point = stamina_point

    def __repr__(self):
        return (f"StaminaPotion: name='{self.name}', cost={self.cost}, "
                f"stamina_point={self.stamina_point}")

    def use_item(self, target):
        try:
            if target.health == 0:
                print(f"{target.name} is already dead and cannot be healed!")
                return f"{target.name} is already dead!"
            if target.stamina == target.max_stamina:
                print(f"{target.name} is already at max Stamina!")
                return f"{target.name} is already at max {target.max_stamina} Stamina!"
            target.inventory.remove_item(self)
            healed_amount = min(self.stamina_point, target.max_stamina - target.stamina)
            target.stamina += healed_amount
            print(f"{target.name} healed {healed_amount} Stamina!")
            return f"{target.name} healed {healed_amount} Stamina!"
        except ValueError:
            print(f"{self.name} is not in {target.name}'s inventory yet!")
            return f"{self.name} is not in {target.name}'s inventory yet!"


class SharpeningStone(OtherItem):
    def __init__(self, name, icon, cost, damage_boost):
        super().__init__(name, icon, cost)
        self.damage_boost = damage_boost

    def __repr__(self):
        return f"SharpeningStone: name={self.name}, cost={self.cost}, damage boost={self.damage_boost}"

    def use_item(self, target):
        found_weapon = False

        for item in target.equipped_items:
            if isinstance(item, Weapon):
                item.damage += self.damage_boost
                target.base_damage += self.damage_boost
                found_weapon = True
        if found_weapon:
            return f"{target.name}'s weapon damage increased by {self.damage_boost}!"
        else:
            return f"{target.name} has no weapon to equip!"


class ArmorAmplifier(OtherItem):
    def __init__(self, name, icon, cost, armor_boost):
        super().__init__(name, icon, cost)
        self.armor_boost = armor_boost

    def __repr__(self):
        return f"ArmorAmplifier: name={self.name}, cost={self.cost}, armor boost={self.armor_boost}"

    def use_item(self, target):
        found_armor = False

        for item in target.equipped_items:
            if isinstance(item, (Armor, Helmet)):
                item.armor += self.armor_boost
                target.armor += self.armor_boost #increases the whole armor also
                found_armor = True

        if found_armor:
            return f"{target.name}'s armor increased by {self.armor_boost}!"
        else:
            return f"{target.name} has no armor to equip!"

health_potion = HealthPotion("Health Potion", "assets/images/h_potion.png",
                             5, 10)
mana_potion = ManaPotion("Mana Potion","assets/images/m_potion.png",
                         5, 10)
stamina_potion = StaminaPotion("Stamina Potion", "assets/images/stam_potion.png",
                               5, 10)

#Paladin equipments
sword = Weapon("Great Sword", 10, "assets/images/equipments/sword.jpg",
               1, "Paladin")
sword_2 = Weapon("Angel's Wraith", 20, "assets/images/equipments/a_sword.jpg",
               3, "Paladin")
pal_helm = Helmet("Knight's Helmet", 10, "assets/images/equipments/pal_helm_1.jpg",
                  1,"Paladin")
pal_helm_2 = Helmet("Winged Helmet", 20, "assets/images/equipments/pal_helm_2.jpg",
                  3,"Paladin")
pal_armor = Armor("Heavy Breastplate", 15, "assets/images/equipments/pal_armor_1.jpg",
                  5, "Paladin")
pal_armor_2 = Armor("Holy Armor", 30, "assets/images/equipments/pal_armor_2.jpg",
                  4, "Paladin")
relic = Object("Holy Relic", 10, "assets/images/equipments/relic.jpg",
               3, "Paladin")

# Barbarian equipments
axe = Weapon("War-axe", 10, "assets/images/equipments/axe.jpg",
               10, "Barbarian")
claymore = Weapon("Blade of Fury", 20, "assets/images/equipments/claymore.jpg",
               30, "Barbarian")
viking_helm = Helmet("Viking Helmet", 10, "assets/images/equipments/viking_helm.jpg",
                  15,"Barbarian")
chaos_helm = Helmet("Chaos Helmet", 20, "assets/images/equipments/chaos_helm.jpg",
                  30,"Barbarian")
fur = Armor("Fur", 20, "assets/images/equipments/fur.jpg",
                  30,"Barbarian")
fur_king = Armor("Fur of Barbarian King", 30, "assets/images/equipments/fur.jpg",
                  50,"Barbarian")
necklace = Object("Wolf necklace", 20, "assets/images/equipments/necklace.jpg",
                  3,"Barbarian")


# Rogue equipments
dagger = Weapon("Dagger", 10, "assets/images/equipments/dagger.jpg",
               10, "Rogue")
rapier = Weapon("Champion's Rapier", 20, "assets/images/equipments/rapier.jpg",
               5, "Rogue")
hood = Helmet("Hood", 10, "assets/images/equipments/hood.jpg",
                  15,"Rogue")
leather_armor= Armor("Leather Armor", 20, "assets/images/equipments/leather_armor.jpg",
                  30,"Rogue")
lantern = Object("Hooded Lantern", 20, "assets/images/equipments/hooded_lantern.jpg",
                  3,"Rogue")

# Necromancer equipments
grimoire = Weapon("Grimoire", 10, "assets/images/equipments/grimoire.jpg",
               10, "Necromancer")
skull_staff = Weapon("Skull Staff", 20, "assets/images/equipments/skull_staff.jpg",
               30, "Necromancer")
scythe = Weapon("Soul Reaper", 20, "assets/images/equipments/scythe.jpg",
               30, "Necromancer")
necro_crown = Helmet("Lich King's Crown", 10, "assets/images/equipments/skull_crown.jpg",
                  15,"Necromancer")
necro_cloak = Armor("Cloak of Misery", 20, "assets/images/equipments/necro_cloak2.jpg",
                  30,"Necromancer")
necro_ring = Object("Phylactery", 20, "assets/images/equipments/skull_ring.jpg",
                  3,"Necromancer")

# Wizard equipments
spellbook = Weapon("Spellbook", 10, "assets/images/equipments/spellbook.jpg",
               10, "Wizard")
mage_staff = Weapon("Graduate's Reward", 20, "assets/images/equipments/mage_staff.jpg",
               30, "Wizard")
wiz_hat = Helmet("Wizard Hat", 10, "assets/images/equipments/wiz_hat.jpg",
                  15,"Wizard")
wiz_cloak_1 = Armor("Apprentice Cloak", 20, "assets/images/equipments/wiz_cloak_1.jpg",
                  30,"Wizard")
wiz_cloak_2 = Armor("Wizard Cloak", 20, "assets/images/equipments/wiz_cloak_2.jpg",
                  30,"Wizard")
magic_orb = Object("Magic Orb", 20, "assets/images/equipments/orb.jpg",
                  3,"Wizard")

# Druid equipments
whip = Weapon("Thorned Rose whip", 10, "assets/images/equipments/whip.jpg",
               10, "Druid")
hive_staff = Weapon("Staff of Swarm Queen", 20, "assets/images/equipments/hive_staff.jpg",
               30, "Druid")
rose_crown = Helmet("Thornbloom Crown", 10, "assets/images/equipments/rose_crown.jpg",
                  15,"Druid")
moss_cloak = Armor("Mossvine Mantle", 20, "assets/images/equipments/moss_cloak.jpg",
                  30,"Druid")
nectar_necklace = Object("Nectar Necklace", 20, "assets/images/equipments/nectar_necklace.jpg",
                  3,"Druid")

# Cryomancer equipments
ice_wand = Weapon("Spellbook", 10, "assets/images/equipments/ice_wand.jpg",
               10, "Cryomancer")
specter = Weapon("Graduate's Reward", 20, "assets/images/equipments/ice_specter.jpg",
               30, "Cryomancer")
ice_crown = Helmet("Wizard Hat", 10, "assets/images/equipments/wiz_hat.jpg",
                  15,"Cryomancer")
ice_cloak = Armor("Apprentice Cloak", 20, "assets/images/equipments/ice_cloak.jpg",
                  30,"Cryomancer")
ice_armor = Armor("Wizard Cloak", 20, "assets/images/equipments/wiz_cloak_2.jpg",
                  30,"Cryomancer")
snow_globe = Object("Magic Orb", 20, "assets/images/equipments/ice_globe.jpg",
                  3,"Cryomancer")