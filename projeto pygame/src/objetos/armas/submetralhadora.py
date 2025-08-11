
import pygame

from src.geral.mat import Mat
from src.objetos.armas.arma import Arma
from src.objetos.armas.bala import Bala

class SubMetralhadora(Arma):

    municaoMaxima = 800

    def __init__(self, posicao: pygame.Vector2):
        super().__init__(posicao, 'white', 0.015 * Mat.segParaMili, 0.1, 0.08, 6, 12)
        self.setarBala(velocidade=20,imprecisao=12, impulso=1)
        self.balaParaSpawnar = Bala
        self.municao = self.__class__.municaoMaxima
