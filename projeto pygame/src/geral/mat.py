import pygame
import math
import random

class Mat():

    radParaGraus = 180 / math.pi
    grausParaRad = math.pi / 180
    segParaMili = 1000

    @classmethod
    def polarCartesiano(cls, raio: float, angulo: float, offset: tuple = (0, 0)):
        angulo = cls.loopAngulo(360 - angulo)

        x = offset[0] + raio * round(math.cos(angulo * cls.grausParaRad), 3)
        y = offset[1] + raio * round(math.sin(angulo * cls.grausParaRad), 3)

        return (x, y)
    
    @classmethod
    def cartesianoPolar(cls, x: float, y: float):
        raio = math.sqrt(x**2 + y**2)

        if (y < 0):
            angulo = abs(angulo)

        elif (y > 0):
            angulo = 360 - angulo

        return (raio, angulo)

    @classmethod
    def rodarVetor(cls, vetor: tuple | pygame.Vector2, angulo: float) -> tuple[float, float] | pygame.Vector2 | None:
        returnVal = None
        if (vetor.__class__.__name__ == 'tuple'):
            returnVal = (
                math.cos(angulo * cls.grausParaRad) * vetor[0] - math.sin(angulo * cls.grausParaRad) * vetor[1],
                math.sin(angulo * cls.grausParaRad) * vetor[0] + math.cos(angulo * cls.grausParaRad) * vetor[1]
            )
        elif (vetor.__class__.__name__ == 'Vector2'):
            returnVal = pygame.Vector2(
                math.cos(angulo * cls.grausParaRad) * vetor.x - math.sin(angulo * cls.grausParaRad) * vetor.y,
                math.sin(angulo * cls.grausParaRad) * vetor.x + math.cos(angulo * cls.grausParaRad) * vetor.y
            )
        return returnVal

    @classmethod
    def anguloEntreVetores(cls, vec1: tuple, vec2: tuple):
        vecf = (vec2[0] - vec1[0], vec2[1] - vec1[1])
        
        angulo = math.atan2(vecf[1], vecf[0]) * cls.radParaGraus
        
        if (vecf[1] < 0):
            angulo = abs(angulo)

        elif (vecf[1] > 0):
            angulo = 360 - angulo

        return angulo
    
    @classmethod
    def loopAngulo(cls, angulo: float):
        if (angulo < 0):
            return 360 - (abs(angulo) % 360)
        elif(angulo > 0):
            return angulo % 360
        return angulo

    @classmethod
    def rodarImagem(cls, imagem: pygame.Surface, angulo: float, centro: tuple):
        novoCentro = imagem.get_rect(center=centro).center

        imagemRotacionada = pygame.transform.rotate(imagem, angulo)
        novoRect = imagemRotacionada.get_rect(center=novoCentro)

        return (imagemRotacionada, novoRect)
    
    @classmethod
    def colisaoRetCirculo(cls, raio: float, circPos: tuple, retTamanho: tuple, retPos: tuple) -> bool:
        testX = circPos[0]
        testY = circPos[1]

        if (circPos[0] < retPos[0]):
            testX = retPos[0]
        elif (circPos[0] > retPos[0] + retTamanho[0]):
            testX = retPos[0] + retTamanho[0]

        if (circPos[1] < retPos[1]):
            testY = retPos[1]
        
        elif (circPos[1] > retPos[1] + retTamanho[1]):
            testY = retPos[1] + retTamanho[1]

        distX = circPos[0] - testX
        distY = circPos[1] - testY

        distance = math.sqrt((distX**2) + (distY**2))

        if (distance <= raio):
            return True
    
        return False
    
    @classmethod
    def parabolaNormal(cls, x: float, a: float = -4, b: float = 0, c: float = 1, o: float = -0.5):
        valor =  a*(x+o)**2 + b*(x+o) + c
        # print(f'retornando {valor}')
        return valor
    
    @classmethod
    def decadenciaDeProbabilidade(cls, tamanho) -> int:
        alcance = range(1, tamanho+1)
        soma = 0
        for ind in alcance:
            soma += ind

        listaPorcentagens = []
        for i in range(tamanho):
            listaPorcentagens.append(((tamanho - i) * 100) / soma)
        
        
        valorEscolha = random.randint(0, 100)
        indiceRetorno = -1

        i = 0
        for p in listaPorcentagens:
            soma = sum(listaPorcentagens[:i+1])
            if (valorEscolha <= soma):
                indiceRetorno = i
                break
            i += 1

        if (indiceRetorno == -1):
            raise Exception('Indíce de retorno indeterminado')
        
        print(
            f'len: {tamanho}\nporcentagens: {listaPorcentagens}\n\n'
            f'valor aleatório: {valorEscolha}, índice: {i}\n====================\n'
        )
        return indiceRetorno
