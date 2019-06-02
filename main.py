from pygame import init as py_init
from frontend.globals.widgethandler import WidgetHandler
from frontend.globals.renderer import Renderer
from backend.eventhandler import EventHandler

py_init()
Renderer.init(640, 480)

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
