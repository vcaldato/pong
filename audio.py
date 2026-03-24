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
        partes.append(np.zeros(int(taxa * 0.02), dtype=np.float32))

    completo = np.concatenate(partes)
    amostras = (completo * 32767 * VOLUME_EFEITOS).astype(np.int16)
    stereo = np.column_stack([amostras, amostras])
    return pygame.sndarray.make_sound(stereo)


def _gerar_musica():
    
    taxa = AUDIO_FREQUENCIA
    duracao_nota = 0.25  

    notas = [
        220, 261, 329,   # Am
        174, 220, 261,   # F
        130, 164, 196,   # C
        196, 246, 293,   # G
    ]

    partes = []
    for freq in notas:
        n = int(taxa * duracao_nota)
        t = np.linspace(0, duracao_nota, n, endpoint=False)
        onda = (
            0.7 * np.sin(2 * np.pi * freq * t) +
            0.2 * np.sin(4 * np.pi * freq * t)
        ).astype(np.float32)
        fade = int(n * 0.2)
        onda[-fade:] *= np.linspace(1, 0, fade)
        partes.append(onda)

    completo = np.concatenate(partes)
    amostras = (completo * 32767 * VOLUME_MUSICA).astype(np.int16)
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
        "musica":  _gerar_musica(),
    }

    return sons