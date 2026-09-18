from datetime import datetime
from time import perf_counter

import cv2

from camera.camera import CameraVF0780
from config.settings import *
from hardware.controles import Acao, tecla_para_acao
from interface.display import Display, guia_leitura, hud
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


def salvar_captura(frame):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    nome = datetime.now().strftime(
        "captura_%Y-%m-%d_%H-%M-%S.png"
    )

    caminho = SCREENSHOT_DIR / nome

    if cv2.imwrite(str(caminho), frame):
        print(f"[OK] Captura salva: {caminho}")
    else:
        print("[ERRO] Falha ao salvar captura.")


def main():
    camera = CameraVF0780(
        index=CAMERA_INDEX,
        width=CAMERA_WIDTH,
        height=CAMERA_HEIGHT,
        fps=CAMERA_FPS,
        buffer_size=CAMERA_BUFFER_SIZE,
        prefer_mjpg=PREFER_MJPG,
    )

    if not camera.is_opened():
        print(
            f"[ERRO] Nao consegui abrir a camera "
            f"no indice {CAMERA_INDEX}."
        )
        print(
            "Execute: python3 tools/diagnostico_camera.py"
        )
        return

    camera_info = camera.info()
    print("[CAMERA]", camera_info)

    display = Display(
        WINDOW_TITLE,
        START_FULLSCREEN,
    )

    zoom_i = min(
        DEFAULT_ZOOM_INDEX,
        len(ZOOM_LEVELS) - 1,
    )

    modo_i = min(
        DEFAULT_READING_MODE_INDEX,
        len(MODOS) - 1,
    )

    centro_x = 0.5
    centro_y = 0.5

    congelado = False
    frame_congelado = None

    mostrar_hud = SHOW_HUD
    mostrar_guia = SHOW_READING_GUIDE

    frames = 0
    fps = 0.0
    timer = perf_counter()

    ultimo_processado = None
    qualidade = None

    print("[LUPA DIGITAL - PERFIL BAIXA VISAO]")
    print(
        "Aproxime a camera do texto ate as letras "
        "ocuparem boa parte da imagem."
    )
    print(
        "Use iluminacao difusa e evite reflexos."
    )
    print("")
    print("[CONTROLES]")
    print("+ / - : zoom")
    print("W A D X : mover area | C : centralizar")
    print("F : modo de leitura | ESPACO : freeze")
    print("R : guia | H : informacoes")
    print("M : tela cheia | S : captura | Q : sair")

    try:
        while True:
            if congelado:
                frame = frame_congelado
            else:
                ok, frame = camera.read()

                if not ok or frame is None:
                    print(
                        "[ERRO] Perda do stream da camera."
                    )
                    break

            # Analisa a captura original para ajudar no
            # posicionamento físico da câmera e da iluminação.
            if ENABLE_QUALITY_ASSIST:
                qualidade = analisar_qualidade(
                    frame,
                    roi_scale=QUALITY_ROI_SCALE,
                    sharpness_low=SHARPNESS_LOW,
                    sharpness_good=SHARPNESS_GOOD,
                    brightness_dark=BRIGHTNESS_DARK,
                    brightness_bright=BRIGHTNESS_BRIGHT,
                )

            zoom = ZOOM_LEVELS[zoom_i]
            modo = MODOS[modo_i]

            processado = frame.copy()

            # 1. Redução leve de ruído.
            if ENABLE_DENOISE:
                processado = reduzir_ruido(
                    processado,
                    DENOISE_STRENGTH,
                )

            # 2. Correção de iluminação.
            if ENABLE_AUTO_GAMMA:
                processado = auto_gamma(
                    processado,
                    AUTO_GAMMA_TARGET,
                )

            # 3. Contraste local antes do zoom no modo colorido.
            if ENABLE_CLAHE and modo == "cor_melhorada":
                processado = clahe_colorido(
                    processado,
                    CLAHE_CLIP_LIMIT,
                    CLAHE_TILE_GRID,
                )

            # 4. Ampliação moderada.
            processado = aplicar_lupa(
                processado,
                zoom,
                centro_x,
                centro_y,
                UPSCALE_QUALITY,
            )

            # 5. Nitidez pós-ampliação.
            if ENABLE_SHARPEN:
                strength = strength_por_zoom(
                    SHARPEN_BASE_STRENGTH,
                    zoom,
                )

                processado = unsharp(
                    processado,
                    strength,
                )

            # 6. Modo visual escolhido.
            processado = aplicar_modo(
                processado,
                modo,
            )

            ultimo_processado = processado.copy()

            frames += 1
            agora = perf_counter()
            delta = agora - timer

            if delta >= 1.0:
                fps = frames / delta
                frames = 0
                timer = agora

            exibicao = processado.copy()

            if mostrar_guia:
                exibicao = guia_leitura(
                    exibicao,
                    READING_GUIDE_Y,
                    READING_GUIDE_HEIGHT,
                    SHOW_READING_MARKERS,
                )

            if mostrar_hud:
                exibicao = hud(
                    exibicao,
                    zoom,
                    NOMES[modo],
                    congelado,
                    fps,
                    camera_info,
                    qualidade=qualidade,
                )

            display.mostrar(exibicao)

            acao = tecla_para_acao(
                display.tecla()
            )

            if acao == Acao.ZOOM_MAIS:
                zoom_i = min(
                    zoom_i + 1,
                    len(ZOOM_LEVELS) - 1,
                )

            elif acao == Acao.ZOOM_MENOS:
                zoom_i = max(
                    zoom_i - 1,
                    0,
                )

            elif acao == Acao.ESQUERDA:
                centro_x = max(
                    0.0,
                    centro_x - PAN_STEP,
                )

            elif acao == Acao.DIREITA:
                centro_x = min(
                    1.0,
                    centro_x + PAN_STEP,
                )

            elif acao == Acao.CIMA:
                centro_y = max(
                    0.0,
                    centro_y - PAN_STEP,
                )

            elif acao == Acao.BAIXO:
                centro_y = min(
                    1.0,
                    centro_y + PAN_STEP,
                )

            elif acao == Acao.CENTRALIZAR:
                centro_x = 0.5
                centro_y = 0.5

            elif acao == Acao.FREEZE:
                if not congelado:
                    ok, freeze = camera.read()

                    if ok and freeze is not None:
                        frame_congelado = freeze.copy()
                        congelado = True
                else:
                    congelado = False
                    frame_congelado = None

            elif acao == Acao.PROXIMO_MODO:
                modo_i = (
                    modo_i + 1
                ) % len(MODOS)

            elif acao == Acao.GUIA_LEITURA:
                mostrar_guia = not mostrar_guia

            elif acao == Acao.HUD:
                mostrar_hud = not mostrar_hud

            elif acao == Acao.FULLSCREEN:
                display.alternar_fullscreen()

            elif acao == Acao.CAPTURAR:
                if ultimo_processado is not None:
                    salvar_captura(
                        ultimo_processado
                    )

            elif acao == Acao.SAIR:
                break

    except KeyboardInterrupt:
        pass

    finally:
        camera.release()
        display.fechar()
        print("[OK] Lupa Digital encerrada.")


if __name__ == "__main__":
    main()
