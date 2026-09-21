from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config.settings import (
    FRAME_TIMER_MS,
    GPIO_TIMER_MS,
    READING_GUIDE_HEIGHT,
    READING_GUIDE_Y,
    SHOW_READING_GUIDE,
    SHOW_STATUS_PANEL,
    START_FULLSCREEN,
    WINDOW_TITLE,
)
from core.lupa_engine import LupaEngine
from hardware.controles import Acao
from ui.styles import APP_STYLE
from ui.video_widget import VideoWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            WINDOW_TITLE
        )
        self.setStyleSheet(
            APP_STYLE
        )

        self.engine = LupaEngine()

        self.guia_ativa = SHOW_READING_GUIDE
        self.status_visivel = SHOW_STATUS_PANEL

        self._montar_interface()
        self._configurar_timers()

        if START_FULLSCREEN:
            self.showFullScreen()
        else:
            self.resize(1280, 800)

    # ------------------------------------------------------
    # Interface
    # ------------------------------------------------------
    def _montar_interface(self):
        raiz = QWidget()
        layout = QVBoxLayout(raiz)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(0)

        self.status_frame = self._criar_status()
        self.video = VideoWidget()
        self.controls_frame = self._criar_controles()

        self.video.configurar_guia(
            READING_GUIDE_Y,
            READING_GUIDE_HEIGHT,
        )
        self.video.set_guia(
            self.guia_ativa
        )

        layout.addWidget(
            self.status_frame
        )
        layout.addWidget(
            self.video,
            1,
        )
        layout.addWidget(
            self.controls_frame
        )

        self.status_frame.setVisible(
            self.status_visivel
        )

        self.setCentralWidget(
            raiz
        )

    def _criar_status(self):
        frame = QFrame()
        frame.setObjectName(
            "StatusBar"
        )

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            18,
            9,
            18,
            9,
        )

        self.zoom_label = QLabel(
            "1.50x"
        )
        self.zoom_label.setObjectName(
            "ZoomLabel"
        )

        self.mode_label = QLabel(
            "Cor melhorada"
        )
        self.mode_label.setObjectName(
            "ModeLabel"
        )

        self.quality_label = QLabel(
            "Nitidez: --  |  Luz: --"
        )
        self.quality_label.setObjectName(
            "QualityLabel"
        )

        self.hardware_label = QLabel(
            "GPIO: verificando..."
        )
        self.hardware_label.setObjectName(
            "HardwareLabel"
        )

        layout.addWidget(
            self.zoom_label
        )
        layout.addSpacing(20)
        layout.addWidget(
            self.mode_label
        )
        layout.addStretch(1)
        layout.addWidget(
            self.quality_label
        )
        layout.addSpacing(18)
        layout.addWidget(
            self.hardware_label
        )

        return frame

    def _criar_controles(self):
        frame = QFrame()
        frame.setObjectName(
            "Controls"
        )

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )
        layout.setSpacing(10)

        self.btn_zoom_menos = QPushButton(
            "−  ZOOM"
        )
        self.btn_zoom_mais = QPushButton(
            "ZOOM  +"
        )
        self.btn_freeze = QPushButton(
            "CONGELAR"
        )
        self.btn_freeze.setObjectName(
            "FreezeButton"
        )

        self.btn_modo = QPushButton(
            "MODO"
        )

        self.btn_guia = QPushButton(
            "GUIA"
        )
        self.btn_guia.setObjectName(
            "GuideButton"
        )

        self.btn_captura = QPushButton(
            "CAPTURAR"
        )

        self.btn_zoom_menos.clicked.connect(
            lambda: self.executar_acao(
                Acao.ZOOM_MENOS
            )
        )
        self.btn_zoom_mais.clicked.connect(
            lambda: self.executar_acao(
                Acao.ZOOM_MAIS
            )
        )
        self.btn_freeze.clicked.connect(
            lambda: self.executar_acao(
                Acao.FREEZE
            )
        )
        self.btn_modo.clicked.connect(
            lambda: self.executar_acao(
                Acao.PROXIMO_MODO
            )
        )
        self.btn_guia.clicked.connect(
            lambda: self.executar_acao(
                Acao.GUIA_LEITURA
            )
        )
        self.btn_captura.clicked.connect(
            lambda: self.executar_acao(
                Acao.CAPTURAR
            )
        )

        for botao in (
            self.btn_zoom_menos,
            self.btn_zoom_mais,
            self.btn_freeze,
            self.btn_modo,
            self.btn_guia,
            self.btn_captura,
        ):
            layout.addWidget(
                botao,
                1,
            )

        return frame

    # ------------------------------------------------------
    # Timers
    # ------------------------------------------------------
    def _configurar_timers(self):
        self.frame_timer = QTimer(
            self
        )
        self.frame_timer.timeout.connect(
            self.atualizar_frame
        )
        self.frame_timer.start(
            FRAME_TIMER_MS
        )

        self.gpio_timer = QTimer(
            self
        )
        self.gpio_timer.timeout.connect(
            self.ler_gpio
        )
        self.gpio_timer.start(
            GPIO_TIMER_MS
        )

    # ------------------------------------------------------
    # Câmera / GPIO
    # ------------------------------------------------------
    def atualizar_frame(self):
        try:
            estado = (
                self.engine.processar_proximo_frame()
            )
        except RuntimeError as exc:
            self.frame_timer.stop()
            QMessageBox.critical(
                self,
                "Erro de câmera",
                str(exc),
            )
            return

        self.video.set_frame(
            estado.frame
        )

        self.zoom_label.setText(
            f"{estado.zoom:.2f}x"
        )

        self.mode_label.setText(
            estado.modo_nome
        )

        if estado.qualidade:
            self.quality_label.setText(
                "Nitidez: "
                f"{estado.qualidade['sharpness_status']} "
                " | Luz: "
                f"{estado.qualidade['brightness_status']} "
                f" | FPS: {estado.fps:.0f}"
            )
        else:
            self.quality_label.setText(
                f"FPS: {estado.fps:.0f}"
            )

        if self.engine.gpio_disponivel:
            self.hardware_label.setText(
                "Joystick: conectado"
            )
        else:
            self.hardware_label.setText(
                "Joystick: teclado/fallback"
            )

        self._atualizar_estado_botoes()

    def ler_gpio(self):
        acao = self.engine.ler_gpio()

        if acao != Acao.NENHUMA:
            self.executar_acao(
                acao
            )

    # ------------------------------------------------------
    # Ações
    # ------------------------------------------------------
    def executar_acao(self, acao):
        if acao == Acao.GUIA_LEITURA:
            self.guia_ativa = not self.guia_ativa
            self.video.set_guia(
                self.guia_ativa
            )
            self._atualizar_estado_botoes()
            return

        if acao == Acao.STATUS:
            self.status_visivel = not self.status_visivel
            self.status_frame.setVisible(
                self.status_visivel
            )
            return

        if acao == Acao.FULLSCREEN:
            self.alternar_fullscreen()
            return

        if acao == Acao.SAIR:
            self.close()
            return

        resultado = self.engine.executar(
            acao
        )

        if acao == Acao.CAPTURAR:
            if resultado:
                self.statusBar().showMessage(
                    f"Captura salva em {resultado}",
                    4000,
                )
            else:
                self.statusBar().showMessage(
                    "Não foi possível salvar a captura.",
                    4000,
                )

        self._atualizar_estado_botoes()

    def _atualizar_estado_botoes(self):
        congelado = self.engine.congelado

        self.btn_freeze.setText(
            "AO VIVO"
            if congelado
            else "CONGELAR"
        )
        self.btn_freeze.setProperty(
            "active",
            congelado,
        )
        self.btn_freeze.style().unpolish(
            self.btn_freeze
        )
        self.btn_freeze.style().polish(
            self.btn_freeze
        )

        self.btn_guia.setProperty(
            "active",
            self.guia_ativa,
        )
        self.btn_guia.style().unpolish(
            self.btn_guia
        )
        self.btn_guia.style().polish(
            self.btn_guia
        )

    def alternar_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # ------------------------------------------------------
    # Teclado de desenvolvimento / fallback
    # ------------------------------------------------------
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        mapa = {
            Qt.Key_Plus: Acao.ZOOM_MAIS,
            Qt.Key_Equal: Acao.ZOOM_MAIS,
            Qt.Key_Minus: Acao.ZOOM_MENOS,

            Qt.Key_W: Acao.CIMA,
            Qt.Key_Up: Acao.CIMA,

            Qt.Key_D: Acao.DIREITA,
            Qt.Key_Right: Acao.DIREITA,

            Qt.Key_X: Acao.BAIXO,
            Qt.Key_Down: Acao.BAIXO,

            Qt.Key_A: Acao.ESQUERDA,
            Qt.Key_Left: Acao.ESQUERDA,

            Qt.Key_C: Acao.CENTRALIZAR,

            Qt.Key_Space: Acao.FREEZE,
            Qt.Key_F: Acao.PROXIMO_MODO,
            Qt.Key_R: Acao.GUIA_LEITURA,
            Qt.Key_H: Acao.STATUS,
            Qt.Key_M: Acao.FULLSCREEN,
            Qt.Key_F11: Acao.FULLSCREEN,
            Qt.Key_S: Acao.CAPTURAR,
            Qt.Key_Q: Acao.SAIR,
            Qt.Key_Escape: Acao.SAIR,
        }

        acao = mapa.get(
            key
        )

        if acao is not None:
            self.executar_acao(
                acao
            )
            event.accept()
            return

        super().keyPressEvent(
            event
        )

    def closeEvent(self, event):
        self.frame_timer.stop()
        self.gpio_timer.stop()

        self.engine.encerrar()

        event.accept()
