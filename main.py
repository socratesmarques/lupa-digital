import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from config.settings import APP_NAME, VERSION
from ui.main_window import MainWindow


def main():
    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )
    app.setApplicationVersion(
        VERSION
    )

    try:
        janela = MainWindow()
    except RuntimeError as exc:
        QMessageBox.critical(
            None,
            "Lupa Digital",
            str(exc),
        )
        return 1

    if not janela.isFullScreen():
        janela.show()
    else:
        janela.showFullScreen()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
