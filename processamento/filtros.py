import cv2
import numpy as np


FILTROS = [
    "normal",
    "preto_e_branco",
    "alto_contraste",
    "negativo",
    "texto_preto_branco",
]

NOMES_FILTROS = {
    "normal": "Normal",
    "preto_e_branco": "Preto e Branco",
    "alto_contraste": "Alto Contraste",
    "negativo": "Negativo",
    "texto_preto_branco": "Leitura P&B",
}


def aplicar_filtro(frame, filtro: str):
    if frame is None:
        return None

    if filtro == "preto_e_branco":
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(cinza, cv2.COLOR_GRAY2BGR)

    if filtro == "alto_contraste":
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        saida = cv2.merge((l, a, b))
        return cv2.cvtColor(saida, cv2.COLOR_LAB2BGR)

    if filtro == "negativo":
        return cv2.bitwise_not(frame)

    if filtro == "texto_preto_branco":
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        suavizada = cv2.GaussianBlur(cinza, (3, 3), 0)
        binaria = cv2.adaptiveThreshold(
            suavizada,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            9,
        )
        return cv2.cvtColor(binaria, cv2.COLOR_GRAY2BGR)

    return frame.copy()
