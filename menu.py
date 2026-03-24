"""
menu.py
=======
Cena de menu principal do Pong.

Princípios aplicados
--------------------
SRP  — Menu apenas apresenta a tela inicial e aguarda o input de início.
       Não conhece a cena ``Jogo`` nem detalhes de gameplay.
"""

from __future__ import annotations

import sys

import pygame

from constants import (
    ALTURA,
    BRANCO,
    FONTE_TAMANHO_INSTRUCAO,
    FONTE_TAMANHO_TITULO,
    LARGURA,
    PISCAR_CICLO_MS,
    PISCAR_LIGADO_MS,
    PRETO,
)


class Menu:
    """
    Tela de menu com título e instrução piscante.

    Responsabilidades
    -----------------
    - Exibir o título do jogo.
    - Exibir instrução "Pressione ESPAÇO" com efeito de piscar.
    - Aguardar ESPAÇO para retornar ao chamador (que iniciará a partida).

    Parâmetros
    ----------
    tela : superfície pygame principal.
    """

    def __init__(self, tela: pygame.Surface) -> None:
        self._tela = tela
        self._fonte_titulo = pygame.font.SysFont(None, FONTE_TAMANHO_TITULO)
        self._fonte_instrucao = pygame.font.SysFont(None, FONTE_TAMANHO_INSTRUCAO)

    def executar(self) -> None:
        """
        Exibe o menu e bloqueia até que o jogador pressione ESPAÇO.

        O efeito de piscar é calculado com base no tempo total do pygame
        (``pygame.time.get_ticks``), sem precisar de variáveis de estado
        externas.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    return  # inicia o jogo

            self._tela.fill(PRETO)
            self._desenhar_titulo()
            self._desenhar_instrucao_piscante()
            pygame.display.flip()

    # ------------------------------------------------------------------
    # Métodos privados de renderização
    # ------------------------------------------------------------------

    def _desenhar_titulo(self) -> None:
        """Renderiza o título 'Pong' no quarto superior da tela."""
        titulo = self._fonte_titulo.render("Pong", True, BRANCO)
        self._tela.blit(
            titulo,
            titulo.get_rect(center=(LARGURA // 2, ALTURA // 4 + 50)),
        )

    def _desenhar_instrucao_piscante(self) -> None:
        """
        Renderiza a instrução de início com efeito de piscar (1 s ligado / 1 s desligado).

        A visibilidade é determinada pela posição no ciclo de PISCAR_CICLO_MS ms:
        visível quando ``ticks % ciclo < ligado``.
        """
        ticks = pygame.time.get_ticks()
        if ticks % PISCAR_CICLO_MS < PISCAR_LIGADO_MS:
            instrucao = self._fonte_instrucao.render(
                "Pressione ESPAÇO para jogar", True, BRANCO
            )
            self._tela.blit(
                instrucao,
                instrucao.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60)),
            )