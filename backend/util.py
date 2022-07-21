from winreg import OpenKey, EnumValue, HKEY_LOCAL_MACHINE
from datetime import datetime
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


def read_registry_data():
    """This function retrieves the a key from the Windows Registry"""
    key = OpenKey(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Ludica Squamata\\ManoGift\\')
    base = EnumValue(key, 0)[1]
    return base


def navigate(request):
    ruta = read_registry_data()
    mod_file = abrir_json(ruta + '/mod.json')
    mobs_folder = mod_file['folders']['mobs']
    mobs_folder += '/behaviours'
    dialg_fd = mod_file['folders']['dialogos']
    if request == 'dialogs':
        return path.join(ruta, dialg_fd)
    elif request == 'behaviours':
        return path.join(ruta, mobs_folder)


def generate_id():
    now = ''.join([char for char in str(datetime.now()) if char not in [' ', '.', ':', '-']])
    now = now[0:-5] + '-' + now[-5:]
    return now
