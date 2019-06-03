from frontend.widgets.node import Square, Diamond
from backend.eventhandler import EventHandler
from frontend.widgets.selection import Selection
from frontend.globals.widgethandler import WidgetHandler


def widget_creator(event):
    pos = event.data.get('pos')
    if event.tipo == 'AddDiamond':
        Diamond(*pos)
    elif event.tipo == 'AddSquare':
        Square(*pos)
    elif event.tipo == 'Selection':
        if 'pos' in event.data:
            Selection(event)


# noinspection PyTypeChecker
EventHandler.register(widget_creator, 'AddDiamond', 'AddSquare', "Selection")
