import json


def get_port_parameters():
    with open('../config.json', 'r') as fp:
        obj = json.load(fp)

        first_COM = obj["port1"]
        second_COM = obj["port2"]
        baudrate = obj["baudrate"]
        timeout = obj["timeout"]
        writeTimeout = obj["writeTimeout"]

    return first_COM, second_COM, baudrate, timeout, writeTimeout
