from dataclasses import dataclass
from datetime import datetime
from time import perf_counter

import cv2

from camera.camera import CameraVF0780
from config.settings import (
    AUTO_GAMMA_TARGET,
    BRIGHTNESS_BRIGHT,
    BRIGHTNESS_DARK,
    CAMERA_BUFFER_SIZE,
    CAMERA_FPS,
    CAMERA_HEIGHT,
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CLAHE_CLIP_LIMIT,
    CLAHE_TILE_GRID,
    DEFAULT_READING_MODE_INDEX,
    DEFAULT_ZOOM_INDEX,
    DENOISE_STRENGTH,
    ENABLE_AUTO_GAMMA,
    ENABLE_CLAHE,
    ENABLE_DENOISE,
    ENABLE_QUALITY_ASSIST,
    ENABLE_SHARPEN,
    PAN_STEP,
    PREFER_MJPG,
    QUALITY_ROI_SCALE,
    SCREENSHOT_DIR,
    SHARPNESS_GOOD,
    SHARPNESS_LOW,
    SHARPEN_BASE_STRENGTH,
    UPSCALE_QUALITY,
    ZOOM_LEVELS,
)
from hardware.botoes_gpio import BotoesGPIO
from hardware.controles import Acao
from processamento.melhoria import (
    analisar_qualidade,
    auto_gamma,
    clahe_colorido,
    reduzir_ruido,
    strength_por_zoom,
    unsharp,
)
from processamento.modos_leitura import MODOS, NOMES, aplicar_modo
from processamento.zoom import aplicar_lupa


@dataclass
class EstadoFrame:
    frame: object
    zoom: float
    modo_nome: str
    congelado: bool
    fps: float
    qualidade: dict
    camera_info: dict


