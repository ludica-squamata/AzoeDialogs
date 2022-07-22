from frontend.globals import COLOR_BOX, COLOR_TEXT, COLOR_SELECTED, node_colors
from backend import EventHandler, render_textrect
from backend.group import WidgetGroup
from .basewidget import BaseWidget
from pygame import font, Rect
from .sidebox import SideBox


class StructureNodes(SideBox):

    def __init__(self):
        super().__init__()

        self.properties = WidgetGroup()
        render = self.fa.render('Structure', 1, COLOR_TEXT, COLOR_BOX)
        renderect = render.get_rect(centerx=self.rect.width // 2)
        self.image.blit(render, renderect)

        standard = ['Sequence', 'Selector', 'Repeater', 'UntilFail', 'Inverter', 'Succeder']
        for i, name in enumerate(standard):
            y = self.rect.y + 21 + + i * 21
            n = StandardNode(self, name, y, node_colors[name])
            self.properties.add(n, layer=1)

        n = StandardNode(self, 'Leaf', self.rect.y + 25 + + (len(standard)) * 21, COLOR_BOX)
        self.properties.add(n, layer=1)
        EventHandler.register(self.toggle, 'F4ToggleMode')

    def deselect_all(self):
        for n in self.properties.widgets():
            n.deselect()

    def toggle(self, event):
        if event.data['mode'] == 'dialog':
            self.hide()
        elif event.data['mode'] == 'behaviour':
            self.show()

    def show(self):
        super().show()
        for node in self.properties.get_widgets_from_layer(1):
            node.show()

    def hide(self):
        super().hide()
        for node in self.properties.get_widgets_from_layer(1):
            node.hide()


EventHandler.register(lambda e: StructureNodes(), 'Init')


class StandardNode(BaseWidget):
    selectable = True
    editable = True
    draggable = False
    order = 'd'

    def __init__(self, parent, name, y, color):
        super().__init__(parent)
        self.name = name
        self.text = name
        if self.name != 'Leaf':
            bg = color
            self.color = color
        else:
            bg = COLOR_BOX
            self.color = COLOR_TEXT
        self.f = font.SysFont('Verdana', 13)
        self.rect = r = Rect(parent.rect.x, y, parent.rect.w, 21)
        self.img_uns = render_textrect(self.name, self.f, r.w, r.h, COLOR_TEXT, bg, 1)
        self.img_sel = render_textrect(self.name, self.f, r.w, r.h, COLOR_SELECTED, bg, 1)
        self.image = self.img_uns
        EventHandler.register(self.toggle_selection, 'select', 'deselect')

    def select(self):
        super().select()
        self.parent.deselect_all()
        self.image = self.img_sel

    def deselect(self):
        super().deselect()
        self.image = self.img_uns

    def __repr__(self):
        return f'Structural Node {self.name}'
