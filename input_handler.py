"""
input_handler.py
================
Centraliza o processamento de entrada do teclado.

Princípios aplicados
--------------------
SRP  — Separar leitura de input da lógica de jogo permite trocar
       o esquema de controles sem alterar ``Jogo``.
OCP  — Novos esquemas de controle (gamepad, rede) podem ser adicionados
       implementando a mesma interface sem modificar código existente.
"""

from __future__ import annotations

import pygame

from raquete import Raquete


class InputHandler:
    """
    Lê o estado do teclado e aplica os comandos à raquete do player 1.

    Responsabilidades
    -----------------
    - Detectar quais teclas estão pressionadas.
    - Traduzir teclas em comandos de movimento para a raquete alvo.

    Parâmetros
    ----------
    raquete : a raquete que será controlada pelo teclado.
    """

    def __init__(self, raquete: Raquete) -> None:
        self._raquete = raquete

    def processar(self) -> None:
        """
        Lê o estado atual do teclado e move a raquete conforme necessário.

        As setas UP/DOWN controlam o movimento vertical.
        """
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self._raquete.mover_cima()
        if teclas[pygame.K_DOWN]:
            self._raquete.mover_baixo()