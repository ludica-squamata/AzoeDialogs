from pygame import event, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, K_ESCAPE, key, mouse
from pygame import KMOD_CTRL, KMOD_SHIFT, K_RETURN, K_F1, K_s, K_d, K_c, K_a, K_F2, K_F3, K_F4, K_F5, Rect, Color
from backend import salir, EventHandler, System, Selected
from backend.group import WidgetGroup


class WidgetHandler:
    widgets = WidgetGroup()
    active_widget = None
    name = "WidgetHandler"
    selection = None
    on_selection = False
    selected = Selected()
    numerable = []
    active_area = Rect(0, 21, 537, 363)

    dialog_nodes = []
    behaviour_nodes = []

    toggle_automatic_connection = False

    on_window = False

    @classmethod
    def add_widget(cls, widget, layer=0):
        cls.widgets.add(widget, layer=layer)
        if widget.numerable:
            cls.numerable.append(widget)
            if System.widget_group_key == 1:
                System.number_of_dialog_nodes += 1
                cls.dialog_nodes.append(widget)
            elif System.widget_group_key == 2:
                System.number_of_behaviour_nodes += 1
                cls.behaviour_nodes.append(widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)
        if widget.numerable:
            cls.numerable.remove(widget)
            if System.widget_group_key == 1:
                System.number_of_dialog_nodes -= 1
                cls.dialog_nodes.remove(widget)
            elif System.widget_group_key == 2:
                System.number_of_behaviour_nodes -= 1
                cls.behaviour_nodes.remove(widget)

        cls.numerable.sort(key=lambda o: o.idx)

    @classmethod
    def wids(cls):
        # for oneliners
        return cls.widgets.widgets()

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
    def trigger_node_creation(cls, evento):
        if evento.data['mode'] == 'dialog':
            cls.load_dialog_nodes()
        elif evento.data['mode'] == 'behaviour':
            cls.create_loaded_behaviour_nodes()
            cls.toggle_automatic_connection = True

    @classmethod
    def add_conections(cls):
        ordered_nodes = []
        unordererd_idexes = [int(i.idx) for i in cls.behaviour_nodes]
        for i in range(len(cls.behaviour_nodes)):
            if i in unordererd_idexes:
                idx = unordererd_idexes.index(i)
                ordered_nodes.append(cls.behaviour_nodes[idx])
        for node in reversed(ordered_nodes):
            node_data = System.data['body'][str(node)]
            if 'child' in node_data:
                child_node = ordered_nodes[node_data['child']]
                node.connect(child_node)

            elif 'children' in node_data:
                children = [n for n in ordered_nodes if int(n.idx) in node_data['children']]
                children.sort(key=lambda c: int(c.idx))
                for child_node in children:
                    node.connect(child_node)

        cls.toggle_automatic_connection = False

        members = {}
        for node in ordered_nodes:
            count = node.count_parents()
            if count not in members:
                members[count] = []
            members[count].append(node)
            dy = node.vertical_position
            node.rect.centery = dy*32 + cls.active_area.y

        for count in members:
            mms = members[count]
            for i, node in enumerate(mms):
                node.rect.centerx += i*32

        cls.on_window = False

    @classmethod
    def create_loaded_behaviour_nodes(cls):
        structural_nodes = [n for n in cls.wids() if n.order == 'd']
        structural_names = [n.name for n in structural_nodes]
        x = cls.active_area.centerx
        y = cls.active_area.y
        for idx in sorted(System.data['body']):
            node_data = System.data['body'][idx]
            text = node_data['name']
            if text in structural_names:
                index = structural_names.index(text)
                color = structural_nodes[index].color
            else:
                color = Color(0, 0, 0)

            EventHandler.trigger('AddNode', cls.name, {'idx': idx, 'pos': [x, y], 'color': color, 'text': text})

    @classmethod
    def load_dialog_nodes(cls):
        diff = len(cls.numerable) - System.lenght
        for i in range(diff):
            cls.numerable[-1].kill()

    @classmethod
    def update(cls):
        events = event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT])
        event.clear()

        # esto es para que se pueda reemplazar un locutor sin tener que reseleccionarlo.
        cls.selected.add([i for i in cls.widgets.widgets() if i.is_selected and (i not in cls.selected)])

        if cls.toggle_automatic_connection:
            cls.add_conections()

        for e in events:
            mods = key.get_mods()
            ctrl = mods & KMOD_CTRL
            shift = mods & KMOD_SHIFT
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                salir()

            elif e.type == KEYDOWN:
                widgets = cls.selected.widgets()
                if System.type_mode:
                    if e.key == K_F3:
                        System.toggle_typemode('MainTB')
                    else:
                        EventHandler.trigger('Key', cls.name, {'key': e.key, 'mod': e.mod})

                elif e.key == K_c:
                    if len(widgets) == 2 and all([o.numerable for o in widgets]):
                        widgets.sort(key=lambda o: o.idx)  # lower idx's go first
                        if not shift:
                            widgets[0].connect(widgets[1])
                        else:
                            widgets[0].disconnect(widgets[1])

                elif e.key == K_a and len(widgets) == 2:
                    base, other = widgets
                    EventHandler.trigger('AddMidPoint', 'System', {'base': base, 'other': other})

                elif e.key == K_RETURN:
                    if cls.on_window:
                        EventHandler.trigger('LoadDataFile', cls.name, {'selected': widgets[0]})

                    elif System.program_mode == 'dialog':
                        EventHandler.trigger('CreateDialog', cls.name, {'nodes': cls.dialog_nodes})

                    elif System.program_mode == 'behaviour':
                        EventHandler.trigger('CreateAI', cls.name, {'nodes': cls.behaviour_nodes})

                elif e.key == K_F1:
                    EventHandler.trigger('LoadData', cls.name, {'value': True})
                    cls.on_window = True

                elif e.key == K_F2:
                    if System.program_mode == 'dialog':
                        System.new_locutor()

                elif e.key == K_F3:
                    if any([o.order == 'b' for o in widgets]):
                        System.toggle_typemode('MainTB')
                    else:
                        for widget in widgets:
                            widget.on_keydown(e)

                elif e.key == K_F4:
                    System.toggle_program_mode()
                    EventHandler.trigger('F4ToggleMode', 'ENGINE', {'mode': System.program_mode})
                    cls.selected.empty()

                elif e.key == K_F5:
                    if System.program_mode == 'dialog':
                        System.toggle_input_mode()

                elif e.key == K_s and (System.get_lenght() > 0 or System.limit_input is False):
                    x, y = mouse.get_pos()
                    color = None
                    identifier = None
                    text = None

                    if any([o.order == 'a' for o in widgets]):
                        identifier = 'a'

                    elif any([o.order == 'd' for o in widgets]):
                        identifier = 'd'

                    if identifier is not None:
                        node = [i for i in widgets if i.order == identifier][0]
                        color = node.color
                        if hasattr(node, 'text'):
                            text = node.text

                    if System.area_nodos.collidepoint(x, y):
                        EventHandler.trigger('AddNode', cls.name, {'pos': [x, y], 'color': color, 'text': text})

                elif e.key == K_d and any([o.order == 'a' for o in widgets]):
                    widgets.sort(key=lambda o: o.order)
                    color_namer = widgets.pop(0)
                    for other in widgets:
                        other.colorize(color_namer)

                elif len(cls.selected):
                    for widget in cls.selected.widgets():
                        widget.on_keydown(e)

            elif e.type == KEYUP:
                if len(cls.selected):
                    for widget in cls.selected.widgets():
                        widget.on_keyup(e)

            elif e.type == MOUSEBUTTONDOWN:  # pos, button
                widgets = [w for w in cls.wids() if w.selectable and w.rect.collidepoint(e.pos) and w.is_visible]
                if not len(widgets) and e.button == 1 and cls.active_area.collidepoint(e.pos):
                    if not shift and not System.type_mode:
                        cls.selected.empty()
                    if not ctrl and not cls.on_window:
                        EventHandler.trigger('AddSelection', cls.name, {"pos": e.pos, 'value': True})

                elif len(widgets) and not len(cls.selected):
                    cls.selected.sumar([w for w in widgets if w.selectable])

                elif not cls.selected.has(widgets) and e.button == 1 and len(widgets):
                    order_c = [i for i in widgets if i.order == 'c']
                    if not ctrl and not System.type_mode and not len(order_c):
                        cls.selected.empty()
                    cls.selected.sumar(widgets)

                if len(widgets):
                    for widget in cls.selected.widgets():
                        if widget is not cls.selection:
                            widget.on_mousebuttondown(e)

                elif e.button != 1:
                    widgets = [w for w in cls.widgets.widgets() if w.numerable]
                    if ctrl and not shift:
                        dx, dy = 1, 0
                    elif shift and not ctrl:
                        dx, dy = 0, 5
                    elif ctrl and shift:
                        dx, dy = 5, 0
                    else:
                        dx, dy = 0, 1

                    for widget in widgets:
                        if e.button == 4:
                            dx *= -1
                            dy *= -1
                        elif e.button == 5:
                            dx *= 1
                            dy *= 1

                        widget.rect.move_ip(dx, dy)

            elif e.type == MOUSEBUTTONUP:  # pos, button
                if cls.on_selection and e.button == 1:
                    cls.selection.on_mousebuttonup(e)
                    cls.selection.rect.normalize()
                    selected = [i for i in cls.widgets if cls.selection.rect.contains(i.rect)]
                    cls.selected.sumar(selected)

            elif e.type == MOUSEMOTION:  # pos, rel, buttons
                if e.buttons[0] and len(cls.selected) and not shift and not System.type_mode:
                    for widget in [i for i in cls.selected.widgets() if i.draggable is True]:
                        widget.on_mousemotion(e)

                elif cls.on_selection and e.buttons[0]:
                    cls.selection.on_mousemotion(e)

                elif ctrl and e.buttons[0]:
                    widgets = [w for w in cls.widgets.widgets() if w.selectable and w.draggable]
                    for widget in widgets:
                        widget.on_mousemotion(e)

        cls.widgets.update()

    @classmethod
    def __repr__(cls):
        return cls.name + " ({} widgets)".format(str(len(cls.widgets)))


EventHandler.register(WidgetHandler.toggle_selection, 'AddSelection', 'EndSelection')
EventHandler.register(WidgetHandler.trigger_node_creation, 'trigger_node_creation')
