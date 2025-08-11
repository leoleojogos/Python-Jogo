
import pygame

from src.geral.game import Game
from src.geral.mat import Mat
from src.geral.camera import Camera

from src.objetos.player import Player
from src.objetos.items.item import Item

class ItemArma(Item):

    def __new__(cls, *args, **kwargs):
        if (args[1] == True):
            return object.__new__(cls)
        Item.listaItems.append(cls)
        return None

    def __init__(self, posicao: pygame.Vector2, escala: float, caminhoFrames: str, classeArma):
        super().__init__(posicao, escala, caminhoFrames)
        self.classeArma = classeArma

    def desenhar(self, tela: pygame.surface):
        self.calcularFrame()

        frameRotacionado = Mat.rodarImagem(self.getFrameAtual(), self.angulo, self.posTupla())

        pos = pygame.Vector2(frameRotacionado[1].topleft)
        pos.x -= Camera.posicao.x
        pos.y -= Camera.posicao.y

        tela.blit(frameRotacionado[0], pos)
    
    def coletar(self, player: Player):
        player.trocarArma(Game.criarObjeto(self.classeArma(self.posicao), 2))
        Game.deletar(self.objId)


from src.objetos.armas.pistola import Pistola
class ItemPistola(ItemArma):

    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        super().__init__(posicao, 1.45, './assets/armas/pistola/pistola*.png', Pistola)


from src.objetos.armas.metralhadora import Metralhadora
class ItemMetralhadora(ItemArma):
    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        super().__init__(posicao, 1.45, './assets/armas/metralhadora/metralhadora*.png', Metralhadora)


from src.objetos.armas.espingarda import Espingarda
class ItemEspingarda(ItemArma):
    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        super().__init__(posicao, 1.45, './assets/armas/espingarda/espingarda*.png', Espingarda)


from src.objetos.armas.bazuca import Bazuca
class ItemBazuca(ItemArma):
    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        super().__init__(posicao, 1.45, './assets/armas/Bazuca/Bazuca*.png', Bazuca)


from src.objetos.armas.submetralhadora import SubMetralhadora
class ItemSubMetralhadora(ItemArma):
    def __init__(self, posicao: pygame.Vector2, inicializar: bool):
        if (inicializar == False):
            return
        super().__init__(posicao, 0.1, './assets/armas/submetralhadora/submetralhadora*.png', SubMetralhadora)
