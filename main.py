"""
main.py
=======
Ponto de entrada do jogo Pong refatorado.

Responsabilidades
-----------------
- Inicializar o pygame.
- Criar a janela.
- Orquestrar o ciclo de vida: Menu → Jogo → Menu → Jogo …

Este módulo é intencionalmente mínimo — toda a lógica fica nas cenas.
"""

import pygame

from constants import ALTURA, LARGURA, TITULO_JANELA
from jogo import Jogo
from menu import Menu


def main() -> None:
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO_JANELA)

    menu = Menu(tela)

    while True:
        menu.executar()
        Jogo(tela).executar()


if __name__ == "__main__":
    main()