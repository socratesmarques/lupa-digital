# Lupa Digital V0.4.3 — Orange Pi 3 LTS

Esta versão corresponde à montagem física atual.

## Montagem final

```text
             ORANGE PI 3 LTS
             Cabeçalho GPIO

  PINO 1  ●  ← 3.3V ───────── Shield VCC

  PINO 9  ●  ← GND ────────── Shield GND

  PINO 11 ●  ← Shield A / D2 ─ CIMA
  PINO 13 ●  ← Shield B / D3 ─ DIREITA
  PINO 15 ●  ← Shield C / D4 ─ BAIXO
  PINO 16 ●  ← Shield D / D5 ─ ESQUERDA

  PINO 18 ●  ← Shield K / D8 ─ FREEZE

  PINO 22 ●  ← Shield F / D7 ─ ZOOM +
  PINO 24 ●  ← Shield E / D6 ─ ZOOM -
```

## Funções

| Shield | Sinal | Orange Pi físico | Função |
|---|---|---:|---|
| A | D2 | 11 | mover cima |
| B | D3 | 13 | mover direita |
| C | D4 | 15 | mover baixo |
| D | D5 | 16 | mover esquerda |
| E | D6 | 24 | Zoom - |
| F | D7 | 22 | Zoom + |
| K | D8 | 18 | Freeze |

Alimentação:

```text
Shield VCC -> pino físico 1 (3.3V)
Shield GND -> pino físico 9 (GND)
```

O pino físico 7 não é utilizado nesta versão.

## Testar

```bash
sudo python3 tools/teste_botoes_gpio.py
```

Resultado esperado:

```text
A -> CIMA
B -> DIREITA
C -> BAIXO
D -> ESQUERDA
E -> ZOOM_MENOS
F -> ZOOM_MAIS
K -> FREEZE
```

## Executar

```bash
sudo python3 main.py
```
