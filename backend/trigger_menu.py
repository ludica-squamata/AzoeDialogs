from .eventhandler import EventHandler
from .system import System
from pygame import K_s, K_d, K_f
from pygame import mouse


class TriggerMenu:
    name = 'TriggerMenu'

    @classmethod
    def trigger(cls, key):
        value = False
        x, y = mouse.get_pos()
        if key == K_s and System.get_lenght() > 0:
            EventHandler.trigger('AddSquare', cls.name, {'pos': [x, y]})
            value = True
        elif key == K_d and System.get_lenght() > 0:
            EventHandler.trigger('AddDiamond', cls.name, {'pos': [x, y]})
            value = True
        elif key == K_f and System.get_lenght() > 0:
            EventHandler.trigger('AddCircle', cls.name, {'pos': [x, y]})
            value = True

        return value
