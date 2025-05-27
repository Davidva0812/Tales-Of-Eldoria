import random, sys
from UI import *


start_button_rect = pygame.Rect(300, 250, 200, 50)
load_button_rect = pygame.Rect(300, 320, 200, 50)
sounds_button_rect = pygame.Rect(300, 390, 200, 50)
sleep_button_rect = pygame.Rect(300, 200, 100, 30)
back_button_rect = pygame.Rect(600, 550, 200, 50)
back_to_menu_button_rect = pygame.Rect(600, 550, 200, 50)
exit_button_rect = pygame.Rect(300, 460, 200, 50)
mute_button_rect = pygame.Rect(300, 250, 200, 50)
vol_button_1_rect = pygame.Rect(300, 320, 200, 50)
vol_button_2_rect = pygame.Rect(300, 390, 200, 50)
lab_button_rect = pygame.Rect(600, 60, 200, 50)
blacksmith_button_rect = pygame.Rect(600, 130, 200, 50)
tavern_button_rect = pygame.Rect(600, 200, 200, 50)
profile_button_rect = pygame.Rect(600, 340, 200, 50)
explore_button_rect = pygame.Rect(600, 410, 200, 50)
#buy_button_rect =
cursor_surf = pygame.image.load(
    "assets/images/other/cursor_shiny.png").convert_alpha()
show_sleep_popup = False
show_alchemist_inventory = show_blacksmith_inventory = show_character_inventory = False
selected_character = None
sleep_message = ""
message_time = None
explore_music_playing = battle_music_playing = mute = show_enemies = False
game_state = MENU  # At the beginning, the menu will appear


