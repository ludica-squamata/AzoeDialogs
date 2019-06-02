from frontend.widgets.node import Square, Diamond
from backend.eventhandler import EventHandler
from frontend.widgets.selection import Selection


def widget_creator(event):
    size = event.data.get('size')
    pos = event.data.get('pos')
    if event.tipo == 'AddDiamond':
        Diamond(size, *pos)
    elif event.tipo == 'AddSquare':
        Square(size, *pos)
    elif event.tipo == 'Selection':
        if 'pos' in event.data:
            Selection(event)


# noinspection PyTypeChecker
EventHandler.register(widget_creator, 'AddDiamond', 'AddSquare', "Selection")
