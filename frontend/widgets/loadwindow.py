from frontend.globals.constants import WIDTH, HEIGHT, COLOR_BOX, COLOR_TEXT, COLOR_SELECTED
from backend.util import abrir_json, navigate
from backend.eventhandler import EventHandler
from backend.textrect import render_textrect
from backend.group import WidgetGroup
from os import listdir, path, remove
from .basewidget import BaseWidget
from backend.system import System
from pygame import Surface, font
from os.path import join


class LoadWindow(BaseWidget):
    layer = 5000
    mode = 'dialogs'
    is_visible = False

    def __init__(self):
        super().__init__()
        self.image = Surface([WIDTH // 2, HEIGHT // 2])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 32))
        self.image.fill(COLOR_BOX, [1, 1, self.rect.w - 2, self.rect.h - 2])
        self.font_title = font.SysFont('Verdana', 14, bold=True)
        self._r = self.render_title()

        self.properties = WidgetGroup()
        self.show_files(self.mode)

        self.button_new = NewButton(self, top=self.rect.top + 1, right=self.rect.right - 3)
        self.button_del = DeleteButton(self, top=self.button_new.rect.bottom + 1, right=self.rect.right - 3)

        EventHandler.register(self.toggle, 'LoadData')
        EventHandler.deregister(self.toggle, 'F4ToggleMode')
        EventHandler.register(self.toggle_mode, 'F4ToggleMode')

        self.indirect_toggle(True)

    def render_title(self):
        self.image.fill(COLOR_BOX, [1, 1, self.rect.w - 2, self.rect.h - 2])
        render = self.font_title.render(f'Load - {self.mode}', 1, COLOR_SELECTED, COLOR_BOX)
        return self.image.blit(render, (1, 1))

    def show_files(self, request):
        ruta = navigate(request)
        files = [file for file in listdir(ruta) if path.isfile(join(ruta, file))]
        for i, file in enumerate(files):
            filename = join(ruta, file)
            x = self.rect.x + 2
            y = i * 20 + self.rect.y + self._r.bottom
            row = Row(self, file[:-5].capitalize(), filename, x, y)
            self.properties.add(row, layer=1)

    def delete_files(self):
        deleted_row = None
        for row in self.properties.get_widgets_from_layer(1):
            if row.is_selected:
                deleted_row = row
                break

        if deleted_row is not None:
            ruta = deleted_row.filepath
            remove(ruta)
            self.reload()
            for row in self.properties.get_widgets_from_layer(1):
                row.show()

    def reload(self):
        for row in self.properties.get_widgets_from_layer(1):
            row.kill()

        self.show_files(self.mode)
        self.render_title()

    def toggle_mode(self, event):
        if event.data['mode'] == 'dialog':
            self.mode = 'dialogs'
        elif event.data['mode'] == 'behaviour':
            self.mode = 'behaviours'

        self.reload()
        if self.is_visible:
            for row in self.properties.widgets():
                row.show()

    def toggle(self, event):
        self.indirect_toggle(event.data['value'])

    def indirect_toggle(self, value):
        if value is True:
            self.show()
            for row in self.properties.get_widgets_from_layer(1):
                row.show()
            self.button_new.show()
            self.button_del.show()

        else:
            self.hide()
            for row in self.properties.get_widgets_from_layer(1):
                row.hide()
            self.button_new.hide()
            self.button_del.hide()

    def deselect_others(self, selected=None):
        for row in self.properties.get_widgets_from_layer(1):
            row.deselect()
        self.button_new.deselect()

        selected.select()

    def on_mousebuttondown(self, event):
        self.deselect_others()


class BaseRowButton(BaseWidget):
    """Clase Base para todos los botones y filas de la ventana que operan de forma similar."""

    selectable = True

    def __init__(self, parent, text, w, h=19):
        super().__init__(parent)
        f1 = font.SysFont('Verdana', 14)

        self.text = text
        self.img_uns = render_textrect(text, f1, w, h, COLOR_TEXT, COLOR_BOX)
        self.img_sel = render_textrect(text, f1, w, h, COLOR_SELECTED, COLOR_BOX)
        self.image = self.img_uns

    def select(self):
        super().select()
        self.image = self.img_sel

    def deselect(self):
        super().deselect()
        self.image = self.img_uns

    def on_mousemotion(self, event):
        # this hook is necessary
        pass

    def toggle(self, event):
        # this hook is necessary
        pass

    def on_mousebuttondown(self, event):
        raise NotImplementedError


class Row(BaseRowButton):
    selectable = True

    def __init__(self, parent, text, ruta, x, y):
        super().__init__(parent, text, 240)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.filepath = ruta
        EventHandler.register(self.load_file, 'LoadDataFile')

    def on_mousebuttondown(self, event):
        if self.is_selected:
            self.be_loaded()
        else:
            self.parent.deselect_others(self)

    def load_file(self, event):
        if event.data['selected'] == self:
            self.be_loaded()

    def be_loaded(self):
        data = abrir_json(self.filepath)
        if len(data['head']) == 2:
            mode = 'behaviour'
        else:
            mode = 'dialog'
        System.load_file_data(data, mode)
        EventHandler.trigger('trigger_node_creation', 'LoadWindow', {'name': self.text, 'mode': mode})
        self.parent.indirect_toggle(False)


EventHandler.register(lambda a: LoadWindow(), 'Init')


class NewButton(BaseRowButton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, '+ New', 47)
        self.rect = self.image.get_rect(**kwargs)

    def on_mousebuttondown(self, event):
        if self.is_selected:
            EventHandler.trigger('CreateNew', self.parent, {'tipo': self.parent.mode})
            self.parent.indirect_toggle(False)
        else:
            self.parent.deselect_others(self)


class DeleteButton(BaseRowButton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, '- Remove', 70)
        self.rect = self.image.get_rect(**kwargs)
        self.select()

    def on_mousebuttondown(self, event):
        self.parent.delete_files()
