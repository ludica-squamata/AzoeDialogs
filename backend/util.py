from os import getcwd, path
from pygame import quit
from sys import exit
import json


def salir():
    quit()
    exit()


def abrir_json(ruta):
    route = path.join(getcwd(), *ruta.split('/'))
    with open(route, 'rt', encoding='latin_1') as file:
        return json.load(file)


def guardar_json(ruta, data):
    route = path.join(getcwd(), *ruta.split('/'))
    with open(route, 'wt', encoding='latin_1') as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': '))
