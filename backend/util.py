from pygame import quit
from sys import exit
import json


def salir():
    quit()
    exit()


def abrir_json(ruta):
    with open(ruta, 'rt') as file:
        return json.load(file)


def guardar_json(ruta, data):
    with open(ruta, 'w', encoding='utf-8') as file:
        json.dump(data, file, sort_keys=True, indent=2, separators=(',', ':'))
