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
                             30, 50)
mana_potion = ManaPotion("Mana Potion","assets/images/m_potion.png",
                         30, 30)
stamina_potion = StaminaPotion("Stamina Potion", "assets/images/stam_potion.png",
                               30, 30)

#Paladin equipments
sword = Weapon("Great Sword", 5, "assets/images/equipments/sword.jpg",
               25, "Paladin")
sword_2 = Weapon("Angel's Wraith", 15, "assets/images/equipments/a_sword.jpg",
               100, "Paladin")
pal_helm = Helmet("Knight's Helmet", 5, "assets/images/equipments/pal_helm_1.jpg",
                  40,"Paladin")
pal_helm_2 = Helmet("Winged Helmet", 10, "assets/images/equipments/pal_helm_2.jpg",
                  60,"Paladin")
pal_armor = Armor("Heavy Breastplate", 10, "assets/images/equipments/pal_armor_1.jpg",
                  50, "Paladin")
pal_armor_2 = Armor("Holy Armor", 20, "assets/images/equipments/pal_armor_2.jpg",
                  100, "Paladin")
relic = Object("Holy Relic", 10, "assets/images/equipments/relic.jpg",
               70, "Paladin")
paladin_item_list = [sword, sword_2, pal_helm, pal_helm_2, pal_armor, pal_armor_2, relic]


# Barbarian equipments
axe = Weapon("War-axe", 10, "assets/images/equipments/axe.jpg",
               25, "Barbarian")
claymore = Weapon("Blade of Fury", 20, "assets/images/equipments/claymore.jpg",
               100, "Barbarian")
viking_helm = Helmet("Viking Helmet", 3, "assets/images/equipments/viking_helm.jpg",
                  40,"Barbarian")
chaos_helm = Helmet("Chaos Helmet", 5, "assets/images/equipments/chaos_helm.jpg",
                  60,"Barbarian")
fur = Armor("Fur", 5, "assets/images/equipments/fur.jpg",
                  50,"Barbarian")
fur_king = Armor("Fur of Barbarian King", 10, "assets/images/equipments/fur.jpg",
                  100,"Barbarian")
necklace = Object("Wolf necklace", 10, "assets/images/equipments/necklace.jpg",
                  70,"Barbarian")
barbarian_item_list = [axe, claymore, viking_helm, chaos_helm, fur, fur_king, necklace]


# Rogue equipments
dagger = Weapon("Dagger", 10, "assets/images/equipments/dagger.jpg",
               25, "Rogue")
rapier = Weapon("Champion's Rapier", 20, "assets/images/equipments/rapier.jpg",
               100, "Rogue")
hood = Helmet("Hood", 5, "assets/images/equipments/hood.jpg",
                  50,"Rogue")
leather_armor= Armor("Leather Armor", 10, "assets/images/equipments/leather_armor.jpg",
                  80,"Rogue")
lantern = Object("Hooded Lantern", 10, "assets/images/equipments/hooded_lantern.jpg",
                  70,"Rogue")
rogue_item_list = [dagger, rapier, hood, leather_armor, lantern]


# Necromancer equipments
grimoire = Weapon("Grimoire", 12, "assets/images/equipments/grimoire.jpg",
               25, "Necromancer")
skull_staff = Weapon("Skull Staff", 25, "assets/images/equipments/skull_staff.jpg",
               75, "Necromancer")
scythe = Weapon("Soul Reaper", 30, "assets/images/equipments/scythe.jpg",
               120, "Necromancer")
necro_crown = Helmet("Lich King's Crown", 3, "assets/images/equipments/skull_crown.jpg",
                  50,"Necromancer")
necro_cloak = Armor("Cloak of Misery", 5, "assets/images/equipments/necro_cloak2.jpg",
                  80,"Necromancer")
necro_ring = Object("Phylactery", 20, "assets/images/equipments/skull_ring.jpg",
                  70,"Necromancer")
