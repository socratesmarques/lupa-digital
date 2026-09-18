# Lupa Digital V0.2.0 — Perfil Baixa Visão

Protótipo desenvolvido para usar a **Creative Labs VF0780 / Creative Senz3D**
como câmera RGB de uma lupa eletrônica.

A V0.2.0 deixa de priorizar zoom digital muito alto e passa a priorizar
**qualidade de captura e legibilidade**.

## Método adotado

```text
Boa iluminação
      +
Câmera próxima ao texto
      +
Texto ocupando grande parte do quadro 720p
      ↓
Captura nativa 1280x720
      ↓
Redução leve de ruído
      ↓
Correção de iluminação
      ↓
Contraste local
      ↓
Zoom moderado: 1.0x a 2.5x
      ↓
Nitidez
      ↓
Modo visual para baixa visão
      ↓
Tela LCD
```

## Por que fazer assim?

Se a câmera estiver muito longe, as letras ocupam poucos pixels.
Nenhum filtro consegue recuperar detalhes que nunca chegaram ao sensor.

Por isso, a V0.2.0 ajuda o usuário a melhorar a imagem **antes do zoom**.

## Assistente de posicionamento

O HUD mostra:

```text
Nitidez: BAIXA / OK / BOA
Luz: ESCURA / BOA / MUITO CLARA
```

Também mostra orientações como:

```text
DICA: aproxime/afaste a camera ate as letras ficarem nitidas
```

ou:

```text
DICA: adicione luz difusa sobre o texto
```

Esse recurso não mede distância em centímetros.
Ele mede diretamente a nitidez e a iluminação da imagem capturada.

## Zoom

Faixa principal:

```text
1.00x
1.25x
1.50x
1.75x
2.00x
2.25x
2.50x
```

O sistema inicia em **1.5x**.

## Modos para baixa visão

A tecla `F` alterna entre:

- Cor melhorada
- Escala de cinza
- Alto contraste
- Preto no branco
- Branco no preto
- Amarelo no preto

## Guia de leitura

Pressione `R`.

A tela destaca apenas uma faixa horizontal para ajudar a acompanhar uma linha.

```text
████████████████████████████

>   linha que estou lendo   <

████████████████████████████
```

## Controles

| Tecla | Ação |
|---|---|
| `+` / `=` | Zoom + |
| `-` | Zoom - |
| `W` | mover para cima |
| `A` | mover para esquerda |
| `D` | mover para direita |
| `X` | mover para baixo |
| `C` | centralizar |
| `F` | trocar modo visual |
| `Espaço` | freeze |
| `R` | guia de leitura |
| `H` | HUD |
| `M` | tela cheia |
| `S` | captura |
| `Q` / `Esc` | sair |

## Montagem física recomendada

```text
                CÂMERA
                  │
                  ▼
          ┌─────────────┐
       LED               LED
        \                 /
         \               /
          ▼             ▼

       ┌────────────────────┐
       │                    │
       │       TEXTO        │
       │                    │
       └────────────────────┘
```

Use luz difusa pelos lados para evitar reflexos na folha.

Aproxime a câmera até as letras ocuparem uma parte grande da imagem,
mas pare no ponto em que o indicador de nitidez estiver melhor.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Diagnóstico da câmera

```bash
sudo apt install v4l-utils
python3 tools/diagnostico_camera.py
```

## Testar processamento sem webcam

```bash
python3 tools/teste_processamento.py
```

## Próxima etapa

Depois de identificar o modelo exato do Orange Pi, os controles podem virar:

```text
BOTÃO 1 -> ZOOM +
BOTÃO 2 -> ZOOM -
BOTÃO 3 -> MODO
BOTÃO 4 -> FREEZE
BOTÃO 5 -> GUIA DE LEITURA
```

**Versão: 0.2.0**

Objetivo principal: tornar a VF0780 mais útil como lupa eletrônica para
pessoas com baixa visão.
