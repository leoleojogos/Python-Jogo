import pygame
from src.geral.game import Game
from src.objetos.armas.bala import Bala
from src.objetos.explosao import Explosao

class Foguete(Bala):
    def __init__(self, posicao: pygame.Vector2, raio: float, direcao: pygame.Vector2, velocidade: float, dano: float, tempoVida: float, imprecisao: float, impulso: float):
        super().__init__(posicao, raio, direcao, velocidade, dano, tempoVida, imprecisao, impulso)
        
    def aoColodir(self):
        Game.criarObjeto(Explosao(self.posicao),3)