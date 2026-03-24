
from __future__ import annotations

import pygame

from raquete import Raquete


class InputHandler:


    def __init__(self, raquete: Raquete) -> None:
        self._raquete = raquete

    def processar(self) -> None:

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self._raquete.mover_cima()
        if teclas[pygame.K_DOWN]:
            self._raquete.mover_baixo()