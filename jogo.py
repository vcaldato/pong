from __future__ import annotations

import random
import sys

import pygame

from bola import Bola
from constants import (
    ALTURA,
    FPS,
    LARGURA,
    RAQUETE_ALTURA,
    RAQUETE_LARGURA,
    RAQUETE_MARGEM,
    VOLUME_MUSICA,
    POWERUP_INTERVALO_MS,
    POWERUP_TOTAL_BOLAS,
)
from input_handler import InputHandler
from placar import Placar
from raquete import IASimples, Raquete


def _cor_aleatoria():
    """Gera uma cor RGB aleatória vibrante (evita cores muito escuras)."""
    return (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255),
    )


def _criar_distractors(bola_original: Bola) -> list:
    """Cria bolas de distração a partir da posição e velocidade da bola original."""
    distractors = []
    for _ in range(POWERUP_TOTAL_BOLAS - 1):
        nova = Bola(cor=_cor_aleatoria(), verdadeira=False)
        nova.x = bola_original.x
        nova.y = bola_original.y
        nova.vx = bola_original.vx * random.choice([-1, 1])
        nova.vy = bola_original.vy + random.randint(-3, 3)
        distractors.append(nova)
    return distractors


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

        # Bola verdadeira (branca) — única que pontua
        self._bola = Bola(cor=(255, 255, 255), verdadeira=True)

        # Lista com todas as bolas ativas (verdadeira + distrações)
        self._bolas: list = [self._bola]

        self._placar = Placar()
        self._input = InputHandler(self._player1)
        self._ia = IASimples()

        self._som_parede_tocado: bool = False

        # Controle do power-up
        self._ultimo_powerup_ms: int = pygame.time.get_ticks()
        self._powerup_pronto: bool = False

    def executar(self) -> None:
        pygame.mixer.music.load("vamo_gremio.mp3")
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.play(loops=-1)

        while True:
            self._processar_eventos()
            self._input.processar()
            self._atualizar_ia()
            self._atualizar_powerup_timer()

            for bola in self._bolas:
                vy_antes = bola.vy
                bola.mover()
                if bola.vy != vy_antes and not self._som_parede_tocado:
                    self._sons["parede"].play()
                    self._som_parede_tocado = True
            self._som_parede_tocado = False

            self._verificar_colisoes()

            if self._verificar_pontuacao():
                pygame.mixer.music.stop()
                return

            self._desenhar()
            self._clock.tick(FPS)

    def _desenhar(self) -> None:
        """Limpa a tela, desenha tudo e atualiza o display uma única vez por frame."""
        self._tela.fill((0, 0, 0))
        self._player1.desenhar(self._tela)
        self._player2.desenhar(self._tela)
        self._placar.desenhar(self._tela)
        for bola in self._bolas:
            bola.desenhar(self._tela)
        pygame.display.flip()

    def _processar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _atualizar_ia(self) -> None:
        # A IA persegue sempre a bola verdadeira
        bola_x, bola_y = self._bola.posicao()
        self._player2.mover_com_ia(bola_x, bola_y, self._ia)

    def _atualizar_powerup_timer(self) -> None:
        """Marca o power-up como pronto após POWERUP_INTERVALO_MS."""
        agora = pygame.time.get_ticks()
        if not self._powerup_pronto:
            if agora - self._ultimo_powerup_ms >= POWERUP_INTERVALO_MS:
                self._powerup_pronto = True

    def _verificar_colisoes(self) -> None:
        for bola in self._bolas:
            colidiu = False

            if bola.rect().colliderect(self._player1.rect()):
                bola.rebater_horizontal(para_direita=True)
                self._sons["raquete"].play()
                colidiu = True

            if bola.rect().colliderect(self._player2.rect()):
                bola.rebater_horizontal(para_direita=False)
                self._sons["raquete"].play()
                colidiu = True

            # Fragmenta apenas a bola verdadeira quando o power-up está pronto
            if colidiu and bola.verdadeira and self._powerup_pronto:
                self._fragmentar(bola)

    def _fragmentar(self, bola: Bola) -> None:
        """Remove distrações antigas e cria novas a partir da posição atual."""
        self._bolas = [b for b in self._bolas if b.verdadeira]
        self._bolas += _criar_distractors(bola)
        self._powerup_pronto = False
        self._ultimo_powerup_ms = pygame.time.get_ticks()

    def _verificar_pontuacao(self) -> bool:
        """Só a bola verdadeira pontua. Distrações que saem são removidas silenciosamente."""
        bolas_para_remover = []

        for bola in self._bolas:
            if bola.saiu_pela_esquerda():
                if bola.verdadeira:
                    self._placar.ponto_player2()
                    self._sons["ponto"].play()
                    self._resetar_bolas()
                    return self._placar.alguem_venceu()
                else:
                    bolas_para_remover.append(bola)

            elif bola.saiu_pela_direita():
                if bola.verdadeira:
                    self._placar.ponto_player1()
                    self._sons["ponto"].play()
                    self._resetar_bolas()
                    return self._placar.alguem_venceu()
                else:
                    bolas_para_remover.append(bola)

        for bola in bolas_para_remover:
            self._bolas.remove(bola)

        return False

    def _resetar_bolas(self) -> None:
        """Volta para apenas a bola verdadeira no centro."""
        self._bola.reset()
        self._bolas = [self._bola]
        self._powerup_pronto = False
        self._ultimo_powerup_ms = pygame.time.get_ticks()