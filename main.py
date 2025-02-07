import pygame, sys
from game import Game
from colors import Colors

# features:
# - count score and highscore
# - change blocks and background colors (by pre-defined schemes or by hand)
# - choose difficulty (change game loop interval)

# TODO:
#  - spawn blocks above the grid (?)
#  - fix score addition for 4 and more lines cleared
#  - (done) - fix crash when rotating a block near the edge
#  - fix crash when rotating a block near the bottom
#  - fix block overlap when rotating near another block
#  - add settings menu for changing music, sound effects, and background color
#  - add pause menu
#  - add high score
#  - (wip) show main menu before starting the game
#  - add better game over screen
#  - add animations for clearing rows (?)

pygame.init()

# initialize screen and clock
screen = pygame.display.set_mode((1000, 1240))
pygame.display.set_caption("Pygame Tetris")
clock = pygame.time.Clock()

# fonts
title_font = pygame.font.Font(None, 80)

# text surfaces
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# ui elements
score_rect = pygame.Rect(640, 110, 340, 120)
next_rect = pygame.Rect(640, 430, 340, 360)

# game instance
game = Game()

# custom user event
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center = (x, y))
    surface.blit(text_obj, text_rect)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over: # restart game after key press
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()
            if event.key == pygame.K_DOWN and not game.game_over:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (730, 40, 100, 100))
    screen.blit(next_surface, (750, 250, 100, 100))

    if game.game_over:
        screen.blit(game_over_surface, (640, 900, 100, 100))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
                                                                  centery = score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)