from backend.util import guardar_json, navigate, generate_id
from .eventhandler import EventHandler


class Behaviour:
    tree = None
    name = ''

    @classmethod
    def init(cls):
        cls.tree = {
            "head": {
                "script": {},
                "special": {}
            },
            "body": {}
        }

        EventHandler.register(cls.save, 'CreateAI')
        EventHandler.register(cls.new, 'CreateNew')

    @classmethod
    def new(cls, event):
        if event.data['tipo'] == 'behaviours':
            name = generate_id()
            EventHandler.trigger('CreateAI', cls.name, {'name': name, 'nodes': []})
            EventHandler.trigger('OnFileCreation', 'None', {'value': False})

    @classmethod
    def save(cls, event):
        nodes = cls.tree['body']
        head = cls.tree['head']['script']
        module = None
        name = None
        for node in event.data['nodes']:
            text = node.text  # leaf, sequence, repeater, etc.
            if '/' in text:
                module, name = text.split('/')
            nodes[str(node)] = {'name': text if name is None else name}
            if len(node.connections) == 1:  # decorator
                nodes[str(node)].update({'child': int(node.connections[0])})
            elif len(node.connections) > 1:  # composites
                nodes[str(node)].update({'children': [int(n) for n in sorted(node.connections, key=lambda n:n.idx)]})
            else:
                if name is None:
                    nodes[str(node)]['name'] += f' #{str(int(node))}'

                mod = 'behaviours/' + module
                if mod not in head:
                    head[mod] = []

                head[mod].append(nodes[str(node)]['name'])

        ruta = navigate('behaviours')
        guardar_json(ruta + '/' + event.data['name'] + '.json', cls.tree)


Behaviour.init()
