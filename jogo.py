

from __future__ import annotations

import sys

import pygame

from bola import Bola
from constants import (
    ALTURA,
    FPS,
    LARGURA,
    PRETO,
    RAQUETE_ALTURA,
    RAQUETE_LARGURA,
    RAQUETE_MARGEM,
)
from input_handler import InputHandler
from placar import Placar
from raquete import IASimples, Raquete
from renderer import Renderer


class Jogo:
  

    def __init__(self, tela: pygame.Surface) -> None:
        self._tela = tela
        self._clock = pygame.time.Clock()

        # --- Entidades ------------------------------------------------
        self._player1 = Raquete(
            x=RAQUETE_MARGEM,
            y=ALTURA // 2 - RAQUETE_ALTURA // 2,
            largura=RAQUETE_LARGURA,
            altura=RAQUETE_ALTURA,
        )
        self._player2 = Raquete(
            x=LARGURA - RAQUETE_MARGEM - RAQUETE_LARGURA,
            y=ALTURA // 2 - RAQUETE_ALTURA // 2,
            largura=RAQUETE_LARGURA,
            altura=RAQUETE_ALTURA,
        )
        self._bola = Bola(LARGURA, ALTURA)
        self._placar = Placar()

        # --- Serviços -------------------------------------------------
        self._input = InputHandler(self._player1)
        self._ia = IASimples()
        self._renderer = Renderer(
            tela,
            [self._player1, self._player2, self._bola, self._placar],
        )


    def executar(self) -> None:
     
        while True:
            self._processar_eventos()
            self._input.processar()
            self._atualizar_ia()
            self._bola.mover()
            self._verificar_colisoes()
            if self._verificar_pontuacao():
                return  # devolve controle ao Menu
            self._renderer.renderizar()
            self._clock.tick(FPS)


    def _processar_eventos(self) -> None:
        """Encerra o processo se o usuário fechar a janela."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _atualizar_ia(self) -> None:
    
        bola_x, bola_y = self._bola.posicao()
        self._player2.mover_com_ia(bola_x, bola_y, self._ia)

    def _verificar_colisoes(self) -> None:
      
        if self._bola.rect().colliderect(self._player1.rect()):
            self._bola.rebater_horizontal(para_direita=True)
        if self._bola.rect().colliderect(self._player2.rect()):
            self._bola.rebater_horizontal(para_direita=False)

    def _verificar_pontuacao(self) -> bool:
    
        if self._bola.saiu_pela_esquerda():
            self._placar.ponto_player2()
            self._bola.reset()
        elif self._bola.saiu_pela_direita():
            self._placar.ponto_player1()
            self._bola.reset()

        return self._placar.alguem_venceu()