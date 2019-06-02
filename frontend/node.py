from pygame import Surface, transform, SRCALPHA, BLEND_MAX, BLEND_MIN, K_DELETE
from .basewidget import BaseWidget
from .widgethandler import WidgetHandler
from .renderer import Renderer
from .constants import COLOR_UNSELECTED, COLOR_SELECTED
from pygame.sprite import Group


class Node(BaseWidget):
    def __init__(self, parent, imagen, x, y):
        super().__init__(parent)
        self.tipo = ''
        self.image = imagen
        self.rect = self.image.get_rect(center=(x, y))
        WidgetHandler.add_widgets(self)
        Renderer.add_widgets(self)

    def on_keydown(self, event):
        if event.key == K_DELETE:
            WidgetHandler.del_widget(self)
            Renderer.del_widget(self)

    def update(self, *args):
        if self.is_selected:
            self.deselect()
        for g in self.groups():
            if isinstance(g, Group):  # a very clunky way of saying "it's selected"
                self.select()


class Square(Node):
    def __init__(self, size, x, y):
        self.size = size
        imagen = Surface((size, size))
        super().__init__('Example', imagen, x, y)

    def scale(self, delta):
        self.size += delta
        self.image = transform.scale(self.image, (self.size, self.size))
        super().scale(delta)

    def select(self):
        super().select()
        self.image.fill(COLOR_SELECTED)

    def deselect(self):
        super().deselect()
        self.image.fill(COLOR_UNSELECTED)


class Diamond(Node):

    def __init__(self, size, x, y):
        self.size = size
        img = Surface((size, size), SRCALPHA)
        img.fill((0, 0, 0, 255))
        imagen = transform.rotate(img, 45)
        super().__init__(None, imagen, x, y)

    def select(self):
        self.image.fill(COLOR_SELECTED, special_flags=BLEND_MAX)
        super().select()

    def deselect(self):
        self.image.fill(COLOR_UNSELECTED, special_flags=BLEND_MIN)
        super().deselect()

    def scale(self, delta):
        self.size += delta
        img = Surface((self.size, self.size), SRCALPHA)
        if self.is_selected:
            img.fill(COLOR_SELECTED)
        else:
            img.fill(COLOR_UNSELECTED)
        self.image = transform.rotate(img, 45)

        super().scale(delta)
