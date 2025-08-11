import pygame
import math

from src.geral.game import Game
from src.objetos.player import Player
from src.objetos.circulo import Circulo

class Explosao(Circulo):
    def __init__(self, posicao: pygame.Vector2):
        self.cor = pygame.Color(245, 234, 159, a=255)
        self.alpha = 255
        super().__init__(posicao, 48, self.cor)
      

    def atualizar(self):

        self.alpha -= 2.9
        self.cor.a = max(int(self.alpha), 0)
        self.raio += 1
        if(self.cor.a <= 0):
            Game.deletar(self.objId)
            return 
        self.causarDano()

    def causarDano(self):
        listaColisao = Game.subListaDeObjetos("Inimigo")
        listaColisao.append({
            "tipo": "Player", "objeto": Player()
        })

        for item in listaColisao:
            distancia = math.sqrt(
                math.pow(self.posicao.x - item['objeto'].posicao.x, 2) +
                math.pow(self.posicao.y - item['objeto'].posicao.y, 2)
            )
            if (distancia <= self.raio + item['objeto'].raio):
                

                direcao = -pygame.math.Vector2.normalize(self.posicao - item["objeto"].posicao)

                item['objeto'].causarDano(1, direcao)
                break


    

        
        
        
