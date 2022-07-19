from frontend.globals import COLOR_TEXT, COLOR_BG
from .basewidget import BaseWidget
from backend import System, EventHandler
from pygame import font


class Counter(BaseWidget):

    def __init__(self):
        super().__init__()
        self.f = font.SysFont('Verdana', 15)
        self.update()
        self.show()

    @staticmethod
    def get_text():
        f5 = '(F5): '
        if System.limit_input:
            cant = System.get_lenght()
            extra = System.get_extra()
            if cant > 1:
                t = 'Quedan '+str(cant)+' nodos disponibles'
            elif cant == 1:
                t = 'Queda ' + str(cant) + ' nodo disponible'
            else:
                t = 'No quedan más nodos'
                if extra > 1:
                    t += ' ('+str(extra)+' adicionales)'
                elif extra != 0:
                    t += ' (1 adicional)'

        else:
            cant = System.number_of_dialog_nodes
            if cant == 1:
                t = 'Hay 1 nodo'
            elif cant == 0:
                t = 'No hay nodos.'
            else:
                t = 'Hay ' + str(cant) + ' nodos.'

        return f5 + t

    def update(self):
        self.image = self.f.render(self.get_text(), 1, COLOR_TEXT, COLOR_BG)
        self.rect = self.image.get_rect()


EventHandler.register(lambda e: Counter(), 'Init')
