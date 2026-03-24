
from __future__ import annotations

import pygame

from constants import (
    BRANCO,
    FONTE_TAMANHO_PLACAR,
    LARGURA,
    LIMITE_PONTOS_PLAYER1,
    LIMITE_PONTOS_PLAYER2,
)


class Placar:

    def __init__(
        self,
        limite_player1: int = LIMITE_PONTOS_PLAYER1,
        limite_player2: int = LIMITE_PONTOS_PLAYER2,
    ) -> None:
        self.player1: int = 0
        self.player2: int = 0
        self._limite_player1 = limite_player1
        self._limite_player2 = limite_player2
        self._fonte = pygame.font.SysFont(None, FONTE_TAMANHO_PLACAR)

    # ------------------------------------------------------------------
    # Pontuação
    # ------------------------------------------------------------------

    def ponto_player1(self) -> None:
        """Incrementa a pontuação do player 1."""
        self.player1 += 1

    def ponto_player2(self) -> None:
        """Incrementa a pontuação do player 2."""
        self.player2 += 1

    def alguem_venceu(self) -> bool:

        return (
            self.player1 >= self._limite_player1
            or self.player2 >= self._limite_player2
        )

    # ------------------------------------------------------------------
    # Renderização
    # ------------------------------------------------------------------

    def desenhar(self, tela: pygame.Surface) -> None:
        """Exibe 'pontos_p1 - pontos_p2' centralizado no topo da tela."""
        texto = self._fonte.render(
            f"{self.player1} - {self.player2}", True, BRANCO
        )
        tela.blit(texto, texto.get_rect(center=(LARGURA // 2, 30)))