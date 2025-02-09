import pygame, sys, os

from game import Game
from colors import Colors
from menus import draw_text, draw_button, pause_menu, main_menu

# TODO:
#  - features:
#  - (done) - count score and highscore
#  - change blocks and background colors (by pre-defined schemes or by hand)
#  - choose difficulty (change game loop interval)
#  -
#  - ability to turn off music/sounds
#  - spawn blocks above the grid (?)
#  - (done) - fix score addition for 4 and more lines cleared
#  - (done) - fix crash when rotating a block near the edge
#  - fix crash when rotating a block near the bottom
#  - fix block overlap when rotating near another block
#  - add settings menu for changing music, sound effects, and background color
#  - (wip) add pause menu
#  - (done) show main menu before starting the game
#  - add better game over screen
#  - add animations for clearing rows (?)

pygame.init()

# this allows for holding down keys
pygame.key.set_repeat(300, 75)

# initialize screen and clock
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Tetris")
clock = pygame.time.Clock()

# fonts
press_2p_120f = pygame.font.Font(f"{os.getcwd()}/assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 120)
press_2p_80f = pygame.font.Font(f"{os.getcwd()}/assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 120)
press_2p_40f = pygame.font.Font(f"{os.getcwd()}/assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 40)
title_f = pygame.font.Font(None, 80)
menu_f = pygame.font.Font(None, 120)

# text surfaces
score_surface = press_2p_40f.render("Score", True, Colors.white)
highscore_surface = press_2p_40f.render("Highscore", True, Colors.white)
next_surface = press_2p_40f.render("Next", True, Colors.white)
game_over_surface = press_2p_40f.render("GAME OVER", True, Colors.white)

# ui elements
score_rect = pygame.Rect(640, 110, 340, 120)
highscore_rect = pygame.Rect(640, 330, 340, 120)
next_rect = pygame.Rect(640, 630, 340, 360)

# game instance
game = Game()
GAME_UPDATE = pygame.USEREVENT
BOUNCE_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, 500)
pygame.time.set_timer(BOUNCE_UPDATE, 1000)

# pause state
paused = False

# button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_COLOR = Colors.light_blue
BUTTON_HOVER_COLOR = Colors.white
TEXT_COLOR = Colors.dark_blue

# run the main menu first
main_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_score(game.score)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # pause button handler
            if event.key == pygame.K_ESCAPE:
                paused = True
                pause_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH, paused)

            # game over handler
            if game.game_over:
                game.save_score(game.score)
                game.game_over = False
                game.reset()

            # game controls handler
            if not game.game_over:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move_right()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.move_down()
                    game.update_score(0, 1)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.rotate()

        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # drawing
    # if score is higher than highscore, display score instead
    score_value_surface = title_f.render(str(game.score), True, Colors.white)
    if not game.score > game.highscore:
        highscore_value_surface = title_f.render(str(game.highscore), True, Colors.white)
    else:
        highscore_value_surface = title_f.render(str(game.score), True, Colors.white)

    screen.fill(Colors.darkish_blue)
    screen.blit(score_surface, (710, 40, 100, 100))
    screen.blit(highscore_surface, (630, 260, 100, 100))
    screen.blit(next_surface, (730, 550, 100, 100))

    if game.game_over:
        screen.blit(game_over_surface, (640, 1200, 100, 100))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))

    pygame.draw.rect(screen, Colors.light_blue, highscore_rect, 0, 10)
    screen.blit(highscore_value_surface, highscore_value_surface.get_rect(centerx = highscore_rect.centerx, centery = highscore_rect.centery))

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)