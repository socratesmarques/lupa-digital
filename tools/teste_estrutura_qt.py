from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

arquivos = [
    "main.py",
    "core/lupa_engine.py",
    "ui/main_window.py",
    "ui/video_widget.py",
    "ui/styles.py",
    "hardware/botoes_gpio.py",
    "hardware/pinos.py",
]

faltando = [
    item
    for item in arquivos
    if not (ROOT / item).exists()
]

if faltando:
    raise SystemExit(
        "Arquivos ausentes: "
        + ", ".join(faltando)
    )

print("[OK] Estrutura PySide6 completa.")
