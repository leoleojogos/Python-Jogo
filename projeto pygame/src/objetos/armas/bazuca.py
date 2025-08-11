import pygame
from src.objetos.armas.arma import Arma
from src.geral.mat import Mat
from src.objetos.armas.foguete import Foguete

class Bazuca(Arma):
   
    municaoMaxima = 3

    def __init__(self, posicao: pygame.Vector2):
        super().__init__(posicao, 'white', 2.5 * Mat.segParaMili, 10, 10, 15, 32)
        self.setarBala(velocidade = 7, vida=2 * Mat.segParaMili, imprecisao=6)
        self.balaParaSpawnar = Foguete
        self.municao = self.__class__.municaoMaxima

