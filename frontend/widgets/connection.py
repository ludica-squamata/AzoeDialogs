from frontend.globals import COLOR_CONNECTION, WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from pygame import Surface, SRCALPHA, draw, BLEND_MAX, BLEND_MIN
from pygame.sprite import Group
from .basewidget import BaseWidget
from backend import System


class Connection(BaseWidget):
    layer = 5
    selectable = False
    numerable = False
    handle = None
    points = None

    def __init__(self, parent_a, parent_b):
        super().__init__()
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.points = []
        self.image = self.create()
        self.rect = self.image.get_rect()
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)
        System.toggle_mode()

    def create_midpoint(self):
        ra = self.parent_a.rect
        rb = self.parent_b.rect
        return [(ra.centerx + rb.centerx) // 2, (ra.centery + rb.centery) // 2]

    def create(self):
        image = Surface((640, 480), SRCALPHA)
        r_a = self.parent_a.rect
        r_b = self.parent_b.rect
        if self.handle is None:
            pc = self.create_midpoint()
        else:
            pc = self.handle.rect.center

        self.points = [r_a.center, pc, r_b.center]

        if self.handle is None:
            self.handle = MidPointHandle(self, pc, self.points.index(pc))

        draw.aalines(image, COLOR_CONNECTION, 0, self.points, 1)

        return image

    def update(self):
        if self.parent_a.alive() and self.parent_b.alive():
            self.image = self.create()
        else:
            self.kill()


class MidPointHandle(BaseWidget):
    numerable = False

    def __init__(self, parent, center, idx):
        super().__init__(parent)
        self.idx = idx
        self.image = Surface((8, 8), SRCALPHA)
        draw.circle(self.image, COLOR_CONNECTION, (3, 3), 4)
        self.rect = self.image.get_rect(center=center)
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def select(self):
        self.image.fill(COLOR_SELECTED, special_flags=BLEND_MAX)
        super().select()

    def deselect(self):
        self.image.fill(COLOR_UNSELECTED, special_flags=BLEND_MIN)
        super().deselect()

    def update(self, *args):
        self.parent.points[self.idx] = self.rect.center
        if self.is_selected:
            self.deselect()
        for g in self.groups():
            if isinstance(g, Group):  # a very clunky way of saying "it's selected"
                self.select()

