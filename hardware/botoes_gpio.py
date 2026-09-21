from time import monotonic

from hardware.controles import Acao
from hardware.pinos import (
    DEBOUNCE_MS,
    GPIO_ATIVO,
    PIN_SHIELD_A,
    PIN_SHIELD_B,
    PIN_SHIELD_C,
    PIN_SHIELD_D,
    PIN_SHIELD_E,
    PIN_SHIELD_F,
    PIN_SHIELD_K,
)


class BotoesGPIO:
    """
    Botões digitais do Joystick Shield V1.A.

    A -> cima
    B -> direita
    C -> baixo
    D -> esquerda
    E -> zoom -
    F -> zoom +
    K -> freeze

    O driver gera somente um evento por pressionamento.
    """

    def __init__(self):
        self.disponivel = False
        self.wiringpi = None
        self.GPIO = None
        self.erro = None

        self._pinos_acoes = {
            PIN_SHIELD_A: Acao.CIMA,
            PIN_SHIELD_B: Acao.DIREITA,
            PIN_SHIELD_C: Acao.BAIXO,
            PIN_SHIELD_D: Acao.ESQUERDA,
            PIN_SHIELD_E: Acao.ZOOM_MENOS,
            PIN_SHIELD_F: Acao.ZOOM_MAIS,
            PIN_SHIELD_K: Acao.FREEZE,
        }

        self._ultimo_estado = {}
        self._ultimo_evento = {}

    def iniciar(self):
        if not GPIO_ATIVO:
            self.erro = "GPIO desativado em hardware/pinos.py"
            return False

        try:
            import wiringpi
            from wiringpi import GPIO
        except Exception as exc:
            self.erro = f"wiringOP-Python indisponível: {exc}"
            return False

        self.wiringpi = wiringpi
        self.GPIO = GPIO

        try:
            resultado = wiringpi.wiringPiSetupPhys()

            if resultado not in (0, None):
                self.erro = f"wiringPiSetupPhys retornou {resultado}"
                return False

            for pin in self._pinos_acoes:
                wiringpi.pinMode(pin, GPIO.INPUT)

                try:
                    wiringpi.pullUpDnControl(pin, GPIO.PUD_UP)
                except Exception:
                    try:
                        wiringpi.pullUpDnControl(pin, 2)
                    except Exception:
                        pass

                self._ultimo_estado[pin] = int(
                    wiringpi.digitalRead(pin)
                )
                self._ultimo_evento[pin] = 0.0

            self.disponivel = True
            self.erro = None
            return True

        except Exception as exc:
            self.erro = f"Falha ao inicializar GPIO: {exc}"
            self.disponivel = False
            return False

    def ler(self):
        if not self.disponivel:
            return Acao.NENHUMA

        agora = monotonic()
        debounce_s = DEBOUNCE_MS / 1000.0

        for pin, acao in self._pinos_acoes.items():
            try:
                atual = int(self.wiringpi.digitalRead(pin))
            except Exception:
                continue

            anterior = self._ultimo_estado.get(pin, 1)

            if anterior == 1 and atual == 0:
                ultimo = self._ultimo_evento.get(pin, 0.0)

                if (agora - ultimo) >= debounce_s:
                    self._ultimo_evento[pin] = agora
                    self._ultimo_estado[pin] = atual
                    return acao

            self._ultimo_estado[pin] = atual

        return Acao.NENHUMA

    def encerrar(self):
        self.disponivel = False
