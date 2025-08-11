

import pygame
import random

from src.geral.game import Game

from src.objetos.sprite import SpriteAnimado

class InimigoMorte(SpriteAnimado):
    def __init__(self, posicao):
        angulo = random.randint(0, 359)
        super().__init__(posicao, './assets/inimigoMorte/inimigoMorte*.png', 2, 10, angulo)

    def aoFinalizar(self):
        Game.deletar(self.objId)
        return True