import math
import pygame
import random

from src.objetos.circulo import Circulo
from src.geral.game import Game
from src.geral.mat import Mat
from src.objetos.explosao import Explosao

class Bala(Circulo):
    def __init__(self, posicao: pygame.Vector2, raio: float, direcao: pygame.Vector2, velocidade: float, dano: float, tempoVida: float, imprecisao: float, impulso: float):
        super().__init__(posicao, raio, 'yellow')

        angulo = (0.5 - random.random()) * imprecisao
        self.direcao = Mat.rodarVetor(direcao, angulo)
        
        self.velocidade = velocidade
        self.dano = dano
        self.tempoVida = tempoVida
        self.tempoNasceu = pygame.time.get_ticks()
        self.imprecisao = imprecisao
        self.impulso = impulso

    def mover(self):
        return super().mover(self.direcao * self.velocidade)
    def atualizar(self):
        self.mover()

        agora = pygame.time.get_ticks()
        if (agora - self.tempoNasceu > self.tempoVida):
            Game.deletar(self.objId)
            return
        
        self.checarColisao()

    def checarColisao(self):
        for inimigo in Game.subListaDeObjetos('Inimigo'):
            distancia = math.sqrt(
                math.pow(self.posicao.x - inimigo['objeto'].posicao.x, 2) +
                math.pow(self.posicao.y - inimigo['objeto'].posicao.y, 2)
            )
            if (distancia <= self.raio + inimigo['objeto'].raio):
                Game.deletar(self.objId)
                inimigo['objeto'].causarDano(self.dano, self.direcao, self.impulso)
                self.aoColodir()
                break
    
    def aoColodir(self):
        pass