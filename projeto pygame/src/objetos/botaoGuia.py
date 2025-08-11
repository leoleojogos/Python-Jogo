import math
import pygame

from src.geral.camera import Camera
from src.objetos.sprite import SpriteAnimado
from src.objetos.objeto import Objeto

class BotaoGuia(SpriteAnimado):
    def __init__(self, objRef: Objeto, posicao: pygame.Vector2, tecla: str):
        super().__init__(posicao, './assets/botaoGuia/botao*.png', 1.25, 1)
        self.texto = pygame.font.SysFont(None, 45)
        self.textoImagem = self.texto.render(tecla, True, 'black')
        self.objRef = objRef

        if (self.objRef != None):
            self.offset = self.posicao - self.objRef.posicao
        else:
            self.offset = pygame.Vector2(0, 0)

    def atualizar(self):
        if (self.objRef != None):
            self.posicao = self.objRef.posicao + self.offset

    def desenhar(self, tela: pygame.surface):
        super().desenhar(tela)

        yAMais = math.ceil(self.escala * 2 * self.frameAtual * 1.75)

        pos = pygame.Vector2()
        pos.x = self.posicao.x - Camera.posicao.x
        pos.y = self.posicao.y + yAMais - Camera.posicao.y

        tela.blit(self.textoImagem, pos)