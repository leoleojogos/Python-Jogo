
import pygame
from src.objetos.armas.arma import Arma
from src.objetos.armas.bala import Bala
from src.geral.game import Game
from src.geral.mat import Mat

class Espingarda(Arma):

    municaoMaxima = 50    

    def __init__(self, posicao: pygame.Vector2):
        super().__init__(posicao, 'white', 1.2 * Mat.segParaMili, 4, 3, 10, 24)
        self.setarBala(velocidade = 10, vida=0.35 * Mat.segParaMili)
        self.balaParaSpawnar = Bala
        self.municao = self.__class__.municaoMaxima

    def atirar(self):
        agora = pygame.time.get_ticks()
        if (agora - self.ultimoTiro > self.delayDeTiro and self.municao > 0):
            self.municao -= 1
            self.ultimoTiro = agora

            angulos = [-8, 0, 8]
            impulsoDirecao = -pygame.Vector2.normalize(self.ponta0 - self.playerRef.posicao)
            for i in range(3):
                angulo = Mat.loopAngulo(self.getAngulo() + angulos[i])
                balaDirecao = pygame.Vector2(Mat.polarCartesiano(1, angulo))
                for i in range(4):
                    Game.criarObjeto(Bala(self.ponta1, self.balaRaio, balaDirecao, self.balaVelocidade, self.dano, self.balaVida, self.balaImprecisao, self.balaImpulso))
           
            self.playerRef.impulsionar(impulsoDirecao * self.forcaImpacto)

            self.hudRef.setarTextoMunicao(self.municao)

        elif(self.municao <= 0):
            self.playerRef.arma = None
            Game.deletar(self.objId)