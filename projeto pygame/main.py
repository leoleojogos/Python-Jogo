
import pygame

from src.geral.game import Game
from src.geral.cursor import Cursor
from src.geral.camera import Camera

from src.objetos.HUD import HUD
from src.objetos.inimigos.inimigoSpawnner import InimigoSpawnner
from src.objetos.player import Player

from src.objetos.items.item import KitMedico, Erva
from src.objetos.items.itemArma import ItemPistola, ItemMetralhadora, ItemEspingarda,ItemBazuca, ItemSubMetralhadora

def ComecarJogo():
    
    Game.criarObjeto(HUD(True, Game), 4)

    Camera.iniciar()
    InimigoSpawnner.iniciar()

    Game.criarObjeto(Cursor(), 4)

    Game.criarObjeto(Player(pygame.Vector2(128, 128), 16, 'blue', 3), 1)
    
    Game.criarObjeto(ItemPistola(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(ItemMetralhadora(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(ItemSubMetralhadora(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(ItemEspingarda(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(Erva(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(ItemBazuca(pygame.Vector2(0, 0), False), 0)
    Game.criarObjeto(KitMedico(pygame.Vector2(0, 0), False), 0)

    Game.rotina()
    Game.fechar()

Game.iniciar(640, 480, "Bolas", ComecarJogo)
