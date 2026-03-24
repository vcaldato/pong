"""
bola.py
=======
Define a entidade Bola do jogo Pong.

Princípios aplicados
--------------------
SRP  — Bola só gerencia sua própria física (posição, velocidade, colisão
       com bordas). A detecção de colisão com raquetes fica em ``Jogo``.
DIP  — Recebe as dimensões da tela no construtor, sem depender de
       variáveis globais.
"""

from __future__ import annotations

from typing import Tuple

import pygame

from constants import (
    ALTURA,
    BOLA_TAMANHO,
    BOLA_VELOCIDADE_X,
    BOLA_VELOCIDADE_Y,
    BRANCO,
    LARGURA,
)


class Bola:
    """
    Representa a bola do Pong.

    Responsabilidades
    -----------------
    - Armazenar posição e velocidade.
    - Mover-se um passo por frame.
    - Rebater nas bordas superior e inferior.
    - Expor métodos semânticos para detectar saída pelos lados.
    - Fornecer retângulo de colisão.
    - Renderizar-se na tela.

    Parâmetros
    ----------
    largura_tela : largura da janela em pixels.
    altura_tela  : altura da janela em pixels.
    """

    def __init__(self, largura_tela: int = LARGURA, altura_tela: int = ALTURA) -> None:
        self._largura_tela = largura_tela
        self._altura_tela = altura_tela
        self.tamanho = BOLA_TAMANHO
        # Velocidade inicial é definida em reset() para evitar duplicação.
        self.vx: int = 0
        self.vy: int = 0
        self.x: int = 0
        self.y: int = 0
        self.reset()

    # ------------------------------------------------------------------
    # Estado
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Volta a bola ao centro da tela com velocidade padrão.

        Chamado no início da partida e após cada ponto marcado.
        """
        self.x = self._largura_tela // 2 - self.tamanho // 2
        self.y = self._altura_tela // 2 - self.tamanho // 2
        self.vx = BOLA_VELOCIDADE_X
        self.vy = BOLA_VELOCIDADE_Y

    def posicao(self) -> Tuple[int, int]:
        """
        Retorna ``(x, y)`` da bola.

        Expõe a posição sem conceder acesso direto aos atributos internos,
        reduzindo o acoplamento com classes externas.
        """
        return self.x, self.y

    # ------------------------------------------------------------------
    # Física
    # ------------------------------------------------------------------

    def mover(self) -> None:
        """
        Avança a bola um frame e rebate nas bordas horizontal (cima/baixo).

        A saída pelas bordas verticais (esquerda/direita) é intencionalmente
        *não* tratada aqui — é responsabilidade de ``Jogo`` decidir o que
        acontece nesses casos (pontuação e reset).
        """
        self.x += self.vx
        self.y += self.vy

        # Rebote na borda superior e inferior
        if self.y <= 0 or self.y >= self._altura_tela - self.tamanho:
            self.vy = -self.vy

    def rebater_horizontal(self, para_direita: bool) -> None:
        """
        Inverte a componente horizontal da velocidade de forma segura.

        O uso de ``abs()`` garante que a bola nunca fique presa dentro
        de uma raquete ao receber dois rebates consecutivos.

        Parâmetros
        ----------
        para_direita : se True, força a bola a ir para a direita;
                       se False, força para a esquerda.
        """
        self.vx = abs(self.vx) if para_direita else -abs(self.vx)

    # ------------------------------------------------------------------
    # Detecção de saída
    # ------------------------------------------------------------------

    def saiu_pela_esquerda(self) -> bool:
        """Retorna True se a bola cruzou a borda esquerda da tela."""
        return self.x <= 0

    def saiu_pela_direita(self) -> bool:
        """Retorna True se a bola cruzou a borda direita da tela."""
        return self.x >= self._largura_tela - self.tamanho

    # ------------------------------------------------------------------
    # Colisão e renderização
    # ------------------------------------------------------------------

    def rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão AABB desta bola."""
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def desenhar(self, tela: pygame.Surface) -> None:
        """Renderiza a bola (círculo) na superfície fornecida."""
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.tamanho)