class LupaEngine:
    """
    Núcleo da aplicação.

    Não conhece PySide6.
    Isso permite manter captura, processamento e GPIO separados da interface.
    """

    def __init__(self):
        self.camera = CameraVF0780(
            index=CAMERA_INDEX,
            width=CAMERA_WIDTH,
            height=CAMERA_HEIGHT,
            fps=CAMERA_FPS,
            buffer_size=CAMERA_BUFFER_SIZE,
            prefer_mjpg=PREFER_MJPG,
        )

        if not self.camera.is_opened():
            raise RuntimeError(
                f"Não foi possível abrir a câmera no índice {CAMERA_INDEX}."
            )

        self.camera_info = self.camera.info()

        self.botoes = BotoesGPIO()
        self.botoes.iniciar()

        self.zoom_i = min(
            DEFAULT_ZOOM_INDEX,
            len(ZOOM_LEVELS) - 1,
        )

        self.modo_i = min(
            DEFAULT_READING_MODE_INDEX,
            len(MODOS) - 1,
        )

        self.centro_x = 0.5
        self.centro_y = 0.5

        self.congelado = False
        self.frame_congelado = None

        self.ultimo_frame_bruto = None
        self.ultimo_frame_processado = None

        self.qualidade = None

        self._fps_frames = 0
        self._fps = 0.0
        self._fps_inicio = perf_counter()

    @property
    def gpio_disponivel(self):
        return self.botoes.disponivel

    @property
    def gpio_erro(self):
        return self.botoes.erro

    @property
    def zoom(self):
        return ZOOM_LEVELS[self.zoom_i]

    @property
    def modo(self):
        return MODOS[self.modo_i]

    @property
    def modo_nome(self):
        return NOMES[self.modo]

    def ler_gpio(self):
        return self.botoes.ler()

    def executar(self, acao: Acao):
        if acao == Acao.ZOOM_MAIS:
            self.zoom_i = min(
                self.zoom_i + 1,
                len(ZOOM_LEVELS) - 1,
            )

        elif acao == Acao.ZOOM_MENOS:
            self.zoom_i = max(
                self.zoom_i - 1,
                0,
            )

        elif acao == Acao.ESQUERDA:
            self.centro_x = max(
                0.0,
                self.centro_x - PAN_STEP,
            )

        elif acao == Acao.DIREITA:
            self.centro_x = min(
                1.0,
                self.centro_x + PAN_STEP,
            )

        elif acao == Acao.CIMA:
            self.centro_y = max(
                0.0,
                self.centro_y - PAN_STEP,
            )

        elif acao == Acao.BAIXO:
            self.centro_y = min(
                1.0,
                self.centro_y + PAN_STEP,
            )

        elif acao == Acao.CENTRALIZAR:
            self.centro_x = 0.5
            self.centro_y = 0.5

        elif acao == Acao.FREEZE:
            self._alternar_freeze()

        elif acao == Acao.PROXIMO_MODO:
            self.modo_i = (
                self.modo_i + 1
            ) % len(MODOS)

        elif acao == Acao.CAPTURAR:
            return self.salvar_captura()

        return None

    def _alternar_freeze(self):
        if self.congelado:
            self.congelado = False
            self.frame_congelado = None
            return

        if self.ultimo_frame_bruto is not None:
            self.frame_congelado = self.ultimo_frame_bruto.copy()
            self.congelado = True

    def _obter_frame_bruto(self):
        if self.congelado and self.frame_congelado is not None:
            return self.frame_congelado

        ok, frame = self.camera.read()

        if not ok or frame is None:
            raise RuntimeError("A câmera parou de fornecer imagem.")

        self.ultimo_frame_bruto = frame.copy()
        return frame

    def _atualizar_fps(self):
        self._fps_frames += 1
        agora = perf_counter()
        delta = agora - self._fps_inicio

        if delta >= 1.0:
            self._fps = self._fps_frames / delta
            self._fps_frames = 0
            self._fps_inicio = agora

    def processar_proximo_frame(self):
        frame = self._obter_frame_bruto()

        if ENABLE_QUALITY_ASSIST:
            self.qualidade = analisar_qualidade(
                frame,
                roi_scale=QUALITY_ROI_SCALE,
                sharpness_low=SHARPNESS_LOW,
                sharpness_good=SHARPNESS_GOOD,
                brightness_dark=BRIGHTNESS_DARK,
                brightness_bright=BRIGHTNESS_BRIGHT,
            )

        processado = frame.copy()

        if ENABLE_DENOISE:
            processado = reduzir_ruido(
                processado,
                DENOISE_STRENGTH,
            )

        if ENABLE_AUTO_GAMMA:
            processado = auto_gamma(
                processado,
                AUTO_GAMMA_TARGET,
            )

        if ENABLE_CLAHE and self.modo == "cor_melhorada":
            processado = clahe_colorido(
                processado,
                CLAHE_CLIP_LIMIT,
                CLAHE_TILE_GRID,
            )

        processado = aplicar_lupa(
            processado,
            self.zoom,
            self.centro_x,
            self.centro_y,
            UPSCALE_QUALITY,
        )

        if ENABLE_SHARPEN:
            intensidade = strength_por_zoom(
                SHARPEN_BASE_STRENGTH,
                self.zoom,
            )
            processado = unsharp(
                processado,
                intensidade,
            )

        processado = aplicar_modo(
            processado,
            self.modo,
        )

        self.ultimo_frame_processado = processado.copy()
        self._atualizar_fps()

        return EstadoFrame(
            frame=processado,
            zoom=self.zoom,
            modo_nome=self.modo_nome,
            congelado=self.congelado,
            fps=self._fps,
            qualidade=self.qualidade,
            camera_info=self.camera_info,
        )

    def salvar_captura(self):
        if self.ultimo_frame_processado is None:
            return None

        SCREENSHOT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        nome = datetime.now().strftime(
            "captura_%Y-%m-%d_%H-%M-%S.png"
        )
        caminho = SCREENSHOT_DIR / nome

        if cv2.imwrite(
            str(caminho),
            self.ultimo_frame_processado,
        ):
            return caminho

        return None

    def encerrar(self):
        self.botoes.encerrar()
        self.camera.release()
