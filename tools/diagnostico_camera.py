import glob
import shutil
import subprocess

import cv2


def executar(cmd):
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=8,
        ).stdout.strip()
    except Exception as exc:
        return f"Erro: {exc}"


print("=== Diagnóstico de câmera - Lupa Digital ===")
print("Dispositivos encontrados:", glob.glob("/dev/video*") or "nenhum")

if shutil.which("v4l2-ctl"):
    print("\n=== v4l2-ctl --list-devices ===")
    print(executar(["v4l2-ctl", "--list-devices"]))

    for dev in glob.glob("/dev/video*"):
        print(f"\n=== Formatos de {dev} ===")
        print(executar([
            "v4l2-ctl",
            "-d", dev,
            "--list-formats-ext",
        ]))

        print(f"\n=== Controles de {dev} ===")
        print(executar([
            "v4l2-ctl",
            "-d", dev,
            "--list-ctrls",
        ]))
else:
    print(
        "\nDica: instale 'v4l-utils' para ver formatos e controles:\n"
        "sudo apt install v4l-utils"
    )

print("\n=== Teste OpenCV ===")
for i in range(8):
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

    if not cap.isOpened():
        cap.release()
        continue

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    fourcc = "".join(
        chr((fourcc_int >> (8 * j)) & 0xFF)
        for j in range(4)
    ).strip("\x00")

    ok, frame = cap.read()

    print(
        f"indice={i} | {w}x{h} | fps={fps:.2f} | "
        f"fourcc={fourcc or '?'} | frame={'OK' if ok else 'FALHOU'}"
    )

    cap.release()

print("\nUse no config/settings.py o índice que entregar a imagem RGB.")
