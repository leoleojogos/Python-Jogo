
import pygame
from src.geral.mat import Mat
from src.geral.game import Game
from src.geral.camera import Camera

from src.objetos.objeto import Objeto
from src.objetos.player import Player
from src.objetos.HUD import HUD

class Arma(Objeto):

    municaoMaxima = 0

    def __init__(self, posicao: pygame.Vector2, cor: str, delayDeTiro: float, forcaImpacto: float, dano: float, largura: int, comprimento: int):
        super().__init__(posicao, cor)
        self.delayDeTiro = delayDeTiro
        self.ultimoTiro = 0
        self.playerRef = Player()
        self.distancia = self.playerRef.raio
        self.forcaImpacto = forcaImpacto
        self.dano = dano
        self.largura = largura
        self.comprimento = comprimento
        self.municao = self.__class__.municaoMaxima

        self.ponta0 = Mat.polarCartesiano(self.distancia, 0, self.posTupla())
        self.ponta1 = Mat.polarCartesiano(self.distancia + 32, 0, self.posTupla())

        self.balaVelocidade: float = 16
        self.balaRaio: float = 8
        self.balaVida: float = 2 * Mat.segParaMili
        self.balaImprecisao: float = 0
        self.balaImpulso = 1

        self.balaParaSpawnar = None
        self.hudRef = HUD()


    def desenhar(self, tela: pygame.Surface):
        pygame.draw.line(tela, self.cor, self.ponta0 - Camera.posicao, self.ponta1 - Camera.posicao, self.largura)

    def atualizar(self):
        self.posicao = self.playerRef.posicao
        self.angulo = self.playerRef.angulo
        
        self.ponta0 = Mat.polarCartesiano(self.distancia, self.angulo, self.posTupla())
        self.ponta1 = Mat.polarCartesiano(self.distancia+self.comprimento, self.angulo, self.posTupla())

        if (pygame.mouse.get_pressed()[0]):
            self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if (agora - self.ultimoTiro > self.delayDeTiro and self.municao > 0):
            self.municao -= 1
            self.ultimoTiro = agora

            impulsoDirecao = -pygame.Vector2.normalize(self.ponta0 - self.playerRef.posicao)
            Game.criarObjeto(self.balaParaSpawnar(self.ponta1, self.balaRaio, -impulsoDirecao, self.balaVelocidade, self.dano, self.balaVida, self.balaImprecisao, self.balaImpulso))

            self.playerRef.impulsionar(impulsoDirecao * self.forcaImpacto)
            
            self.hudRef.setarTextoMunicao(self.municao)
            
        elif(self.municao <= 0):
            self.playerRef.arma = None
            Game.deletar(self.objId)


    def getAngulo(self):
        return Mat.anguloEntreVetores(
            (self.posicao.x - Camera.posicao.x, self.posicao.y - Camera.posicao.y),
            pygame.mouse.get_pos()
        )
    
    def setarBala(self, velocidade: float = 0, raio: float = 0, vida: float = 0, imprecisao: float = 0, impulso: float = 1):
        if (velocidade != 0):
            self.balaVelocidade = velocidade
        if (raio != 0):
            self.balaRaio = raio
        if (vida != 0):
            self.balaVida = vida
        if (imprecisao != 0):
            self.balaImprecisao = imprecisao
        if (impulso != 1):
            self.balaImpulso = impulso

