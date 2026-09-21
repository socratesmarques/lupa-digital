"""
Orange Pi 3 LTS + Joystick Shield V1.A
Lupa Digital V0.5.0

MONTAGEM EXISTENTE PRESERVADA:

Shield VCC -> físico 1  (3.3 V)
Shield GND -> físico 9  (GND)

A / D2 -> físico 11 -> CIMA
B / D3 -> físico 13 -> DIREITA
C / D4 -> físico 15 -> BAIXO
D / D5 -> físico 16 -> ESQUERDA

E / D6 -> físico 24 -> ZOOM -
F / D7 -> físico 22 -> ZOOM +

K / D8 -> físico 18 -> FREEZE
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
