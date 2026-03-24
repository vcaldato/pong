"""
constants.py
============
Centraliza todas as constantes do jogo Pong.

Seguindo o princípio da responsabilidade única (SRP), este módulo
existe apenas para declarar valores fixos usados em todo o projeto,
facilitando ajustes sem necessidade de rastrear o código inteiro.
"""

# ---------------------------------------------------------------------------
# Tela
# ---------------------------------------------------------------------------
LARGURA: int = 800
ALTURA: int = 600
FPS: int = 60
TITULO_JANELA: str = "Pong"

# ---------------------------------------------------------------------------
# Cores (R, G, B)
# ---------------------------------------------------------------------------
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# ---------------------------------------------------------------------------
# Raquete
# ---------------------------------------------------------------------------
RAQUETE_LARGURA: int = 10
RAQUETE_ALTURA: int = 60
RAQUETE_VELOCIDADE: int = 5
RAQUETE_MARGEM: int = 15   # distância da raquete à borda da tela

# ---------------------------------------------------------------------------
# Bola
# ---------------------------------------------------------------------------
BOLA_TAMANHO: int = 7
BOLA_VELOCIDADE_X: int = 5
BOLA_VELOCIDADE_Y: int = 5

# ---------------------------------------------------------------------------
# Placar
# ---------------------------------------------------------------------------
LIMITE_PONTOS_PLAYER1: int = 10
LIMITE_PONTOS_PLAYER2: int = 2

# ---------------------------------------------------------------------------
# Fonte
# ---------------------------------------------------------------------------
FONTE_TAMANHO_PLACAR: int = 36
FONTE_TAMANHO_TITULO: int = 50
FONTE_TAMANHO_INSTRUCAO: int = 26

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
PISCAR_CICLO_MS: int = 2000   # duração de um ciclo de piscar em milissegundos
PISCAR_LIGADO_MS: int = 1000  # quanto tempo o texto fica visível por ciclo