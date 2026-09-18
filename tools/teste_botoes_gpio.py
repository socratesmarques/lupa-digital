from pathlib import Path
import sys
from time import sleep

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hardware.botoes_gpio import BotoesGPIO
from hardware.controles import Acao


def main():
    botoes = BotoesGPIO()

    if not botoes.iniciar():
        print("GPIO não inicializado.")
        return

    print("A=CIMA  B=DIREITA  C=BAIXO  D=ESQUERDA")
    print("E=ZOOM- F=ZOOM+ K=FREEZE")
    print("Ctrl+C encerra.")

    try:
        while True:
            acao = botoes.ler()
            if acao != Acao.NENHUMA:
                print("AÇÃO:", acao.name)
            sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        botoes.encerrar()


if __name__ == "__main__":
    main()