necro_item_list = [grimoire, skull_staff, scythe, necro_crown, necro_cloak, necro_ring]


# Wizard equipments
spellbook = Weapon("Spellbook", 10, "assets/images/equipments/spellbook.jpg",
               25, "Wizard")
mage_staff = Weapon("Graduate's Reward", 22, "assets/images/equipments/mage_staff.jpg",
               100, "Wizard")
wiz_hat = Helmet("Wizard Hat", 3, "assets/images/equipments/wiz_hat.jpg",
                  40,"Wizard")
wiz_cloak_1 = Armor("Apprentice Cloak", 5, "assets/images/equipments/wiz_cloak_1.jpg",
                  50,"Wizard")
wiz_cloak_2 = Armor("Wizard Cloak", 8, "assets/images/equipments/wiz_cloak_2.jpg",
                  100,"Wizard")
magic_orb = Object("Magic Orb", 20, "assets/images/equipments/orb.jpg",
                  70,"Wizard")
wizard_item_list = [spellbook, mage_staff, wiz_hat, wiz_cloak_1, wiz_cloak_2, magic_orb]


# Druid equipments
whip = Weapon("Thorned Rose whip", 10, "assets/images/equipments/whip.jpg",
               25, "Druid")
hive_staff = Weapon("Staff of Swarm Queen", 22, "assets/images/equipments/hive_staff.jpg",
               100, "Druid")
rose_crown = Helmet("Thornbloom Crown", 5, "assets/images/equipments/rose_crown.jpg",
                  50,"Druid")
moss_cloak = Armor("Mossvine Mantle", 10, "assets/images/equipments/moss_cloak.jpg",
                  80,"Druid")
nectar_necklace = Object("Nectar Necklace", 20, "assets/images/equipments/nectar_necklace.jpg",
                  70,"Druid")
druid_item_list = [whip, hive_staff, rose_crown, moss_cloak, nectar_necklace]


# Cryomancer equipments
ice_wand = Weapon("Blizzard Wand", 10, "assets/images/equipments/ice_wand.jpg",
               25, "Cryomancer")
specter = Weapon("Frost Queen's Specter", 22, "assets/images/equipments/ice_specter.jpg",
               100, "Cryomancer")
ice_crown = Helmet("Ice Crystal Crown", 5, "assets/images/equipments/ice_crown.jpg",
                  40,"Cryomancer")
ice_cloak = Armor("Mantle of Endless Winter", 10, "assets/images/equipments/ice_cloak.jpg",
                  50,"Cryomancer")
ice_armor = Armor("Frostspike Armor", 15, "assets/images/equipments/frost_armor.jpg",
                  100,"Cryomancer")
snow_globe = Object("Globe of Last Winter", 20, "assets/images/equipments/ice_globe.jpg",
                  70,"Cryomancer")
cryomancer_item_list = [ice_wand, specter, ice_crown, ice_cloak, ice_armor, snow_globe]


# Bard equipments
flute = Weapon("Flute", 10, "assets/images/equipments/flute.jpg",
               25, "Bard")
lute = Weapon("Lute of Endless Songs", 23, "assets/images/equipments/lyre.jpg",
               100, "Bard")
bard_hat= Helmet("Storyteller's Hat", 3, "assets/images/equipments/bard_hat.jpg",
                  50,"Bard")
bard_cloak = Armor("Elegant Cloak", 10, "assets/images/equipments/bard_cloak.jpg",
                  80,"Bard")
lucky_coin = Object("Lucky Coin", 20, "assets/images/equipments/luck_coin.jpg",
                  70,"Bard")
bard_item_list = [flute, lute, bard_hat, bard_cloak, lucky_coin]


all_possible_items = [health_potion, mana_potion, stamina_potion, paladin_item_list,
                      wizard_item_list, rogue_item_list, necro_item_list, druid_item_list,
                      cryomancer_item_list, bard_item_list, barbarian_item_list]