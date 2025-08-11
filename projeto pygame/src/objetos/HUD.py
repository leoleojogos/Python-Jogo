
import random
import pygame
import math

from src.objetos.objeto import Objeto

class HUD(Objeto):
    
    inicializado = False
    __instance = None
    def __new__(cls, *args, **kwargs):
        if (cls.__instance == None):
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def __init__(self, inicializar: bool = False, gameRef = None):
        if (inicializar == False):
            return
        HUD.inicializado = True
        
        super().__init__(pygame.Vector2(0, 0), 'white')

        self.gameRef = gameRef

        self.mortes = 0
        self.playerVida = 1
        self.playerVidaLerp = self.playerVida
        self.playerVidaDelta = 0

        self.larguraMaxima = 256
        self.borda = 2
        self.margem = 16
        self.barraLargura = 18

        self.resetar()        

    def resetar(self):
        self.decrementoProbabilidadeItem = 0.0003
        self.probabilidadeDeItem = 0.08
        self.probabilidadeDeItemMinima = 0.008

        self.inimigoSpawnnTimerMinimo = 100
        self.inimigoSpawnnTimerMaximo = 2500
        self.inimigoSpawnFator = 1
        self.inimigoSpawnDecrementoFator = 0.01
        self.inimigoSpawnFatorMinimo = 0.23
        self.vidaCor = pygame.Color(255, 255, 255)

        self.inimigoQuantidade = 0
        self.inimigoQuantidadeMaxima = 1

        self.jogoPausado = False
        texto = pygame.font.SysFont(None, 55)
        self.textoPause = texto.render('JOGO PAUSADO', True, 'white')

        self.setarTextoMunicao(0)

    def desenhar(self, tela):

        if (abs(self.playerVidaLerp - self.playerVida) >= 0.01):
            self.playerVidaDelta = self.playerVidaLerp
            self.playerVidaLerp += 0.1*(self.playerVida - self.playerVidaLerp)
            self.playerVidaDelta = self.playerVidaLerp - self.playerVidaDelta
            
            if (self.playerVidaDelta > 0):
                x = min(self.playerVidaDelta, 0.005) / 0.005
                novaCor = (
                    math.floor(255 * (1-x)),
                    255,
                    math.floor(255 * (1-x))
                )
            elif (self.playerVidaDelta < 0):
                x = min(abs(self.playerVidaDelta), 0.005) / 0.005
                novaCor = (
                    255,
                    math.floor(255 * (1 - x)),
                    math.floor(255 * (1 - x))
                )
            self.vidaCor = pygame.Color(novaCor[0], novaCor[1], novaCor[2])

        self.desenharBarraDeVida(tela)

        pos = pygame.Vector2(
            self.margem*2 + self.borda*2 + self.larguraMaxima,
            self.margem
        )
        tela.blit(self.textoMunicao, pos)
    
    def desenharBarraDeVida(self, tela):

        fundoStartPos = pygame.Vector2(
            self.margem, self.margem + self.barraLargura / 2
        )
        fundoEndPos = pygame.Vector2(
            self.margem + self.larguraMaxima + self.borda, self.margem + self.barraLargura / 2
        )
        pygame.draw.line(
            tela, 'blue', fundoStartPos, fundoEndPos, self.barraLargura)
        

        barraStartPos = pygame.Vector2(
            self.margem + self.borda,
            self.margem + self.borda + self.barraLargura / 2 - self.borda
        )
        barraEndPos = pygame.Vector2(
            max(self.margem + self.larguraMaxima * self.playerVidaLerp, self.margem + self.borda + 1),
            self.margem + self.borda + self.barraLargura / 2 - self.borda
        )
        pygame.draw.line(
            tela, self.vidaCor, barraStartPos, barraEndPos, self.barraLargura - self.borda * 2
        )

    def registrarMorte(self):
        self.mortes += 1
        self.inimigoQuantidade -= 1

        if (self.probabilidadeDeItem > self.probabilidadeDeItemMinima):
            self.probabilidadeDeItem *= (1 - self.decrementoProbabilidadeItem)
    
        if (self.inimigoSpawnFator > self.inimigoSpawnFatorMinimo):
            self.inimigoSpawnFator *= (1 - self.inimigoSpawnDecrementoFator)

        self.inimigoQuantidadeMaxima = math.floor(self.mortes/4.25)+1
        """ print(
            f"kills: {self.mortes}; spawn minimo: {self.inimigoSpawnnTimerMinimo * self.inimigoSpawnFator/1000}\n"
            f"spawn maximo: {self.inimigoSpawnnTimerMaximo * self.inimigoSpawnFator/1000}\n"
            f'inimigoMax: {self.inimigoQuantidadeMaxima}\n'
            '====================\n'
        ) """

    def registrarSpawn(self):
        self.inimigoQuantidade += 1


    def getInimigoSpawnnDelay(self):
        if (HUD.inicializado == False):
            return 0

        return random.randint(
            self.inimigoSpawnnTimerMinimo, self.inimigoSpawnnTimerMaximo
        ) * self.inimigoSpawnFator

    def playerCausarDano(self, dano: float):
        self.playerVida -= dano / 100
        if (self.playerVida <= 0):
            self.gameRef.reiniciar()

    def playerGanharVida(self, vida: int):
        if (vida == -1):
            self.playerVida = 1
        else:
            self.playerVida += vida / 100
            self.playerVida = min(self.playerVida, 1)
            

    def setarTextoMunicao(self, municao: int):
        self.municao = municao
        texto = pygame.font.SysFont(None, 45)
        self.textoMunicao = texto.render(str(municao), True, 'white')

    def setarPause(self, valor: bool, tela: pygame.Surface):
        self.jogoPausado = valor

        pos = pygame.Vector2(
            self.gameRef.tamanho[0] / 2 - self.textoPause.get_rect().width / 2,
            self.gameRef.tamanho[1] / 2 - self.textoPause.get_rect().height / 2
        )

        tela.blit(self.textoPause, pos)
        pygame.display.flip()
