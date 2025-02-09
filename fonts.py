import pygame, os

class Fonts:
    @classmethod
    def basic(cls, size):
        return pygame.font.Font(None, size)

    @classmethod
    def press_2p(cls, size):
        cwd = os.getcwd()
        return pygame.font.Font(f"{cwd}/assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", size)