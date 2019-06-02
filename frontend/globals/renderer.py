from pygame import display, draw, font
from pygame.sprite import LayeredUpdates
from .constants import COLOR_BG, COLOR_TEXT
from backend.eventhandler import EventHandler
from backend.system import System


class Renderer:
    widgets = None
    on_selection = False
    selection = None
    f = None

    @classmethod
    def init(cls, w, h):
        display.set_mode((w, h))
        cls.widgets = LayeredUpdates()
        cls.f = font.SysFont('Verdana', 16)

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
        fondo.blit(cls.f.render(System.MODE[0], 1, COLOR_TEXT, COLOR_BG), (0, 0))
        if cls.on_selection:
            draw.rect(fondo, cls.selection.color, cls.selection.rect, 1)
        rect.extend(cls.widgets.draw(fondo))
        display.update(rect)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']


# noinspection PyTypeChecker
EventHandler.register(Renderer.toggle_selection, 'Selection')
