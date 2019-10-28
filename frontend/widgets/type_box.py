from pygame import K_0, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, KMOD_SHIFT,  KMOD_CAPS
from frontend.globals import WidgetHandler, Renderer, COLOR_BOX, COLOR_TEXT, WIDTH, HEIGHT
from pygame import Surface, key, font  # , draw, Rect
from backend.textrect import render_textrect
from backend import EventHandler  # , System
from .basewidget import BaseWidget


class TypeBox(BaseWidget):
    numerable = False
    selectable = False
    lenght = 0
    ticks = 0

    def __init__(self):
        super().__init__()
        self.image = Surface((WIDTH, HEIGHT // 5))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))
        self.x, self.y, self.w, self.h = self.rect
        self.f = font.SysFont('Courier New', 16)
        self.altura_del_texto = self.f.get_height()

        self.input = []

        EventHandler.register(self.typed, 'Key')
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    def on_mousedown(self, event):
        pass

    def on_mousemotion(self, event):
        pass

    def typed(self, event):
        tecla = event.data['key']
        mods = event.data['mod']
        shift = mods & KMOD_SHIFT or mods & KMOD_CAPS
        name = key.name(tecla).strip('[]')
        print(name)
        # self.activate()
        if name == 'space':
            self.input_character(' ')
        elif name == 'backspace':
            self.del_character()
        elif name in ['enter', 'return']:
            self.input_character('\n')
        elif name.isdecimal():
            if shift:
                if tecla == K_0:
                    name = '='
                elif tecla == K_2:
                    name = '"'
                elif tecla == K_3:
                    name = '#'
                elif tecla == K_4:
                    name = '$'
                elif tecla == K_5:
                    name = '%'
                elif tecla == K_6:
                    name = '&'
                elif tecla == K_7:
                    name = '•'
                elif tecla == K_8:
                    name = '('
                elif tecla == K_9:
                    name = ')'
            self.input_character(name)
        elif name.isalpha and len(name) == 1:
            if shift:
                if name == '.':
                    name = ':'
                if name == ',':
                    name = ';'
                name = name.upper()
            self.input_character(name)

    def input_character(self, char):
        self.input.append(char)
        self.lenght += 1

    def del_character(self):
        if self.lenght > 0:
            del self.input[-1]
            self.lenght -= 1

    def update(self):
        self.ticks += 1
        self.image.fill(COLOR_BOX, (1, 1, self.w - 2, self.h - 2))

        t = ''.join(self.input)
        # rr = Rect((self.x, self.y), self.f.size(t))

        render = render_textrect(t, self.f, self.rect, COLOR_TEXT, COLOR_BOX)
        self.image.blit(render, (1, 1))

        # if 10 < self.ticks < 30 and System.type_mode:
        #     draw.aaline(self.image, COLOR_TEXT, (rr.w + 2, 3), (rr.w + 2, rr.h - 3))
        # elif self.ticks > 40:
        #     self.ticks = 0


EventHandler.register(lambda e: TypeBox(), 'Init')
