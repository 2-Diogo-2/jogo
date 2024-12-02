import pygame
from scripts.plataformas import PlataformaPuloAlto  # Importando a classe PlataformaPuloAlto

class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.velocidade = 0
        self.pontos = 0
        self.na_plataforma = False
        self.caiu = False
        self.no_ar = False
        self.pulo_duplo = True  # Permite um pulo extra no ar

    def atualizar(self, plataformas):
        keys = pygame.key.get_pressed()

        # Movimentação
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 10  # Aumentar velocidade para 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 10

        # Pulo
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]):
            if not self.no_ar or self.pulo_duplo:
                self.velocidade = -20
                self.no_ar = True
                if self.pulo_duplo:
                    self.pulo_duplo = False

        # Gravidade
        self.velocidade += 1
        self.rect.y += self.velocidade

        # Limitar movimento lateral
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))

        # Impedir que o jogador saia pela parte superior
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocidade = 0

        colidiu = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Colisão superior
                if self.rect.bottom <= plataforma.rect.top + self.velocidade:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidade = -25 if isinstance(plataforma, PlataformaPuloAlto) else -20
                    colidiu = True
                    self.no_ar = False  # Permite pular novamente
                    self.pulo_duplo = True  # Restaura o pulo duplo
                    if not self.na_plataforma:
                        self.pontos += 5
                        self.na_plataforma = True

        if not colidiu:
            self.na_plataforma = False

        # Verifique se o jogador caiu
        if self.rect.bottom >= 600:
            self.caiu = True

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 0, 0), self.rect)  # Cor vermelha para o jogador