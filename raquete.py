
from __future__ import annotations

from typing import Protocol

import pygame

from constants import (
    ALTURA,
    BRANCO,
    RAQUETE_VELOCIDADE,
)

class EstrategiaIA(Protocol):

    def calcular_movimento(
        self,
        raquete_y: int,
        raquete_altura: int,
        bola_x: float,
        bola_y: float,
    ) -> int:

        ...


class IASimples:


    def calcular_movimento(
        self,
        raquete_y: int,
        raquete_altura: int,
        bola_x: float,
        bola_y: float,
    ) -> int:
        centro = raquete_y + raquete_altura // 2
        if centro < bola_y:
            return 1    # mover para baixo
        if centro > bola_y:
            return -1   # mover para cima
        return 0        # parado


class Raquete:

    def __init__(
        self,
        x: int,
        y: int,
        largura: int,
        altura: int,
        velocidade: int = RAQUETE_VELOCIDADE,
        altura_tela: int = ALTURA,
    ) -> None:
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self._altura_tela = altura_tela

    def mover_cima(self, limite_topo: int = 0) -> None:
        """Move a raquete para cima sem ultrapassar ``limite_topo``."""
        if self.y > limite_topo:
            self.y -= self.velocidade

    def mover_baixo(self, limite_base: int | None = None) -> None:
        """Move a raquete para baixo sem ultrapassar ``limite_base``."""
        limite = limite_base if limite_base is not None else self._altura_tela
        if self.y < limite - self.altura:
            self.y += self.velocidade

    def mover_com_ia(self, bola_x: float, bola_y: float, ia: EstrategiaIA) -> None:

        direcao = ia.calcular_movimento(self.y, self.altura, bola_x, bola_y)
        if direcao == -1:
            self.mover_cima()
        elif direcao == 1:
            self.mover_baixo()

    def rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão AABB desta raquete."""
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela: pygame.Surface) -> None:
        """Renderiza a raquete na superfície fornecida."""
        pygame.draw.rect(tela, BRANCO, self.rect())