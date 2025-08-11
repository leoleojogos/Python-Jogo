import pygame
import random

from src.objetos.HUD import HUD
from src.objetos.objeto import Objeto
from src.geral.sistema import Sistema

class Game():

    tela = 0
    relogio = 0
    running = True
    listaObjetos = []
    listaObjetosRotina = []

    listaSistemas = []
    tamanho = ()

    @classmethod
    def iniciar(cls, largura: int, altura: int, titulo: str, funcaoJogar):
        
        pygame.init()
        pygame.display.set_caption(titulo)
        pygame.mouse.set_visible(False)

        cls.relogio = pygame.time.Clock()
        cls.tamanho = (largura, altura)
        cls.tela = pygame.display.set_mode(cls.tamanho)
        cls.hudRef = HUD()

        cls.auxilioEsc = False

        cls.pausado = False

        cls.funcaoJogar = funcaoJogar
        cls.funcaoJogar()

    
    @classmethod
    def reiniciar(cls):
        cls.listaObjetos = []
        cls.listaObjetosRotina = []
        cls.hudRef.resetar()

        cls.funcaoJogar()

    @classmethod
    def criarObjeto(cls, objeto: Objeto, camada: int = 0):
        if (objeto == None):
            return
        
        cls.listaObjetos.append({
            'tipo': objeto.__class__.__name__, 'objeto': objeto
        })
        cls.listaObjetosRotina.append({
            'objeto': objeto, 'camada': camada
        })

        objeto.objId = len(cls.listaObjetos) - 1
        cls.reordenar()


        return objeto
    
    @classmethod
    def criarSistema(cls, sistema: Sistema):
        cls.listaSistemas.append(sistema)

    @classmethod
    def processarEventos(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.running = False
            elif event.type == pygame.WINDOWFOCUSLOST:
                cls.pausado = True
                cls.hudRef.setarPause(True, cls.tela)
            

        teclas = pygame.key.get_pressed()
        if(teclas[pygame.K_ESCAPE]):
            if (cls.auxilioEsc == False):
                cls.pausado = not cls.pausado
                cls.hudRef.setarPause(cls.pausado, cls.tela)
            cls.auxilioEsc = True
        else:
            cls.auxilioEsc = False
        
        if (teclas[pygame.K_r]):
            cls.reiniciar()

    @classmethod
    def rotina(cls):
        while True:
            cls.processarEventos()

            if (cls.running == False):
                break
                
            if (cls.pausado == True):
                continue
            

            for sistema in cls.listaSistemas:
                sistema.atualizar()

            for item in cls.listaObjetosRotina:
                item['objeto'].atualizar()

            cls.desenhar()

            cls.relogio.tick(60)
    @classmethod
    def desenhar(cls):
        cls.tela.fill("black")

        for item in cls.listaObjetosRotina:
            item['objeto'].desenhar(cls.tela)
        pygame.display.flip()

    @classmethod
    def deletar(cls, id: int):
        itemDeletar = cls.listaObjetos[id]

        ind = 0
        for itemIteracao in cls.listaObjetosRotina:
            if (itemIteracao['objeto'].objId == itemDeletar['objeto'].objId):
                cls.listaObjetosRotina.pop(ind)
                break
            ind += 1

        cls.listaObjetos.pop(id)
        cls.reordenar()

    @classmethod
    def subListaDeObjetos(cls, classeNome: str):

        inicio = -1
        fim = -1
        ind = 0
        for item in cls.listaObjetos:
            if (item['tipo'] == classeNome):
                if (inicio == -1):
                    inicio = ind
            if (inicio != -1):
                if (item['tipo'] != classeNome):
                    fim = ind
                    break
            ind += 1

        if (fim == -1):
            fim = len(cls.listaObjetos)
        if (inicio == -1):
            return []
        return cls.listaObjetos[inicio:fim]
    
    @classmethod
    def reordenar(cls):
        cls.listaObjetos.sort(key = lambda e: e['tipo'])
        cls.listaObjetosRotina.sort(key = lambda e: e['camada'])

        ind = 0
        for item in cls.listaObjetos:
            item['objeto'].objId = ind
            ind += 1
        
    @classmethod
    def fechar(cls):
        pygame.quit()
