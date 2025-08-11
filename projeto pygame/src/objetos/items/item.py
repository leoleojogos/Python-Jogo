
import random
import pygame
import math

from src.geral.game import Game
from src.geral.mat import Mat
from src.objetos.HUD import HUD
from src.geral.camera import Camera

from src.objetos.sprite import SpriteAnimado
from src.objetos.botaoGuia import BotaoGuia
from src.objetos.player import Player

class Item(SpriteAnimado):

    listaItems = []

    def __init__(self, posicao: pygame.Vector2, escala: float, caminhoFrames: str):
        super().__init__(posicao, caminhoFrames, escala, 10)
        self.raio = min(self.rect.width, self.rect.height)
        self.botaoGuia = None

        self.rotacaoAmplitude = 15
        self.rotacaoAngulo = random.random() * 360 * Mat.grausParaRad
        self.rotacaoVelocidade = 1 * Mat.grausParaRad
        
        self.tempoSumir = random.randint(30, 35) * Mat.segParaMili
        self.horaSpawnn = pygame.time.get_ticks()

    def rotacaoSeno(self):
        self.rotacaoAngulo += self.rotacaoVelocidade
        if (self.rotacaoAngulo >= 360 * Mat.grausParaRad):
            self.rotacaoAngulo -= 360 * Mat.grausParaRad

        self.angulo = math.sin(self.rotacaoAngulo) * self.rotacaoAmplitude

    def atualizar(self):
        super().atualizar()

        agora = pygame.time.get_ticks()
        if (agora - self.horaSpawnn >= self.tempoSumir):
            Game.deletar(self.objId)

            if (self.botaoGuia != None):
                Game.deletar(self.botaoGuia.objId)
                self.botaoGuia = None
            return

        self.rotacaoSeno()

        player = Player()

        distancia = math.sqrt(
            math.pow(self.posicao.x - player.posicao.x, 2) +
            math.pow(self.posicao.y - player.posicao.y, 2)
        )
        if (distancia <= self.raio + player.raio):
            if (self.botaoGuia == None):
                self.botaoGuia = Game.criarObjeto(BotaoGuia(
                    self, pygame.Vector2(self.posicao.x, self.posicao.y - self.raio * 1.35), 'E'
                ), 3)

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_e]):
                self.coletar(player)

                Game.deletar(self.botaoGuia.objId)
                self.botaoGuia = None

        elif (self.botaoGuia != None):
            Game.deletar(self.botaoGuia.objId)
            self.botaoGuia = None
            
                
    def coletar(self, player):
        pass

class KitMedico(Item):

    def __new__(cls, *args, **kwargs):
        if (args[1] == True):
            return object.__new__(cls)
        Item.listaItems.append(cls)
        return None

    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        self.hudRef = HUD()
        super().__init__(posicao, 1.45, './assets/kitMedico/kitmedico*.png')

    def desenhar(self, tela: pygame.surface):
        self.calcularFrame()

        frameRotacionado = Mat.rodarImagem(self.getFrameAtual(), self.angulo, self.posTupla())

        pos = pygame.Vector2(frameRotacionado[1].topleft)
        pos.x -= Camera.posicao.x
        pos.y -= Camera.posicao.y

        tela.blit(frameRotacionado[0], pos)

    def coletar(self, player):
        self.hudRef.playerGanharVida(-1)
        Game.deletar(self.objId)

class Erva(Item):

    def __new__(cls, *args, **kwargs):
        if (args[1] == True):
            return object.__new__(cls)
        Item.listaItems.append(cls)
        return None

    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        self.hudRef = HUD()
        super().__init__(posicao, 1.45, './assets/erva/erva*.png')

    def desenhar(self, tela: pygame.surface):
        self.calcularFrame()

        frameRotacionado = Mat.rodarImagem(self.getFrameAtual(), self.angulo, self.posTupla())

        pos = pygame.Vector2(frameRotacionado[1].topleft)
        pos.x -= Camera.posicao.x
        pos.y -= Camera.posicao.y

        tela.blit(frameRotacionado[0], pos)

    def coletar(self, player):
        self.hudRef.playerGanharVida(25)
        Game.deletar(self.objId)

    