from frontend.globals import WidgetHandler, Renderer, COLOR_BOX, COLOR_TEXT, WIDTH, HEIGHT
from pygame import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, KMOD_SHIFT, KMOD_CAPS
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_KP_ENTER
from pygame import Surface, key, font, draw
from backend import EventHandler, System
from .basewidget import BaseWidget


class TypeBox(BaseWidget):
    ticks = 0

    cursor_pos = -1

    acento = False
    written = False
    name = ''

    line_lenght = 0
    current_line = 0
    line_lenghts = None
    draggable = False
    cursor_at_left = True
    selectable = True

    def __init__(self, parent, x, y, w, h, size, name):
        super().__init__(parent)
        self.image = Surface((w, h))
        self.image.fill(COLOR_BOX)
        self.name = name
        if self.name == 'MainTB':
            System.MAIN_TB = self
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.x, self.y, self.w, self.h = self.rect
        self.right = self.rect.right
        self.left = self.rect.left
        self.char_x = self.x
        self.char_y = self.y
        self.f = font.SysFont('Courier New', size)
        self.altura_del_texto = self.f.get_height()

        self.line_lenghts = []
        self.lines = [[]]
        self.cursor = Cursor(self)
        self.cursor.place(self.char_x + 1, self.char_y)

        EventHandler.register(self.switch, 'ToggleTypeMode')

    def switch(self, event):
        instance = System.MAIN_TB if event.data['instance'] == 'MainTB' else event.data['instance']
        if instance is self:
            if event.data['value'] is True:
                WidgetHandler.add_widget(self)
                Renderer.add_widget(self)
                EventHandler.register(self.filter, 'Key')
                self.cursor.switch(True)
            else:
                self.return_text()
                self.clear()
                WidgetHandler.del_widget(self)
                Renderer.del_widget(self)
                EventHandler.deregister(self.filter, 'Key')
                self.cursor.switch(False)

    def return_text(self):
        s = [o for o in WidgetHandler.selected.sprites() if o.numerable]
        if len(s) == 1 and any([len(line) for line in self.lines]):
            idx = s[0].idx
            text = '\n'.join([''.join(line) for line in self.lines])
            EventHandler.trigger('WriteNode', self, {'idx': idx, 'text': text})
            self.clear()

    def on_mousedown(self, event):
        pos = event.pos
        flat_list = [item for sublist in self.lines for item in sublist]
        for char in flat_list:
            if char.rect.collidepoint(pos):
                self.char_y = char.rect.y
                self.char_x = char.rect.left
                self.cursor_pos = self.lines[char.line].index(char)-1
                self.cursor.place(self.char_x - 1, self.char_y)

    def filter(self, event):
        tecla = event.data['key']
        if tecla == K_UP:
            if self.current_line - 1 >= 0:
                self.char_y -= 17
                self.current_line -= 1
                self.cursor.place(self.char_x - 1, self.char_y)

        elif tecla == K_DOWN:
            if self.current_line + 1 < len(self.lines):
                self.char_y += 17
                self.current_line += 1
                self.cursor.place(self.char_x - 1, self.char_y)

        elif tecla == K_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1

            elif self.current_line - 1 >= 0:
                self.current_line -= 1
                self.char_y -= 17
                self.cursor_pos = len(self.lines[self.current_line]) - 1
            else:
                self.cursor_at_left = False

            char = self.lines[self.current_line][self.cursor_pos]
            if self.cursor_at_left:
                self.char_x = char.rect.right
            else:
                self.char_x = char.rect.left

            self.cursor.place(self.char_x - 1, self.char_y)

        elif tecla == K_RIGHT:
            if self.cursor_pos + 1 < len(self.lines[self.current_line]):
                self.cursor_pos += 1
            elif self.current_line + 1 < len(self.lines):
                self.cursor_pos = 0
                self.char_x = 0
                self.char_y += 17
                self.current_line += 1
            else:
                self.cursor_at_left = True

            char = self.lines[self.current_line][self.cursor_pos]
            if not self.cursor_at_left:
                self.char_x = char.rect.left
            else:
                self.char_x = char.rect.right
            self.cursor.place(self.char_x - 1, self.char_y)

        elif tecla in (K_RETURN, K_KP_ENTER):
            if self.name == 'MainTB':
                self.typed(event)
            else:
                text = ''.join([i.char for i in self.lines[self.current_line]])
                self.parent.update_text(text)
        else:
            self.typed(event)

    def typed(self, event):
        tecla = event.data['key']
        mods = event.data['mod']
        shift = mods & KMOD_SHIFT or mods & KMOD_CAPS
        raw = key.name(tecla).strip('[]')
        name = None
        if raw == 'space':
            name = ' '
        elif raw == 'backspace':
            self.del_character()
        elif raw in ['enter', 'return']:
            name = '\n'
        elif raw.isdecimal():
            if tecla == K_0:
                name = '=' if shift else raw
            elif tecla == K_1:
                name = '!' if shift else raw
            elif tecla == K_2:
                name = '"' if shift else raw
            elif tecla == K_3:
                name = '#' if shift else raw
            elif tecla == K_4:
                name = '$' if shift else raw
            elif tecla == K_5:
                name = '%' if shift else raw
            elif tecla == K_6:
                name = '&' if shift else raw
            elif tecla == K_7:
                name = '•' if shift else raw
            elif tecla == K_8:
                name = '(' if shift else raw
            elif tecla == K_9:
                name = ')' if shift else raw
        elif raw.isalpha and len(raw) == 1:
            if raw == '.':
                name = ':' if shift else raw
            elif raw == ',':
                name = ';' if shift else raw
            elif raw == "´":
                self.acento = True
            elif raw == "'":
                name = "?" if shift else "'"
            elif raw == '¡':
                name = '¿' if shift else '¡'
            else:
                name = raw.upper() if shift else raw

            if self.acento:
                vowels = 'aeiou'
                accented_v = 'áéíóú'
                if raw in vowels:
                    name = accented_v[vowels.index(raw)]
                    name = name.upper() if shift else name

        if name is not None:
            self.acento = False
            self.input_character(name)

    def input_character(self, letra):
        if letra == '\n':
            self.char_y += 17
            self.char_x = self.x
            self.cursor.place(self.char_x - 1, self.char_y)
            char = None
            self.line_lenght = 0
            self.cursor_pos = 0
            self.current_line += 1
            self.lines.append([])

        elif letra == ' ':
            char = Space(self, self.line_lenght, self.altura_del_texto, COLOR_BOX)
        else:
            char = Character(self, self.line_lenght, letra, self.f, COLOR_TEXT)
            if self.char_x + char.w > self.right:
                self.char_y += char.h
                self.char_x = self.left  # 0

        if char is not None:
            char.place(self.char_x, self.char_y, self.current_line)
            self.char_x += char.w
            self.cursor.place(self.char_x - 1, self.char_y)
            self.lines[self.current_line].append(char)
            self.cursor_pos += 1

    def del_character(self):
        if self.line_lenght > 0:
            char = self.lines[self.current_line][-1]
            self.char_x -= char.w
            if self.char_x < 0:
                self.char_y = char.y
                self.char_x = char.x
            char.remove()
            self.cursor.place(self.char_x + 1, self.char_y)
            self.lines[self.current_line].remove(char)
            self.cursor_pos -= 1
            self.line_lenght -= 1

    def clear(self):
        flat_list = [item for sublist in self.lines for item in sublist]
        for widget in flat_list:
            widget.kill()
        self.lines = [[]]
        self.char_x = self.x
        self.char_y = self.y
        self.cursor.kill()
        self.written = False
        self.line_lenght = 0

    @staticmethod
    def get_selected():
        s = [o for o in WidgetHandler.selected.widgets() if o.editable]
        text = ''
        if len(s) > 0 and hasattr(s[0], 'idx'):
            idx = s[0].idx
            if 0 <= idx < len(System.data):
                text = System.data[idx]
        elif len(s) > 0 and hasattr(s[0], 'name'):
            text = s[0].name

        return text

    def update(self):
        self.image.fill(COLOR_BOX)
        text = self.get_selected()
        if text and not self.written:
            for char in text:
                self.input_character(char)
            self.written = True

    def __repr__(self):
        return 'TypeBox ' + self.name


