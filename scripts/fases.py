import pygame
import random
from scripts.plataformas import PlataformaParada, PlataformaMovel, PlataformaPuloAlto

# Classe Jogador
class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(375, 500, 50, 50)
        self.velocidade = 0
        self.pontos = 0
        self.pontos_totais = 0  # Nova variável para pontos totais acumulados
        self.caiu = False
        self.movimento = pygame.Vector2(0, 0)  # Movimentos X e Y
        self.velocidade_horizontal = 5  # Velocidade de movimento lateral
        self.em_pulo = False
        self.imagem = pygame.image.load("assets/jogador.png").convert_alpha()  # Carrega a imagem do jogador
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))  # Redimensiona a imagem do jogador

    def atualizar(self, plataformas):
        # Gravidade
        self.velocidade += 0.5  # Gravidade
        self.rect.y += self.velocidade

        # Movimento lateral
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade_horizontal
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade_horizontal

        # Colisão com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self.velocidade > 0:
                self.velocidade = -10 if hasattr(plataforma, 'trampolim') and plataforma.trampolim else -5
                self.em_pulo = False
                break

        # Impede o jogador de sair da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def pular(self):
        if not self.em_pulo:
            self.velocidade = -15
            self.em_pulo = True

    def adicionar_pontos(self, pontos):
        """Adiciona pontos à pontuação total"""
        self.pontos_totais += pontos  # Adiciona os pontos da fase
        self.pontos = 0  # Reinicia os pontos da fase atual

    def desenhar(self, tela):
        # Desenha o jogador usando a imagem
        tela.blit(self.imagem, self.rect.topleft)  # Usa a imagem do jogador na posição atual

# Classe FaseBase
class FaseBase:
    def __init__(self, tela, jogador, plano_de_fundo, velocidade_fundo):
        self.tela = tela
        self.jogador = jogador
        self.velocidade_fundo = velocidade_fundo  # Velocidade das plataformas
        self.offset_y = 0
        self.plano_de_fundo = pygame.image.load(f"assets/{plano_de_fundo}").convert()
        self.plano_de_fundo = pygame.transform.scale(self.plano_de_fundo, (800, 600))
        self.plataformas = []

        # Inicializando o mixer de áudio e tocando a música de fundo
        pygame.mixer.init()  # Inicializa o mixer de áudio
        pygame.mixer.music.load('assets/musica_fundo.mp3')  # Carrega o arquivo de áudio
        pygame.mixer.music.play(-1, 0.0)  # Toca a música em loop (-1 indica loop infinito)

        for i in range(5):
            tipo = random.choice([PlataformaParada, PlataformaMovel, PlataformaPuloAlto])
            largura = random.randint(100, 150)
            altura = 20
            x = random.randint(50, 800 - largura)
            y = 600 - i * 120
            if tipo == PlataformaMovel:
                plataforma = PlataformaMovel(x, y, largura, altura, velocidade=random.randint(1, 3))
            else:
                plataforma = tipo(x, y, largura, altura)
            self.plataformas.append(plataforma)

        self.posicionar_jogador_na_primeira_plataforma_visivel()

    def posicionar_jogador_na_primeira_plataforma_visivel(self):
        for plataforma in self.plataformas:
            if plataforma.rect.top < self.tela.get_height():
                self.jogador.rect.midbottom = (plataforma.rect.centerx, plataforma.rect.top)
                self.jogador.velocidade = 0
                break

    def gerar_plataforma(self):
        """Gera uma nova plataforma no topo da tela."""
        tipo = random.choice([PlataformaParada, PlataformaMovel, PlataformaPuloAlto])
        largura = random.randint(100, 150)
        altura = 20
        x = random.randint(50, 800 - largura)
        y = random.randint(-150, -50)  # Posicionar fora da tela, acima
        if tipo == PlataformaMovel:
            return PlataformaMovel(x, y, largura, altura, velocidade=random.randint(1, 3))
        return tipo(x, y, largura, altura)

    def atualizar(self):
        self.offset_y += self.velocidade_fundo
        if self.offset_y >= self.plano_de_fundo.get_height():
            self.offset_y = 0

        self.jogador.atualizar(self.plataformas)

        # Atualizar plataformas e gerar novas
        for plataforma in self.plataformas[:]:
            if isinstance(plataforma, PlataformaMovel):
                plataforma.atualizar()
            # Mover todas as plataformas para baixo (movimento de fundo)
            plataforma.rect.y += self.velocidade_fundo

            # Remover plataformas que saem pela parte inferior
            if plataforma.rect.top > self.tela.get_height():
                self.plataformas.remove(plataforma)

        # Adicionar novas plataformas se o número estiver abaixo do limite
        while len(self.plataformas) < 6:  # Garante no mínimo 6 plataformas
            self.plataformas.append(self.gerar_plataforma())

    def desenhar(self):
        # Desenha o fundo (movimento de fundo)
        self.tela.blit(self.plano_de_fundo, (0, -self.plano_de_fundo.get_height() + self.offset_y))
        self.tela.blit(self.plano_de_fundo, (0, self.offset_y))
        for plataforma in self.plataformas:
            plataforma.desenhar(self.tela)
        self.jogador.desenhar(self.tela)  # Desenha o jogador com a imagem

    def finalizar_fase(self):
        """Método para finalizar a fase e somar pontos totais."""
        self.jogador.adicionar_pontos(100)  # Exemplo: adicionar 100 pontos por fase

    def verificar_vitoria(self):
        """Verifica se o jogador atingiu 400 pontos na 3ª fase."""
        if self.jogador.pontos_totais >= 400:
            return True
        return False

# Classes Fase1, Fase2 e Fase3
class Fase1(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cenario_predio_2.png", 2)

    def finalizar_fase(self):
        super().finalizar_fase()

class Fase2(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cidade.png", 3)

    def finalizar_fase(self):
        super().finalizar_fase()

class Fase3(FaseBase):
    def __init__(self, tela, jogador):
        super().__init__(tela, jogador, "cenario_ceu_3.png", 4)  # Mais rápido na terceira fase

    def finalizar_fase(self):
        super().finalizar_fase()

    def verificar_vitoria(self):
        """Verifica se o jogador atingiu 400 pontos na 3ª fase."""
        if self.jogador.pontos_totais >= 400:
            return True
        return False

# Função para exibir a pontuação final ao morrer
def exibir_pontuacao_final(tela, jogador):
    font = pygame.font.Font(None, 50)
    texto = font.render(f'Pontos Totais: {jogador.pontos_totais}', True, (255, 255, 255))
    tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() // 2))

def acao_final(tela, jogador):
    font = pygame.font.Font(None, 50)
    texto = font.render("Você Venceu!", True, (255, 255, 255))
    tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() // 2))
