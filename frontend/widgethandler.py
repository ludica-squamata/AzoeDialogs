from pygame import event, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, MOUSEWHEEL
from pygame import K_ESCAPE, K_s, K_d, mouse
from pygame.sprite import LayeredUpdates
from backend import salir, EventHandler


class WidgetHandler:
    widgets = LayeredUpdates()
    active_widget = None

    @classmethod
    def add_widgets(cls, *widget):
        cls.widgets.add(*widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)

    @classmethod
    def update(cls):
        events = event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, MOUSEWHEEL])
        event.clear()

        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                salir()

            elif e.type == KEYDOWN:
                x, y = mouse.get_pos()
                if cls.active_widget is not None:
                    cls.active_widget.on_keydown(e)
                elif e.key == K_s:
                    EventHandler.trigger('AddSquare', 'WidgetHandler', {'size': 16, 'pos': [x, y]})
                elif e.key == K_d:
                    EventHandler.trigger('AddDiamond', 'WidgetHandler', {'size': 16, 'pos': [x, y]})

            elif e.type == KEYUP:
                if cls.active_widget is not None:
                    cls.active_widget.on_keyup(e)

            elif e.type == MOUSEBUTTONDOWN:  # pos, button
                if e.button == 1:
                    for widget in cls.widgets:
                        widget.deselect()
                    widgets = cls.widgets.get_sprites_at(e.pos)
                    if len(widgets):
                        cls.active_widget = widgets[0]
                    else:
                        cls.active_widget = None

                if cls.active_widget is not None:
                    cls.active_widget.on_mousedown(e)

            elif e.type == MOUSEBUTTONUP:  # pos, button
                if cls.active_widget is not None:
                    cls.active_widget.on_mouseup(e)

            elif e.type == MOUSEMOTION:  # pos, rel, buttons
                if cls.active_widget is not None and cls.active_widget.rect.collidepoint(e.pos):
                    cls.active_widget.on_mousemotion(e)

        cls.widgets.update()
