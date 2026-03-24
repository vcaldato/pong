"""
renderer.py
===========
Centraliza toda a lógica de renderização de uma partida.

Princípios aplicados
--------------------
SRP  — ``Jogo`` não precisa saber como os objetos são desenhados ou em
       que ordem; essa responsabilidade pertence ao ``Renderer``.
DIP  — ``Renderer`` depende da interface ``Desenhavel``, não de classes
       concretas, permitindo adicionar novos objetos visuais sem alteração.
"""

from __future__ import annotations

from typing import List

import pygame

from constants import PRETO
from interfaces import Desenhavel


class Renderer:
    """
    Orquestra o ciclo de desenho de uma cena.

    A cada frame limpa a tela, chama ``desenhar`` em cada objeto registrado
    e atualiza o display.

    Parâmetros
    ----------
    tela     : superfície pygame principal.
    objetos  : lista de objetos ``Desenhavel`` a renderizar, em ordem.
    """

    def __init__(self, tela: pygame.Surface, objetos: List[Desenhavel]) -> None:
        self._tela = tela
        self._objetos = objetos

    def adicionar(self, obj: Desenhavel) -> None:
        """Registra um novo objeto para ser desenhado nos próximos frames."""
        self._objetos.append(obj)

    def renderizar(self) -> None:
        """Limpa a tela, desenha todos os objetos e atualiza o display."""
        self._tela.fill(PRETO)
        for obj in self._objetos:
            obj.desenhar(self._tela)
        pygame.display.flip()