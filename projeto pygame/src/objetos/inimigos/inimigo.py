
import random
import pygame
import math

from src.geral.game import Game
from src.geral.mat import Mat

from src.objetos.circulo import Circulo
from src.objetos.HUD import HUD
from src.objetos.player import Player
from src.objetos.items.item import Item
from src.objetos.inimigos.inimigoMorte import InimigoMorte

class Inimigo(Circulo):
    def __init__(self, posicao: pygame.Vector2, raio: float, cor: str, velocidade: float, vida: float):
        super().__init__(posicao, raio, cor)
        self.targetDirecao: pygame.Vector2 = pygame.Vector2(0, 0)
        self.velocidade: float = velocidade
        self.playerRef = Player()
        self.vida = vida
        self.dano = 10
        self.hudRef = HUD()
        
        self.invulneravel = False
        self.tempoInvulneravel = 1 * Mat.segParaMili
        self.ultimaVezInVulneravel = pygame.time.get_ticks()
    
    def atualizar(self):
        super().atualizar()

        if (not self.invulneravel):
            self.targetDirecao = self.playerRef.posicao - self.posicao
            self.targetDirecao = pygame.math.Vector2.normalize(self.targetDirecao)
            self.mover(self.targetDirecao * self.velocidade)
        else:
            agora = pygame.time.get_ticks()
            if (agora - self.ultimaVezInVulneravel >= self.tempoInvulneravel):
                self.invulneravel = False

        self.colisaoJogador()
    
    def causarDano(self, quantidade: float, direcao: pygame.Vector2 = pygame.Vector2(0, 0), impulso: float = 1):
        self.vida -= quantidade
        if (self.vida <= 0):
            if (random.random() <= self.hudRef.probabilidadeDeItem):
                tamanho = min(math.floor(self.hudRef.mortes / 20) + 1, len(Item.listaItems))

                indice = Mat.decadenciaDeProbabilidade(tamanho)
                itemParaSpawnnar = Item.listaItems[indice](self.posicao, True)
                Game.criarObjeto(itemParaSpawnnar, 0)

            Game.criarObjeto(InimigoMorte(self.posicao))
            self.hudRef.registrarMorte()
            Game.deletar(self.objId)
            return

        self.impulsionar(impulso * direcao)
        
    def colisaoJogador(self):
        distancia = (
            (self.posicao.x - self.playerRef.posicao.x) ** 2 +
            (self.posicao.y - self.playerRef.posicao.y) ** 2
        ) ** 0.5

        if (distancia <= self.raio + self.playerRef.raio and self.playerRef.invulneravel == False):
            direcao = -pygame.math.Vector2.normalize(
                self.posicao - self.playerRef.posicao
            )

            self.playerRef.causarDano(self.dano, direcao, 3)

    def setInvulneravel(self):
        self.invulneravel = True
        self.ultimaVezInVulneravel = pygame.time.get_ticks()
