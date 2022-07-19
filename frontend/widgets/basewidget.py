from frontend.globals import WidgetHandler, Renderer
from backend.eventhandler import EventHandler
from pygame.sprite import Sprite
from pygame import K_DELETE


class BaseWidget(Sprite):
    rect = None
    is_selected = False
    on_focus = False
    selectable = False
    numerable = False
    editable = False
    draggable = True
    order = None

    is_visible = True

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        if self.parent is not None:
            self.layer = self.parent.layer + 1
        else:
            self.layer = 1
        EventHandler.register(self.toggle, 'F4ToggleMode')

    @property
    def center(self):
        return self.rect.center

    def __getitem__(self, item):
        return self.rect.center[item]

    # event catcher functions
    def on_keydown(self, event):
        if event.key == K_DELETE:
            self.kill()
            return True
        return False

    def on_keyup(self, event):
        pass

    def on_mousedown(self, event):
        pass

    def on_mouseup(self, event):
        pass

    def on_mousemotion(self, event):
        self.rect.move_ip(event.rel)

    def toggle_selection(self, event):
        if event.data['target'] is self:
            if event.tipo == 'select':
                self.select()
            elif event.tipo == 'deselect':
                self.deselect()

    # state functions
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def toggle(self, event):
        if event.data['mode'] == 'dialog':
            self.show()
        elif event.data['mode'] == 'behaviour':
            self.hide()

    def show(self):
        self.is_visible = True
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)

    def hide(self):
        self.is_visible = False
        WidgetHandler.del_widget(self)
        Renderer.del_widget(self)
