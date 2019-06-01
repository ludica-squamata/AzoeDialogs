from pygame import display
from pygame.sprite import LayeredUpdates
from .constants import COLOR_BG


class Renderer:
    widgets = None

    @classmethod
    def init(cls, w, h):
        display.set_mode((w, h))
        cls.widgets = LayeredUpdates()

    @classmethod
    def add_widgets(cls, *widget):
        cls.widgets.add(*widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        rect = [fondo.fill(COLOR_BG)]
        rect.extend(cls.widgets.draw(fondo))
        display.update(rect)
