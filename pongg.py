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
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = 5

    def mover_cima(self, limite_topo=0):
        if self.y > limite_topo:
            self.y -= self.velocidade

    def mover_baixo(self, limite_base=ALTURA):
        # Impede sair pela borda de baixo
        if self.y < limite_base - self.altura:
            self.y += self.velocidade

    def seguir_bola(self, bola_x, bola_y):
        # IA: recebe a posição da bola em vez de depender do objeto Bola
        centro = self.y + self.altura // 2
        if centro < bola_y:
            self.mover_baixo()
        elif centro > bola_y:
            self.mover_cima()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect())


class Bola:
    def __init__(self, largura_tela, altura_tela):
        # Recebe as dimensões da tela em vez de usar constantes globais
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = 7
        self.reset()

    def reset(self):
        # Volta a bola para o centro com velocidade padrão
        self.x = self.largura_tela // 2 - self.tamanho // 2
        self.y = self.altura_tela // 2 - self.tamanho // 2
        self.vx = 5
        self.vy = 5

    def mover(self):
        self.x += self.vx
        self.y += self.vy

        # Rebate na borda de cima e de baixo
        if self.y <= 0 or self.y >= self.altura_tela - self.tamanho:
            self.vy = -self.vy

    def rebater_horizontal(self, para_direita: bool):
        # Inverte a direção horizontal de forma segura
        # abs() garante que a bola nunca fique presa dentro de uma raquete
        self.vx = abs(self.vx) if para_direita else -abs(self.vx)

    def saiu_pela_esquerda(self):
        return self.x <= 0

    def saiu_pela_direita(self):
        return self.x >= self.largura_tela - self.tamanho

    def posicao(self):
        # Expõe a posição sem dar acesso direto aos atributos internos
        return self.x, self.y

    def rect(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.tamanho)


class Placar:
    def __init__(self, limite_player1, limite_player2):
        # Limites de vitória ficam no Placar, não espalhados pelo Jogo
        self.player1 = 0
        self.player2 = 0
        self.limite_player1 = limite_player1
        self.limite_player2 = limite_player2
        self.font = pygame.font.SysFont(None, 36)

    def ponto_player1(self):
        self.player1 += 1

    def ponto_player2(self):
        self.player2 += 1

    def alguem_venceu(self):
        return self.player1 >= self.limite_player1 or self.player2 >= self.limite_player2

    def desenhar(self, tela):
        # Exibe "pontos_p1 - pontos_p2" no topo central da tela
        texto = self.font.render(f"{self.player1} - {self.player2}", True, BRANCO)
        tela.blit(texto, texto.get_rect(center=(LARGURA // 2, 30)))


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()

        # Player 1 à esquerda, Player 2 (IA) à direita
        self.player1 = Raquete(15, ALTURA // 2 - 30, 10, 60)
        self.player2 = Raquete(LARGURA - 25, ALTURA // 2 - 30, 10, 60)
        self.bola = Bola(LARGURA, ALTURA)
        self.placar = Placar(limite_player1=10, limite_player2=2)

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
        # Usa métodos da Bola para rebater — Jogo não acessa vx/vy diretamente
        if self.bola.rect().colliderect(self.player1.rect()):
            self.bola.rebater_horizontal(para_direita=True)
        if self.bola.rect().colliderect(self.player2.rect()):
            self.bola.rebater_horizontal(para_direita=False)

    def verificar_pontuacao(self):
        # Usa métodos da Bola e do Placar — sem acessar atributos internos
        if self.bola.saiu_pela_esquerda():
            self.placar.ponto_player2()
            self.bola.reset()

        elif self.bola.saiu_pela_direita():
            self.placar.ponto_player1()
            self.bola.reset()

        return self.placar.alguem_venceu()

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

            # IA recebe apenas a posição, não o objeto Bola inteiro
            bola_x, bola_y = self.bola.posicao()
            self.player2.seguir_bola(bola_x, bola_y)

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
