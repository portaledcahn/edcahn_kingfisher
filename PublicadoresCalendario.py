"""
PROYECTO : Portal EDCA-HN
NOMBRE : Edca
Descripcion : Clase principal para el flujo completo y control de la
    diferentes etapa:
        1. descargar archivos masivos zip de los publicadores
        2. prepara los archivos para la carga a la base de datos EDCA
        3. cargar los archivos al King Fisher.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.
"""

from config import calendario_config as cfg


class PublicadoresCalendarios:

    @staticmethod
    def get_calendario_publicadores(publicador):
        return cfg.publicador_job_calendario[publicador]

    @staticmethod
    def get_horario_publicadores(publicador):
        return cfg.publicador_job_horario[publicador]

    @staticmethod
    def get_test_publicadores(publicador):
        __test = cfg.publicador_prueba_horario[publicador]
        return __test
