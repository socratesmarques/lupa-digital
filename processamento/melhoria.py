import cv2
import numpy as np


def auto_gamma(frame, target=0.50):
    """Corrige cenas escuras/claras sem alterações extremas."""
    if frame is None:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean = float(gray.mean()) / 255.0

    mean = min(0.95, max(0.08, mean))
    target = min(0.80, max(0.20, target))

    gamma = np.log(target) / np.log(mean)
    gamma = float(np.clip(gamma, 0.72, 1.42))

    inv = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** inv) * 255 for i in range(256)],
        dtype=np.uint8,
    )
    return cv2.LUT(frame, table)


def clahe_colorido(frame, clip_limit=2.0, tile_grid=(8, 8)):
    """Aumenta contraste local preservando as cores."""
    if frame is None:
        return None

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=float(clip_limit),
        tileGridSize=tuple(tile_grid),
    )

    l2 = clahe.apply(l)

    return cv2.cvtColor(
        cv2.merge((l2, a, b)),
        cv2.COLOR_LAB2BGR,
    )


def reduzir_ruido(frame, strength=3):
    """Redução leve de ruído preservando bordas de letras."""
    if frame is None or strength <= 0:
        return frame

    sigma = max(8, int(strength) * 8)

    return cv2.bilateralFilter(
        frame,
        d=5,
        sigmaColor=sigma,
        sigmaSpace=sigma,
    )


def unsharp(frame, strength=0.68):
    """Nitidez moderada para melhorar bordas de letras."""
    if frame is None:
        return None

    strength = max(0.0, float(strength))

    if strength == 0:
        return frame

    blur = cv2.GaussianBlur(frame, (0, 0), 1.05)

    sharpened = cv2.addWeighted(
        frame,
        1.0 + strength,
        blur,
        -strength,
        0,
    )

    return np.clip(sharpened, 0, 255).astype(np.uint8)


def strength_por_zoom(base_strength, zoom):
    if zoom <= 1.5:
        return base_strength
    if zoom <= 2.0:
        return base_strength * 0.88
    return base_strength * 0.72


def analisar_qualidade(
    frame,
    roi_scale=0.72,
    sharpness_low=55.0,
    sharpness_good=115.0,
    brightness_dark=65.0,
    brightness_bright=205.0,
):
    """
    Mede nitidez e luminosidade da área central.

    Não mede distância física. O objetivo é orientar o usuário a ajustar
    câmera e iluminação até obter uma captura melhor para leitura.
    """
    if frame is None:
        return {
            "sharpness": 0.0,
            "sharpness_status": "SEM IMAGEM",
            "brightness": 0.0,
            "brightness_status": "SEM IMAGEM",
            "hint": "Verifique a câmera.",
        }

    h, w = frame.shape[:2]
    scale = max(0.25, min(1.0, float(roi_scale)))

    rw = int(w * scale)
    rh = int(h * scale)
    x1 = (w - rw) // 2
    y1 = (h - rh) // 2

    roi = frame[y1:y1 + rh, x1:x1 + rw]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(gray.mean())

    if sharpness < sharpness_low:
        sharp_status = "BAIXA"
    elif sharpness < sharpness_good:
        sharp_status = "OK"
    else:
        sharp_status = "BOA"

    if brightness < brightness_dark:
        bright_status = "ESCURA"
    elif brightness > brightness_bright:
        bright_status = "MUITO CLARA"
    else:
        bright_status = "BOA"

    hints = []

    if sharp_status == "BAIXA":
        hints.append("aproxime/afaste a camera ate as letras ficarem nitidas")

    if bright_status == "ESCURA":
        hints.append("adicione luz difusa sobre o texto")
    elif bright_status == "MUITO CLARA":
        hints.append("reduza luz ou reflexo sobre a folha")

    if not hints:
        hints.append("posicionamento adequado para leitura")

    return {
        "sharpness": sharpness,
        "sharpness_status": sharp_status,
        "brightness": brightness,
        "brightness_status": bright_status,
        "hint": "; ".join(hints),
    }
