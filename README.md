# 🏓 Pong

Jogo Pong clássico feito em Python com Pygame, organizado em classes desacopladas.

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

```
pong.py
 ├── Raquete   — posição, movimento e colisão da raquete
 ├── Bola      — posição, movimento e colisão da bola
 ├── Placar    — pontuação e condição de vitória
 ├── Jogo      — loop principal, une todas as classes
 └── Menu      — tela inicial
```

---

## Classes

### `Raquete`

Representa uma raquete. Recebe posição e tamanho no construtor, sem depender de nenhuma outra classe.

- `mover_cima()` / `mover_baixo()` — move respeitando os limites da tela
- `seguir_bola(bola_x, bola_y)` — lógica da IA. Recebe apenas as coordenadas da bola, não o objeto `Bola` inteiro, então a `Raquete` não depende de como a `Bola` é implementada internamente
- `rect()` — retorna o retângulo de colisão

---

### `Bola`

Representa a bola. Recebe as dimensões da tela no construtor em vez de usar constantes globais, o que a torna reutilizável em qualquer tamanho de janela.

Todos os atributos internos (`vx`, `vy`, `x`, `y`) são acessados apenas por métodos, impedindo que outras classes dependam deles diretamente:

- `mover()` — atualiza posição e rebate no teto/chão
- `rebater_horizontal(para_direita)` — inverte a direção horizontal de forma segura. Usa `abs()` para garantir que a bola nunca fique presa dentro de uma raquete
- `saiu_pela_esquerda()` / `saiu_pela_direita()` — informa se a bola saiu da tela
- `posicao()` — retorna `(x, y)` sem expor os atributos diretamente
- `reset()` — recoloca a bola no centro após um ponto

---

### `Placar`

Guarda a pontuação e os limites de vitória. Os limites (`10` e `2`) são definidos aqui, não espalhados pelo `Jogo`.

- `ponto_player1()` / `ponto_player2()` — incrementa a pontuação
- `alguem_venceu()` — retorna `True` se algum jogador atingiu o limite
- `desenhar()` — renderiza o placar no topo da tela

---

### `Jogo`

Orquestra o loop principal. Não acessa atributos internos de nenhuma classe — só chama métodos.

A cada frame, na ordem:

1. `processar_eventos()` — verifica se o usuário fechou a janela
2. `processar_input()` — lê o teclado e move o player 1
3. `seguir_bola()` — move a IA passando apenas a posição da bola
4. `bola.mover()` — atualiza a posição da bola
5. `verificar_colisoes()` — checa se a bola bateu em alguma raquete
6. `verificar_pontuacao()` — checa se alguém fez ponto ou venceu
7. `desenhar()` — limpa a tela e desenha tudo
8. `clock.tick(60)` — limita a 60 frames por segundo

---

### `Menu`

Exibe a tela inicial e aguarda `ESPAÇO` para começar. Não conhece nenhuma outra classe do jogo.

- O efeito de piscar usa `pygame.time.get_ticks() % 2000 < 1000`: nos primeiros 1000ms o texto aparece, nos 1000ms seguintes some

---

## Por que as classes são desacopladas?

| Situação                                    | O que muda                                    |
| ------------------------------------------- | --------------------------------------------- |
| Renomear `bola.vx` para `bola.velocidade_x` | Só dentro de `Bola`                           |
| Mudar os limites de vitória                 | Só em `Placar`                                |
| Trocar a lógica da IA                       | Só em `Raquete.seguir_bola()`                 |
| Mudar o tamanho da janela                   | Só as constantes `LARGURA` e `ALTURA` no topo |

---

## Fluxo do programa

```
main()
 └── loop eterno
      ├── Menu.executar()   → aguarda ESPAÇO
      └── Jogo.executar()   → roda até alguém vencer, depois volta ao menu
```
