from pygame import display, draw, image
from pygame.sprite import LayeredUpdates
from .constants import COLOR_BG
from backend import EventHandler


class Renderer:
    widgets = None
    on_selection = False
    selection = None
    f = None
    width, height = 0, 0

    @classmethod
    def init(cls, w, h):
        display.set_caption('AzoeDialogs')
        display.set_icon(image.load('frontend/favicon.png'))
        display.set_mode((w, h))

        cls.width = w
        cls.height = h
        cls.widgets = LayeredUpdates()

    @classmethod
    def enable_selection(cls, selection_object):
        cls.selection = selection_object
        cls.on_selection = True

    @classmethod
    def add_widget(cls, widget):
        cls.widgets.add(widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        rect = [fondo.fill(COLOR_BG)]
        if cls.on_selection:
            draw.rect(fondo, cls.selection.color, cls.selection.rect, 1)
        rect.extend(cls.widgets.draw(fondo))
        display.update(rect)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']


EventHandler.register(Renderer.toggle_selection, 'EndSelection')
