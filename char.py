#from npc import *
from UI import *


sleep_button_rect = pygame.Rect(300, 200, 100, 30)
(start_button, exit_button, lab_button, blacksmith_button, back_button,
tavern_button, profile_button, explore_button, battle_button_enchanted, battle_button_dark_forest,
battle_button_cemetery, battle_button_ruin, battle_button_peak,battle_button_sunken,
sounds_button, show_enemies_button, gate_button, buy_button, sell_button, cross_button,
show_inventory_button, sell_item_button, attack_button, ability_button,
ok_button, surrender_button, bag_button, to_explore_button) = [None] * 28
cursor_surf = pygame.image.load("assets/images/other/cursor_shiny.png").convert_alpha()
cursor_rect = pygame.Rect(0, 0, 50, 50)
show_sleep_popup = False
show_alchemist_inventory = show_blacksmith_inventory = show_character_inventory = False
alchemist_inventory_loaded = False
blacksmith_inventory_loaded = False
selected_character = None
selected_enemy = None

previous_game_state = None
explore_music_playing = location_music_playing = chapel_music_playing = battle_music_playing = mute = show_enemies = False
game_state = MENU  # At the beginning, the menu will appear
player_name = ""
bless_cooldown = 0  # When was the latest bonus
bless_delay = 15000
enemy_rects = []

