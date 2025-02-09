import pygame, random

from grid import Grid
from blocks import *

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.highscore = 0
        self.difficulty = 0
        self.difficulty_ms = 500
        self.points_modifier = 100
        self.move_down_points = 1
        self.is_music_on = True
        self.is_sounds_on = True

        # initialize rotate, clear, and game over sounds
        self.rotate_sound = pygame.mixer.Sound("assets/sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("assets/sounds/clear.ogg")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")

        # load main menu music
        pygame.mixer.music.load("assets/sounds/music.ogg")
        pygame.mixer.music.play(-1)

        # load highscore on game initialization
        self.highscore = self.load_highscore()

        self.is_music_on_states = {
            True: "Music:ON",
            False: "Music:OFF"
        }

        self.is_sounds_on_states = {
            True: "Sounds:ON",
            False: "Sounds:OFF"
        }

        self.difficulty_states = {
            0: "Mode:Easy",
            1: "Mode:Medium",
            2: "Mode:Hard"
        }

    def toggle_music(self):
        if self.is_music_on:
            self.is_music_on = False
            pygame.mixer.music.stop()
        else:
            self.is_music_on = True
            pygame.mixer.music.load("assets/sounds/music.ogg")
            pygame.mixer.music.play(-1)

    def toggle_sounds(self):
        if self.is_sounds_on:
            self.is_sounds_on = False
        else:
            self.is_sounds_on = True

    def toggle_difficulty(self):
        if self.difficulty == 0:
            self.difficulty = 1
            self.difficulty_ms = 400
        elif self.difficulty == 1:
            self.difficulty = 2
            self.difficulty_ms = 300
        elif self.difficulty == 2:
            self.difficulty = 0
            self.difficulty_ms = 500
        return self.difficulty_ms

    def update_score(self, lines_cleared, move_down_points):
        if self.difficulty == 0:
            self.points_modifier = 100
        elif self.difficulty == 1:
            self.points_modifier = 125
        elif self.difficulty == 2:
            self.points_modifier = 150

        if lines_cleared > 0:
            self.score += int(self.points_modifier * (2 ** (lines_cleared - 1)))
        self.score += move_down_points

    # def save_highscore(self):
    #     with open("highscore.txt", "w") as file:
    #         file.write(str(self.score))

    def save_score(self, score):
        if self.score > self.highscore:
            with open("highscore.txt", "w") as file:
                file.write(str(self.score))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)
            if self.is_sounds_on:
                self.clear_sound.play()
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.highscore = self.load_highscore()

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            if self.is_sounds_on:
                self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 22, 22)

        # if next block is IBlock
        if self.next_block.id == 3:
            self.next_block.draw(screen, 510, 780)
        # if next block is OBlock
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 510, 760)
        else:
            self.next_block.draw(screen, 540, 740)