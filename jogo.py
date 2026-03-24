"""
jogo.py
=======
Cena principal de uma partida do Pong.

Princípios aplicados
--------------------
SRP  — ``Jogo`` coordena o loop da partida, delegando cada
       responsabilidade a objetos especializados:
         • InputHandler  → leitura de teclado
         • IASimples     → decisão da IA
         • Renderer      → desenho na tela
         • Placar        → pontuação e condição de vitória
OCP  — Novas estratégias de IA ou esquemas de controle podem ser
       injetados sem alterar este módulo.
DIP  — ``Jogo`` depende de abstrações (protocolos) e de instâncias
       injetadas, não de classes concretas.
"""

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
    """
    Cena de uma partida completa de Pong.

    Responsabilidades
    -----------------
    - Instanciar e compor todos os objetos da partida.
    - Executar o loop principal: eventos → input → IA → física → colisão
      → pontuação → render.
    - Retornar ao chamador quando a partida terminar.

    Parâmetros
    ----------
    tela : superfície pygame principal, criada externamente e passada
           por injeção de dependência.
    """

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

    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------

    def executar(self) -> None:
        """
        Executa o loop da partida até que alguém vença.

        Ordem de execução por frame
        ---------------------------
        1. Processar eventos do sistema (fechar janela).
        2. Processar input do jogador humano.
        3. Calcular movimento da IA.
        4. Mover a bola.
        5. Verificar colisões bola ↔ raquetes.
        6. Verificar pontuação e condição de fim de jogo.
        7. Renderizar o frame.
        8. Limitar a taxa de frames.
        """
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

    # ------------------------------------------------------------------
    # Métodos privados de atualização
    # ------------------------------------------------------------------

    def _processar_eventos(self) -> None:
        """Encerra o processo se o usuário fechar a janela."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _atualizar_ia(self) -> None:
        """
        Passa apenas as coordenadas da bola para a IA.

        A raquete da IA não recebe o objeto Bola inteiro — apenas os
        dados que ela precisa — reduzindo o acoplamento.
        """
        bola_x, bola_y = self._bola.posicao()
        self._player2.mover_com_ia(bola_x, bola_y, self._ia)

    def _verificar_colisoes(self) -> None:
        """
        Detecta e resolve colisões entre a bola e as raquetes.

        O ``Jogo`` coordena a colisão, mas delega a resolução à ``Bola``
        por meio de um método semântico (``rebater_horizontal``),
        sem acessar ``vx``/``vy`` diretamente.
        """
        if self._bola.rect().colliderect(self._player1.rect()):
            self._bola.rebater_horizontal(para_direita=True)
        if self._bola.rect().colliderect(self._player2.rect()):
            self._bola.rebater_horizontal(para_direita=False)

    def _verificar_pontuacao(self) -> bool:
        """
        Atualiza o placar se a bola saiu da tela e verifica vitória.

        Retorna
        -------
        bool : True se a partida terminou, False caso contrário.
        """
        if self._bola.saiu_pela_esquerda():
            self._placar.ponto_player2()
            self._bola.reset()
        elif self._bola.saiu_pela_direita():
            self._placar.ponto_player1()
            self._bola.reset()

        return self._placar.alguem_venceu()