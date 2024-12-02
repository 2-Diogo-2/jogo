import pygame
import random
from scripts.plataformas import PlataformaParada, PlataformaMovel, PlataformaPuloAlto  # Importando as plataformas

# Classe Jogador
class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(375, 500, 50, 50)
        self.velocidade = 0
        self.pontos = 0
        self.caiu = False

    def atualizar(self, plataformas):
        self.velocidade += 0.5  # Gravidade
        self.rect.y += self.velocidade

        # Colisão com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self.velocidade > 0:
                self.velocidade = -10 if hasattr(plataforma, 'trampolim') and plataforma.trampolim else -5
                break

# Classe FaseBase
class FaseBase:
    def __init__(self, tela, jogador, plano_de_fundo="cenario_predio_2.png", movendo=False):
        self.tela = tela
        self.jogador = jogador
        self.movendo = movendo
        self.velocidade_fundo = 2
        self.offset_y = 0
        self.plataformas = []

        # Carregar e redimensionar o fundo
        self.plano_de_fundo = pygame.image.load(f"assets/{plano_de_fundo}")
        self.plano_de_fundo = pygame.transform.scale(self.plano_de_fundo, (800, 600))

        # Gerar plataformas iniciais
        for i in range(5):
            tipo = random.choice([PlataformaParada, PlataformaMovel, PlataformaPuloAlto])
            plataforma = tipo(random.randint(50, 750), 600 - i * 120, random.randint(80, 150), random.randint(15, 25))
            self.plataformas.append(plataforma)

        # Posicionar o jogador sobre a primeira plataforma visível
        self.posicionar_jogador_na_primeira_plataforma_visivel()

    def posicionar_jogador_na_primeira_plataforma_visivel(self):
        for plataforma in self.plataformas:
            if plataforma.rect.top < self.tela.get_height():
                self.jogador.rect.midbottom = (plataforma.rect.centerx, plataforma.rect.top)
                self.jogador.velocidade = 0
                break

    def atualizar(self):
        # Verificar se o jogador caiu
        if self.jogador.rect.top > self.tela.get_height():
            self.jogador.caiu = True
            return self.jogador.pontos

        # Movimento do fundo
        self.offset_y = (self.offset_y + self.velocidade_fundo) % self.plano_de_fundo.get_height()

        # Atualizar jogador
        self.jogador.atualizar(self.plataformas)

        # Atualizar plataformas
        for plataforma in self.plataformas:
            plataforma.atualizar(self.jogador)

        # Desenhar plataformas
        self.desenhar()

    def desenhar(self):
        self.tela.blit(self.plano_de_fundo, (0, self.offset_y))
        for plataforma in self.plataformas:
            plataforma.desenhar(self.tela)
        pygame.draw.rect(self.tela, (255, 0, 0), self.jogador.rect)  # Cor vermelha para o jogador

# Classes Fase1, Fase2 e Fase3
class Fase1(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cenario_predio_2.png")

class Fase2(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cidade.png")

class Fase3(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cenario_ceu_3.png")