from frontend.globals import COLOR_BOX, WIDTH, HEIGHT
from .basewidget import BaseWidget
from pygame import font, Surface


class SideBox(BaseWidget):

    def __init__(self):
        super().__init__()
        self.fa = font.SysFont('Verdana', 15)
        self.fb = font.SysFont('Verdana', 12)
        self.fa.set_underline(1)

        self.image = Surface((WIDTH // 5 - 25, (HEIGHT // 5) * 2 - 10))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(topright=(WIDTH, 0))
        self.clear_area = self.rect.copy()
        self.clear_area.centerx = self.rect.width // 2
        self.clear_area.height -= 21
        self.clear_area.top += 21
