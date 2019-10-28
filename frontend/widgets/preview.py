from frontend.globals import WidgetHandler, Renderer, COLOR_BOX, COLOR_TEXT, WIDTH, HEIGHT
from .basewidget import BaseWidget
from backend import System, render_textrect  # , EventHandler,
from pygame import font, Surface


class Preview(BaseWidget):
    numerable = False
    selectable = False

    def __init__(self):
        super().__init__()
        self.f = font.SysFont('Verdana', 16)
        self.image = Surface((WIDTH, HEIGHT // 5))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(bottomleft=(0, WIDTH))
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    @staticmethod
    def get_selected():
        s = [o for o in WidgetHandler.selected.sprites() if o.numerable]
        if len(s) == 1:
            idx = s[0].idx
            t = '"'+System.data[idx]+'"'
        elif len(s) == 2:
            t = 'Dos nodos están seleccionados. Presione C para crear una conexión entre ellos,'
            t += ' o A, si ya hay una conexión, para crear un punto intermedio'
        elif len(s) > 2:
            t = 'Múltiples nodos están selecionados. Elija sólo uno.'
        else:
            t = 'Seleccione un nodo para ver su contenido'

        return t

    def update(self):
        text = self.get_selected()
        r = render_textrect(text, self.f, self.rect, COLOR_TEXT, COLOR_BOX)
        self.image.fill(COLOR_BOX)
        self.image.blit(r, (3, 3))


# EventHandler.register(lambda e: Preview(), 'Init')
