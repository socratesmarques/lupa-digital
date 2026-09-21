APP_STYLE = """
QMainWindow {
    background: #090909;
}

QWidget {
    color: #ffffff;
    font-family: Sans Serif;
}

QFrame#StatusBar {
    background: #111111;
    border-bottom: 1px solid #3b3b3b;
}

QLabel#ZoomLabel {
    font-size: 28px;
    font-weight: 800;
}

QLabel#ModeLabel {
    font-size: 18px;
    font-weight: 700;
}

QLabel#QualityLabel {
    font-size: 16px;
}

QLabel#HardwareLabel {
    font-size: 14px;
    color: #d2d2d2;
}

QFrame#Controls {
    background: #111111;
    border-top: 1px solid #3b3b3b;
}

QPushButton {
    min-height: 58px;
    padding: 8px 18px;
    border: 2px solid #f2f2f2;
    border-radius: 10px;
    background: #1b1b1b;
    color: #ffffff;
    font-size: 20px;
    font-weight: 800;
}

QPushButton:hover {
    background: #2d2d2d;
}

QPushButton:pressed {
    background: #ffffff;
    color: #000000;
}

QPushButton#FreezeButton[active="true"] {
    background: #ffffff;
    color: #000000;
}

QPushButton#GuideButton[active="true"] {
    background: #ffffff;
    color: #000000;
}
"""
