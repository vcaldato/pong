
from __future__ import annotations

from typing import List

import pygame

from constants import PRETO
from interfaces import Desenhavel


class Renderer:


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