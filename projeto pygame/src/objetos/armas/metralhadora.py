
import pygame

from src.geral.game import Game
from src.geral.mat import Mat
from src.objetos.armas.arma import Arma
from src.objetos.armas.bala import Bala

class Metralhadora(Arma):

    municaoMaxima = 300

    def __init__(self, posicao: pygame.Vector2):
        super().__init__(posicao, 'white', 0.1 * Mat.segParaMili, 0.1, 0.25, 6, 19)
        self.setarBala(imprecisao=8, impulso=2)
        self.balaParaSpawnar = Bala
        self.municao = self.__class__.municaoMaxima
