# Changelog

## [0.5.0] — PySide6 / Qt

### Reestruturação
- Interface migrada de OpenCV HighGUI para PySide6.
- Removido `cv2.imshow`.
- Removido `cv2.waitKey`.
- Adicionado `QApplication` e `QMainWindow`.
- Captura atualizada com QTimer.
- GPIO atualizado com QTimer separado.
- Criado `core/LupaEngine`.
- Criado `VideoWidget` com QPainter.
- Guia de leitura migrado para Qt.
- Adicionado painel visual de baixa visão.
- Adicionados botões grandes na interface.
- Fullscreen gerenciado pelo Qt.

### Hardware mantido
- A/D2 -> físico 11.
- B/D3 -> físico 13.
- C/D4 -> físico 15.
- D/D5 -> físico 16.
- E/D6 -> físico 24.
- F/D7 -> físico 22.
- K/D8 -> físico 18.
- VCC -> físico 1.
- GND -> físico 9.
