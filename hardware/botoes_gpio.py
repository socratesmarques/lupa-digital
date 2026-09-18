"""
Ponto de integração para a próxima versão com Orange Pi.

Não foram definidos pinos GPIO porque o modelo exato do Orange Pi
ainda precisa ser confirmado.

Mapeamento mínimo planejado:
- Botão Zoom +
- Botão Zoom -
- Botão Freeze (opcional)
- Botão Modo de leitura (opcional)

O teclado usado no protótipo serve como substituto temporário.
"""


class BotoesGPIO:
    def iniciar(self):
        raise NotImplementedError(
            "Defina o modelo/pinout do Orange Pi antes de configurar GPIO."
        )

    def ler(self):
        return None

    def encerrar(self):
        pass
