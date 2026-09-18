"""
Lupa Digital V0.4.3
Orange Pi 3 LTS + Joystick Shield V1.A

MONTAGEM FINAL:

1  -> 3.3V -> Shield VCC
9  -> GND  -> Shield GND

11 -> Shield A / D2 -> CIMA
13 -> Shield B / D3 -> DIREITA
15 -> Shield C / D4 -> BAIXO
16 -> Shield D / D5 -> ESQUERDA
18 -> Shield K / D8 -> FREEZE

24 -> Shield E / D6 -> ZOOM -
22 -> Shield F / D7 -> ZOOM +

Pino 7 não é mais utilizado.
"""

PIN_SHIELD_A = 11
PIN_SHIELD_B = 13
PIN_SHIELD_C = 15
PIN_SHIELD_D = 16

PIN_SHIELD_E = 24
PIN_SHIELD_F = 22

PIN_SHIELD_K = 18

PIN_3V3 = 1
PIN_GND = 9

DEBOUNCE_MS = 90
GPIO_ATIVO = True
