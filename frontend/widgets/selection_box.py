from frontend.globals import COLOR_SELECTION, WidgetHandler, Renderer
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from pygame import Rect


class SelectionBox(BaseWidget):
    layer = 0

    def __init__(self, event):
        x, y = event.data['pos']
        self.rect = Rect(x, y, 1, 1)
        self.color = COLOR_SELECTION
        super().__init__()
        Renderer.enable_selection(self)
        WidgetHandler.enable_selection(self)

    def on_mousemotion(self, event):
        if event.buttons[0]:
            dx, dy = event.rel
            if dx < 0:
                self.rect.x += dx
                self.rect.width += abs(dx)
            elif dx > 0:
                self.rect.width += dx

            if dy < 0:
                self.rect.y += dy
                self.rect.height += abs(dy)
            elif dy > 0:
                self.rect.height += dy

    def on_mouseup(self, event):
        EventHandler.trigger('EndSelection', 'SelectionObject', {'value': False})
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def __repr__(self):
        return 'Selection Object @{},{},{},{}'.format(*self.rect)


EventHandler.register(lambda e: SelectionBox(e), 'AddSelection')
