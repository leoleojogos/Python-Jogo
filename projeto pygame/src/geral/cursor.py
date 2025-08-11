
import pygame

from src.objetos.sprite import HudSpriteEstatico

class Cursor(HudSpriteEstatico):

    __instance = None
    def __new__(cls, *args, **kwargs):
        if (cls.__instance == None):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__(pygame.Vector2(0, 0), './assets/cursor/frame0.png', 1)
    
    def atualizar(self):
        self.posicao = pygame.Vector2(pygame.mouse.get_pos())

