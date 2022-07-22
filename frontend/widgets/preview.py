from frontend.globals.constants import COLOR_BOX, COLOR_TEXT, WIDTH, HEIGHT, NODOS_DIALOGO, NODOS_BEHAVIOUR
from backend.textrect import render_textrect, TextRectException
from frontend.globals import WidgetHandler, Renderer
from backend import System, EventHandler
from .basewidget import BaseWidget
from pygame import font, Surface


class Preview(BaseWidget):

    def __init__(self):
        super().__init__()
        self.f = font.SysFont('Verdana', 16)
        self.image = Surface((WIDTH, HEIGHT // 5))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))
        EventHandler.register(self.switch, 'ToggleTypeMode')
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    def switch(self, event):
        if event.data['instance'] == 'MainTB':
            if event.data['value'] is False:
                WidgetHandler.add_widget(self)
                Renderer.add_widget(self)
            else:
                WidgetHandler.del_widget(self)
                Renderer.del_widget(self)

    @staticmethod
    def get_selected():
        s = [o for o in WidgetHandler.selected.widgets() if o.numerable]
        c = [d for d in WidgetHandler.selected.widgets() if d.order == 'a']
        d = [d for d in WidgetHandler.selected.widgets() if d.order == 'd']

        t = ''
        if len(s) and len(c):
            ss = 's' if len(s) > 1 else ''
            elos = 'el' if len(s) == 1 else 'los'
            t = 'Hay un locutor y {} nodo{} seleccionado{}.'.format(len(s), ss, ss)
            t += ' Presione D para vincular al locutor con {} nodo{}.'.format(elos, ss)
        elif len(c) == 1 or System.replacing_locutor:
            t = 'Presione F3 para editar el nombre del locutor seleccionado, o SUPR para cambiar su color.'
        elif len(d) == 1:
            t = 'Presione S para crear nodos del tipo seleccionado.'

        if len(s) == 1:
            if s[0].group == NODOS_DIALOGO:
                n = s[0].text
                if s[0].named:
                    t = s[0].locutor_name + ': "' + n + '"'
                else:
                    t = '"' + n + '"'

            elif s[0].group == NODOS_BEHAVIOUR:
                t = s[0].text

        elif len(s) == 2:
            t = 'Dos nodos están seleccionados. Presione C para crear una conexión entre ellos,'
            t += ' o A, si ya hay una conexión, para crear un punto intermedio'
        elif len(s) > 2:
            t = 'Múltiples nodos están selecionados. Elija sólo uno para ver su contenido o bien dos para crear una'
            t += ' conexión entre ellos (tecla C).'
        elif not len(s):
            t = 'No hay nodos seleccionados. Haga click en uno para ver su contenido'
            if not System.limit_input or System.get_lenght() > 0:
                t += ' o bien toque S para crear un nodo.'
            else:
                t += '.'

        return t

    def update(self):
        text = self.get_selected()
        h = -3
        while True:
            try:
                r = render_textrect(text, self.f, *self.rect.inflate(-3, h).size, COLOR_TEXT, COLOR_BOX)
                break
            except TextRectException:
                h += 3
        self.image.fill(COLOR_BOX)
        self.image.blit(r, (3, 3))

    def toggle(self, event):
        pass


EventHandler.register(lambda e: Preview(), 'Init')
