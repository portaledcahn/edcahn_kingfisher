"""
PROYECTO : Portal EDCA-HN
NOMBRE : PublicadoresTareas
Descripcion : Clase para ejecutar las tareas de los publicadores.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""
import logging
from PublicadoresCalendario import PublicadoresCalendarios as cfg
from edca_core.Edca import Edca
from ocdshunter_control import OcdsHunter_Control as ctrl

class PublicadoresTareas:

    def __init__(self, publicador):
        self.__publicador = publicador
        self.logger = logging.getLogger(__class__.__module__)

    def ejecutar(self):
        try:
            #if not self.__validarBloqueo():
            #    self.__bloquear()
            Edca(self.__publicador, 1).ejecutar()
            #    self.__desBloquear()
        
        except Exception as ex:
            print(str(ex))
            self.__desBloquear()
            
        
    @staticmethod
    def __imprimir(publicador):
        __test = cfg.get_test(publicador)
        print(__test)

    def __validarBloqueo(self):
        return ctrl().bloqueado()
    
    def __bloquear(self):
        ctrl().bloquear()

    def __desBloquear(self):
        ctrl().desBloquear()