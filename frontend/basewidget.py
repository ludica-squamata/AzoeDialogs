from pygame.sprite import Sprite


class BaseWidget(Sprite):
    image = None
    rect = None
    is_selected = False
    on_focus = False

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()

    # event catcher functions
    def on_keydown(self, event):
        pass

    def on_keyup(self, event):
        pass

    def on_mousedown(self, event):
        if event.button == 1:
            self.select()

        elif event.button == 4:  # arriba
            self.scale(-1)

        elif event.button == 5:  # abajo
            self.scale(1)

    def on_mouseup(self, event):
        pass

    def on_mousemotion(self, event):
        self.rect.move_ip(event.rel)

    # state functions
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def scale(self, delta):
        x, y = self.rect.center
        self.rect = self.image.get_rect(center=(x, y))
