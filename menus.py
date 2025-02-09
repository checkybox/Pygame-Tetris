import pygame, sys

from colors import Colors
from fonts import Fonts

# button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_COLOR = Colors.light_blue
BUTTON_HOVER_COLOR = Colors.white
TEXT_COLOR = Colors.dark_blue

# this function draws centered text (i guess)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# this function draws a button
def draw_button(text, x, y, width, height, screen, font):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    draw_text(text, font, TEXT_COLOR, screen, x + width // 2, y + height // 2)
    return button_rect

def settings_menu(screen, game, SCREEN_WIDTH):
    running = True
    while running:
        screen.fill(Colors.dark_blue)
        draw_text("Settings", Fonts.press_2p(120), Colors.white, screen, SCREEN_WIDTH // 2, 300)

        # draw buttons
        if game.is_music_on:
            music_toggle = draw_button("Music:ON", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        else:
            music_toggle = draw_button("Music:OFF", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_score(game.score)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and music_toggle.collidepoint(event.pos):
                game.toggle_music()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def pause_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH, paused):
    bounce_offset = 0
    bounce_direction = 15

    while paused:
        screen.fill(Colors.dark_blue)
        draw_text("PAUSED", Fonts.press_2p(120), Colors.white, screen, SCREEN_WIDTH // 2, 300 + bounce_offset)

        # draw buttons
        continue_button = draw_button("Continue", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        settings_button = draw_button("Settings", 350 - 50, 550, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        help_button = draw_button("Help", 350 - 50, 650, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        quit_button = draw_button("Quit", 350 - 50, 750, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_score(game.score)
                pygame.quit()
                sys.exit()

            # unpause on escape
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

            # mouse button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    paused = False
                elif settings_button.collidepoint(event.pos):
                    settings_menu(screen, game, SCREEN_WIDTH)
                elif help_button.collidepoint(event.pos):
                    print("Help menu placeholder")
                elif quit_button.collidepoint(event.pos):
                    game.save_score(game.score)
                    pygame.quit()
                    sys.exit()

            # bounce animation
            if event.type == BOUNCE_UPDATE:
                if bounce_offset >= 15:
                    bounce_direction = -15
                elif bounce_offset <= -15:
                    bounce_direction = 15
                bounce_offset += bounce_direction

def main_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH):
    bounce_offset = 0
    bounce_direction = 15

    while True:
        screen.fill(Colors.dark_blue)
        draw_text("TETRIS", Fonts.press_2p(120), Colors.white, screen, 500, 300 + bounce_offset)
        play_button = draw_button("Play", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        settings_button = draw_button("Settings", 350 - 50, 550, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        help_button = draw_button("Help", 350 - 50, 650, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))
        quit_button = draw_button("Quit", 350 - 50, 750, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, Fonts.press_2p(40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_score(game.score)
                pygame.quit()
                sys.exit()

            # mouse button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return
                elif settings_button.collidepoint(event.pos):
                    settings_menu(screen, game, SCREEN_WIDTH)
                elif help_button.collidepoint(event.pos):
                    print("Help menu placeholder")
                elif quit_button.collidepoint(event.pos):
                    game.save_score(game.score)
                    pygame.quit()
                    sys.exit()

            # bounce animation
            if event.type == BOUNCE_UPDATE:
                if bounce_offset >= 15:
                    bounce_direction = -15
                elif bounce_offset <= -15:
                    bounce_direction = 15
                bounce_offset += bounce_direction