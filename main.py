
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