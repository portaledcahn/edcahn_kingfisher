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


class PublicadoresTareas:

    def __init__(self, publicador):
        self.__publicador = publicador
        self.logger = logging.getLogger(__class__.__module__)

    def ejecutar(self):
        Edca(self.__publicador, 1).ejecutar()

    @staticmethod
    def __imprimir(publicador):
        __test = cfg.get_test_publicadores(publicador)
        print(__test)
