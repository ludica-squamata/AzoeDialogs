from .basewidget import BaseWidget
from pygame import Surface, SRCALPHA, draw
from .widgethandler import WidgetHandler
from .renderer import Renderer
from .constants import COLOR_CONNECTION


class Connection(BaseWidget):
    layer = 5
    selectable = False

    def __init__(self, parent_a, parent_b):
        super().__init__()
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.image, self.rect = self.create()
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def create(self):
        r_a = self.parent_a.rect
        r_b = self.parent_b.rect

        rect = r_a.union(r_b)
        image = Surface(rect.size, SRCALPHA)
        pa = r_a.centerx - rect.x, r_a.centery - rect.y
        pb = r_b.centerx - rect.x, r_b.centery - rect.y
        draw.aaline(image, COLOR_CONNECTION, pb, pa, 1)
        return image, rect

    def update(self):
        if self.parent_a.alive() and self.parent_b.alive():
            self.image, self.rect = self.create()
        else:
            self.kill()
