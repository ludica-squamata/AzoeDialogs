from frontend.globals import WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED, NODOS_DIALOGO, NODOS_BEHAVIOUR
from pygame import Surface, font, transform, draw, Color, SRCALPHA
from backend.eventhandler import EventHandler
from .connection import toggle_connection
from .basewidget import BaseWidget
from backend.system import System


class Node(BaseWidget):
    idx = 0
    order = 'b'
    type_overriden = False
    _tipo = 'node'
    tamanio = 16

    locutor_name = ''
    named = False
    color_base = COLOR_UNSELECTED
    color_font = COLOR_SELECTED
    color_box = COLOR_SELECTED

    interlocutor = None
    numerable = True
    selectable = True
    editable = True

    id_overritten = False

    parent_node = None
    vertical_position = 0

    x, y = 0, 0

    node_reqs = None
    node_leads = None

    def __init__(self, data):
        super().__init__()
        self.connections = []
        self.fuente = font.SysFont('Verdana', 10)
        self.group = System.widget_group_key
        self.tipo = data['text'] if data.get('text', None) is not None else 'leaf'
        WidgetHandler.add_widget(self, layer=System.widget_group_key)
        Renderer.add_widget(self, layer=System.widget_group_key)
        if 'text' in data:
            self.text = data['text']
        elif 'data' in data and 'text' in data['data']:
            self.text = data['data']['txt']
        elif 'data' in data and 'txt' in data['data']:
            self.text = data['data']['txt']

        if 'idx' in data:
            self.idx = data['idx']
            self.id_overritten = True
            self.real_idx = data['idx']

        if 'data' in data and 'from' in data['data']:
            self.locutor_name = (data['data']['from'])
            self.named = True

        if 'data' in data and 'reqs' in data['data']:
            self.node_reqs = data['data']['reqs']

        if 'data' in data and 'leads' in data['data']:
            leads = data['data']['leads']
            self.node_leads = leads

        self.img_sel = self.create(True)
        self.img_uns = self.create()
        self.image = self.img_uns
        if data['color'] is not None:
            self.colorize(data['color'])
            self.img_sel = self.create(True)
            self.img_uns = self.create()
            self.image = self.img_uns
        self.rect = self.image.get_rect(center=data['pos'])
        self.x, self.y = self.rect.center
        EventHandler.register(self.toggle_selection, 'select', 'deselect')
        EventHandler.register(self.recolorize, 'NewLocutor')

    def connect(self, other):
        to_conect = None
        if other not in self.connections:
            self.connections.append(other)
            to_conect = other
            self.interlocutor = other

        if len(self.connections) > 1:
            for child in self.connections:
                child.type_overriden = True
                child.tipo = 'branch'

        for child in self.connections:
            child.interlocutor = self
            child.parent_node = self

        if to_conect is not None:
            toggle_connection(self, to_conect)

    def disconnect(self, other):
        if other in self.connections:
            toggle_connection(self, other, value=False)
            self.connections.remove(other)

    def get_idx(self):
        if not self.id_overritten:
            g = System.widget_group_key
            sprites = WidgetHandler.widgets.get_widgets_from_layer(g)
            numerables = [w for w in sprites if w.numerable]
            if self in numerables:
                return numerables.index(self)

        return self.idx

    def colorize(self, color_namer):
        a = color_namer.color if hasattr(color_namer, 'color') else color_namer

        if not self.named:
            self.locutor_name = color_namer.name if hasattr(color_namer, 'name') else '%02x%02x%02x' % (a.r, a.g, a.b)
            self.named = True if hasattr(color_namer, 'name') else False

        self.color_base = a
        if (0.2126 * a.r + 0.7152 * a.g + 0.0722 * a.b) < 50:
            color_b = COLOR_SELECTED
        else:
            color_b = COLOR_UNSELECTED
        self.color_font = color_b
        self.color_box = color_b

    def recolorize(self, event):
        old_color = event.data.get('old_color', None)
        idx = event.data['idx']
        if old_color is not None:
            if old_color.color == self.color_base:
                new_color = System.generated_colors[idx]
                self.colorize(Color('0x' + new_color))

    def name_locutor(self, new_name, color=None):
        if color is not None:
            self.colorize(color)
        self.locutor_name = new_name
        self.named = True

    def create(self, selected=False):
        self.idx = self.get_idx()
        size = self.size
        image = Surface((size, size), SRCALPHA)
        image.fill(self.color_base)
        image = transform.rotate(image, 45)
        rect = image.get_rect()
        render_uns = self.fuente.render(str(self.idx), 1, self.color_font, self.color_base)
        render_uns_rect = render_uns.get_rect(center=rect.center)
        image.blit(render_uns, render_uns_rect)

        r = image.get_rect()
        left = r.midleft
        right = r.midright
        top = r.midtop
        bottom = r.midbottom

        if selected is True:
            draw.polygon(image, self.color_font, [right, bottom, left, top], 3)

        return image

    @property
    def size(self):
        len_idx = len(str(self.get_idx()))
        if len_idx == 1:
            return 16
        if len_idx == 2:
            return 17
        elif len_idx == 3:
            return 22
        else:
            raise ValueError("Do you really need more that 999 nodes?")

    def update(self, *args):
        idx = self.get_idx()
        if idx != self.idx:
            self.idx = idx
            self.img_uns = self.create()
            self.img_sel = self.create(True)
            if self.is_selected:
                self.image = self.img_sel
            else:
                self.image = self.img_uns

        self.rect = self.image.get_rect(center=self.rect.center)
        self.x, self.y = self.rect.center

    def __repr__(self):
        return self.tipo + ' #' + str(self.idx)

    def __int__(self):
        return self.idx

    def __lt__(self, other):
        return self.idx < other.idx

    def __str__(self):
        return str(self.idx)

    def kill(self):
        WidgetHandler.del_widget(self)
        Renderer.del_widget(self)
        super().kill()

    @property
    def tipo(self):
        tipo = self._tipo
        if not self.type_overriden:
            tipo = 'node'
        if not len(self.connections):
            tipo = 'leaf'
        return tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def lead(self):
        lenght = len(self.connections)
        if lenght > 1:
            return [int(i) for i in self.connections]
        elif lenght == 1:
            return int(self.connections[0])

    def select(self):
        super().select()
        self.image = self.img_sel

    def deselect(self):
        super().deselect()
        self.image = self.img_uns

    def toggle(self, event):
        if event.data['mode'] == 'dialog':
            if self.group == NODOS_DIALOGO:
                self.show()
            else:
                self.hide()

        elif event.data['mode'] == 'behaviour':
            if self.group == NODOS_BEHAVIOUR:
                self.show()
            else:
                self.hide()

    def count_parents(self, count=0):
        if self.parent_node is not None:
            count += 1
            count = self.parent_node.count_parents(count)
            self.vertical_position = count

        return count


EventHandler.register(lambda e: Node(e.data), 'AddNode')
