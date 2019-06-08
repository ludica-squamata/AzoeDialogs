from frontend.globals import COLOR_CONNECTION, WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from backend.eventhandler import EventHandler
from pygame import Surface, SRCALPHA, draw, BLEND_MAX, BLEND_MIN
from pygame.sprite import Group
from .basewidget import BaseWidget
from bisect import bisect


class Connection(BaseWidget):
    layer = 5
    selectable = False
    numerable = False
    handles = None
    points = None

    def __init__(self, parent_a, parent_b):
        super().__init__()
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.points = [self.parent_a.rect.center, self.parent_b.rect.center]
        self.handles = [self.parent_a, self.parent_b]
        self.image = self.create()
        self.rect = self.image.get_rect()
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

        # noinspection PyTypeChecker
        EventHandler.register(self.event_handle, 'AddMidPoint')

    @staticmethod
    def create_midpoint(ra, rb):
        return (ra[0] + rb[0]) // 2, (ra[1] + rb[1]) // 2

    def event_handle(self, event):
        base = event.data['base']
        other = event.data['other']
        if all(handle in self.handles for handle in [base, other]):
            base = self.points.index(event.data['base'].rect.center)
            other = self.points.index(event.data['other'].rect.center)
            if other == base+1:
                self.add_handle(base, other)

    def add_handle(self, a, b):
        pc = self.create_midpoint(self.points[a], self.points[b])
        p = bisect(self.points, pc)

        self.points.insert(p, pc)
        self.handles.insert(p, MidPointHandle(self, pc, self.points.index(pc)))
        for handle in self.handles[p:-1]:
            handle.reset_idx(self.points.index(handle.rect.center))

    def create(self):
        image = Surface((640, 480), SRCALPHA)
        draw.aalines(image, COLOR_CONNECTION, 0, self.points, 1)
        return image

    def update(self):
        self.points[0] = self.parent_a.rect.center
        self.points[-1] = self.parent_b.rect.center
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

    def reset_idx(self, idx):
        self.idx = idx

    def update(self, *args):
        if not self.parent.alive():
            self.kill()
        self.parent.points[self.idx] = self.rect.center
        if self.is_selected:
            self.deselect()
        for g in self.groups():
            if isinstance(g, Group):  # a very clunky way of saying "it's selected"
                self.select()
