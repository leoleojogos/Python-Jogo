
import pygame

from src.geral.game import Game
from src.geral.mat import Mat
from src.geral.camera import Camera

from src.objetos.HUD import HUD
from src.objetos.circulo import Circulo
from src.objetos.ataque import Ataque

class Player(Circulo):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance == None):
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def __init__(self, posicao: pygame.Vector2 = pygame.Vector2(0, 0), raio: float = 0, cor: str = 'white', velocidade: float = 0):
        if (raio == 0):
            return
        
        super().__init__(posicao, raio, cor)
        self.velocidade = velocidade

        self.arma = None
        self.ataque = None

        self.hudRef = HUD()
        self.anguloIncremento = 0

        self.invulneravel = False
        self.tempoInvulneravel = 1 * Mat.segParaMili
        self.ultimaVezInVulneravel = pygame.time.get_ticks()

    def andar(self, keys: list):
        movimento = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w])
        )
        if (movimento.x != 0 or movimento.y != 0):
            movimento.normalize()

        super().mover(movimento * self.velocidade)

    def atualizar(self):
        super().atualizar()

        self.angulo = Mat.anguloEntreVetores(
            (self.posicao.x - Camera.posicao.x, self.posicao.y - Camera.posicao.y), pygame.mouse.get_pos()
        )
        self.angulo += self.anguloIncremento
        self.anguloIncremento = 0

        keys = pygame.key.get_pressed()
        self.andar(keys)

        if (keys[pygame.K_SPACE] and self.ataque == None):
            self.ataque = Game.criarObjeto(Ataque(self, self.posicao), 2)

        agora = pygame.time.get_ticks()
        if (agora - self.ultimaVezInVulneravel >= self.tempoInvulneravel):
            self.invulneravel = False

        Camera.setarPosicao(self.posicao)

    def trocarArma(self, armaNova):
        if (self.arma != None):
            Game.deletar(self.arma.objId)
        if (self.arma.__class__.__name__ == armaNova.__class__.__name__):
            self.arma.municao = self.arma.__class__.municaoMaxima
        self.arma = armaNova
        self.hudRef.setarTextoMunicao(self.arma.municao)

    def causarDano(self, dano: float, direcao: pygame.Vector2 = pygame.Vector2(0,0), forca: float = 0):
        self.hudRef.playerCausarDano(dano)
        self.impulsionar(direcao * forca)
        
        self.setInvulneravel()

    def setInvulneravel(self):
        self.invulneravel = True
        self.ultimaVezInVulneravel = pygame.time.get_ticks()
