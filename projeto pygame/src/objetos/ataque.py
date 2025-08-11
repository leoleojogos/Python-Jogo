
import pygame

from src.geral.mat import Mat
from src.geral.game import Game
from src.geral.camera import Camera

from src.objetos.sprite import SpriteAnimado

class Ataque(SpriteAnimado):

    def __init__(self, playerRef, posicao: pygame.Vector2):
        super().__init__(posicao, 'assets/ataque/ataque*.png', 1.8, 25)

        self.playerRef = playerRef
        self.angulo = playerRef.angulo
        self.raio = playerRef.raio
        self.limiteDeAcertos = 1

        self.posicao = Mat.polarCartesiano(self.raio, self.angulo, self.playerRef.posicao)

    def atualizar(self):

        self.angulo = self.playerRef.angulo

        agora = pygame.time.get_ticks()
        porcentagemFrame = (agora - self.tickUltimoFrame) / self.delayDeFrame
        x = min(max((self.frameAtual + porcentagemFrame) / self.totalFrames, 0), 1)
        self.playerRef.anguloIncremento = Mat.loopAngulo(-(80 * Mat.parabolaNormal(x)))

        self.posicao = pygame.Vector2(
            Mat.polarCartesiano(self.raio, self.angulo, self.playerRef.posicao))
        
        self.colisaoInimigo()

        if (self.playerRef.arma != None):
            arma = self.playerRef.arma

            
    
    def desenhar(self, tela: pygame.surface):
        finalizar = self.calcularFrame()
        if (finalizar):
            return

        imagem = self.frames[self.frameAtual]
        imagem = Mat.rodarImagem(imagem, self.angulo, self.posTupla())

        pos = pygame.Vector2(imagem[1].topleft)
        pos.x -= Camera.posicao.x
        pos.y -= Camera.posicao.y

        tela.blit(imagem[0], pos)

        """ tamanho = self.frames[self.frameAtual].get_size()
        rect = pygame.Rect(
            self.posicao.x - tamanho[0]/2, self.posicao.y - tamanho[1]/2, tamanho[0], tamanho[1])
        pygame.draw.rect(tela, 'green', rect) """

    def aoFinalizar(self):
        self.playerRef.ataque = None
        Game.deletar(self.objId)
        return True
    
    def colisaoInimigo(self):
        
        acertos = 0
        for item in Game.subListaDeObjetos('Inimigo'):
            if (item['objeto'].invulneravel == True):
                continue

            rectTamanho = self.getFrameAtual().get_size()

            rectPos = pygame.Vector2(self.posicao)

            rectPos[0] -= rectTamanho[0]/2
            rectPos[1] -= rectTamanho[1]/2

            colisao = Mat.colisaoRetCirculo(
                self.raio, item['objeto'].posTupla(), rectTamanho, rectPos)

            if (colisao):
                acertos += 1

                direcao = -pygame.math.Vector2.normalize(
                    self.posicao - item['objeto'].posicao
                )

                item['objeto'].causarDano(0.5)
                item['objeto'].impulsionar(direcao * 5)
                
                item['objeto'].setInvulneravel()

                if (acertos >= self.limiteDeAcertos):
                    break