EventHandler.register(lambda e: TypeBox('System', 0, HEIGHT, WIDTH, HEIGHT // 5, 16, 'MainTB'), 'Init')


class Character(BaseWidget):
    line = None

    def __init__(self, parent, idx, char, fuente, color_f):
        super().__init__(parent)
        self.fuente = fuente
        self.char = char
        self.image = self.fuente.render(char, 1, color_f)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect
        self.idx = idx

        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def place(self, x, y, line):
        self.x, self.y = x, y
        self.rect.move_ip(x, y)
        self.line = line

    def remove(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def __repr__(self):
        return self.char


class Space(BaseWidget):
    char = ' '
    line = None

    def __init__(self, parent, idx, h, color):
        super().__init__(parent)
        self.image = Surface((10, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect

        self.idx = idx
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def place(self, x, y, line):
        self.x, self.y = x, y
        self.rect.move_ip(x, y)
        self.line = line

    def remove(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def __repr__(self):
        return 'space'


class Cursor(BaseWidget):
    ticks = True

    def __init__(self, parent):
        super().__init__(parent)
        self.image = Surface([3, 19])
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect()
        self.x, self.y, self.w, self.h = self.rect
        draw.aaline(self.image, COLOR_TEXT, [1, 0], [1, self.h])

    def place(self, x, y):
        self.rect.topleft = x, y
        self.x, self.y = x, y

    def switch(self, value):
        if value:
            WidgetHandler.add_widget(self)
            Renderer.add_widget(self)
        else:
            WidgetHandler.del_widget(self)
            Renderer.del_widget(self)

    def kill(self):
        super().kill()
        self.place(self.parent.x, self.parent.y)

    def update(self):
        self.ticks = not self.ticks
        if not self.ticks:
            Renderer.del_widget(self)
        else:
            Renderer.add_widget(self)
