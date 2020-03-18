from .eventhandler import EventHandler
from backend.util import guardar_json
from .system import System


class Dialog:
    name = ''
    nodes = None

    @classmethod
    def init(cls):
        cls.nodes = {}
        EventHandler.register(cls.save, 'CreateDialog')

    @classmethod
    def save(cls, event):
        for node in event.data['nodes']:
            cls.nodes[str(node)] = {'type': node.tipo}
            if node.tipo != 'leaf':
                cls.nodes[str(node)]['leads'] = node.lead
            cls.nodes[str(node)]['txt'] = System.data[int(node)]
            cls.nodes[str(node)]['from'] = node.locutor_name
            cls.nodes[str(node)]['to'] = node.interlocutor.locutor_name if node.interlocutor is not None else ''
        guardar_json('data/output.json', cls.nodes)


Dialog.init()
