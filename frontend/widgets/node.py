from frontend.globals import WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from backend.eventhandler import EventHandler
from pygame import Surface, font
from .connection import toggle_connection
from .basewidget import BaseWidget
from pygame.sprite import Group


class Node(BaseWidget):
    _layer = 1
    idx = 0
    type_overriden = False
    _tipo = 'node'

    def __init__(self, x, y):
        super().__init__()
        self.connections = []
        self.fuente = font.SysFont('Verdana', 10)
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)
        self.layer = 1
        self.image = self.create()
        self.rect = self.image.get_rect(center=(x, y))

    def connect(self, other):
        if other not in self.connections:
            toggle_connection(self, other)
            self.connections.append(other)
        if len(self.connections) > 1:
            for child in self.connections:
                child.type_overriden = True
                child.tipo = 'branch'

    def disconnect(self, other):
        if other in self.connections:
            toggle_connection(self, other, value=False)
            self.connections.remove(other)

    def set_connected(self, other):
        self.connections.append(other)

    def del_connected(self, other):
        self.connections.remove(other)

    def get_idx(self):
        return [w for w in WidgetHandler.widgets.sprites() if w.numerable].index(self)

    def create(self):
        len_idx = len(str(self.get_idx()))
        size = 16
        if len_idx == 2:
            size = 20
        elif len_idx == 3:
            size = 25
        return Surface((size, size))

    def update(self, *args):
        self.idx = self.get_idx()
        render_sel = self.fuente.render(str(self.idx), 1, COLOR_UNSELECTED, COLOR_SELECTED)
        render_uns = self.fuente.render(str(self.idx), 1, COLOR_SELECTED, COLOR_UNSELECTED)
        self.image = self.create()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(render_uns, render_uns.get_rect(center=self.image.get_rect().center))

        if self.is_selected:
            self.deselect()
        for g in self.groups():
            if isinstance(g, Group):  # a very clunky way of saying "it's selected"
                self.select()
                self.image.blit(render_sel, render_uns.get_rect(center=self.image.get_rect().center))

    def __repr__(self):
        return self.tipo + ' #' + str(self.idx)

    def __str__(self):
        return str(self.idx)

    def __int__(self):
        return self.idx

    def kill(self):
        WidgetHandler.del_widget(self)
        Renderer.del_widget(self)
        super().kill()

    @property
    def tipo(self):
        tipo = self._tipo
        if not self.type_overriden:
            tipo = 'node'
        if not len(self.connections):
            tipo = 'leaf'
        return tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def lead(self):
        lenght = len(self.connections)
        if lenght > 1:
            return [int(i) for i in self.connections]
        elif lenght == 1:
            return int(self.connections[0])

    def select(self):
        super().select()
        self.image.fill(COLOR_SELECTED)

    def deselect(self):
        super().deselect()
        self.image.fill(COLOR_UNSELECTED)


EventHandler.register(lambda e: Node(*e.data.get('pos')), 'AddNode')
