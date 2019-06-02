
class System:
    MODE = 'Selection'

    @classmethod
    def toggle_mode(cls):
        if cls.MODE == 'Selection':
            cls.MODE = 'Connection'
        elif cls.MODE == 'Connection':
            cls.MODE = 'Selection'
