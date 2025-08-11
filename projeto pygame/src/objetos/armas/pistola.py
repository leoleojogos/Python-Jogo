
import pygame

from src.geral.mat import Mat
from src.objetos.armas.arma import Arma
from src.objetos.armas.bala import Bala

class Pistola(Arma):

    municaoMaxima = 80

    def __init__(self, posicao: pygame.Vector2):
        super().__init__(posicao, 'white', 0.53 * Mat.segParaMili, 1, 1, 8, 12)
        self.setarBala(imprecisao=4)
        self.balaParaSpawnar = Bala
        self.municao = self.__class__.municaoMaxima
