from frontend.globals.constants import WIDTH, HEIGHT, COLOR_BOX, COLOR_TEXT, COLOR_SELECTED
from backend.eventhandler import EventHandler
from frontend.globals import WidgetHandler
from backend.group import WidgetGroup
from backend.util import abrir_json
from .basewidget import BaseWidget
from backend.system import System
from pygame import Surface, font
from os import getcwd, listdir
from os.path import join


class LoadWindow(BaseWidget):
    layer = 5000

    def __init__(self):
        super().__init__()
        self.image = Surface([WIDTH // 2, HEIGHT // 2])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 32))
        self.image.fill(COLOR_BOX)
        f = font.SysFont('Verdana', 13, bold=True)
        render = f.render('Load', 1, COLOR_SELECTED, COLOR_BOX)
        r = self.image.blit(render, (0, 0))

        self.properties = WidgetGroup()
        ruta = join(getcwd(), 'data')
        for i, file in enumerate(listdir(ruta)):
            x = self.rect.x + 2
            y = i * 21 + self.rect.y + r.bottom
            filename = join(ruta, file)
            row = Row(self, file[:-5].capitalize(), filename, x, y)
            self.properties.add(row, layer=1)

        EventHandler.register(self.toggle, 'LoadData')
        EventHandler.deregister(self.toggle, 'F4ToggleMode')

    def toggle(self, event=None):
        if event is not None and event.data['value'] is True:
            self.show()
            for row in self.properties.get_widgets_from_layer(1):
                row.show()
        else:
            self.hide()
            for row in self.properties.get_widgets_from_layer(1):
                row.hide()

    def deselect_all(self):
        for row in self.properties.get_widgets_from_layer(1):
            row.deselect()


class Row(BaseWidget):
    selectable = True

    def __init__(self, parent, text, ruta, x, y):
        super().__init__(parent)
        f1 = font.SysFont('Verdana', 14)

        self.img_uns = f1.render(text, 1, COLOR_TEXT, COLOR_BOX)
        self.img_sel = f1.render(text, 1, COLOR_SELECTED, COLOR_BOX)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(x, y))

        self.filepath = ruta

        EventHandler.register(self.load_file, 'LoadDataFile')

    def toggle(self, event):
        pass

    def select(self):
        super().select()
        self.image = self.img_sel

    def deselect(self):
        super().deselect()
        self.image = self.img_uns

    def on_mousebuttondown(self, event):
        self.parent.deselect_all()
        self.select()

    def on_mousemotion(self, event):
        # this hook is necessary
        pass

    def load_file(self, event):
        if event.data['selected'] == self:
            data = abrir_json(self.filepath)
            if len(data['head']) == 2:
                mode = 'behaviour'
            else:
                mode = 'dialog'
            System.load_file_data(data, mode)
            EventHandler.trigger('trigger_node_creation', 'LoadWindow', {'mode': mode})
            self.parent.toggle()


EventHandler.register(lambda a: LoadWindow(), 'Init')
