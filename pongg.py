import pygame
import sys

pygame.init()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Tamanho da janela
LARGURA = 800
ALTURA = 600


class Raquete:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 10
        self.altura = 60
        self.velocidade = 5

    def mover_cima(self):
        # Impede sair pela borda de cima
        if self.y > 0:
            self.y -= self.velocidade

    def mover_baixo(self):
        # Impede sair pela borda de baixo
        if self.y < ALTURA - self.altura:
            self.y += self.velocidade

    def seguir_bola(self, bola):
        # IA: move o centro da raquete em direção à bola
        centro = self.y + self.altura // 2
        if centro < bola.y:
            self.mover_baixo()
        elif centro > bola.y:
            self.mover_cima()

    def rect(self):
        # Retorna o retângulo de colisão da raquete
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect())


class Bola:
    def __init__(self):
        self.tamanho = 7
        self.reset()

    def reset(self):
        # Volta a bola para o centro com velocidade padrão
        self.x = LARGURA // 2 - self.tamanho // 2
        self.y = ALTURA // 2 - self.tamanho // 2
        self.vx = 5
        self.vy = 5

    def mover(self):
        self.x += self.vx
        self.y += self.vy

        # Rebate na borda de cima e de baixo
        if self.y <= 0 or self.y >= ALTURA - self.tamanho:
            self.vy = -self.vy

    def rect(self):
        # Retorna o retângulo de colisão da bola
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.tamanho)


class Placar:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.font = pygame.font.SysFont(None, 36)

    def desenhar(self, tela):
        # Exibe "pontos_p1 - pontos_p2" no topo central da tela
        texto = self.font.render(f"{self.player1} - {self.player2}", True, BRANCO)
        tela.blit(texto, texto.get_rect(center=(LARGURA // 2, 30)))


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()

        # Player 1 à esquerda, Player 2 (IA) à direita
        self.player1 = Raquete(15, ALTURA // 2 - 30)
        self.player2 = Raquete(LARGURA - 25, ALTURA // 2 - 30)
        self.bola = Bola()
        self.placar = Placar()

    def processar_eventos(self):
        # Fecha o jogo se o usuário clicar no X da janela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def processar_input(self):
        # Move o player 1 com as setas do teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player1.mover_cima()
        if keys[pygame.K_DOWN]:
            self.player1.mover_baixo()

    def verificar_colisoes(self):
        # Rebate a bola ao colidir com alguma raquete
        # abs() garante que a bola sempre saia na direção certa
        if self.bola.rect().colliderect(self.player1.rect()):
            self.bola.vx = abs(self.bola.vx)   # empurra para a direita
        if self.bola.rect().colliderect(self.player2.rect()):
            self.bola.vx = -abs(self.bola.vx)  # empurra para a esquerda

    def verificar_pontuacao(self):
        # Bola saiu pela esquerda: ponto para a IA
        if self.bola.x <= 0:
            self.placar.player2 += 1
            self.bola.reset()
            if self.placar.player2 >= 2:
                return True  # IA venceu, encerra o jogo

        # Bola saiu pela direita: ponto para o jogador
        if self.bola.x >= LARGURA - self.bola.tamanho:
            self.placar.player1 += 1
            self.bola.reset()
            if self.placar.player1 >= 10:
                return True  # Jogador venceu, encerra o jogo

        return False

    def desenhar(self):
        self.tela.fill(PRETO)
        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)
        self.bola.desenhar(self.tela)
        self.placar.desenhar(self.tela)
        pygame.display.flip()

    def executar(self):
        while True:
            self.processar_eventos()
            self.processar_input()
            self.player2.seguir_bola(self.bola)  # move a IA
            self.bola.mover()
            self.verificar_colisoes()
            if self.verificar_pontuacao():
                return  # volta para o menu
            self.desenhar()
            self.clock.tick(60)  # limita a 60 frames por segundo


class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.font_titulo = pygame.font.SysFont(None, 50)
        self.font_instrucao = pygame.font.SysFont(None, 26)

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    return  # inicia o jogo

            self.tela.fill(PRETO)

            titulo = self.font_titulo.render("Pong", True, BRANCO)
            self.tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, ALTURA // 4 + 50)))

            # Pisca a instrução a cada 1 segundo (1000ms ligado, 1000ms desligado)
            if pygame.time.get_ticks() % 2000 < 1000:
                instrucao = self.font_instrucao.render("Pressione ESPAÇO para jogar", True, BRANCO)
                self.tela.blit(instrucao, instrucao.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60)))

            pygame.display.flip()


def main():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pong")

    menu = Menu(tela)

    # Loop principal: menu → jogo → menu → jogo ...
    while True:
        menu.executar()
        Jogo(tela).executar()


if __name__ == "__main__":
    main()
