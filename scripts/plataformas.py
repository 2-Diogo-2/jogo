import pygame

class Plataforma:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)

class PlataformaParada(Plataforma):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura, (0, 255, 0))  # Verde para plataformas estáticas

class PlataformaMovel(Plataforma):
    def __init__(self, x, y, largura, altura, velocidade):
        super().__init__(x, y, largura, altura, (0, 0, 255))  # Azul para plataformas móveis
        self.direcao = 1
        self.velocidade = velocidade

    def atualizar(self):
        self.rect.x += self.direcao * self.velocidade
        if self.rect.left < 0 or self.rect.right > 800:
            self.direcao *= -1

class PlataformaPuloAlto(Plataforma):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura, (255, 0, 0))  # Vermelho para trampolins
        self.trampolim = True
