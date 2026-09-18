from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from processamento.melhoria import (
    analisar_qualidade,
    clahe_colorido,
    unsharp,
)
from processamento.modos_leitura import (
    MODOS,
    aplicar_modo,
)
from processamento.zoom import aplicar_lupa


def criar_imagem():
    img = np.full(
        (720, 1280, 3),
        225,
        dtype=np.uint8,
    )

    cv2.putText(
        img,
        "LUPA DIGITAL - TESTE DE LEITURA",
        (90, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (35, 35, 35),
        3,
        cv2.LINE_AA,
    )

    linhas = [
        "Este texto simula uma folha vista pela camera.",
        "A versao 0.2.0 prioriza legibilidade.",
        "Zoom moderado, contraste e nitidez.",
        "Perfil desenvolvido para baixa visao.",
    ]

    y = 280

    for linha in linhas:
        cv2.putText(
            img,
            linha,
            (120, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (50, 50, 50),
            2,
            cv2.LINE_AA,
        )
        y += 80

    return img


def main():
    frame = criar_imagem()

    qualidade = analisar_qualidade(
        frame
    )

    assert qualidade["sharpness"] >= 0
    assert qualidade["brightness"] >= 0

    base = clahe_colorido(
        frame
    )

    zoom = aplicar_lupa(
        base,
        2.0,
        0.5,
        0.5,
        "maxima",
    )

    zoom = unsharp(
        zoom,
        0.6,
    )

    assert zoom.shape == frame.shape

    for modo in MODOS:
        out = aplicar_modo(
            zoom,
            modo,
        )

        assert out.shape == frame.shape

    print("[OK] Processamento validado.")
    print(
        "[INFO] Qualidade sintetica:",
        qualidade,
    )


if __name__ == "__main__":
    main()
