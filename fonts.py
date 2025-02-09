import pygame, os

class Fonts:
    #returns basic font with specified size
    @classmethod
    def basic(cls, size):
        return pygame.font.Font(None, size = 40)

    # returns press_2p font with specified size
    @classmethod
    def press_2p(cls, size = 40):
        cwd = os.getcwd()
        return pygame.font.Font(f"{cwd}/assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", size)