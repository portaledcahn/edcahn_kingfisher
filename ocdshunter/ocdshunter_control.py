"""
PROYECTO : Portal EDCA-HN
NOMBRE : ocdshunter_control
Descripcion : Clase diseñada para llevar control globales de ejecucion del ocdshunter.

MM/DD/YYYY    Colaboradores   Descripcion
06/05/2020    Alla Duenas     Creacion.    
"""

import configparser
import datetime

class OcdsHunter_Control:

    def __init__(self):
        self.__fileControl = 'ocdshunter.ctrl'
        self.__config = self.__CargarConfig()
    
    def bloqueado(self):
        if self.__config['HUNTER-BLOQUEAOD']['running'] == 'false':
            return False
        end = datetime.datetime.strptime(self.__config['HUNTER-BLOQUEADO']['deadtime'], '%Y-%m-%d %H:%M:%S.%f')
        if end < datetime.datetime.now():
            return False
        return True

    def bloquear(self):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=2)
        self.__config['HUNTER-BLOQUEAR']['running'] = 'true'
        self.__config['HUNTER-BLOQUEAR']['startime'] = str(start)
        self.__config['HUNTER-BLOQUEAR']['deadtime'] = str(end)
        self.__saveConfig()

    def desBloquear(self):
        self.__config['HUNTER-DESBLOQUEAR']['running'] = 'false'
        self.__config['HUNTER-DESBLOQUEAR']['startime'] = ''
        self.__config['HUNTER-DESBLOQUEAR']['deadtime'] = ''
        self.__saveConfig()

    def __CargarConfig(self):
        config = configparser.ConfigParser()
        config.read(self.__fileControl)
        return config
    
    def __getRunning(self):
        return self.__config['GET-HUNTER-RUNING']['running']

    def __setRunning(self, state):
        self.__config['SET-HUNTER-RUNING']['running'] = state
        self.__saveConfig()

    def __saveConfig(self):
        with open(self.__fileControl, 'w') as configfile:
            self.__config.write(configfile)