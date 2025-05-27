from characters import Barbarian, Wizard, Rogue, Paladin, Necromancer, Druid
#from items import Weapon, Helmet, Armor
from settings_images import *
from enemies import *
from locations import *


exit_confirmed = False
hovered_character = None
selected_character = None
selected_item = None
current_alchemist_dialogue = current_blacksmith_dialogue = current_saloon_keeper_dialogue = None
is_victory = False
is_defeat = False

# List of Characters
characters = [
    Barbarian(),
    Wizard(),
    Rogue(),
    Paladin(),
    Necromancer(),
    Druid()
]

# Buttons, all was (0, 0, 0, 0)
"""start_button = pygame.Rect(300, 250, 200, 50)  # (x, y, width, height)
exit_button = pygame.Rect(300, 390, 200, 50)
load_button = pygame.Rect(300, 320, 200, 50)
lab_button = pygame.Rect(600, 60, 200, 50)
blacksmith_button = pygame.Rect(600, 130, 200, 50)
back_button = pygame.Rect(600, 550, 200, 50)
tavern_button = pygame.Rect(600, 200, 200, 50)
profile_button = pygame.Rect(600, 340, 200, 50)
explore_button = pygame.Rect(600, 410, 200, 50)
sounds_button = pygame.Rect(600, 200, 200, 50)"""
input_box = pygame.Rect(160, 240, 485, 80)
back_button_rect = pygame.Rect(600, 550, 200, 50)
yes_button_rect = pygame.Rect(100, 350, 200, 50)
no_button_rect = pygame.Rect(350, 350, 200, 50)
#buy_button_rect = pygame.Rect(600, 200, 200, 50)
buy_button_rect = pygame.Rect(300, 500, 200, 50)
sell_button_rect = pygame.Rect(300, 500, 200, 50)
bless_button_rect = pygame.Rect(600, 400, 200, 50)
ok_button_rect = pygame.Rect(290, 450, 200, 50)
#popup buttons
popup_rect = pygame.Rect(100, 250, 450, 150)
popup_rect_battle = pygame.Rect(200, 250, 400, 250)


