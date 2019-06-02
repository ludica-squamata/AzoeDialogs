from pygame import Rect
from .basewidget import BaseWidget
from .constants import COLOR_SELECTION
from .widgethandler import WidgetHandler
from .renderer import Renderer
from backend.eventhandler import EventHandler


class Selection(BaseWidget):
    def __init__(self, event):
        x, y = event.data['pos']
        self.rect = Rect(x, y, 1, 1)
        self.color = COLOR_SELECTION
        super().__init__()
        Renderer.enable_selection(self)
        WidgetHandler.enable_selection(self)

    def on_mousemotion(self, event):
        if event.buttons[0]:
            self.rect.width = event.pos[0]-self.rect.x
            self.rect.height = event.pos[1]-self.rect.y

    def on_mouseup(self, event):
        EventHandler.trigger('Selection', 'SelectionObject', {'value': False})
        self.rect.normalize()
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def __repr__(self):
        return 'Selection Object @{},{},{},{}'.format(*self.rect)