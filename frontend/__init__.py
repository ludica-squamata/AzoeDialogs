from .node import Square, Diamond
from backend.eventhandler import EventHandler


def widget_creator(event):
    size = event.data.get('size')
    pos = event.data.get('pos')
    if event.tipo == 'AddDiamond':
        Diamond(size, *pos)
    elif event.tipo == 'AddSquare':
        Square(size, *pos)


# noinspection PyTypeChecker
EventHandler.register(widget_creator, 'AddDiamond', 'AddSquare')
