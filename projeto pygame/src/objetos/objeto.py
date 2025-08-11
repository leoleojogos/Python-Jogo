
import pygame

class Objeto():

    def __init__(self, posicao: pygame.Vector2, cor: str | pygame.Color):
        self.posicao = pygame.Vector2(posicao)
        self.cor = cor
        self.impulso = pygame.Vector2(0, 0)
        self.angulo = 0
        self.objId = None
    
    def desenhar(self, tela):
        pass
    
    def mover(self, quantidade: pygame.Vector2):
        self.posicao += quantidade

    def atualizar(self):
        self.posicao += self.impulso
        self.impulso = round(self.impulso * 0.9, 3)

    def impulsionar(self, impulso: pygame.Vector2):
        self.impulso += impulso

    def posTupla(self):
        return (self.posicao.x, self.posicao.y)