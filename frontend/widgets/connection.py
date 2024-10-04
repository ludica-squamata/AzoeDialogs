from frontend.globals import COLOR_CONNECTION, WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED, WIDTH, HEIGHT
from pygame import Surface, SRCALPHA, draw, BLEND_MAX, BLEND_MIN
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget


class Connection(BaseWidget):
    handles = None

    def __init__(self, parent_a, parent_b):
        super().__init__()
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.handles = [parent_a, parent_b]
        self.image = self.create()
        self.rect = self.image.get_rect()
        self.layer = min([parent_a.layer, parent_b.layer]) - 1
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

        EventHandler.register(self.event_handle, 'AddMidPoint')
        EventHandler.register(self.delete, 'DeleteConnection')

    def event_handle(self, event):
        base = event.data['base']
        other = event.data['other']
        data = event.data.get('data', None)
        if all([handle in self.handles for handle in [base, other]]):
            base = self.handles.index(event.data['base'])
            other = self.handles.index(event.data['other'])
            if base + 1 == other or other + 1 == base:
                self.add_handle(base, other, data)

    @staticmethod
    def create_midpoint(ra, rb):
        return (ra[0] + rb[0]) // 2, (ra[1] + rb[1]) // 2

    def add_handle(self, a, b, data=None):
        center = self.create_midpoint(self.handles[a], self.handles[b])
        p = a + 1 if a < b else b + 1
        midpoint = Metadata(self, center, data)

        self.handles.insert(p, midpoint)

    def create(self):
        image = Surface((WIDTH, HEIGHT), SRCALPHA)
        if self.parent_b in self.parent_a.connections:  #parent_b is a child of parent_a
            side_a = self.parent_a.rect.midbottom
            side_b = self.parent_b.rect.midtop
        elif self.parent_a in self.parent_b.connections:  # parent_a is a child of parent_b
            side_a = self.parent_b.rect.midbottom
            side_b = self.parent_a.rect.midtop
        else:
            raise TypeError("parents are not related")

        if len(self.handles) > 2:
            _centers = [side_a, *[h.rect.center for h in self.handles[1:-1]], side_b]
            draw.aalines(image, COLOR_CONNECTION, 0, _centers)
        else:
            draw.aalines(image, COLOR_CONNECTION, 0, [side_a, side_b])
        return image

    def delete(self, event):
        a, b = event.data['parents']
        if not event.data['value'] and all([x in self.handles for x in [a, b]]):
            self.kill()

    def update(self):
        if self.parent_a.alive() and self.parent_b.alive():
            self.image = self.create()
        else:
            self.kill()

    def __repr__(self):
        return 'Connection between ' + ', '.join(['{}'] * len(self.handles)).format(*self.handles)


class MidPointHandle(BaseWidget):
    selectable = True

    def __init__(self, parent, center):
        super().__init__(parent)
        self.layer = 20
        self.image = Surface((8, 8), SRCALPHA)
        draw.circle(self.image, COLOR_CONNECTION, (3, 3), 4)
        self.rect = self.image.get_rect(center=center)
        self.x, self.y = self.rect.center
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)
        EventHandler.register(self.toggle_selection, 'select', 'deselect')

    def on_keydown(self, event):
        if super().on_keydown(event):
            self.parent.handles.remove(self)

    def select(self):
        self.image.fill(COLOR_SELECTED, special_flags=BLEND_MAX)
        super().select()

    def deselect(self):
        self.image.fill(COLOR_UNSELECTED, special_flags=BLEND_MIN)
        super().deselect()

    @property
    def idx(self):
        return self.parent.handles.index(self)

    def update(self, *args):
        if not self.parent.alive():
            self.kill()

    def __repr__(self):
        return 'MidPoint #' + str(self.idx)


def toggle_connection(a, b, value=True):
    if value:
        Connection(a, b)
    else:
        EventHandler.trigger('DeleteConnection', None, {'value': value, 'parents': [a, b]})


class Metadata(MidPointHandle):
    def __init__(self, parent, center, data):
        self.data = data
        super().__init__(parent, center)