def draw_button(text, x, y, width, height):
    """Draws buttons and checks clicking"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    # Draws wooden pattern
    screen.blit(wood_texture, (x, y))
    # If the mouse is over it, a faint overlay effect (e.g., darker overlay)
    # pygame.SRCALPHA: supports the hover effect
    if button_rect.collidepoint(mouse_x, mouse_y):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))  #darker overlay
        screen.blit(overlay, (x, y))
    # Text in the middle
    text_surface = button_font.render(text, True, IVORY)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect


def draw_battle_button(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    # Draws battle icon pattern
    screen.blit(battle_icon, (x, y))
    return button_rect


def draw_gate_button(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    screen.blit(gate_icon, (x, y))
    return button_rect


def draw_cross_button(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    screen.blit(cross_icon, (x, y))
    return button_rect


def draw_bag_button(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    # Draw border
    pygame.draw.rect(screen, BROWN, button_rect, 2)  # 2=border thickness
    screen.blit(bag_icon, (x, y))
    return button_rect


def draw_tavern_popup():
    pygame.draw.rect(screen, DARKER_GREY, popup_rect)  # Popup háttér
    text_surface = button_font.render("Would you like to rent a room?", True, IVORY)
    screen.blit(text_surface, (popup_rect.x + 50, popup_rect.y + 30))
    draw_button("Yes", 100, 350, 200, 50)
    draw_button("No", 350, 350, 200, 50)


def draw_battle_popup(selected_character, selected_enemy):
    global is_victory, is_defeat

    if selected_enemy.health <= 0:
        is_victory = True
        pygame.draw.rect(screen, GREEN, popup_rect_battle)
        text_surface = font.render("Victory!", True, GOLD)
        screen.blit(text_surface,(popup_rect_battle.x + 80, popup_rect_battle.y))
        ok_button = draw_button("OK", 290, 450, 200, 50)
        #is_victory = False
        #is_defeat = False
        return ok_button
    elif selected_character.health <= 0:
        is_defeat = True
        pygame.draw.rect(screen, RED, popup_rect_battle)
        text_surface = stats_font.render("Game Over! Close the window to exit.", True, BLACK)
        ok_button = draw_button("Exit game", 290, 450, 200, 50)
        screen.blit(text_surface, (popup_rect_battle.x + 15, popup_rect_battle.y))
        return ok_button


def draw_grid(color, cell_offset_x, cell_offset_y, inventory, equipped_items=None, selected_character=None):
    index = 0  # Inventory index
    cell_data = []  # Stores the data of cells and items
    # Draw Inventory
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + cell_offset_x
            y = row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + cell_offset_y
            cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, cell_rect, 2)
            # Draw inventory item
            if index < len(inventory.items):
                item = inventory.items[index]
                screen.blit(item.icon, (x, y))  # Draw item
                if cell_rect.collidepoint(pygame.mouse.get_pos()):
                    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 50))  # darker overlay
                    screen.blit(overlay, (x, y))
                    item_info = f"{item.name} - Cost: {item.cost}"
                    if hasattr(item, "healing_point"):
                        item_info += f" - HP Restore: {item.healing_point}"
                    if hasattr(item, "mana_point"):
                        item_info += f" - Mana Restore: {item.mana_point}"
                    if hasattr(item, "stamina_point"):
                        item_info += f" - Stamina Restore: {item.stamina_point}"
                    if hasattr(item, "damage"):
                        item_info += f" - Damage: {item.damage}"
                    if hasattr(item, "armor"):
                        item_info += f" - Armor: {item.armor}"
                    if hasattr(item, "bonus"):
                        item_info += f" - Bonus Energy: {item.bonus}"
                    info_text = item_stat_font.render(item_info, True, WHITE)
                    screen.blit(info_text, (185 - info_text.get_width() // 2,
                        SCREEN_HEIGHT - 51))
                    cell_data.append((cell_rect, item))
            index += 1
    # Draw the slots for equipped items
    if selected_character:
        SLOT_SIZE = 65  # Slot size
        SLOT_PADDING = 5  # Gap between slots
        equipment_slots = [
            (SCREEN_WIDTH // 2 - 155, 165, SLOT_SIZE, SLOT_SIZE), # Helmet slot
            (SCREEN_WIDTH // 2 - 155, 165 + (SLOT_SIZE + SLOT_PADDING), SLOT_SIZE, SLOT_SIZE),  # Armor slot
            (SCREEN_WIDTH // 2 - 155, 165 + 2 * (SLOT_SIZE + SLOT_PADDING), SLOT_SIZE, SLOT_SIZE),  # Weapon slot
            (SCREEN_WIDTH // 2 - 155, 165 + 3 * (SLOT_SIZE + SLOT_PADDING), SLOT_SIZE, SLOT_SIZE)  # Object slot
        ]
        # Position of equipped items in slots
        equipped_items_dict = {
            'helmet': None,
            'armor': None,
            'weapon': None,
            'other': None
        }
        if equipped_items:
            for item in equipped_items:
                if isinstance(item, Helmet) and equipped_items_dict['helmet'] is None:
                    equipped_items_dict['helmet'] = item
                elif isinstance(item, Armor) and equipped_items_dict['armor'] is None:
                    equipped_items_dict['armor'] = item
                elif isinstance(item, Weapon) and equipped_items_dict['weapon'] is None:
                    equipped_items_dict['weapon'] = item
                elif equipped_items_dict['other'] is None:
                    equipped_items_dict['other'] = item
        # Draw items to their correct position
        slot_labels = ["Helmet", "Armor", "Weapon", "Other"]
        for i, slot in enumerate(equipment_slots):
            slot_rect = pygame.Rect(slot[0], slot[1], 65, 65)
            pygame.draw.rect(screen, color, slot_rect, 3, border_radius=5)
            if slot_rect.collidepoint(pygame.mouse.get_pos()):
                overlay = pygame.Surface((CELL_SIZE, CELL_SIZE) ,pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 50))  # darker overlay
                screen.blit(overlay, (slot[0], slot[1]))
            equipped_item = None
            if i == 0 and equipped_items_dict['helmet']:  # Helmet slot
                equipped_item = equipped_items_dict['helmet']
            elif i == 1 and equipped_items_dict['armor']:  # Armor slot
                equipped_item = equipped_items_dict['armor']
            elif i == 2 and equipped_items_dict['weapon']:  # Weapon slot
                equipped_item = equipped_items_dict['weapon']
            elif i == 3 and equipped_items_dict['other']:  # Other slot
                equipped_item = equipped_items_dict['other']

            if equipped_item:
                screen.blit(equipped_item.icon, (slot[0], slot[1]))
                if slot_rect.collidepoint(pygame.mouse.get_pos()):
                    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 50))  # darker overlay
                    screen.blit(overlay, (slot[0], slot[1]))
                cell_data.append((slot_rect, equipped_item))
            else:
                # If no item, write the slot's name
                slot_text = item_font.render(slot_labels[i], True, WHITE)
                text_x = slot[0] + (SLOT_SIZE - slot_text.get_width()) // 2
                text_y = slot[1] + (SLOT_SIZE - slot_text.get_height()) // 2
                screen.blit(slot_text, (text_x, text_y))

    return cell_data  # Return the inventory and equipped item's cells


def bless_in_chapel(character):
    """The hero gains blessing, restoring a small amount of HP, MP or Stamina."""
    if character.gold_amount >= 20:
        character.gold_amount -= 20
        if character.health < character.max_health:
            character.health = character.max_health
            return f"{character.name} gains bless and restored full HP."
        else:
            return f"{character.name} already at full HP."
    else:
        return f"{character.name} has not enough gold!"

def draw_enemies(game_state):
    if game_state not in location_enemies:
        return  # If no current location, exit

    enemies = location_enemies[game_state]  # Current location's enemies
    start_x = SCREEN_WIDTH // 2 - 405  # Starting x position
    start_y = 160  # Starting y position
    enemy_rects = []  # Storing enemies' positions
    for i, enemy in enumerate(enemies):
        x = start_x + (i * 205) # Separate enemies
        y = start_y
        # Draw enemy rect
        enemy_rect = pygame.Rect(x, y, 195, 205)
        pygame.draw.rect(screen, (100, 0, 0), enemy_rect, border_radius=10)
        # Draw enemy image
        screen.blit(enemy.img, (x + 10, y + 10))
        # Write enemy name
        if game_state == ENCHANTED_FOREST:
            name_text = stats_font.render(enemy.name, True, WHITE)
        elif game_state in [FROSTFANG_PEAK, DARK_FOREST]:
            name_text = stats_font.render(enemy.name, True, BLACK)
        elif game_state in [HAUNTED_RUIN, CEMETERY, SUNKEN_TEMPLE]:
            name_text = stats_font.render(enemy.name, True, ORANGE)
        else:
            name_text = stats_font.render(enemy.name, True, WHITE)
        screen.blit(name_text, (x + 90 - name_text.get_width() // 2, y - 35))

        # Draw battle button
        battle_button = pygame.Rect(x + 40, y + 220, 100, 40)
        pygame.draw.rect(screen, (150, 0, 0), battle_button, border_radius=5)
        battle_text = button_font.render("Battle", True, WHITE)
        screen.blit(battle_text, (x + 90 - battle_text.get_width() // 2, y + 230))
        enemy_rects.append((enemy_rect, battle_button, enemy))

    return enemy_rects  # Return rects to event handling


def draw_battle_ui(screen, selected_character, selected_enemy):
    screen.blit(battle_img, (0, 0))
    # Player and enemy picture
    if selected_character == characters[0]:
        screen.blit(barbarian_img, (20, 150))
    elif selected_character == characters[1]:
        screen.blit(wizard_img, (20, 150))
    elif selected_character == characters[2]:
        screen.blit(rogue_img, (20, 150))
    elif selected_character == characters[3]:
        screen.blit(paladin_img, (20, 150))
    elif selected_character == characters[4]:
        screen.blit(necromancer_img, (20, 150))

    """# Harci napló megjelenítése
    y_offset = 400
    for log in battle_log[-5:]:  # Csak az utolsó 5 eseményt mutatjuk
        text = font.render(log, True, (255, 255, 255))
        screen.blit(text, (50, y_offset))
        y_offset += 30"""

    attack_button = draw_button("Attack", 300, 190, 200, 50)
    ability_button = draw_button("Use Ability", 300, 260, 200, 50)
    surrender_button = draw_button("Surrender", 300, 330, 200, 50)

    return attack_button, ability_button, surrender_button


def draw_health_bar(surface, x, y, current_hp, max_hp, width=150, height=30):
    # HP ratio counting
    hp_ratio = max(0, current_hp / max_hp)  # Cannot be negative
    # Draw rect
    pygame.draw.rect(surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4))
    if hp_ratio > 0.6:
        color = (255, 0, 0)
    elif hp_ratio > 0.3:
        color = (150, 2, 2)
    else:
        color = (77, 0, 0)
    pygame.draw.rect(surface, color, (x, y, width * hp_ratio, height))
    # Write life points
    number_font = pygame.font.Font(None, 30)
    text = number_font.render(f"{current_hp} / {max_hp}", True, (255, 255, 255))
    surface.blit(text, (x + width // 2 - text.get_width() // 2, y + height // 2 - text.get_height() // 2))


def draw_mana_bar(surface, x, y, current_mana, max_mana, width=150, height=30):
    mana_ratio = max(0, current_mana / max_mana)
    pygame.draw.rect(surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4))
    if mana_ratio > 0.6:
        color = BLUE
    elif mana_ratio > 0.3:
        color = (34, 3, 128)
    else:
        color = (25, 3, 92)
    pygame.draw.rect(surface, color, (x, y, width * mana_ratio, height))
    number_font = pygame.font.Font(None, 30)
    text = number_font.render(f"{current_mana} / {max_mana}", True, (255, 255, 255))
    surface.blit(text, (x + width // 2 - text.get_width() // 2, y + height // 2 - text.get_height() // 2))


def draw_stamina_bar(surface, x, y, current_stamina, max_stamina, width=150, height=30):
    stamina_ratio = max(0, current_stamina / max_stamina)
    pygame.draw.rect(surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4))
    if stamina_ratio > 0.6:
        color = (0, 184, 37)
    elif stamina_ratio > 0.3:
        color = GREEN
    else:
        color = (2, 79, 18)
    pygame.draw.rect(surface, color, (x, y, width * stamina_ratio, height))
    number_font = pygame.font.Font(None, 30)
    text = number_font.render(f"{current_stamina} / {max_stamina}", True, (255, 255, 255))
    surface.blit(text, (x + width // 2 - text.get_width() // 2, y + height // 2 - text.get_height() // 2))


def draw_location_level(surface, level, color):
    text = font.render(f"Location level: {level}", True, color)
    surface.blit(text, (200, 2))


def draw_looting(surface, gold, xp_reward, enemy_loot_table):
    if enemy_loot_table:
        for item in enemy_loot_table:
            text = button_font.render(f"You get: {gold} gold and found item(s)!", True, IVORY)
            text_xp = button_font.render(f"You earned {xp_reward} XP!", True, IVORY)
            surface.blit(text, (150, 20))
            surface.blit(text_xp, (150, 60))
    else:
        text = button_font.render(f"You get: {gold} gold!", True, IVORY)
        surface.blit(text, (150, 20))
        text_xp = button_font.render(f"You earned {xp_reward} XP!", True, IVORY)
        surface.blit(text_xp, (150, 60))


def draw_enemy_attack_point(surface, attack):
    text = button_font.render(f"Attack point: {attack}", True, IVORY)
    surface.blit(text, (570, 478))


def draw_hero_attack_and_armor(surface, attack, armor):
    text_1 = button_font.render(f"Attack: {attack}", True, IVORY)
    text_2 = button_font.render(f"Armor: {armor}", True, IVORY)
    surface.blit(text_1, (60, 520))
    surface.blit(text_2, (60, 560))


def draw_dodge_chance(surface, x, y):
    text = button_font.render("Chance to dodge: 30%.", True, IVORY)
    surface.blit(text, (x, y))


def get_stat_name(character):
    if isinstance(character, Barbarian):
        return "Strength"
    elif isinstance(character, Wizard):
        return "Intelligence"
    elif isinstance(character, Rogue):
        return "Dexterity"
    elif isinstance(character, Paladin):
        return "Holy power"
    elif isinstance(character, Necromancer):
        return "Knowledge"