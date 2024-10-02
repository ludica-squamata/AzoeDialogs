from frontend.globals import COLOR_CONNECTION, WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED, WIDTH, HEIGHT
from pygame import Surface, SRCALPHA, draw, BLEND_MAX, BLEND_MIN
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from bisect import bisect_left


class Connection(BaseWidget):
    handles = None

    centers = None

    def __init__(self, parent_a, parent_b):
        super().__init__()
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.handles = [self.parent_a, self.parent_b]
        self.centers = [self.parent_a.rect.center, self.parent_b.rect.center]
        self.image = self.create()
        self.rect = self.image.get_rect()
        self.layer = min([self.parent_a.layer, self.parent_b.layer]) - 1
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

        EventHandler.register(self.event_handle, 'AddMidPoint')
        EventHandler.register(self.delete, 'DeleteConnection')

    def event_handle(self, event):
        base = event.data['base']
        other = event.data['other']
        if all([handle in self.handles for handle in [base, other]]):
            base = self.handles.index(event.data['base'])
            other = self.handles.index(event.data['other'])
            if base + 1 == other or other + 1 == base:
                ra = self.handles[base]
                rb = self.handles[other]
                self.add_handle(ra, rb)

    def add_handle(self, ra, rb):
        center = (ra.x + rb.x) // 2, (ra.y + rb.y) // 2  # previously callend "pc", this is the center point
        # relative to both ends.
        _temp = [h.x for h in self.handles]  # a temporal list of all the exes of each point.
        p = bisect_left(_temp, center[0])  # bisect_left() places the new index in the correct position

        self.centers.insert(p, center)
        self.handles.insert(p, Metadata(self, center))

    def create(self):
        image = Surface((WIDTH, HEIGHT), SRCALPHA)
        differences = [abs(self.parent_a.rect.centerx - self.parent_b.rect.centerx),
                       abs(self.parent_a.rect.centery - self.parent_b.rect.centery)]

        if differences[0] > differences[1]:  # X-differnece, Y-difference; which is the most significant?
            if self.parent_a.rect.centerx < self.parent_b.rect.centerx:
                side_a = self.parent_a.rect.midright
                side_b = self.parent_b.rect.midleft
            else:
                side_a = self.parent_a.rect.midleft
                side_b = self.parent_b.rect.midright
        else:
            if self.parent_a.rect.centery < self.parent_b.rect.centery:
                side_a = self.parent_a.rect.midbottom
                side_b = self.parent_b.rect.midtop
            else:
                side_a = self.parent_a.rect.midtop
                side_b = self.parent_b.rect.midbottom

        if len(self.centers) > 2:
            _centers = self.centers[1:-1]  # this use of self.centers excludes both side_a and side_b
            draw.aalines(image, COLOR_CONNECTION, 0, [side_a, *_centers, side_b])
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

    def on_mousemotion(self, event):
        # now the movement is explicit.
        indice = self.parent.centers.index(self.rect.center)
        super().on_mousemotion(event)  # here's where the movement happens.
        self.x, self.y = self.rect.center
        self.parent.centers[indice] = self.rect.center

    @property
    def idx(self):
        return self.parent.centers.index(self.rect.center)

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
    def __init__(self, parent, idx):
        super().__init__(parent, idx)
