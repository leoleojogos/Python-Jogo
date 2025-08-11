
import pygame
import random
import math

from src.geral.game import Game
from src.geral.camera import Camera

from src.objetos.inimigos.inimigo import Inimigo
from src.objetos.HUD import HUD
from src.objetos.player import Player
from src.geral.sistema import Sistema

class InimigoSpawnner(Sistema):
    listaInimigoTipos = [Inimigo]
    ultimoSpawn = 0
    playerRef = 0
    tempoMinimo = 700
    tempoMaximo = 2500
    tempo = 0

    @classmethod
    def iniciar(cls):
        cls.ultimoSpawn = pygame.time.get_ticks()
        cls.playerRef = Player()
        cls.hudRef = HUD()
        cls.tempo = cls.hudRef.getInimigoSpawnnDelay()
        cls.spawnnar()

        Game.criarSistema(cls)

    @classmethod
    def atualizar(cls):
        agora = pygame.time.get_ticks()
        if (agora - cls.ultimoSpawn >= cls.tempo):
            cls.tempo = cls.hudRef.getInimigoSpawnnDelay()
            cls.ultimoSpawn = agora
            cls.spawnnar()
    
    @classmethod
    def spawnnar(cls):
        if (cls.hudRef.inimigoQuantidade >= cls.hudRef.inimigoQuantidadeMaxima):
            return

        tipoParaSpawnnar = cls.listaInimigoTipos[random.randint(0, len(cls.listaInimigoTipos)-1)]
        
        cantoInd = random.randint(0, 2)
        pos = pygame.Vector2(0, 0)

        esquerda = math.floor(Camera.posicao.x - 64)
        direita = math.floor(Camera.posicao.x + Game.tamanho[0] + 64)
        cima = math.floor(Camera.posicao.y - 64)
        baixo = math.floor(Camera.posicao.y + Game.tamanho[1] + 64)

        if (cantoInd == 0):
            pos = pygame.Vector2(
                esquerda, random.randint(cima, baixo)
            )
        elif (cantoInd == 1):
            pos = pygame.Vector2(
                direita, random.randint(cima, baixo)
            )
        elif (cantoInd == 2):
            pos = pygame.Vector2(
                random.randint(esquerda, direita), cima
            )
        else:
            pos = pygame.Vector2(
                random.randint(esquerda, direita), baixo
            )
    
        
        Game.criarObjeto(tipoParaSpawnnar(
            pos, 16, 'red', 1.3, 1
        ), 1)
        cls.hudRef.registrarSpawn()


