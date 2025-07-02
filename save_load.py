# save_load.py
import json
from characters import Barbarian, Wizard, Rogue, Paladin, Necromancer, Druid, Cryomancer, Bard
from items import *  # A list of all item instances


def get_item_by_name(name):
    for item_group in all_possible_items:
        if isinstance(item_group, list):
            for item in item_group:
                if item.name == name:
                    return item
        else:
            if item_group.name == name:
                return item_group
    return None


def save_game(character, filename="savegame.json"):
    data = {
        "name": character.name,
        "class": character.__class__.__name__,
        "level": character.level,
        "health": character.health,
        "max_health": character.max_health,
        "attack": character.attack,
        "mana": character.mana,
        "max_mana": character.max_mana,
        "stamina": character.stamina,
        "max_stamina": character.max_stamina,
        "armor": character.armor,
        "xp": character.xp,
        "gold_amount": character.gold_amount,
        "inventory": [item.name for item in character.inventory.items],
        "equipped_items": [item.name if item else None for item in character.equipped_items],
        "bloodstone_amount": character.bloodstone_amount
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved successfully.")

def load_game(filename="savegame.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    class_map = {
        "Barbarian": Barbarian,
        "Wizard": Wizard,
        "Rogue": Rogue,
        "Paladin": Paladin,
        "Necromancer": Necromancer,
        "Druid": Druid,
        "Cryomancer": Cryomancer,
        "Bard": Bard
    }

    character_class = class_map.get(data["class"])
    if not character_class:
        raise ValueError(f"Unknown class {data['class']} in save file.")

    character = character_class()

    character.name = data["name"]
    character.level = data["level"]
    character.health = data["health"]
    character.max_health = data["max_health"]
    character.mana = data["mana"]
    character.max_mana = data["max_mana"]
    character.stamina = data["stamina"]
    character.max_stamina = data["max_stamina"]
    character.armor = data["armor"]
    character.xp = data["xp"]
    character.gold_amount = data["gold_amount"]
    character.bloodstone_amount = data["bloodstone_amount"]

    character.inventory.items = [get_item_by_name(name) for name in data["inventory"] if name]
    character.equipped_items = [get_item_by_name(name) if name else None for name in data["equipped_items"]]

    print("Game loaded successfully.")
    return character
