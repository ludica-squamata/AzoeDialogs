from .eventhandler import EventHandler
from pygame import K_s, K_d
from pygame import mouse


class TriggerMenu:
    name = 'TriggerMenu'

    @classmethod
    def trigger(cls, key):
        value = False
        x, y = mouse.get_pos()
        if key == K_s:
            EventHandler.trigger('AddSquare', cls.name, {'pos': [x, y]})
            value = True
        elif key == K_d:
            EventHandler.trigger('AddDiamond', cls.name, {'pos': [x, y]})
            value = True

        return value
