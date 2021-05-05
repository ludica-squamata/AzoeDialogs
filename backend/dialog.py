from .eventhandler import EventHandler
from backend.util import guardar_json
from .system import System


class Dialog:
    name = ''
    tree = None

    @classmethod
    def init(cls):
        cls.tree = {
            'head': {
                'class': "scripted",
                "conditional_tags": {},
                "style": "",
                "locutors": [],
                "about": "",
                "icon": None,
                "keywords": [],
                "events": {},
                "panels": {
                    "objects": {},
                    "themes": {}
                }
            },
            'body': {}
        }
        EventHandler.register(cls.save, 'CreateDialog')

    @classmethod
    def save(cls, event):
        nodes = cls.tree['body']
        for node in event.data['nodes']:
            text = System.data[int(node)]
            nodes[str(node)] = {'type': node.tipo}
            if node.tipo != 'leaf':
                nodes[str(node)]['leads'] = node.lead
            nodes[str(node)]['txt'] = text
            nodes[str(node)]['from'] = node.locutor_name
            if node.locutor_name not in cls.tree['head']['locutors']:
                cls.tree['head']['locutors'].append(node.locutor_name)
            nodes[str(node)]['to'] = node.interlocutor.locutor_name if node.interlocutor is not None else ''
        guardar_json('data/output.json', cls.tree)


Dialog.init()
