# 🏓 Pong

Jogo Pong clássico feito em Python com Pygame, organizado em classes.

---

## Como executar

```bash
pip install pygame
python pong.py
```

**Controles:** `↑` / `↓` para mover a raquete. O adversário é controlado por IA.

---

## Condições de vitória

| Jogador           | Condição         |
| ----------------- | ---------------- |
| Player 1 (humano) | Marcar 10 pontos |
| Player 2 (IA)     | Marcar 2 pontos  |

Ao encerrar, o jogo volta automaticamente para o menu.

---

## Estrutura do código

O código é dividido em 5 classes. Cada uma cuida de uma parte do jogo.

---

### `Raquete`

Representa uma raquete na tela.

- Guarda a posição (`x`, `y`), tamanho e velocidade
- `mover_cima()` e `mover_baixo()` movem a raquete respeitando os limites da tela
- `seguir_bola()` é usado pela IA: compara o centro da raquete com a posição da bola e move na direção certa
- `rect()` retorna o retângulo de colisão, usado para detectar se a bola bateu

---

### `Bola`

Representa a bola e controla seu movimento.

- `reset()` recoloca a bola no centro da tela com velocidade padrão — chamado no início e após cada ponto
- `mover()` atualiza a posição a cada frame e rebate nas bordas de cima e baixo invertendo `vy`
- `rect()` retorna o retângulo de colisão

---

### `Placar`

Guarda e exibe a pontuação.

- Mantém `player1` e `player2` como contadores simples
- `desenhar()` renderiza o placar no topo central da tela

---

### `Jogo`

Classe principal que une tudo e roda o loop do jogo.

- `processar_eventos()` — fecha o jogo se o usuário clicar no X
- `processar_input()` — lê as setas do teclado e move o player 1
- `verificar_colisoes()` — detecta se a bola bateu em alguma raquete e inverte a direção horizontal. Usa `abs()` para garantir que a bola sempre saia na direção correta, evitando que ela fique presa dentro da raquete
- `verificar_pontuacao()` — checa se a bola saiu pela esquerda ou direita, atribui o ponto e verifica se alguém venceu
- `desenhar()` — limpa a tela e desenha todos os elementos
- `executar()` — loop principal: processa input → move → colisão → pontuação → desenha → 60 FPS

---

### `Menu`

Exibe a tela inicial.

- Mostra o título "Pong" e uma mensagem piscante
- O efeito de piscar usa `pygame.time.get_ticks() % 2000 < 1000`: nos primeiros 1000ms do ciclo o texto aparece, nos 1000ms seguintes some
- Aguarda o jogador pressionar `ESPAÇO` para iniciar

---

## Fluxo do programa

```
main()
 └── loop eterno
      ├── Menu.executar()   → aguarda ESPAÇO
      └── Jogo.executar()   → roda até alguém vencer, depois volta ao menu
```
