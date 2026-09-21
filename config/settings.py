from pathlib import Path

APP_NAME = "Lupa Digital"
VERSION = "0.5.0"
WINDOW_TITLE = f"{APP_NAME} V{VERSION} - Orange Pi 3 LTS"

# ==========================================================
# CÂMERA - Creative Labs VF0780
# ==========================================================
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
CAMERA_BUFFER_SIZE = 1
PREFER_MJPG = True

# ==========================================================
# ZOOM PARA BAIXA VISÃO
# ==========================================================
ZOOM_LEVELS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
DEFAULT_ZOOM_INDEX = 2
PAN_STEP = 0.065
UPSCALE_QUALITY = "maxima"

# ==========================================================
# PROCESSAMENTO
# ==========================================================
ENABLE_AUTO_GAMMA = True
AUTO_GAMMA_TARGET = 0.50

ENABLE_CLAHE = True
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_GRID = (8, 8)

ENABLE_DENOISE = True
DENOISE_STRENGTH = 3

ENABLE_SHARPEN = True
SHARPEN_BASE_STRENGTH = 0.68

ENABLE_QUALITY_ASSIST = True
SHARPNESS_LOW = 55.0
SHARPNESS_GOOD = 115.0
BRIGHTNESS_DARK = 65.0
BRIGHTNESS_BRIGHT = 205.0
QUALITY_ROI_SCALE = 0.72

DEFAULT_READING_MODE_INDEX = 0

# ==========================================================
# PYSIDE6 / QT
# ==========================================================
START_FULLSCREEN = True
SHOW_STATUS_PANEL = True
SHOW_READING_GUIDE = False

# Frequência da interface.
FRAME_TIMER_MS = 33
GPIO_TIMER_MS = 15

# Guia de leitura.
READING_GUIDE_Y = 0.53
READING_GUIDE_HEIGHT = 86

# Interface de baixa visão.
UI_FONT_SIZE = 18
UI_BUTTON_FONT_SIZE = 20
UI_STATUS_HEIGHT = 68
UI_CONTROLS_HEIGHT = 86

SCREENSHOT_DIR = Path("capturas")
