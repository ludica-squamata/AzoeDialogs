from frontend.globals.constants import WIDTH, HEIGHT, COLOR_BOX, COLOR_SELECTED
from backend.group import WidgetGroup
from .basewidget import BaseWidget

from pygame import Surface, font


class BaseWindow(BaseWidget):
    is_visible = False

    def __init__(self, title):
        super().__init__()
        self.image = Surface([WIDTH // 2, HEIGHT // 2])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 32))
        self.image.fill(COLOR_BOX, [1, 1, self.rect.w - 2, self.rect.h - 2])
        self.font_title = font.SysFont('Verdana', 14, bold=True)
        self._r = self.render_title(title)

        self.properties = WidgetGroup()

    def render_title(self, title):
        self.image.fill(COLOR_BOX, [1, 1, self.rect.w - 2, self.rect.h - 2])
        render = self.font_title.render(title, 1, COLOR_SELECTED, COLOR_BOX)
        return self.image.blit(render, (1, 1))
