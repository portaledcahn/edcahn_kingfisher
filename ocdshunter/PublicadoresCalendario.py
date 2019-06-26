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

import datetime

from config import calendario_config as cfg


class PublicadoresCalendarios:

    __fecha_inicio = datetime.datetime.now()
    __fecha_fin = datetime.datetime.now()

    # Constructor para configurar el publicador
    def __init__(self, publicador):
        self.__publicador = publicador
        self.__periodo = PublicadoresCalendarios.get_perido(self.__publicador)
        self.__periodo_valor = PublicadoresCalendarios.get_perido_valor(self.__publicador)
        self.__hora = PublicadoresCalendarios.get_horario(self.__publicador)
        
    # valida si el publicador puede ejecutar su tareas segun su configuracion.
    def ejecutar(self):
        self.__armar_fechas()
        if self.__fecha_inicio <= datetime.datetime.now() <= self.__fecha_fin:
            return True
        return True
    
    # construye las fechas de inicio y fin
    def __armar_fechas(self):

        __now = datetime.datetime.now()
        __hr_ini = int(self.__hora.split(':')[0])
        __mi_ini = int(self.__hora.split(':')[1])
        __hr_fin = int(self.__hora.split(':')[0])
        __mi_fin = int(self.__hora.split(':')[1]) + cfg.minutos_tolerancia  # se agregan 10 mintos de tolerancia
        if __mi_fin > 60:
            __mi_fin = __mi_fin - 60
            __hr_fin = __hr_fin + 1

        # para la programacion diaria solo se ajusta la hora.
        if self.__periodo == cfg.periodo_diaria:
            __fecha_inicio = datetime.datetime(__now.year(), __now.month, __now.day, __hr_ini, __mi_ini)
            __fecha_fin = datetime.datetime(__now.year(), __now.month, __now.day, __hr_fin, __mi_fin)
            return
        
        # para la programacion semanal 
        if self.__periodo == cfg.periodo_semanal:
            return

        if self.__periodo == cfg.periodo_mensual:
            return
            
        return 

    @staticmethod
    def get_perido(publicador):
        return cfg.publicador_job_periodo.get(publicador)

    @staticmethod
    def get_perido_valor(publicador):
        return cfg.publicador_job_periodo_valor.get(publicador)

    @staticmethod
    def get_horario(publicador):
        return cfg.publicador_job_horario.get(publicador)

    @staticmethod
    def get_test(publicador):
        __test = cfg.publicador_prueba_horario[publicador]
        return __test
