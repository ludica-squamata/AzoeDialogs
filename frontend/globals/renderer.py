from frontend.globals import WIDTH, HEIGHT, COLOR_TEXT
from pygame import display, image, font, Surface, draw
from pygame.sprite import LayeredUpdates
from backend import EventHandler, System
from .constants import COLOR_BG
from os import getcwd, path


class Renderer:
    widgets = None
    on_selection = False
    selection = None
    typemode_label = None
    typemode_mark = None

    mode_label = None

    @classmethod
    def init(cls):
        display.set_caption('Azoe Integration')
        if path.exists(path.join(getcwd(), 'lib')):
            prefix = 'lib/'
        else:
            prefix = ''
        display.set_icon(image.load(prefix + 'frontend/favicon.png'))
        display.set_mode((WIDTH, HEIGHT))

        f = font.SysFont('Verdana', 14)
        cls.mode_label = f.render('Toggle Mode (F4)', 1, COLOR_TEXT, COLOR_BG)
        cls.typemode_label = f.render('TypeMode (F3):', 1, COLOR_TEXT, COLOR_BG)
        cls.typemode_mark = Surface((19, 19))
        cls.widgets = LayeredUpdates()

    @classmethod
    def enable_selection(cls, selection_object):
        cls.selection = selection_object
        cls.on_selection = True

    @classmethod
    def add_widget(cls, widget, layer=0):
        if widget not in cls.widgets:
            cls.widgets.add(widget, layer=layer)

    @classmethod
    def del_widget(cls, widget):
        if widget in cls.widgets:
            cls.widgets.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        rect = [fondo.fill(COLOR_BG)]
        if System.type_mode:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

        r = fondo.blit(cls.typemode_label, (505, 360))
        cls.typemode_mark.fill(color)
        fondo.blit(cls.typemode_mark, (r.right + 3, r.y))
        r2 = cls.mode_label.get_rect(bottom=r.top - 2, left=r.left)
        fondo.blit(cls.mode_label, r2)

        rect.extend(cls.widgets.draw(fondo))
        if cls.on_selection:
            corners = [cls.selection.rect.topleft,
                       cls.selection.rect.topright,
                       cls.selection.rect.bottomright,
                       cls.selection.rect.bottomleft]
            draw.aalines(fondo, cls.selection.color, 1, corners)
        display.update(rect)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']


EventHandler.register(Renderer.toggle_selection, 'EndSelection')
