import pygame, sys
from colors import Colors
from game import Game

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

def pause_menu(screen, game, press_2p_120f, press_2p_40f, BOUNCE_UPDATE, SCREEN_WIDTH, paused):
    bounce_offset = 0
    bounce_direction = 15

    while paused:
        screen.fill(Colors.dark_blue)
        draw_text("PAUSED", press_2p_120f, Colors.white, screen, SCREEN_WIDTH // 2, 300 + bounce_offset)

        # draw buttons
        continue_button = draw_button("Continue", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen,
                                      press_2p_40f)
        settings_button = draw_button("Settings", 350 - 50, 550, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen,
                                      press_2p_40f)
        quit_button = draw_button("Quit", 350 - 50, 650, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, press_2p_40f)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if game.score > game.load_highscore():
                    game.save_highscore()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    paused = False
                elif settings_button.collidepoint(event.pos):
                    print("Settings menu placeholder")
                elif quit_button.collidepoint(event.pos):
                    if game.score > game.load_highscore():
                        game.save_highscore()
                    pygame.quit()
                    sys.exit()

            # bounce animation
            if event.type == BOUNCE_UPDATE:
                if bounce_offset >= 15:
                    bounce_direction = -15
                elif bounce_offset <= -15:
                    bounce_direction = 15
                bounce_offset += bounce_direction

def main_menu(screen, game, press_2p_120f, press_2p_40f, BOUNCE_UPDATE):
    bounce_offset = 0
    bounce_direction = 15

    while True:
        screen.fill(Colors.dark_blue)
        draw_text("TETRIS", press_2p_120f, Colors.white, screen, 500, 300 + bounce_offset)
        play_button = draw_button("Play", 350 - 50, 450, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, press_2p_40f)
        settings_button = draw_button("Settings", 350 - 50, 550, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen,press_2p_40f)
        quit_button = draw_button("Quit", 350 - 50, 650, BUTTON_WIDTH + 100, BUTTON_HEIGHT, screen, press_2p_40f)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if game.score > game.load_highscore():
                    game.save_highscore()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            # bounce animation
            if event.type == BOUNCE_UPDATE:
                if bounce_offset >= 15:
                    bounce_direction = -15
                elif bounce_offset <= -15:
                    bounce_direction = 15
                bounce_offset += bounce_direction