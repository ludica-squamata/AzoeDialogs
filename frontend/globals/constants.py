# Constantes
from pygame import Color

# Colores
COLOR_BG = Color(125, 125, 125, 255)
COLOR_BOX = Color(100, 100, 100, 255)
COLOR_UNSELECTED = Color(0, 0, 0, 255)
COLOR_SELECTED = Color(255, 255, 255, 255)
COLOR_SELECTION = Color(0, 255, 255)
COLOR_CONNECTION = Color(0, 0, 0, 255)
COLOR_TEXT = Color(0, 0, 0, 255)

# Tamaño de la Ventana
WIDTH = 640
HEIGHT = 480

NODOS_DIALOGO = 1
NODOS_BEHAVIOUR = 2

node_colors = {
    'Selector': Color(70, 232, 210),
    'Sequence': Color(46, 153, 138),
    'Succeder': Color(76, 153, 46),
    'Failer': Color(146, 191, 128),
    'Repeater': Color(191, 164, 128),
    'UntilFail': Color(156, 72, 139),
    'UntilSuccess': Color(97, 22, 82),
    'Inverter': Color(130, 93, 59)
}
