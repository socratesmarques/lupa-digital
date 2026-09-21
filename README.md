# Lupa Digital V0.5.0 — PySide6 / Qt

Reestruturação da Lupa Digital para usar **PySide6 (Qt)** como interface gráfica.

O OpenCV continua responsável por:

- Creative VF0780;
- captura dos frames;
- zoom;
- nitidez;
- contraste;
- filtros para baixa visão.

O PySide6 passa a ser responsável por:

- janela;
- tela cheia;
- exibição do vídeo;
- painel de informações;
- botões visuais;
- guia de leitura;
- atalhos de teclado;
- integração do loop de eventos.

## Arquitetura

```text
main.py
   │
   ▼
PySide6 / MainWindow
   │
   ├─────────────── QTimer câmera
   │                       │
   │                       ▼
   │                 LupaEngine
   │                 │       │
   │                 │       ├── OpenCV
   │                 │       ├── zoom
   │                 │       ├── filtros
   │                 │       └── melhoria
   │                 │
   │                 ▼
   │              VF0780
   │
   └─────────────── QTimer GPIO
                           │
                           ▼
                    Joystick Shield
```

O antigo:

```text
while True
cv2.imshow()
cv2.waitKey()
```

foi removido da interface.

## Estrutura do projeto

```text
lupa-digital-v0.5.0-pyside6-orange-pi-3-lts/
│
├── main.py
├── requirements.txt
├── run_orangepi.sh
│
├── core/
│   └── lupa_engine.py
│
├── ui/
│   ├── main_window.py
│   ├── video_widget.py
│   └── styles.py
│
├── camera/
│   └── camera.py
│
├── hardware/
│   ├── botoes_gpio.py
│   ├── controles.py
│   └── pinos.py
│
├── processamento/
│   ├── melhoria.py
│   ├── modos_leitura.py
│   └── zoom.py
│
├── config/
│   └── settings.py
│
└── tools/
```

## Joystick Shield V1.A

A montagem física atual foi preservada.

| Botão | Shield | Orange Pi 3 LTS | Função |
|---|---|---:|---|
| A | D2 | físico 11 | cima |
| B | D3 | físico 13 | direita |
| C | D4 | físico 15 | baixo |
| D | D5 | físico 16 | esquerda |
| E | D6 | físico 24 | Zoom - |
| F | D7 | físico 22 | Zoom + |
| K | D8 | físico 18 | Freeze |

Alimentação:

```text
Shield VCC -> físico 1 (3.3 V)
Shield GND -> físico 9
```

## Interface de baixa visão

A interface usa:

- fundo escuro;
- texto branco;
- fontes grandes;
- botões grandes;
- indicador de zoom;
- modo visual atual;
- estado de nitidez e iluminação;
- indicador do Joystick Shield;
- fullscreen automático.

Os controles visuais são complementares. O Joystick Shield continua sendo o
controle físico principal.

## Controles físicos

```text
A = cima
B = direita
C = baixo
D = esquerda

E = Zoom -
F = Zoom +

K = Freeze
```

## Teclado para desenvolvimento

| Tecla | Ação |
|---|---|
| `+` | Zoom + |
| `-` | Zoom - |
| `W` / ↑ | cima |
| `A` / ← | esquerda |
| `D` / → | direita |
| `X` / ↓ | baixo |
| `C` | centralizar |
| `Espaço` | Freeze |
| `F` | próximo modo |
| `R` | guia de leitura |
| `H` | esconder/mostrar status |
| `M` / `F11` | fullscreen |
| `S` | captura |
| `Q` / `Esc` | sair |

## Instalação

Crie o ambiente:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Atualize o pip:

```bash
pip install --upgrade pip
```

Instale:

```bash
pip install -r requirements.txt
```

A versão do PySide6 foi fixada em `6.8.0` porque essa geração possui pacote
Linux ARM64 compatível com uma base glibc mais antiga do que as versões
PySide6 mais novas.

### Se você já usa OpenCV do sistema

Como a interface agora é Qt, não precisamos de `cv2.imshow()`.

Por isso o requirements usa:

```text
opencv-python-headless
```

Isso reduz o risco de conflito entre o Qt empacotado pelo OpenCV e o PySide6.

Se preferir o OpenCV instalado pelo sistema:

```bash
sudo apt install python3-opencv
```

nesse caso você pode remover `opencv-python-headless` do `requirements.txt`.

## Executar

Dentro da sessão gráfica do Orange Pi:

```bash
python3 main.py
```

ou:

```bash
./run_orangepi.sh
```

### GPIO e sudo

Uma aplicação Qt deve ter acesso à sessão gráfica.

Evite começar diretamente com:

```bash
sudo python3 main.py
```

porque `sudo` pode perder as variáveis da tela gráfica.

Se a sua imagem exigir root para os GPIOs, use:

```bash
sudo -E env DISPLAY="$DISPLAY" \
XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}" \
./.venv/bin/python main.py
```

## Testar processamento

```bash
python3 tools/teste_processamento.py
```

## Testar estrutura Qt

```bash
python3 tools/teste_estrutura_qt.py
```

## Testar Joystick Shield

```bash
python3 tools/teste_botoes_gpio.py
```

Se houver erro de permissão:

```bash
sudo python3 tools/teste_botoes_gpio.py
```

## Principais diferenças da V0.5.0

- PySide6 substitui `cv2.imshow`.
- Não existe mais `cv2.waitKey`.
- A câmera é atualizada por `QTimer`.
- O GPIO é lido por outro `QTimer`.
- Processamento foi separado em `LupaEngine`.
- Interface foi separada em `ui/`.
- Guia de leitura agora é desenhado com `QPainter`.
- Fullscreen é controlado pelo Qt.
- Freeze e zoom físicos continuam iguais.
- Toda a fiação atual do Orange Pi 3 LTS foi mantida.

## Versão

`0.5.0`
