
import pygame

from src.geral.camera import Camera
from src.objetos.objeto import Objeto

class Circulo(Objeto):
    def __init__(self, posicao: pygame.Vector2, raio: float, cor: str | pygame.Color):
        super().__init__(posicao, cor)
        self.raio = raio

    def desenhar(self, tela):
        if (self.posicao.x - Camera.posicao.x <= 0):
            return

        if(self.cor.__class__.__name__ == "Color"):
            imagem = pygame.Surface((self.raio * 2,self.raio * 2))
            imagem.set_colorkey((0,0,0))
            imagem.set_alpha(self.cor.a)
            
            pygame.draw.circle(imagem, self.cor, (self.raio, self.raio), self.raio)

            pos = pygame.Vector2(self.posicao)
            pos.x -= self.raio
            pos.y -= self.raio

            tela.blit(imagem, pos - Camera.posicao)
            return 
        
        pygame.draw.circle(tela, self.cor, self.posicao - Camera.posicao, self.raio)