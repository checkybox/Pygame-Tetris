import pygame, sys, os

from game import Game
from colors import Colors
from fonts import Fonts
from menus import draw_text, draw_button, pause_menu, main_menu, game_over_menu

pygame.init()

# this allows for holding down keys
pygame.key.set_repeat(300, 75)

# initialize screen and clock
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Tetris")
clock = pygame.time.Clock()

# initialize text surfaces
score_surface = Fonts.press_2p(40).render("Score", True, Colors.white)
highscore_surface = Fonts.press_2p(40).render("Highscore", True, Colors.white)
next_surface = Fonts.press_2p(40).render("Next", True, Colors.white)

# draw ui elements
score_rect = pygame.Rect(640, 110, 340, 120)
highscore_rect = pygame.Rect(640, 330, 340, 120)
next_rect = pygame.Rect(640, 630, 340, 360)

# initialize game instance and timers
game = Game()
GAME_UPDATE = pygame.USEREVENT
BOUNCE_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, game.difficulty_ms)
pygame.time.set_timer(BOUNCE_UPDATE, 1000)

# save pause state
paused = False

# button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_COLOR = Colors.light_blue
BUTTON_HOVER_COLOR = Colors.white
TEXT_COLOR = Colors.dark_blue

# run the main menu first
main_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH, GAME_UPDATE)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_score(game.score)
            pygame.quit()
            sys.exit()

        # game over handler
        # when game_over is false, it tries to save the score
        # by calling game.save_score(game.score)
        # next it calls the game_over_menu function which handles the rest
        if game.game_over:
            game.save_score(game.score)
            game_over_menu(screen, game, BUTTON_WIDTH, BUTTON_HEIGHT, SCREEN_WIDTH)

        if event.type == pygame.KEYDOWN:
            # pause button handler
            if event.key == pygame.K_ESCAPE:
                paused = True
                pause_menu(screen, game, BOUNCE_UPDATE, SCREEN_WIDTH, GAME_UPDATE, paused)

            # game controls handler
            # works for both arrows and wasd
            if not game.game_over:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move_right()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.move_down()
                    game.update_score(0, game.move_down_points)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.rotate()

        # this makes the block go downwards by itself
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # drawing
    # if score is higher than highscore, display score instead
    score_value_surface = Fonts.press_2p(40).render(str(game.score), True, Colors.white)
    if not game.score > game.highscore:
        highscore_value_surface = Fonts.press_2p(40).render(str(game.highscore), True, Colors.white)
    else:
        highscore_value_surface = Fonts.press_2p(40).render(str(game.score), True, Colors.white)

    # display surfaces
    screen.fill(Colors.darkish_blue)
    screen.blit(score_surface, (710, 40, 100, 100))
    screen.blit(highscore_surface, (630, 260, 100, 100))
    screen.blit(next_surface, (730, 550, 100, 100))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))

    pygame.draw.rect(screen, Colors.light_blue, highscore_rect, 0, 10)
    screen.blit(highscore_value_surface, highscore_value_surface.get_rect(centerx = highscore_rect.centerx, centery = highscore_rect.centery))

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)