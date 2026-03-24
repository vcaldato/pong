"""
interfaces.py
=============
Define as interfaces (protocolos) do jogo Pong.

Aplicando os princípios de Interface Segregation (ISP) e Dependency
Inversion (DIP) do SOLID:

- As classes de alto nível (Jogo, Menu) dependem dessas abstrações,
  não de implementações concretas.
- Cada protocolo declara apenas o contrato mínimo necessário para
  o papel que representa.

Uso de ``typing.Protocol`` (Python 3.8+) permite duck-typing estrutural:
qualquer classe que implemente os métodos exigidos satisfaz a interface,
sem herança explícita.
"""

from __future__ import annotations

from typing import Protocol, Tuple

import pygame


class Desenhavel(Protocol):
    """Interface para qualquer objeto que sabe se desenhar na tela."""

    def desenhar(self, tela: pygame.Surface) -> None:
        """Renderiza o objeto na superfície fornecida."""
        ...


class Movel(Protocol):
    """Interface para objetos que possuem movimento próprio."""

    def mover(self) -> None:
        """Avança o objeto um passo de simulação."""
        ...


class Colisivel(Protocol):
    """Interface para objetos que participam de colisão."""

    def rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão AABB do objeto."""
        ...


class Resetavel(Protocol):
    """Interface para objetos que podem retornar ao estado inicial."""

    def reset(self) -> None:
        """Restaura o estado inicial do objeto."""
        ...


class Controlavel(Protocol):
    """Interface para objetos cujo movimento é comandado externamente."""

    def mover_cima(self, limite_topo: int = 0) -> None:
        """Move o objeto para cima respeitando o limite superior."""
        ...

    def mover_baixo(self, limite_base: int = 0) -> None:
        """Move o objeto para baixo respeitando o limite inferior."""
        ...


class Cena(Protocol):
    """
    Interface para qualquer cena do jogo (Menu, Partida, Tela de Fim).

    Segue o padrão *Game State* / *Scene*: cada tela encapsula seu
    próprio loop e devolve controle ao gerenciador ao terminar.
    """

    def executar(self) -> None:
        """Executa o loop desta cena até que ela decida terminar."""
        ...