class GameState:
    def __init__(self):
        self.running = True
        self.state = MENU
        self.player_name = ""
        self.selected_character = None
        self.adventure_music_playing = False
        self.explore_music_playing = False
        self.chapel_music_playing = False

    def handle_events(self):
        global cursor_rect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEMOTION:
                offset_x = - 2
                offset_y = - 2
                cursor_rect = cursor_surf.get_rect(
                    topleft=(event.pos[0] + offset_x, event.pos[1] + offset_y))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            if self.state == NAME_INPUT and event.type == pygame.KEYDOWN:
                self.handle_name_input(event)

    def handle_mouse_click(self, pos):
        if self.state == MENU:
            self.menu_click(pos)
        elif self.state == CHARACTER_SELECT:
            self.character_select_click(pos)
        elif self.state == TOWN:
            self.town_click(pos)
        elif self.state in [ALCHEMIST_LABORATORY, BLACKSMITH, TAVERN, PROFILE, EXPLORE]:
            self.back_to_town_click(pos)
        elif self.state == CONFIRM_EXIT:
            self.confirm_exit_click(pos)
        elif self.state == CHARACTER_SELECT:
            self.back_to_menu_clink(pos)

    def handle_name_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.player_name:
                self.state = TOWN
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                if len(self.player_name) < 12:
                    self.player_name += event.unicode

    def menu_click(self, pos):
        if start_button_rect.collidepoint(pos):
            self.state = CHARACTER_SELECT
        elif exit_button_rect.collidepoint(pos):
            self.state = CONFIRM_EXIT

    def character_select_click(self, pos):
        for i, character in enumerate(["Warrior", "Mage", "Rogue"]):
            char_button = pygame.Rect(300, 150 + i * 60, 200, 50)
            if char_button.collidepoint(pos):
                self.selected_character = character
                self.state = NAME_INPUT
                self.player_name = ""

    def town_click(self, pos):
        """Town interactions"""
        if lab_button_rect.collidepoint(pos):
            self.state = ALCHEMIST_LABORATORY
        elif blacksmith_button_rect.collidepoint(pos):
            self.state = BLACKSMITH
        elif tavern_button_rect.collidepoint(pos):
            self.state = TAVERN
        elif profile_button_rect.collidepoint(pos):
            self.state = PROFILE
        elif explore_button_rect.collidepoint(pos):
            self.state = EXPLORE

    def back_to_town_click(self, pos):
        if back_button_rect.collidepoint(pos):
            self.state = TOWN

    def back_to_menu_clink(self, pos):
        if back_to_menu_button_rect.collidepoint(pos):
            self.state = MENU

    def confirm_exit_click(self, pos):
        yes_button = pygame.Rect(300, 250, 200, 50)
        no_button = pygame.Rect(300, 320, 200, 50)
        if yes_button.collidepoint(pos):
            self.running = False
        elif no_button.collidepoint(pos):
            self.state = MENU

    def draw(self):
        screen.fill(BROWN)
        if self.state == MENU:
            title_text = font.render("Tales Of Eldoria", True, BLUE)
            text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            border_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10,
                                      text_rect.width + 20,
                                      text_rect.height + 20)
            pygame.draw.rect(screen, (120, 120, 120), border_rect,
                             border_radius=15)
            pygame.draw.rect(screen, LIGHT_BROWN, border_rect, 5,
                             border_radius=15)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            draw_button("Start Game", 300, 250, 200, 50)
            draw_button("Load Game", 300, 320, 200, 50)
            draw_button("Audio", 300, 390, 200, 50)
            draw_button("Exit Game", 300, 460, 200, 50)
            screen.blit(cursor_surf, cursor_rect)

        elif self.state == CHARACTER_SELECT:
            screen.blit(char_select_bg, (0, 0))
            title_text = font.render("Choose Your Character", True, IVORY)
            screen.blit(title_text,
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
            for i, character in enumerate(characters):
                draw_button(character.name, 300, 150 + i * 60, 200, 50)
            if hovered_character:
                description_text = depiction_font.render(f"{hovered_character.depiction}", True, BLACK)
                screen.blit(description_text,
                            (SCREEN_WIDTH // 2 - description_text.get_width() // 2, 500))
            draw_button("Back to Menu", 600, 550, 200, 50)
            screen.blit(cursor_surf, cursor_rect)

        elif self.state == NAME_INPUT:
            screen.fill(DARK_GREY)
            title_text = font.render("Enter your name: ", True, BLACK)
            screen.blit(title_text,
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
            pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
            pygame.draw.rect(screen, BLACK, input_box, 3, border_radius=10)
            name_surface = font.render(self.player_name, True, BLUE)
            screen.blit(name_surface, (SCREEN_WIDTH // 2 - 100, 250))
            instructions = font.render("Press ENTER to confirm", True, BLACK)
            screen.blit(instructions, (
            SCREEN_WIDTH // 2 - instructions.get_width() // 2, 500))
            screen.blit(cursor_surf, cursor_rect)

        elif self.state == TOWN:
            screen.blit(town_bg, (0, 0))
            selected_char_text = font.render(f"Welcome, {self.player_name}!", True, BLUE)
            screen.blit(selected_char_text, (
                SCREEN_WIDTH // 2 - selected_char_text.get_width() // 2, 1))
            draw_button("Laboratory", 600, 60, 200, 50)
            draw_button("Blacksmith", 600, 130, 200, 50)
            draw_button("Tavern", 600, 200, 200, 50)
            draw_button("Profile", 600, 340, 200, 50)
            draw_button("Explore", 600, 410, 200, 50)
            screen.blit(cursor_surf, cursor_rect)

        elif self.state == CONFIRM_EXIT:
            screen.fill(GRAY)
            confirm_text = font.render("Are you sure?", True, BLACK)
            screen.blit(confirm_text, (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, 100))
            draw_button("Yes", 300, 250, 200, 50)
            draw_button("No", 300, 320, 200, 50)
            screen.blit(cursor_surf, cursor_rect)

        pygame.display.update()


game = GameState()
while game.running:
    game.handle_events()
    game.draw()

pygame.quit()
sys.exit()
