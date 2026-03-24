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
    VOLUME_MUSICA,
)
from input_handler import InputHandler
from placar import Placar
from raquete import IASimples, Raquete
from renderer import Renderer


class Jogo:

    def __init__(self, tela: pygame.Surface, sons: dict) -> None:
        self._tela = tela
        self._clock = pygame.time.Clock()
        self._sons = sons

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

        self._input = InputHandler(self._player1)
        self._ia = IASimples()
        self._renderer = Renderer(
            tela,
            [self._player1, self._player2, self._bola, self._placar],
        )

    def executar(self) -> None:
        # Inicia a música de fundo em loop
        pygame.mixer.music.load("vamo_gremio.mp3")
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.play(loops=-1)

        while True:
            self._processar_eventos()
            self._input.processar()
            self._atualizar_ia()

            vy_antes = self._bola.vy
            self._bola.mover()

            self._verificar_colisoes(vy_antes)

            if self._verificar_pontuacao():
                pygame.mixer.music.stop()
                return

            self._renderer.renderizar()
            self._clock.tick(FPS)

    def _processar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _atualizar_ia(self) -> None:
        bola_x, bola_y = self._bola.posicao()
        self._player2.mover_com_ia(bola_x, bola_y, self._ia)

    def _verificar_colisoes(self, vy_antes: int) -> None:
        if self._bola.rect().colliderect(self._player1.rect()):
            self._bola.rebater_horizontal(para_direita=True)
            self._sons["raquete"].play()

        if self._bola.rect().colliderect(self._player2.rect()):
            self._bola.rebater_horizontal(para_direita=False)
            self._sons["raquete"].play()

        # Detecta rebote na parede pela inversão do vy
        if self._bola.vy != vy_antes:
            self._sons["parede"].play()

    def _verificar_pontuacao(self) -> bool:
        if self._bola.saiu_pela_esquerda():
            self._placar.ponto_player2()
            self._sons["ponto"].play()
            self._bola.reset()
        elif self._bola.saiu_pela_direita():
            self._placar.ponto_player1()
            self._sons["ponto"].play()
            self._bola.reset()

        return self._placar.alguem_venceu()