import cv2
import numpy as np


class Display:
    def __init__(self, titulo, fullscreen=False):
        self.titulo = titulo
        self.fullscreen = fullscreen

        cv2.namedWindow(self.titulo, cv2.WINDOW_NORMAL)
        self._aplicar_fullscreen()

    def _aplicar_fullscreen(self):
        modo = (
            cv2.WINDOW_FULLSCREEN
            if self.fullscreen
            else cv2.WINDOW_NORMAL
        )

        cv2.setWindowProperty(
            self.titulo,
            cv2.WND_PROP_FULLSCREEN,
            modo,
        )

    def alternar_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._aplicar_fullscreen()

    def mostrar(self, frame):
        cv2.imshow(self.titulo, frame)

    def tecla(self):
        return cv2.waitKey(1) & 0xFF

    def fechar(self):
        cv2.destroyAllWindows()


def _texto_com_fundo(
    img,
    texto,
    pos,
    escala=0.64,
    espessura=2,
    padding=7,
):
    fonte = cv2.FONT_HERSHEY_SIMPLEX

    (tw, th), baseline = cv2.getTextSize(
        texto,
        fonte,
        escala,
        espessura,
    )

    x, y = pos
    x2 = min(img.shape[1] - 1, x + tw + padding * 2)
    y1 = max(0, y - th - padding)
    y2 = min(img.shape[0] - 1, y + baseline + padding)

    overlay = img.copy()

    cv2.rectangle(
        overlay,
        (x, y1),
        (x2, y2),
        (0, 0, 0),
        -1,
    )

    cv2.addWeighted(
        overlay,
        0.67,
        img,
        0.33,
        0,
        img,
    )

    cv2.putText(
        img,
        texto,
        (x + padding, y),
        fonte,
        escala,
        (255, 255, 255),
        espessura,
        cv2.LINE_AA,
    )


def guia_leitura(
    frame,
    y_norm=0.53,
    altura=84,
    marcadores=True,
):
    if frame is None:
        return None

    out = frame.copy()
    h, w = out.shape[:2]

    cy = int(h * max(0.0, min(1.0, y_norm)))
    half = max(20, int(altura // 2))

    y1 = max(0, cy - half)
    y2 = min(h, cy + half)

    overlay = out.copy()
    overlay[:y1, :] = 0
    overlay[y2:, :] = 0

    out = cv2.addWeighted(
        out,
        0.35,
        overlay,
        0.65,
        0,
    )

    cv2.line(
        out,
        (0, y1),
        (w, y1),
        (255, 255, 255),
        1,
    )

    cv2.line(
        out,
        (0, y2),
        (w, y2),
        (255, 255, 255),
        1,
    )

    if marcadores:
        mid = (y1 + y2) // 2
        tamanho = 22

        pts_left = np.array(
            [
                [8, mid],
                [8 + tamanho, mid - tamanho // 2],
                [8 + tamanho, mid + tamanho // 2],
            ],
            dtype=np.int32,
        )

        pts_right = np.array(
            [
                [w - 9, mid],
                [w - 9 - tamanho, mid - tamanho // 2],
                [w - 9 - tamanho, mid + tamanho // 2],
            ],
            dtype=np.int32,
        )

        cv2.fillPoly(out, [pts_left], (255, 255, 255))
        cv2.fillPoly(out, [pts_right], (255, 255, 255))

    return out


def hud(
    frame,
    zoom,
    modo_nome,
    congelado,
    fps,
    camera_info,
    qualidade=None,
):
    if frame is None:
        return None

    out = frame.copy()

    linhas = [
        f"Zoom {zoom:.2f}x",
        f"Modo: {modo_nome}",
        f"Freeze: {'SIM' if congelado else 'NAO'}",
        f"FPS: {fps:.1f}",
    ]

    if qualidade:
        linhas.extend(
            [
                (
                    f"Nitidez: {qualidade['sharpness_status']} "
                    f"({qualidade['sharpness']:.0f})"
                ),
                (
                    f"Luz: {qualidade['brightness_status']} "
                    f"({qualidade['brightness']:.0f})"
                ),
            ]
        )

    y = 34

    for linha in linhas:
        _texto_com_fundo(
            out,
            linha,
            (14, y),
        )
        y += 34

    if qualidade:
        dica = qualidade.get("hint", "")

        if dica:
            _texto_com_fundo(
                out,
                f"DICA: {dica}",
                (14, out.shape[0] - 20),
                escala=0.56,
                espessura=2,
            )

    return out
