from frontend.globals import WidgetHandler, Renderer, COLOR_BOX, COLOR_TEXT, WIDTH, HEIGHT
from pygame import K_0, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, KMOD_SHIFT, KMOD_CAPS
from pygame import Surface, key, font, draw
from .basewidget import BaseWidget
from backend import EventHandler


class TypeBox(BaseWidget):
    selectable = False
    ticks = 0

    char_x = 0
    char_y = 0

    def __init__(self):
        super().__init__()
        self.image = Surface((WIDTH, HEIGHT // 5))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))
        self.x, self.y, self.w, self.h = self.rect
        self.char_y = self.y
        self.f = font.SysFont('Courier New', 16)
        self.altura_del_texto = self.f.get_height()

        self.input = []
        self.cursor = Cursor(self)
        self.cursor.place(self.char_x+1, self.char_y)

        EventHandler.register(self.typed, 'Key')
        EventHandler.register(self.switch, 'ToggleTypeMode')

    @property
    def lenght(self):
        return len(self.input)

    def switch(self, event):
        if event.data['value'] is True:
            WidgetHandler.add_widget(self)
            Renderer.add_widget(self)
        else:
            WidgetHandler.del_widget(self)
            Renderer.del_widget(self)

    def on_mousedown(self, event):
        pass

    def on_mousemotion(self, event):
        pass

    def typed(self, event):
        tecla = event.data['key']
        mods = event.data['mod']
        shift = mods & KMOD_SHIFT or mods & KMOD_CAPS
        name = key.name(tecla).strip('[]')
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

    def input_character(self, letra):
        if letra == '\n':
            self.char_y += 17
            self.char_x = self.x
            self.cursor.place(self.char_x + 1, self.char_y)
            char = None
        elif letra == ' ':
            char = Space(self, self.lenght, self.altura_del_texto, COLOR_BOX)
        else:
            char = Character(self, self.lenght, letra, self.f, COLOR_TEXT)
            if self.char_x + char.w > self.w:
                self.char_y += char.h
                self.char_x = 0

        if char is not None:
            char.place(self.char_x, self.char_y)
            self.char_x += char.w
            self.cursor.place(self.char_x+1, self.char_y)
            self.input.append(char)

    def del_character(self):
        if self.lenght > 0:
            char = self.input[-1]
            self.char_x -= char.w
            if self.char_x < 0:
                self.char_y = char.y
                self.char_x = char.x
            char.remove()
            self.cursor.place(self.char_x+1, self.char_y)
            self.input.remove(char)

    def update(self):
        self.image.fill(COLOR_BOX)


EventHandler.register(lambda e: TypeBox(), 'Init')


class Character(BaseWidget):
    selectable = False

    def __init__(self, parent, idx, char, fuente, color_f):
        super().__init__(parent)
        self.fuente = fuente
        self.image = self.fuente.render(char, 1, color_f)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect
        self.idx = idx

        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def place(self, x, y):
        self.x, self.y = x, y
        self.rect.move_ip(x, y)

    def remove(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)


class Space(BaseWidget):
    def __init__(self, parent, idx, h, color):
        super().__init__(parent)
        self.image = Surface((10, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect

        self.idx = idx
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def place(self, x, y):
        self.x, self.y = x, y
        self.rect.move_ip(x, y)

    def remove(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)


class Cursor(BaseWidget):
    ticks = True
    selectable = False

    def __init__(self, parent):
        super().__init__(parent)
        self.image = Surface([3, 19])
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect
        draw.aaline(self.image, COLOR_TEXT, [1, 0], [1, self.h])
        EventHandler.register(self.switch, 'ToggleTypeMode')

    def place(self, x, y):
        self.rect.topleft = x, y
        self.x, self.y = x, y

    def switch(self, event):
        if event.data['value'] is True:
            WidgetHandler.add_widget(self)
            Renderer.add_widget(self)
        else:
            WidgetHandler.del_widget(self)
            Renderer.del_widget(self)

    def update(self):
        self.ticks = not self.ticks
        if not self.ticks:
            Renderer.del_widget(self)
        else:
            Renderer.add_widget(self)