"""
# Drawing
def drawing():
    sleep_message = ""
    bless_message = ""
    message_time = None
    if game_state == MENU:
        title_text = title_font.render("Tales Of Eldoria", True, BLUE)
        text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        border_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10,
                                  text_rect.width + 20, text_rect.height + 20)
        pygame.draw.rect(screen, (120, 120, 120), border_rect, border_radius=15)
        pygame.draw.rect(screen, LIGHT_BROWN, border_rect, 5, border_radius=15)
        screen.blit(title_text, text_rect)
        start_button = draw_button("Start Game", 300, 250, 200, 50)
        # load_button = draw_button("Load Game", 300, 320, 200, 50)
        sounds_button = draw_button("Audio", 300, 320, 200, 50)
        exit_button = draw_button("Exit Game", 300, 390, 200, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == AUDIO:
        mute_button_text = "Unmute" if mute else "Mute"
        mute_button = draw_button(mute_button_text, 300, 250, 200, 50)
        vol_button_1 = draw_button("Volume +", 300, 320, 200, 50)
        vol_button_2 = draw_button("Volume -", 300, 390, 200, 50)
        back_button = draw_button("Back to Menu", 600, 550, 200, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == CHARACTER_SELECT:
        screen.blit(char_select_bg, (0, 0))
        title_text = font.render("Choose Your Character", True, IVORY)
        screen.blit(title_text,
                    (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
        for i, character in enumerate(characters):
            draw_button(character.name, 300, 140 + i * 60, 200, 50)
        if hovered_character:
            description_text = depiction_font.render(
                f"{hovered_character.depiction}", True, BLACK)
            screen.blit(description_text, (
            SCREEN_WIDTH // 2 - description_text.get_width() // 2, 500))
        back_button = draw_button("Back to Menu", 600, 550, 200, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == TOWN:
        screen.blit(town_bg, (0, 0))
        selected_char_text = font.render(f"Welcome, {player_name}!", True, BLUE)
        screen.blit(selected_char_text,
                    (SCREEN_WIDTH // 2 - selected_char_text.get_width() // 2, 1))
        lab_button = draw_button("Laboratory", 600, 60, 200, 50)
        blacksmith_button = draw_button("Blacksmith", 600, 130, 200, 50)
        tavern_button = draw_button("Tavern", 600, 200, 200, 50)
        profile_button = draw_button("Profile", 600, 340, 200, 50)
        explore_button = draw_button("Explore", 600, 410, 200, 50)
        exit_button = draw_button("Exit game", 600, 550, 200, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == ALCHEMIST_LABORATORY:
        screen.blit(lab, (0, 0))
        if current_alchemist_dialogue:
            alchemist_text = dialogue_font.render(current_alchemist_dialogue, True,
                                                  IVORY)
            screen.blit(alchemist_text,
                        (SCREEN_WIDTH // 2 - alchemist_text.get_width() // 2, 1))
        back_button = draw_button("Back to Town", 600, 550, 200, 50)
        show_inventory_button = draw_button("Buy items", 600, 200, 200, 50)
        sell_item_button = draw_button("Sell items", 600, 270, 200, 50)
        cells = []
        if show_alchemist_inventory:
            buy_button = draw_button(
                "Buy" if selected_character.gold_amount >= 5 else "Not enough gold",
                SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
            alchemist_i_text = dialogue_font.render("Alchemist's Stock", True,
                                                    WHITE)
            screen.blit(alchemist_i_text,
                        (150 - alchemist_i_text.get_width() // 2, 150))
            cells = draw_grid(IVORY, 50, 200, alchemist.inventory)
        elif show_character_inventory:
            sell_button = draw_button("Sell", SCREEN_WIDTH // 2 - 100,
                                      SCREEN_HEIGHT - 100, 200, 50)
            character_i_text = dialogue_font.render("Your Inventory", True, WHITE)
            screen.blit(character_i_text,
                        (150 - character_i_text.get_width() // 2, 150))
            cells = draw_grid(IVORY, 50, 200, selected_character.inventory)
        money_surf = dialogue_font.render(
            f"Gold amount: {selected_character.gold_amount}", True, IVORY)
        money_rect = money_surf.get_rect(center=(120, 80))
        screen.blit(money_surf, money_rect)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == BLACKSMITH:
        screen.blit(forge, (0, 0))
        if current_blacksmith_dialogue:
            blacksmith_text = dialogue_font.render(current_blacksmith_dialogue,
                                                   True, IVORY)
            screen.blit(blacksmith_text,
                        (SCREEN_WIDTH // 2 - blacksmith_text.get_width() // 2, 1))
        back_button = draw_button("Back to Town", 600, 550, 200, 50)
        show_inventory_button = draw_button("Buy items", 600, 200, 200, 50)
        sell_item_button = draw_button("Sell items", 600, 270, 200, 50)
        cells = []
        if show_blacksmith_inventory:
            buy_button = draw_button(
                "Buy" if selected_character.gold_amount >= 5 else "Not enough gold",
                SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
            blacksmith_i_text = dialogue_font.render("Blacksmith's Stock", True,
                                                     BLACK)
            screen.blit(blacksmith_i_text,
                        (150 - blacksmith_i_text.get_width() // 2, 150))
            cells = draw_grid(IVORY, 50, 200, blacksmith.inventory)
        elif show_character_inventory:
            sell_button = draw_button("Sell", SCREEN_WIDTH // 2 - 100,
                                      SCREEN_HEIGHT - 100, 200, 50)
            character_i_text = dialogue_font.render("Your Inventory", True, BLACK)
            screen.blit(character_i_text,
                        (150 - character_i_text.get_width() // 2, 150))
            cells = draw_grid(IVORY, 50, 200, selected_character.inventory)
        money_surf = dialogue_font.render(
            f"Gold amount: {selected_character.gold_amount}", True, IVORY)
        money_rect = money_surf.get_rect(center=(120, 80))
        screen.blit(money_surf, money_rect)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == TAVERN:
        screen.blit(tavern, (0, 0))
        if current_saloon_keeper_dialogue:
            saloon_keeper_text = dialogue_font.render(
                current_saloon_keeper_dialogue, True, IVORY)
            screen.blit(saloon_keeper_text, (
            SCREEN_WIDTH // 2 - saloon_keeper_text.get_width() // 2, 1))
        back_button = draw_button("Back to Town", 600, 550, 200, 50)
        sleep_button_rect = draw_button("Rent a room", 600, 270, 200, 50)
        if show_sleep_popup:
            draw_tavern_popup()
        if sleep_message:
            message_surface = button_font.render(sleep_message, True, IVORY)
            screen.blit(message_surface, (
            SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 500))
            if pygame.time.get_ticks() - message_time > MESSAGE_LIFETIME:
                sleep_message = ""
                message_time = None
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == PROFILE:
        starting_y = 450
        lines_spacing = 2  # Distance between rows
        cells = []
        if selected_character:
            stat_name = get_stat_name(selected_character)
            stats = [f"Name: {player_name}",
                     f"Health: {selected_character.health}",
                     f"{stat_name}: {selected_character.attack}",
                     f"Armor: {selected_character.armor}",
                     f"Mana: {selected_character.mana}/{selected_character.max_mana}",
                     f"Stamina: {selected_character.stamina}/{selected_character.max_stamina}"]
            stats_width = max(stats_font.size(stat)[0] for stat in stats)
            total_height = sum(stats_font.get_height() for stat in stats) + (
                        len(stats) + 9) * lines_spacing
            stats_rect = pygame.Rect(SCREEN_WIDTH // 2 - stats_width // 2 + 38,
                                     starting_y, stats_width + 15, total_height)
            if selected_character == characters[0]:  # Barbarian
                screen.fill(DARK_GREY)
                border_color = RED
                screen.blit(barbarian_img, barbarian_rect)
                pygame.draw.rect(screen, border_color, berserk_rect)
                screen.blit(berserk_img, (SCREEN_WIDTH // 2 + 180, 305))
                berserk_text = button_font.render(
                    f"{selected_character.special_ability}", True, IVORY)
                screen.blit(berserk_text, (SCREEN_WIDTH // 2 + 245, 316))
                # Inventory grid
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items,
                                  selected_character)
            elif selected_character == characters[1]:  # Wizard
                screen.fill(BROWN)
                border_color = LIGHT_BLUE
                screen.blit(wizard_img, rogue_rect)
                pygame.draw.rect(screen, border_color, fireball_rect)
                screen.blit(fireball_img, (SCREEN_WIDTH // 2 + 180, 305))
                fireball_text = button_font.render(
                    f"{selected_character.special_ability}", True, IVORY)
                screen.blit(fireball_text, (SCREEN_WIDTH // 2 + 245, 316))
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items,
                                  selected_character)
            elif selected_character == characters[2]:  # Rogue
                screen.fill(BROWN)
                border_color = DARK_GREY
                screen.blit(rogue_img, rogue_rect)
                pygame.draw.rect(screen, border_color, stab_rect)
                screen.blit(stab_img, (SCREEN_WIDTH // 2 + 180, 305))
                stab_text = button_font.render(
                    f"{selected_character.special_ability}", True, IVORY)
                screen.blit(stab_text, (SCREEN_WIDTH // 2 + 245, 316))
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items,
                                  selected_character)
            elif selected_character == characters[3]:  # Paladin
                screen.fill(BROWN)
                border_color = LIGHT_BROWN
                screen.blit(paladin_img, paladin_rect)
                pygame.draw.rect(screen, border_color, heal_rect)
                screen.blit(heal_img, (SCREEN_WIDTH // 2 + 180, 305))
                heal_text = button_font.render(
                    f"{selected_character.special_ability}", True, IVORY)
                screen.blit(heal_text, (SCREEN_WIDTH // 2 + 245, 316))
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items,
                                  selected_character)
            elif selected_character == characters[4]:  # Necromancer
                screen.fill(DARKER_GREY)
                border_color = DARK_GREEN
                screen.blit(necromancer_img, necromancer_rect)
                pygame.draw.rect(screen, border_color, reanimate_rect)
                screen.blit(reanimate_img, (SCREEN_WIDTH // 2 + 180, 305))
                reanimate_text = button_font.render(
                    f"{selected_character.special_ability}", True, IVORY)
                screen.blit(reanimate_text, (SCREEN_WIDTH // 2 + 245, 316))
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items,
                                  selected_character)
            else:
                border_color = BLUE
                cells = draw_grid(border_color, 0, 200,
                                  selected_character.inventory,
                                  selected_character.equipped_items)

                # Draw stats
            for i, stat in enumerate(stats):
                stat_text = stats_font.render(stat, True, IVORY)
                screen.blit(stat_text,
                            (SCREEN_WIDTH // 2 + 45 - stat_text.get_width() // 2,
                             starting_y + i * (
                                         lines_spacing + button_font.get_height())))
            back_button = draw_button("Back to Town", 600, 550, 200, 50)
            to_explore_button = draw_button("To Explore", 600, 490, 200, 50)
            pygame.draw.rect(screen, border_color, stats_rect, 3, border_radius=10)
            # Coin icon
            pygame.draw.rect(screen, border_color, coin_rect, 3, border_radius=10)
            screen.blit(coin_img, (SCREEN_WIDTH // 2 + 180, 185))
            coin_text = depiction_font.render(f"{selected_character.gold_amount}",
                                              True, IVORY)
            screen.blit(coin_text, (SCREEN_WIDTH // 2 + 245, 190))
            # Level icon
            pygame.draw.rect(screen, border_color, level_icon_rect, 3,
                             border_radius=10)
            screen.blit(level_icon, (SCREEN_WIDTH // 2 + 180, 245))
            level_text = depiction_font.render(f"{selected_character.level}", True,
                                               IVORY)
            screen.blit(level_text, (SCREEN_WIDTH // 2 + 245, 250))
            screen.blit(profile_title_surf, profile_title_rect)
            screen.blit(inventory_surf, inventory_rect)
            # XP icon
            pygame.draw.rect(screen, border_color, xp_rect, 3, border_radius=10)
            screen.blit(xp_img, (SCREEN_WIDTH // 2 + 180, 365))
            xp_text = (depiction_font.render
                       (f"{selected_character.xp} / {selected_character.xp_to_next_level}",
                        True, IVORY))
            screen.blit(xp_text, (SCREEN_WIDTH // 2 + 245, 370))
            screen.blit(profile_title_surf, profile_title_rect)
            screen.blit(inventory_surf, inventory_rect)
            # Special ability depiction
            ability_desc = item_font.render(
                selected_character.special_ability_depiction, True, IVORY)
            screen.blit(ability_desc, (1, 480))
            screen.blit(cursor_surf, cursor_rect)

    elif game_state == EXPLORE:
        screen.blit(map_img, (0, 0))
        back_button = draw_button("Back to Town", 600, 550, 200, 50)
        battle_button_enchanted = draw_battle_button(550, 330, 100, 25)
        battle_button_dark_forest = draw_battle_button(230, 280, 100, 25)
        battle_button_cemetery = draw_battle_button(40, 320, 100, 25)
        battle_button_ruin = draw_battle_button(320, 130, 100, 25)
        battle_button_peak = draw_battle_button(700, 50, 100, 25)
        battle_button_sunken = draw_battle_button(670, 480, 100, 25)
        gate_button = draw_gate_button(65, 75, 100, 25)
        cross_button = draw_cross_button(260, 50, 100, 25)
        bag_button = draw_bag_button(500, 550, 50, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == CONFIRM_EXIT:
        screen.fill(DARK_GREY)
        confirm_text = font.render("Are you sure?", True, BLACK)
        screen.blit(confirm_text,
                    (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, 100))
        draw_button("Yes", 300, 250, 200, 50)
        draw_button("No", 300, 320, 200, 50)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == NAME_INPUT:
        screen.fill(DARK_GREY)
        title_text = font.render("Enter your name: ", True, BLACK)
        screen.blit(title_text,
                    (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, input_box, 3, border_radius=10)
        name_surface = font.render(player_name, True, BLUE)
        screen.blit(name_surface, (SCREEN_WIDTH // 2 - 100, 250))
        instructions = font.render("Press ENTER to confirm", True, BLACK)
        screen.blit(instructions,
                    (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 500))
        screen.blit(cursor_surf, cursor_rect)

    elif game_state in [ENCHANTED_FOREST, CEMETERY, DARK_FOREST, HAUNTED_RUIN,
                        FROSTFANG_PEAK, SUNKEN_TEMPLE]:
        if game_state == ENCHANTED_FOREST:
            screen.blit(enchanted_img, (0, 0))
            draw_location_level(screen, 4, WHITE)
        elif game_state == DARK_FOREST:
            screen.blit(dark_forest_img, (0, 0))
            draw_location_level(screen, 2, ORANGE)
        elif game_state == CEMETERY:
            screen.blit(cemetery_img, (0, 0))
            draw_location_level(screen, 1, ORANGE)
        elif game_state == HAUNTED_RUIN:
            screen.blit(ruin_img, (0, 0))
            draw_location_level(screen, 3, ORANGE)
        elif game_state == FROSTFANG_PEAK:
            screen.blit(frost_peak_img, (0, 0))
            draw_location_level(screen, 5, BLUE)
        elif game_state == SUNKEN_TEMPLE:
            screen.blit(sunken_temple_img, (0, 0))
            draw_location_level(screen, 6, ORANGE)
        back_button = draw_button("Back to Explore", 600, 550, 200, 50)
        show_enemies_button = draw_button(
            "Show Enemies" if not show_enemies else "Hide enemies",
            600, 480, 200, 50)
        if show_enemies:
            enemy_rects = draw_enemies(game_state)
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == CHAPEL:
        screen.blit(chapel_img, (0, 0))
        chapel_text = dialogue_font.render(
            "Within these walls, all find peace, safe from evil.", True, IVORY)
        screen.blit(chapel_text,
                    (SCREEN_WIDTH // 2 - chapel_text.get_width() // 2, 1))
        back_button = draw_button("Back to Explore", 600, 550, 200, 50)
        draw_button("Bless", 600, 400, 200, 50)
        if bless_message:
            message_surface = button_font.render(bless_message, True, IVORY)
            screen.blit(message_surface, (
            SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 500))
            if pygame.time.get_ticks() - message_time > MESSAGE_LIFETIME:
                bless_message = ""
                message_time = None
        screen.blit(cursor_surf, cursor_rect)

    elif game_state == BATTLE:
        draw_battle_ui(screen, selected_character, selected_enemy)
        draw_health_bar(screen, 60, 420, selected_character.health,
                        selected_character.max_health)
        draw_enemy_attack_point(screen, selected_enemy.attack)
        if selected_character == characters[0]:
            draw_hero_attack_and_armor(screen, selected_character.attack,
                                       selected_character.armor)
        if selected_character == characters[2]:
            draw_dodge_chance(screen, 20, 520)
        if selected_character == characters[0] or selected_character == characters[
            2]:
            draw_stamina_bar(screen, 60, 470, selected_character.stamina,
                             selected_character.max_stamina)
        else:
            draw_mana_bar(screen, 60, 470, selected_character.mana,
                          selected_character.max_mana)
        if selected_enemy:  # Draw enemy with health bar
            draw_health_bar(screen, 590, 420, selected_enemy.health,
                            selected_enemy.max_health)
            screen.blit(selected_enemy.img_for_battle, (530, 150))
        draw_battle_popup(selected_character, selected_enemy)
        if selected_enemy.health <= 0:
            draw_looting(screen, selected_enemy.gold_drop_range,
                         selected_enemy.xp_reward, selected_enemy.loot_table)
        # is_victory = False
        # is_defeat = False
        screen.blit(cursor_surf, cursor_rect)
"""