import pygame
from scripts.fases import Fase1, Fase2, Fase3  # Certifique-se de que as fases estão importadas corretamente
from scripts.jogador import Jogador
from scripts.plataformas import PlataformaParada, PlataformaMovel, PlataformaPuloAlto

def tela_de_morte(tela, pontos):
    fonte = pygame.font.Font(None, 74)
    texto_game_over = fonte.render("Você caiu!", True, (255, 0, 0))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    texto_reiniciar = pygame.font.Font(None, 36).render("Pressione qualquer tecla para reiniciar", True, (255, 255, 255))

    tela.fill((0, 0, 0))
    tela.blit(texto_game_over, (200, 200))
    tela.blit(texto_pontos, (250, 300))
    tela.blit(texto_reiniciar, (150, 400))
    pygame.display.flip()

    # Esperar entrada do jogador para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

# Loop principal do jogo
def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jogo de Plataformas")
    clock = pygame.time.Clock()

    # Fontes para exibir pontuação
    fonte_pontos = pygame.font.Font(None, 36)

    # Imagens de fundo para cada fase
    fundo_fase1 = pygame.image.load("assets/cenario_predio_2.png")
    fundo_fase2 = pygame.image.load("assets/cidade.png")
    fundo_fase3 = pygame.image.load("assets/cenario_ceu_3.png")

    jogador = Jogador(400, 500)  # Passando x e y
    fase_atual = Fase1(tela, jogador)  # Sem o argumento 'plano_de_fundo'
    fundo_atual = fundo_fase1  # Começa com o fundo da Fase1

    # Criar plataformas
    plataforma1 = PlataformaParada(200, 400, 100, 20)
    plataforma_mov = PlataformaMovel(400, 300, 100, 20, 2)  # Plataforma móvel no centro
    plataforma_pulo_alto = PlataformaPuloAlto(300, 200, 100, 20)  # Plataforma de pulo alto
    plataformas = [plataforma1, plataforma_mov, plataforma_pulo_alto]

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if jogador.caiu:
            tela_de_morte(tela, jogador.pontos)
            jogador = Jogador(400, 500)  # Passando x e y
            fase_atual = Fase1(tela, jogador)  # Sem o argumento 'plano_de_fundo'
            fundo_atual = fundo_fase1

        # Verificar mudança de fase com base nos pontos
        if jogador.pontos >= 400:
            if isinstance(fase_atual, Fase1):
                fase_atual = Fase2(tela, jogador)  # Sem o argumento 'plano_de_fundo'
                fundo_atual = fundo_fase2
            elif isinstance(fase_atual, Fase2):
                fase_atual = Fase3(tela, jogador)  # Sem o argumento 'plano_de_fundo'
                fundo_atual = fundo_fase3
            else:
                fase_atual = Fase1(tela, jogador)  # Sem o argumento 'plano_de_fundo'
                fundo_atual = fundo_fase1
            jogador.pontos = 0

            # Pausa de 3 segundos
            tela.fill((0, 0, 0))
            texto_pausa = fonte_pontos.render("Próxima fase em 3 segundos...", True, (255, 255, 255))
            tela.blit(texto_pausa, (200, 300))
            pygame.display.flip()
            pygame.time.delay(3000)

        # Desenhar o fundo
        tela.blit(fundo_atual, (0, 0))

        # Atualizar e desenhar a fase
        fase_atual.atualizar()
        fase_atual.desenhar()

        # Atualizar plataformas
        for plataforma in plataformas:
            plataforma.atualizar(jogador )
            plataforma.desenhar(tela)

        # Exibir pontuação
        texto_pontos = fonte_pontos.render(f"Pontos: {jogador.pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()