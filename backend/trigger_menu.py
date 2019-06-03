from .eventhandler import EventHandler
from .system import System
from pygame import K_s, K_d, K_c
from pygame import mouse


class TriggerMenu:
    name = 'TriggerMenu'

    @classmethod
    def trigger(cls, key):
        x, y = mouse.get_pos()
        if key == K_s and System.MODE == 'Selection':
            EventHandler.trigger('AddSquare', cls.name, {'pos': [x, y]})
        elif key == K_d and System.MODE == 'Selection':
            EventHandler.trigger('AddDiamond', cls.name, {'pos': [x, y]})
        elif key == K_c:
            System.toggle_mode()
