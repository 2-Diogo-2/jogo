import pygame
from scripts.fases import Fase1, Fase2, Fase3
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

    jogador = Jogador(400, 500)
    fase_atual = Fase1(tela, jogador)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if jogador.caiu:
            tela_de_morte(tela, jogador.pontos)
            jogador = Jogador(400, 500)
            fase_atual = Fase1(tela, jogador)

        if jogador.pontos >= 400:
            if isinstance(fase_atual, Fase1):
                fase_atual = Fase2(tela, jogador)
            elif isinstance(fase_atual, Fase2):
                fase_atual = Fase3(tela, jogador)
            else:
                fase_atual = Fase1(tela, jogador)
            jogador.pontos = 0

            tela.fill((0, 0, 0))
            texto_pausa = pygame.font.Font(None, 36).render("Próxima fase em 3 segundos...", True, (255, 255, 255))
            tela.blit(texto_pausa, (200, 300))
            pygame.display.flip()
            pygame.time.delay(3000)

        tela.fill((0, 0, 0))
        fase_atual.atualizar()
        fase_atual.desenhar()

        texto_pontos = pygame.font.Font(None, 36).render(f"Pontos: {jogador.pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
