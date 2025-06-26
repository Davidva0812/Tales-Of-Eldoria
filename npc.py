import random
from characters import Inventory
from items import *
from utils import resource_path

selected_item = None

class NPC:
    def __init__(self, name, dialogues):
        self.name = name
        self.dialogues = dialogues

    def talk(self):
        return f"{self.name} says: {random.choice(self.dialogues)}"


class Merchant(NPC):
    def __init__(self, name, dialogue):
        super().__init__(name, dialogue)
        self.inventory = []

    def handle_buy_button(self, selected_item, character):
        """Handle the logic of purchasing an item."""
        if selected_item and selected_item.cost <= character.gold_amount:
            if character.inventory.add_item(selected_item):
                character.gold_amount -= selected_item.cost
                if selected_item in alchemist.inventory.items:
                    if alchemist.inventory.remove_item(selected_item):
                        print(f"You bought {selected_item.name}")
                elif selected_item in blacksmith.inventory.items:
                    if blacksmith.inventory.remove_item(selected_item):
                        print(f"You bought {selected_item.name}")
            return True  # Buying successful
        elif selected_item:
            print("Not enough gold!")
        return False  # Buying not successful

    def handle_sell_button(self, selected_item, character):
        if selected_item and selected_item in character.inventory.items:
            character.gold_amount += selected_item.cost
            character.inventory.remove_item(selected_item)
            print(f"You sold {selected_item.name}")
            return True  # Selling successful
        print("No item selected!")
        return False  # Selling not successful


class Alchemist(Merchant):  #creates an instance of HealthPotion class by itself
    def __init__(self, name, dialog):
        super().__init__(name, dialog)
        self.inventory = Inventory()

    def load_alchemist_inventory(self, selected_character):
        # Health Potions (4)
        for _ in range(4):
            self.inventory.add_item(
                HealthPotion("Health Potion",
                             resource_path("assets/images/h_potion.png"),
                             30,
                             50))

        if selected_character.name == "Paladin":
            # Mana Potions (4)
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(relic)

        elif selected_character.name == "Barbarian":
            # Stamina Potions (4)
            for _ in range(4):
                self.inventory.add_item(StaminaPotion("Stamina Potion",
                                                      resource_path("assets/images/stam_potion.png"),
                                                      30, 30))
            self.inventory.add_item(necklace)

        elif selected_character.name == "Rogue":
            for _ in range(4):
                self.inventory.add_item(StaminaPotion("Stamina Potion",
                                                      resource_path("assets/images/stam_potion.png"),
                                                      30, 30))
            self.inventory.add_item(lantern)

        elif selected_character.name == "Necromancer":
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(necro_ring)

        elif selected_character.name == "Wizard":
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(magic_orb)

        elif selected_character.name == "Swarmcaller":
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(nectar_necklace)

        elif selected_character.name == "Cryomancer":
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(snow_globe)

        elif selected_character.name == "Bard":
            for _ in range(4):
                self.inventory.add_item(ManaPotion("Mana Potion",
                                                   resource_path("assets/images/m_potion.png"),
                                                   30, 30))
            self.inventory.add_item(lucky_coin)


class Blacksmith(Merchant):
    def __init__(self, name, dialog):
        super().__init__(name, dialog)
        self.inventory = Inventory()

    def load_blacksmith_inventory(self, selected_character):
        if selected_character.name == "Paladin":
            self.inventory.add_item(sword)
            self.inventory.add_item(sword_2)
            self.inventory.add_item(pal_helm)
            self.inventory.add_item(pal_armor)
            self.inventory.add_item(pal_helm_2)
            self.inventory.add_item(pal_armor_2)
        elif selected_character.name == "Barbarian":
            self.inventory.add_item(axe)
            self.inventory.add_item(claymore)
            self.inventory.add_item(viking_helm)
            self.inventory.add_item(fur)
            self.inventory.add_item(fur_king)
            self.inventory.add_item(chaos_helm)
        elif selected_character.name == "Rogue":
            self.inventory.add_item(dagger)
            self.inventory.add_item(rapier)
            self.inventory.add_item(hood)
            self.inventory.add_item(leather_armor)
        elif selected_character.name == "Necromancer":
            self.inventory.add_item(grimoire)
            self.inventory.add_item(skull_staff)
            self.inventory.add_item(necro_crown)
            self.inventory.add_item(necro_cloak)
            self.inventory.add_item(scythe)
        elif selected_character.name == "Wizard":
            self.inventory.add_item(spellbook)
            self.inventory.add_item(mage_staff)
            self.inventory.add_item(wiz_cloak_1)
            self.inventory.add_item(wiz_cloak_2)
            self.inventory.add_item(wiz_hat)
        elif selected_character.name == "Swarmcaller":
            self.inventory.add_item(whip)
            self.inventory.add_item(hive_staff)
            self.inventory.add_item(moss_cloak)
            self.inventory.add_item(rose_crown)
        elif selected_character.name == "Cryomancer":
            self.inventory.add_item(ice_wand)
            self.inventory.add_item(specter)
            self.inventory.add_item(ice_cloak)
            self.inventory.add_item(ice_crown)
            self.inventory.add_item(ice_armor)
        elif selected_character.name == "Bard":
            self.inventory.add_item(flute)
            self.inventory.add_item(lute)
            self.inventory.add_item(bard_cloak)
            self.inventory.add_item(bard_hat)


class SaloonKeeper(Merchant):
    def __init__(self, name, dialog):
        super().__init__(name, dialog)
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)

    def show_quest(self):
        if not self.quests:
            return "There are no quests!"
        return "\n".join(quest.name for quest in self.quests)

    def give_quest(self, quest_name):
        for quest in self.quests:
            if quest.name.lower() == quest_name.lower():
                return f"You got a quest: {quest.name}"
        return "Invalid quest!"

    @staticmethod
    def go_to_sleep(character):
        """Your character can sleep, regaining up to 50% of max HP."""
        print("Would you like to sleep? Rent a room for 20 gold.")
        if character.gold_amount >= 20:
            if character.health < character.max_health:
                character.gold_amount -= 20
                regeneration = int(character.max_health * 0.3 ) #regenerate 30 % of the max HP
                character.health = min(character.health + regeneration, character.max_health)
                return f"Your hero regenerated {regeneration} HP while sleeping!"
            return "Your hero is already at max HP!"
        return "Your hero does not have enough gold for renting a room!"


#NPCs
alchemist = Alchemist("Alchemist", [
    "Welcome to my Magic shop!",
    "Looking for potions? I have the best ones!",
    "Be careful out there, traveler!"])

blacksmith = Blacksmith("Blacksmith", [
    "Welcome to my Armory shop!",
    "Need stronger gear? Come in!",
    "Sharpen your blade before you go out there."])

saloon_keeper = SaloonKeeper("Saloon-keeper", [
    "Welcome, traveler! Looking for a place to rest?",
    "A long journey, huh? Sit down and have a drink!",
    "If you need a place to stay, I can rent you a room."])


