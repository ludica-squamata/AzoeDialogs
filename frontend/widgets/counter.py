from frontend.globals import COLOR_TEXT, COLOR_BG, WidgetHandler, Renderer
from .basewidget import BaseWidget
from backend import System  # , EventHandler
from pygame import font


class Counter(BaseWidget):
    numerable = False
    selectable = False

    def __init__(self):
        super().__init__()
        self.f = font.SysFont('Verdana', 15)
        t = 'Nodos Disponibles: ' + str(System.get_lenght())
        self.image = self.f.render(t, 1, COLOR_TEXT, COLOR_BG)
        self.rect = self.image.get_rect()
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    @staticmethod
    def get_text():
        cant = System.get_lenght()
        if cant > 1:
            return 'Quedan '+str(cant)+' nodos disponibles'
        elif cant == 1:
            return 'Queda ' + str(cant) + ' nodo disponible'
        else:
            return 'No quedan más nodos'

    def update(self):
        self.image = self.f.render(self.get_text(), 1, COLOR_TEXT, COLOR_BG)
        self.rect = self.image.get_rect()


# EventHandler.register(lambda e: Counter(), 'Init')
