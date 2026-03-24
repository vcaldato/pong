"""
placar.py
=========
Define a entidade Placar do jogo Pong.

Princípios aplicados
--------------------
SRP  — Placar só gerencia pontuação e condição de vitória.
       A renderização faz parte do contrato de ``Desenhavel``, mas toda
       a lógica de apresentação (fonte, posição) também fica aqui para
       não vazar para ``Jogo``.
OCP  — O limite de pontos é configurável via construtor; não é preciso
       alterar a classe para mudar as regras da partida.
"""

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
    """
    Mantém e exibe a pontuação de dois jogadores.

    Responsabilidades
    -----------------
    - Registrar pontos para cada jogador.
    - Determinar se algum jogador atingiu o limite de vitória.
    - Renderizar o placar na tela.

    Parâmetros
    ----------
    limite_player1 : pontos necessários para o player 1 vencer.
    limite_player2 : pontos necessários para o player 2 vencer.
    """

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
        """
        Retorna True se algum jogador atingiu seu limite de pontos.

        Separar essa verificação em um método semântico evita que ``Jogo``
        precise conhecer os atributos internos de ``Placar``.
        """
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