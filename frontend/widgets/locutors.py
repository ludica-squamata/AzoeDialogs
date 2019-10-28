from frontend.globals import WidgetHandler, Renderer, COLOR_BOX, COLOR_TEXT, COLOR_UNSELECTED, COLOR_SELECTED
from backend import EventHandler, System
from .basewidget import BaseWidget
from pygame import font, Surface, Color, draw
from pygame.sprite import Group


class LocutorsPanel(BaseWidget):
    numerable = False
    selectable = False

    def __init__(self):
        super().__init__()
        self.fa = font.SysFont('Verdana', 15)
        self.fb = font.SysFont('Verdana', 12)
        self.fa.set_underline(1)

        self.image = Surface((Renderer.width // 5-25, (Renderer.height // 5) * 2-10))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(topright=(Renderer.width, 0))

        render = self.fa.render('Locutores', 1, COLOR_TEXT, COLOR_BOX)
        renderect = render.get_rect(centerx=self.rect.width // 2)
        self.image.blit(render, renderect)

        Renderer.add_widget(self)
        EventHandler.register(self.add_locutor, 'NewLocutor')

    def add_locutor(self, event):
        idx = event.data.get('idx')
        render = self.fb.render('#' + str(idx) + ': ', 1, COLOR_TEXT, COLOR_BOX)
        r = self.image.blit(render, (4+idx//10*46, 20 + (idx % 10) * 16))
        a = LocImage(self, Color('0x' + event.data.get('name')), r.right + 2, r.y + 2, idx)
        if event.data['replace']:
            a.select()


class LocImage(BaseWidget):
    numerable = False
    order = 'a'

    def __init__(self, parent, color, dx, dy, idx):
        super().__init__(parent)
        self.image = Surface((14, 14))
        self.image.fill(color)
        self.idx = idx
        self.color = color
        self.rect = self.image.get_rect(topleft=(parent.rect.x + dx, parent.rect.y + dy))
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    def select(self):
        super().select()
        a = self.color
        if (0.2126 * a.r + 0.7152 * a.g + 0.0722 * a.b) < 50:
            color_b = COLOR_SELECTED
        else:
            color_b = COLOR_UNSELECTED
        draw.rect(self.image, color_b, (0, 0, 14, 14), 1)

    def deselect(self):
        super().deselect()
        self.image.fill(self.color)

    def on_mousemotion(self, event):
        pass

    def kill(self):
        WidgetHandler.del_widget(self)
        Renderer.del_widget(self)
        super().kill()
        System.replace_locutor(self.idx)

    def update(self):
        self.deselect()
        for g in self.groups():
            if isinstance(g, Group):  # a very clunky way of saying "it's selected"
                self.select()

    def __repr__(self):
        return 'LocImage #'+str(self.idx)


EventHandler.register(lambda e: LocutorsPanel(), 'Init')
