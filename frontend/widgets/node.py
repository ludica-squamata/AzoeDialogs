from frontend.globals import WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from pygame import Surface, transform, SRCALPHA, BLEND_MAX, BLEND_MIN, font
from .connection import Connection
from .basewidget import BaseWidget
from pygame.sprite import Group


class Node(BaseWidget):
    _layer = 1
    tipo = ''
    idx = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connections = []
        self.fuente = font.SysFont('Verdana', 10)
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    def connect(self, other):
        if other not in self.connections:
            Connection(self, other)
            self.connections.append(other)
            other.set_connected(self)

    def set_connected(self, other):
        self.connections.append(other)

    def get_idx(self):
        return [w for w in WidgetHandler.widgets.sprites() if w.numerable].index(self)

    def create(self):
        pass

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


class Square(Node):
    def __init__(self, x, y):

        super().__init__()

        self.layer = 1
        self.tipo = 'Square'
        self.image = self.create()
        self.rect = self.image.get_rect(center=(x, y))

    def create(self):
        len_idx = len(str(self.get_idx()))
        size = 16
        if len_idx == 2:
            size = 20
        elif len_idx == 3:
            size = 25
        return Surface((size, size))

    def select(self):
        super().select()
        self.image.fill(COLOR_SELECTED)

    def deselect(self):
        super().deselect()
        self.image.fill(COLOR_UNSELECTED)


class Diamond(Node):

    def __init__(self, x, y, ):
        super().__init__()
        len_idx = len(str(self.get_idx()))
        if len_idx == 1:
            self.size = 16
        elif len_idx == 2:
            self.size = 20
        elif len_idx == 3:
            self.size = 25
        self.layer = 1
        self.tipo = 'Diamond'
        self.image = self.create()
        self.rect = self.image.get_rect(center=(x, y))

    def create(self):
        len_idx = len(str(self.get_idx()))
        size = 16
        if len_idx == 2:
            size = 20
        elif len_idx == 3:
            size = 25
        img = Surface((size, size), SRCALPHA)
        img.fill((0, 0, 0, 255))
        imagen = transform.rotate(img, 45)
        return imagen

    def select(self):
        self.image.fill(COLOR_SELECTED, special_flags=BLEND_MAX)
        super().select()

    def deselect(self):
        self.image.fill(COLOR_UNSELECTED, special_flags=BLEND_MIN)
        super().deselect()
