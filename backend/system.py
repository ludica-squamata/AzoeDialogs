from frontend.globals import WIDTH, HEIGHT, NODOS_DIALOGO, NODOS_BEHAVIOUR
from .eventhandler import EventHandler
from pygame import Color, Rect
from random import randint


class System:
    data = {}
    lenght = 0
    number_of_dialog_nodes = 0
    number_of_behaviour_nodes = 0
    generated_colors = []

    type_mode = False
    area_nodos = Rect(0, 21, WIDTH // 5 * 4 + 25, HEIGHT // 5 * 4)
    MAIN_TB = None

    limit_input = True
    replacing_locutor = False

    program_mode = 'dialog'
    widget_group_key = NODOS_DIALOGO

    @classmethod
    def toggle_typemode(cls, typebox):
        cls.type_mode = not cls.type_mode
        EventHandler.trigger('ToggleTypeMode', 'System', {'instance': typebox, 'value': cls.type_mode})

    @classmethod
    def toggle_input_mode(cls):
        if cls.program_mode == 'dialog':
            cls.limit_input = not cls.limit_input

    @classmethod
    def toggle_program_mode(cls):
        if cls.program_mode == 'dialog':
            cls.program_mode = 'behaviour'
            cls.limit_input = False
            cls.widget_group_key = NODOS_BEHAVIOUR

        elif cls.program_mode == 'behaviour':
            cls.program_mode = 'dialog'
            cls.widget_group_key = NODOS_DIALOGO

    @classmethod
    def set_program_mode(cls, mode):
        if mode == 'dialog':
            cls.program_mode = 'dialog'
            cls.widget_group_key = NODOS_DIALOGO

        elif mode == 'behaviour':
            cls.program_mode = 'behaviour'
            cls.limit_input = False
            cls.widget_group_key = NODOS_BEHAVIOUR

    @classmethod
    def get_lenght(cls):
        return len(cls.data) - cls.number_of_dialog_nodes

    @classmethod
    def get_extra(cls):
        return cls.number_of_dialog_nodes - len(cls.data)

    @classmethod
    def load_file_data(cls, data, mode):
        cls.data = data
        cls.lenght = len(cls.data)
        cls.set_program_mode(mode)
        EventHandler.trigger('F4ToggleMode', 'ENGINE', {'mode': cls.program_mode})

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
    def replace_locutor(cls, old_color):
        name = cls.generate_color()
        cls.generated_colors[old_color.idx] = name
        cls.replacing_locutor = True
        EventHandler.trigger('NewLocutor', 'System', {'idx': old_color.idx, 'name': name,
                                                      'replace': True, 'old_color': old_color})

    @classmethod
    def modify_data(cls, data):
        idx = data['idx']
        text = data['text']
        cls.data[idx] = text


EventHandler.register(lambda o: System.modify_data(o.data), 'WriteNode')
