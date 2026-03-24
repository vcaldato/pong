
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

    def __init__(self, tela: pygame.Surface) -> None:
        self._tela = tela
        self._fonte_titulo = pygame.font.SysFont(None, FONTE_TAMANHO_TITULO)
        self._fonte_instrucao = pygame.font.SysFont(None, FONTE_TAMANHO_INSTRUCAO)

    def executar(self) -> None:

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

    def _desenhar_titulo(self) -> None:
        """Renderiza o título 'Pong' no quarto superior da tela."""
        titulo = self._fonte_titulo.render("Pong", True, BRANCO)
        self._tela.blit(
            titulo,
            titulo.get_rect(center=(LARGURA // 2, ALTURA // 4 + 50)),
        )

    def _desenhar_instrucao_piscante(self) -> None:

        ticks = pygame.time.get_ticks()
        if ticks % PISCAR_CICLO_MS < PISCAR_LIGADO_MS:
            instrucao = self._fonte_instrucao.render(
                "Pressione ESPAÇO para jogar", True, BRANCO
            )
            self._tela.blit(
                instrucao,
                instrucao.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60)),
            )