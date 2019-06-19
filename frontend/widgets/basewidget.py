from pygame.sprite import Sprite
from pygame import K_DELETE


class BaseWidget(Sprite):
    image = None
    rect = None
    is_selected = False
    on_focus = False
    selectable = True
    numerable = True

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()

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

    # state functions
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False
