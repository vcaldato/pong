"""
raquete.py
==========
Define a entidade Raquete e a estratégia de IA para o adversário.

Princípios aplicados
--------------------
SRP  — Raquete apenas representa e move uma raquete; a lógica de IA
       fica em ``IASimples``, que pode ser substituída sem tocar em Raquete.
OCP  — Novas estratégias de IA podem ser adicionadas implementando
       ``EstrategiaIA`` sem modificar o código existente.
DIP  — ``Raquete`` não sabe nada sobre ``Bola``; recebe apenas coordenadas.
"""

from __future__ import annotations

from typing import Protocol

import pygame

from constants import (
    ALTURA,
    BRANCO,
    RAQUETE_VELOCIDADE,
)


# ---------------------------------------------------------------------------
# Protocolo – Estratégia de IA (Strategy pattern)
# ---------------------------------------------------------------------------

class EstrategiaIA(Protocol):
    """
    Contrato para qualquer estratégia de movimentação automática.

    Ao depender desse protocolo em vez de uma implementação concreta,
    ``Raquete`` respeita o Dependency Inversion Principle.
    """

    def calcular_movimento(
        self,
        raquete_y: int,
        raquete_altura: int,
        bola_x: float,
        bola_y: float,
    ) -> int:
        """
        Retorna a direção do movimento: -1 (cima), 0 (parado) ou +1 (baixo).
        """
        ...


# ---------------------------------------------------------------------------
# Implementação padrão de IA
# ---------------------------------------------------------------------------

class IASimples:
    """
    Estratégia de IA que alinha o centro da raquete com a bola.

    Esta implementação é intencionalmente simples para que o jogador
    humano tenha chance de pontuar. Pode ser substituída por qualquer
    outra implementação de ``EstrategiaIA``.
    """

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


# ---------------------------------------------------------------------------
# Entidade Raquete
# ---------------------------------------------------------------------------

class Raquete:
    """
    Representa uma raquete do Pong.

    Responsabilidades
    -----------------
    - Armazenar posição e dimensões.
    - Aplicar movimento com verificação de limites de tela.
    - Fornecer retângulo de colisão.
    - Renderizar-se na tela.

    Parâmetros
    ----------
    x, y        : posição inicial (canto superior esquerdo).
    largura     : largura em pixels.
    altura      : altura em pixels.
    velocidade  : pixels por frame de deslocamento.
    altura_tela : altura da janela, usado para limitar o movimento inferior.
    """

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

    # ------------------------------------------------------------------
    # Movimentação
    # ------------------------------------------------------------------

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
        """
        Delega o cálculo de direção à estratégia de IA e aplica o movimento.

        Nota: A raquete recebe coordenadas brutas da bola, não o objeto Bola.
        Isso reduz o acoplamento — a raquete não precisa conhecer Bola.
        """
        direcao = ia.calcular_movimento(self.y, self.altura, bola_x, bola_y)
        if direcao == -1:
            self.mover_cima()
        elif direcao == 1:
            self.mover_baixo()

    # ------------------------------------------------------------------
    # Colisão e renderização
    # ------------------------------------------------------------------

    def rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão AABB desta raquete."""
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela: pygame.Surface) -> None:
        """Renderiza a raquete na superfície fornecida."""
        pygame.draw.rect(tela, BRANCO, self.rect())