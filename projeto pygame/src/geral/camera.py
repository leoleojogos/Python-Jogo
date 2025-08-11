
import pygame
import math

from src.geral.game import Game

class Camera():
    @classmethod
    def iniciar(cls):
        cls.posicao = pygame.Vector2(0, 0)

    @classmethod
    def setarPosicao(cls, posicao: pygame.Vector2):
        posClamp = pygame.Vector2(posicao)
        posClamp.x -= Game.tamanho[0] / 2
        posClamp.y -= Game.tamanho[1] / 2

        posClamp.x = max(min(posClamp.x, 550), 0)
        posClamp.y = max(min(posClamp.y, 550), 0)

        cls.posicao = cls.posicao + 0.15*(posClamp - cls.posicao)
