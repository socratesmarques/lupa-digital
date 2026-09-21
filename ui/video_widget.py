import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QImage,
    QPainter,
    QPen,
    QPixmap,
    QPolygon,
)
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget


class VideoWidget(QWidget):
    """
    Exibe frames OpenCV usando QPainter.

    A imagem é preservada com KeepAspectRatio.
    O guia de leitura é desenhado pelo Qt, não pelo OpenCV.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._pixmap = None
        self._guia_ativa = False
        self._guia_y = 0.53
        self._guia_altura = 86

        self.setMinimumSize(640, 360)
        self.setStyleSheet("background-color: #000000;")

    def set_frame(self, frame_bgr):
        rgb = cv2.cvtColor(
            frame_bgr,
            cv2.COLOR_BGR2RGB,
        )

        h, w, canais = rgb.shape
        bytes_por_linha = canais * w

        imagem = QImage(
            rgb.data,
            w,
            h,
            bytes_por_linha,
            QImage.Format_RGB888,
        ).copy()

        self._pixmap = QPixmap.fromImage(imagem)
        self.update()

    def set_guia(self, ativa: bool):
        self._guia_ativa = bool(ativa)
        self.update()

    def configurar_guia(self, y_norm: float, altura: int):
        self._guia_y = max(
            0.0,
            min(1.0, float(y_norm)),
        )
        self._guia_altura = max(
            30,
            int(altura),
        )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(
            self.rect(),
            QColor("#000000"),
        )

        if self._pixmap is None:
            painter.setPen(QColor("#ffffff"))
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "Aguardando câmera...",
            )
            return

        scaled = self._pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        painter.drawPixmap(
            x,
            y,
            scaled,
        )

        if self._guia_ativa:
            self._desenhar_guia(
                painter,
                x,
                y,
                scaled.width(),
                scaled.height(),
            )

    def _desenhar_guia(
        self,
        painter,
        x,
        y,
        largura,
        altura,
    ):
        centro = y + int(
            altura * self._guia_y
        )

        meia = min(
            self._guia_altura // 2,
            max(20, altura // 3),
        )

        y1 = max(
            y,
            centro - meia,
        )
        y2 = min(
            y + altura,
            centro + meia,
        )

        escuro = QColor(
            0,
            0,
            0,
            170,
        )

        painter.fillRect(
            x,
            y,
            largura,
            max(0, y1 - y),
            escuro,
        )

        painter.fillRect(
            x,
            y2,
            largura,
            max(0, y + altura - y2),
            escuro,
        )

        painter.setPen(
            QPen(
                QColor("#ffffff"),
                2,
            )
        )

        painter.drawLine(
            x,
            y1,
            x + largura,
            y1,
        )
        painter.drawLine(
            x,
            y2,
            x + largura,
            y2,
        )

        meio = (y1 + y2) // 2
        tamanho = 20

        left = QPolygon(
            [
                QPoint(x + 8, meio),
                QPoint(x + 8 + tamanho, meio - 10),
                QPoint(x + 8 + tamanho, meio + 10),
            ]
        )

        right = QPolygon(
            [
                QPoint(x + largura - 8, meio),
                QPoint(x + largura - 8 - tamanho, meio - 10),
                QPoint(x + largura - 8 - tamanho, meio + 10),
            ]
        )

        painter.setBrush(
            QColor("#ffffff")
        )
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(left)
        painter.drawPolygon(right)
