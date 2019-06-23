from .util import abrir_json


class System:
    data = abrir_json('data/input.json')
    lenght = len(data)
    number_of_nodes = 0

    @classmethod
    def get_lenght(cls):
        return len(cls.data)-cls.number_of_nodes

    @classmethod
    def load_data(cls):
        cls.data = abrir_json('data/input.json')
        cls.lenght = len(cls.data)
