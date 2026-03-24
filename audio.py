import numpy as np
import pygame

from constants import (
    AUDIO_FREQUENCIA,
    AUDIO_TAMANHO,
    AUDIO_CANAIS,
    AUDIO_BUFFER,
    VOLUME_EFEITOS,
    VOLUME_MUSICA,
)


def _gerar_som(frequencia, duracao_ms):
    n = int(AUDIO_FREQUENCIA * duracao_ms / 1000)
    t = np.linspace(0, duracao_ms / 1000, n, endpoint=False)
    onda = np.sin(2 * np.pi * frequencia * t).astype(np.float32)

    fade = int(n * 0.3)
    onda[-fade:] *= np.linspace(1, 0, fade)

    amostras = (onda * 32767 * VOLUME_EFEITOS).astype(np.int16)
    stereo = np.column_stack([amostras, amostras])
    return pygame.sndarray.make_sound(stereo)


def _gerar_ponto():
    taxa = AUDIO_FREQUENCIA
    notas = [(523, 80), (659, 80), (784, 160)]  # C5, E5, G5
    partes = []

    for freq, ms in notas:
        n = int(taxa * ms / 1000)
        t = np.linspace(0, ms / 1000, n, endpoint=False)
        onda = np.sin(2 * np.pi * freq * t).astype(np.float32)
        fade = int(n * 0.3)
        onda[-fade:] *= np.linspace(1, 0, fade)
        partes.append(onda)
        partes.append(np.zeros(int(taxa * 0.02), dtype=np.float32))  # pausa entre notas

    completo = np.concatenate(partes)
    amostras = (completo * 32767 * VOLUME_EFEITOS).astype(np.int16)
    stereo = np.column_stack([amostras, amostras])
    return pygame.sndarray.make_sound(stereo)


def inicializar():
    pygame.mixer.init(
        frequency=AUDIO_FREQUENCIA,
        size=AUDIO_TAMANHO,
        channels=AUDIO_CANAIS,
        buffer=AUDIO_BUFFER,
    )

    sons = {
        "raquete": _gerar_som(480, 55),
        "parede":  _gerar_som(320, 45),
        "ponto":   _gerar_ponto(),
    }

    return sons