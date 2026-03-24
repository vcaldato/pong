from __future__ import annotations

import random
from typing import Tuple

import pygame

from constants import (
    ALTURA,
    BOLA_TAMANHO,
    BOLA_VELOCIDADE_X,
    BOLA_VELOCIDADE_Y,
    BRANCO,
    LARGURA,
    BOLA_VARIACAO_ANGULO,
    BOLA_VY_MINIMO,
    BOLA_VY_MAXIMO,
)


class Bola:

    def __init__(self, largura_tela: int = LARGURA, altura_tela: int = ALTURA) -> None:
        self._largura_tela = largura_tela
        self._altura_tela = altura_tela
        self.tamanho = BOLA_TAMANHO
        self.vx: int = 0
        self.vy: int = 0
        self.x: int = 0
        self.y: int = 0
        self.reset()

    def reset(self) -> None:
        self.x = self._largura_tela // 2 - self.tamanho // 2
        self.y = self._altura_tela // 2 - self.tamanho // 2
        self.vx = BOLA_VELOCIDADE_X
        self.vy = BOLA_VELOCIDADE_Y

    def posicao(self) -> Tuple[int, int]:
        return self.x, self.y

    def mover(self) -> None:
        self.x += self.vx
        self.y += self.vy

        if self.y <= 0 or self.y >= self._altura_tela - self.tamanho:
            self.vy = -self.vy
            self._variar_angulo()

    def rebater_horizontal(self, para_direita: bool) -> None:
        self.vx = abs(self.vx) if para_direita else -abs(self.vx)
        self._variar_angulo()

    def _variar_angulo(self) -> None:
 
        variacao = random.randint(-BOLA_VARIACAO_ANGULO, BOLA_VARIACAO_ANGULO)
        novo_vy = self.vy + variacao

        sinal = 1 if novo_vy >= 0 else -1
        self.vy = sinal * max(BOLA_VY_MINIMO, min(abs(novo_vy), BOLA_VY_MAXIMO))

    def saiu_pela_esquerda(self) -> bool:
        return self.x <= 0

    def saiu_pela_direita(self) -> bool:
        return self.x >= self._largura_tela - self.tamanho

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def desenhar(self, tela: pygame.Surface) -> None:
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.tamanho)