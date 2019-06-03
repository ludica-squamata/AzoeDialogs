from pygame import event, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, K_ESCAPE
from pygame.sprite import LayeredUpdates, Group
from backend import salir, EventHandler, TriggerMenu, System


class WidgetHandler:
    widgets = LayeredUpdates()
    active_widget = None
    name = "WidgetHandler"
    selection = None
    on_selection = False
    selected = Group()

    @classmethod
    def add_widget(cls, widget):
        cls.widgets.add(widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)

    @classmethod
    def set_active(cls, widget):
        cls.active_widget = widget

    @classmethod
    def enable_selection(cls, selection_object):
        cls.selection = selection_object
        cls.add_widget(selection_object)
        cls.on_selection = True
        cls.set_active(selection_object)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']

    @classmethod
    def update(cls):
        events = event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT])
        event.clear()

        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                salir()

            elif e.type == KEYDOWN:
                if len(cls.selected):
                    for widget in cls.selected:
                        widget.on_keydown(e)
                TriggerMenu.trigger(e.key)

            elif e.type == KEYUP:
                if len(cls.selected):
                    for widget in cls.selected:
                        widget.on_keyup(e)

            elif e.type == MOUSEBUTTONDOWN:  # pos, button
                widgets = [w for w in cls.widgets.get_sprites_at(e.pos) if w.selectable]
                if System.MODE == 'Selection':
                    if not len(widgets) and e.button == 1:
                        cls.selected.empty()
                        EventHandler.trigger('Selection', cls.name, {"pos": e.pos, 'value': True})

                    elif len(widgets) and not len(cls.selected):
                        cls.selected.add([w for w in widgets if w.selectable])

                    elif not cls.selected.has(widgets) and e.button == 1:
                        cls.selected.empty()
                        cls.selected.add(widgets)

                elif System.MODE == 'Connection':
                    if not cls.selected.has(widgets) and e.button == 1 and len(widgets):
                        for base in [w for w in cls.selected if w.selectable]:
                            base.connect(widgets[-1])

                if len(widgets):  # this is only valid for the mouse wheel
                    for widget in cls.selected:
                        if widget is not cls.selection:
                            widget.on_mousedown(e)

            elif e.type == MOUSEBUTTONUP:  # pos, button
                if System.MODE == 'Selection':
                    if cls.on_selection and e.button == 1:
                        cls.selection.on_mouseup(e)
                        for widget in cls.widgets:
                            if cls.selection.rect.contains(widget.rect):
                                cls.selected.add(widget)

            elif e.type == MOUSEMOTION:  # pos, rel, buttons
                if System.MODE == 'Selection':
                    if e.buttons[0] and len(cls.selected):
                        for widget in cls.selected:
                            widget.on_mousemotion(e)

                    elif cls.on_selection and e.buttons[0]:
                        cls.selection.on_mousemotion(e)

        cls.widgets.update()

    @classmethod
    def __repr__(cls):
        return cls.name + " ({} widgets)".format(str(len(cls.widgets)))


# noinspection PyTypeChecker
EventHandler.register(WidgetHandler.toggle_selection, 'Selection')