
import pygame
import math
import os.path

from src.geral.mat import Mat
from src.geral.camera import Camera

from src.objetos.objeto import Objeto

class Sprite(Objeto):
    def __init__(self, posicao: pygame.Vector2, angulo: float = 0):
        super().__init__(posicao, 'white')
        self.angulo = angulo

    def getFrameAtual(self):
        pass

class SpriteEstatico(Sprite):
    def __init__(self, posicao: pygame.Vector2, caminhoImagem: str, escala: float, angulo: float = 0):
        super().__init__(posicao)

        self.imagem = pygame.image.load(caminhoImagem)
        self.imagem = pygame.transform.scale(
            self.imagem,
            pygame.Vector2(
                math.floor(self.imagem.get_size()[0] * escala),
                math.floor(self.imagem.get_size()[1] * escala)
            )
        )

        imagemRotacionada = Mat.rodarImagem(self.imagem, self.angulo, self.posicao)
        self.imagem = imagemRotacionada[0]

        # self.posicao -= self.getFrameAtual().get_rect().center
    
    def getFrameAtual(self):
        return self.imagem

    def desenhar(self, tela: pygame.surface):
        tela.blit(self.imagem, self.posicao - Camera.posicao)

class SpriteAnimado(Sprite):
    def __init__(self, posicao: pygame.Vector2, caminhoFrames: str, escala: float, fps: float, angulo: float = 0):
        super().__init__(posicao)
        
        self.frames = []
        self.delayDeFrame = (1 / fps) * 1000
        self.tickUltimoFrame = pygame.time.get_ticks()

        self.frameAtual = 0
        self.escala = escala

        ind = 0
        while(os.path.isfile(caminhoFrames.replace('*', str(ind)))):
            caminho = caminhoFrames.replace('*', str(ind))

            frame = pygame.image.load(caminho)
            frame = pygame.transform.scale(
                frame,
                pygame.Vector2(
                    math.floor(frame.get_size()[0] * escala),
                    math.floor(frame.get_size()[1] * escala)
                )
            )
            self.rect = frame.get_rect()

            if (angulo != 0):
                imagemRotacionada = Mat.rodarImagem(frame, angulo, self.posTupla())
                frame = imagemRotacionada[0]

            self.frames.append(frame)
            ind += 1

        if (ind == 0):
            raise Exception(f"Nenhum frame encontrado no caminho genério: '{caminhoFrames}'")
        
        self.totalFrames = ind - 1

        self.posicao -= self.rect.center
        
    def desenhar(self, tela: pygame.surface):
        finalizar = self.calcularFrame()
        if (finalizar):
            return

        tela.blit(self.frames[self.frameAtual], self.posicao - Camera.posicao)

    def calcularFrame(self):
        agora = pygame.time.get_ticks()
        if (agora - self.tickUltimoFrame >= self.delayDeFrame):
            self.tickUltimoFrame = agora

            if (self.frameAtual < len(self.frames) - 1):
                self.frameAtual += 1
            else:
                self.frameAtual = 0
                return self.aoFinalizar()

    def aoFinalizar(self):
        return False
    
    def getFrameAtual(self):
        return self.frames[self.frameAtual]


class HudSpriteEstatico(SpriteEstatico):
    def __init__(self, posicao: pygame.Vector2, caminhoImagem: str, escala: float, angulo: float = 0):
        super().__init__(posicao, caminhoImagem, escala, angulo)

    def desenhar(self, tela: pygame.surface):
        tela.blit(self.imagem, self.posicao)
