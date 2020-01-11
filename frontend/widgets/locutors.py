from frontend.globals import COLOR_BOX, COLOR_TEXT, COLOR_UNSELECTED, COLOR_SELECTED, WIDTH, HEIGHT
from frontend.globals import WidgetHandler, Renderer
from backend import EventHandler, System, render_textrect
from .basewidget import BaseWidget
from pygame import font, Surface, Color, draw, Rect
from pygame.sprite import Group


class LocutorsPanel(BaseWidget):

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

        render = self.fa.render('Locutores', 1, COLOR_TEXT, COLOR_BOX)
        renderect = render.get_rect(centerx=self.rect.width // 2)
        self.image.blit(render, renderect)

        t = 'Presione F2 para crear un nuevo locutor.'
        exp = render_textrect(t, self.fb, self.rect, COLOR_TEXT, COLOR_BOX, 1)
        rendexp = exp.get_rect(centerx=self.rect.width // 2, top=30)
        self.image.blit(exp, rendexp)
        self.empty = True

        Renderer.add_widget(self)
        EventHandler.register(self.add_locutor, 'NewLocutor')

    def add_locutor(self, event):
        if self.empty:
            self.image.fill(COLOR_BOX, self.clear_area)
            self.empty = False

        idx = event.data.get('idx')
        render = self.fb.render('#' + str(idx) + ': ', 1, COLOR_TEXT, COLOR_BOX)
        r = self.image.blit(render, (4 + idx // 10 * 46, 20 + (idx % 10) * 16))
        name = event.data.get('name')
        a = LocImage(self, name, Color('0x' + name), r.right + 2, r.y + 2, idx)
        if event.data['replace']:
            a.select()


class LocImage(BaseWidget):
    numerable = False
    selectable = True
    order = 'a'

    def __init__(self, parent, name, color, dx, dy, idx):
        super().__init__(parent)
        self.image = Surface((14, 14))
        self.image.fill(color)
        self.idx = idx
        self.color = color
        self.name = name
        self.spr_name = LocName(self)
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
        self.spr_name.show()

    def deselect(self):
        super().deselect()
        self.image.fill(self.color)
        self.spr_name.hide()

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
        return 'LocImage #' + str(self.idx)


EventHandler.register(lambda e: LocutorsPanel(), 'Init')


class LocName(BaseWidget):
    selectable = True

    def __init__(self, parent):
        super().__init__(parent)
        self.name = self.parent.name
        grandparent = self.parent.parent.rect
        self.f = font.SysFont('Verdana', 14)
        self.rect = r = Rect(grandparent.x, grandparent.bottom + 1, grandparent.w, 21)
        self.img_uns = render_textrect(self.name, self.f, r, COLOR_TEXT, COLOR_BOX, 1)
        self.img_sel = render_textrect(self.name, self.f, r, COLOR_SELECTED, COLOR_BOX, 1)
        self.image = self.img_uns
        # WidgetHandler.add_widget(self)

    def show(self):
        Renderer.add_widget(self)

    def hide(self):
        Renderer.del_widget(self)

    # def select(self):
    #     super().select()
    #     self.image = self.img_sel
    #
    # def deselect(self):
    #     super().deselect()
    #     self.image = self.img_uns
    #
    # def on_mousedown(self, event):
    #     self.select()
