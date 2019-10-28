from frontend.globals import WIDTH, HEIGHT
from .eventhandler import EventHandler
from pygame import Color, Rect
from .util import abrir_json
from random import randint


class System:
    data = abrir_json('data/input.json')
    lenght = len(data)
    number_of_nodes = 0
    generated_colors = []

    type_mode = False
    area_nodos = Rect(0, 21, WIDTH // 5 * 4 + 25, HEIGHT // 5 * 4)

    @classmethod
    def toggle_typemode(cls):
        cls.type_mode = not cls.type_mode

    @classmethod
    def get_lenght(cls):
        return len(cls.data) - cls.number_of_nodes

    @classmethod
    def load_data(cls):
        cls.data = abrir_json('data/input.json')
        cls.lenght = len(cls.data)

    @classmethod
    def generate_color(cls):
        h = randint(0, 360)
        a = Color('white')
        a.hsla = h, 100, 50, 100
        return '%02x%02x%02x' % (a.r, a.g, a.b)

    @classmethod
    def new_locutor(cls):
        name = cls.generate_color()
        cls.generated_colors.append(name)
        idx = cls.generated_colors.index(name)
        if idx < 20:
            EventHandler.trigger('NewLocutor', 'System', {'idx': idx, 'name': name, 'replace': False})

    @classmethod
    def replace_locutor(cls, idx):
        name = cls.generate_color()
        cls.generated_colors.insert(idx, name)
        EventHandler.trigger('NewLocutor', 'System', {'idx': idx, 'name': name, 'replace': True})
