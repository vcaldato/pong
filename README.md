# 🏓 Pong — Refatorado
 
Projeto do clássico jogo Pong desenvolvido em Python com Pygame, refatorado com foco em boas práticas de engenharia de software.
 
---
 
## 📁 Estrutura de Arquivos
 
```
pong/
├── main.py            # Ponto de entrada — inicialização e loop principal
├── constants.py       # Centraliza todas as constantes do jogo
├── interfaces.py      # Define protocolos/contratos (ISP, DIP)
├── bola.py            # Entidade Bola — física e colisão
├── raquete.py         # Entidade Raquete + estratégia de IA
├── placar.py          # Pontuação e condição de vitória
├── input_handler.py   # Leitura de teclado e tradução em comandos
├── renderer.py        # Orquestra o ciclo de desenho
├── jogo.py            # Cena da partida — coordena o loop
└── menu.py            # Cena do menu inicial
```
 
---
 
## ▶️ Como Executar
 
```bash
pip install pygame
python main.py
```
 
**Controles:** setas `↑` / `↓` movem a raquete do player 1.
 
---
 
## 🔍 Critérios de Refatoração
 
### Abstração
 
- `interfaces.py` declara protocolos estruturais (`Desenhavel`, `Movel`, `Controlavel`, `Cena`) usando `typing.Protocol` — duck-typing sem herança explícita.
- `Bola.posicao()` expõe apenas `(x, y)` como tupla, sem dar acesso direto aos atributos internos `vx` e `vy`.
- `Bola.rebater_horizontal(para_direita)` encapsula a lógica de inversão de velocidade — `Jogo` não precisa conhecer o atributo `vx`.
- `EstrategiaIA` (protocolo em `raquete.py`) permite trocar a inteligência artificial sem alterar a classe `Raquete`.
 
---
 
### Separação de Responsabilidades
 
| Responsabilidade | Código Original | Refatorado para |
|---|---|---|
| Leitura do teclado | `Jogo.processar_input()` | `InputHandler` |
| Decisão de movimento da IA | `Raquete.seguir_bola()` | `IASimples` |
| Renderização | `Jogo.desenhar()` | `Renderer` |
| Condição de vitória | `Placar.alguem_venceu()` | Mantido em `Placar` |
| Constantes globais | Espalhadas em vários lugares | `constants.py` |
| Contratos/interfaces | Inexistente | `interfaces.py` |
 
---
 
### Princípios SOLID
 
**S — Single Responsibility**
Cada módulo tem uma única razão para mudar. `renderer.py` muda apenas se a lógica de desenho mudar. `input_handler.py` muda apenas se o esquema de controles mudar.
 
**O — Open/Closed**
`Raquete.mover_com_ia()` recebe uma `EstrategiaIA` por parâmetro. Para criar uma IA mais difícil, basta criar uma nova classe sem modificar `Raquete` ou `Jogo`:
 
```python
class IADificil:
    def calcular_movimento(self, raquete_y, raquete_altura, bola_x, bola_y) -> int:
        # lógica preditiva aqui
        ...
```
 
**L — Liskov Substitution**
Qualquer implementação de `EstrategiaIA` pode substituir `IASimples` sem quebrar o sistema. O contrato de assinatura e semântica de retorno é preservado por design.
 
**I — Interface Segregation**
Os protocolos em `interfaces.py` são granulares: `Desenhavel` exige apenas `desenhar()`, `Resetavel` exige apenas `reset()`. Nenhuma classe implementa métodos que não usa.
 
**D — Dependency Inversion**
- `Renderer` depende da lista de `Desenhavel`, não de `Raquete`, `Bola` ou `Placar` concretos.
- `Bola` e `Raquete` recebem as dimensões da tela pelo construtor, sem ler variáveis globais.
 
---
 
### Legibilidade
 
- Métodos com nomes semânticos: `saiu_pela_esquerda()`, `rebater_horizontal()`, `alguem_venceu()`.
- Atributos privados prefixados com `_` (`_ia`, `_renderer`, `_input`) sinalizam que não fazem parte da API pública.
- Nenhum método ultrapassa 20 linhas.
- Constantes nomeadas (`PISCAR_CICLO_MS`, `RAQUETE_MARGEM`) substituem literais mágicos espalhados pelo código.
 
---
 
### Documentação
 
Todos os módulos, classes e métodos públicos possuem docstrings descrevendo o propósito, os parâmetros e os princípios SOLID aplicados. Exemplo:
 
```python
def rebater_horizontal(self, para_direita: bool) -> None:
    """
    Inverte a componente horizontal da velocidade de forma segura.
 
    O uso de abs() garante que a bola nunca fique presa dentro
    de uma raquete ao receber dois rebates consecutivos.
    """
```
 
---
 
## 📊 Comparativo: Antes × Depois
 
| Critério | Antes | Depois |
|---|---|---|
| Arquivos | 1 | 10 |
| Constantes globais espalhadas | Sim | Não — centralizadas em `constants.py` |
| Acoplamento `Jogo` ↔ `Bola` | Alto (acessa `vx`, `vy` diretamente) | Baixo (apenas `posicao()`) |
| Testabilidade | Baixa | Alta — injeção de dependência |
| Extensibilidade da IA | Requer editar `Raquete` | Criar nova classe |
| Docstrings | Nenhuma | 100% dos módulos e métodos |
| Type hints | Parcial | Completo |
 
---