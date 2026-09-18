from enum import Enum, auto


class Acao(Enum):
    NENHUMA = auto()
    ZOOM_MAIS = auto()
    ZOOM_MENOS = auto()
    ESQUERDA = auto()
    DIREITA = auto()
    CIMA = auto()
    BAIXO = auto()
    CENTRALIZAR = auto()
    FREEZE = auto()
    PROXIMO_MODO = auto()
    GUIA_LEITURA = auto()
    HUD = auto()
    FULLSCREEN = auto()
    CAPTURAR = auto()
    SAIR = auto()


def tecla_para_acao(tecla):
    if tecla in (ord("+"), ord("=")):
        return Acao.ZOOM_MAIS

    if tecla == ord("-"):
        return Acao.ZOOM_MENOS

    if tecla in (ord("a"), ord("A")):
        return Acao.ESQUERDA

    if tecla in (ord("d"), ord("D")):
        return Acao.DIREITA

    if tecla in (ord("w"), ord("W")):
        return Acao.CIMA

    if tecla in (ord("x"), ord("X")):
        return Acao.BAIXO

    if tecla in (ord("c"), ord("C")):
        return Acao.CENTRALIZAR

    if tecla == ord(" "):
        return Acao.FREEZE

    if tecla in (ord("f"), ord("F")):
        return Acao.PROXIMO_MODO

    if tecla in (ord("r"), ord("R")):
        return Acao.GUIA_LEITURA

    if tecla in (ord("h"), ord("H")):
        return Acao.HUD

    if tecla in (ord("m"), ord("M")):
        return Acao.FULLSCREEN

    if tecla in (ord("s"), ord("S")):
        return Acao.CAPTURAR

    if tecla in (ord("q"), ord("Q"), 27):
        return Acao.SAIR

    return Acao.NENHUMA
