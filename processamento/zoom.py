import cv2


def _interpolacao(modo: str):
    if modo == "maxima":
        return cv2.INTER_LANCZOS4
    if modo == "rapida":
        return cv2.INTER_LINEAR
    return cv2.INTER_CUBIC


def aplicar_lupa(
    frame,
    zoom: float,
    centro_x: float = 0.5,
    centro_y: float = 0.5,
    qualidade: str = "maxima",
):
    """
    Zoom digital voltado para leitura.

    A qualidade final depende principalmente de a câmera estar próxima,
    bem posicionada e com boa iluminação. O zoom é mantido moderado para
    preservar o máximo possível dos detalhes capturados em 720p.
    """
    if frame is None:
        return None

    zoom = max(1.0, float(zoom))

    if zoom <= 1.0:
        return frame.copy()

    h, w = frame.shape[:2]

    roi_w = max(4, int(round(w / zoom)))
    roi_h = max(4, int(round(h / zoom)))

    centro_x = max(0.0, min(1.0, float(centro_x)))
    centro_y = max(0.0, min(1.0, float(centro_y)))

    max_x = max(0, w - roi_w)
    max_y = max(0, h - roi_h)

    x1 = int(round(max_x * centro_x))
    y1 = int(round(max_y * centro_y))

    x1 = max(0, min(x1, w - roi_w))
    y1 = max(0, min(y1, h - roi_h))

    roi = frame[y1:y1 + roi_h, x1:x1 + roi_w]

    return cv2.resize(
        roi,
        (w, h),
        interpolation=_interpolacao(qualidade),
    )
