import pygame

class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.rect)  # Cor verde para plataformas


class PlataformaParada(Plataforma):
    pass  # Comportamento padrão, sem alterações


class PlataformaMovel(Plataforma):
    def __init__(self, x, y, largura, altura, velocidade):
        super().__init__(x, y, largura, altura)
        self.direcao = 1  # 1 para direita, -1 para esquerda
        self.velocidade = velocidade

    def atualizar(self):
        self.rect.x += self.direcao * self.velocidade  # Mover para a direita
        if self.rect.left < 0 or self.rect.right > 800:  # Verificar limites da tela
            self.direcao *= -1  # Inverter direção


class PlataformaPuloAlto(Plataforma):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura)
        self.trampolim = True  # Indica que é um trampolim