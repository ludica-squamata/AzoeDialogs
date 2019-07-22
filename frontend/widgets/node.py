from frontend.globals import WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from pygame import Surface, font, Color, transform
from backend.eventhandler import EventHandler
from .connection import toggle_connection
from .basewidget import BaseWidget
from pygame.sprite import Group


class Node(BaseWidget):
    _layer = 1
    idx = 0
    order = 'b'
    type_overriden = False
    _tipo = 'node'
    tamanio = 16

    color_name = ''
    color_a = COLOR_SELECTED
    color_b = COLOR_UNSELECTED

    interlocutor = None

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
            self.interlocutor = other

        if len(self.connections) > 1:
            for child in self.connections:
                child.type_overriden = True
                child.tipo = 'branch'

        for child in self.connections:
            child.interlocutor = self

    def disconnect(self, other):
        if other in self.connections:
            toggle_connection(self, other, value=False)
            self.connections.remove(other)

    def get_idx(self):
        return [w for w in WidgetHandler.widgets.sprites() if w.numerable].index(self)

    def colorize(self, a):
        self.color_name = '%02x%02x%02x' % (a.r, a.g, a.b)
        b = Color("white")  # a base color is needed
        b.hsla = a.hsla[0], 50, 75, 100
        self.color_a = a
        self.color_b = b

    def create(self):
        size = self.size()
        return Surface((size, size))

    def size(self):
        len_idx = len(str(self.get_idx()))
        size = self.tamanio
        if len_idx == 2:
            size = 20
        elif len_idx == 3:
            size = 25
        return size

    def update(self, *args):
        self.idx = self.get_idx()
        a = self.color_a
        b = self.color_b
        c = COLOR_SELECTED if b == COLOR_UNSELECTED else COLOR_UNSELECTED
        render_sel = self.fuente.render(str(self.idx), 1, COLOR_UNSELECTED, a)
        render_uns = self.fuente.render(str(self.idx), 1, c, b)
        size = self.size() if self.tamanio < self.size() else self.tamanio
        self.image = transform.scale(self.image, (size, size))
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
        self.image.fill(self.color_a)

    def deselect(self):
        super().deselect()
        self.image.fill(self.color_b)


EventHandler.register(lambda e: Node(*e.data.get('pos')), 'AddNode')
