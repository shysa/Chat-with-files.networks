import json
from sys import platform

# -------------------------------------------------------------------
# Функция парсит config.json и возвращает значения параметров
# открываемых COM-портов
# Используется в phizical.portinit(com_params)
# -------------------------------------------------------------------


def get_port_parameters():
    with open('config.json', 'r') as fp:
        obj = json.load(fp)

        if platform == "win32":
            first_COM = obj["win_port1"]
            second_COM = obj["win_port2"]
        else:
            first_COM = obj["linux_port1"]
            second_COM = obj["linux_port2"]

        baudrate = obj["baudrate"]
        timeout = obj["timeout"]
        writeTimeout = obj["writeTimeout"]

    return first_COM, second_COM, baudrate, timeout, writeTimeout
