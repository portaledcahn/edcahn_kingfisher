"""
PROYECTO : Portal EDCA-HN
NOMBRE : PublicadoresTareas
Descripcion : Clase para el manejo de Log.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.
"""

import logging
import logging.config
from config import edca_global_config as cfg


class EdcaLogger:

    # Constructor
    def __init__(self, clase):
        # Leer configuracion del archivo
        logging.config.fileConfig(cfg.logger_config_ini, disable_existing_loggers=False)
        self.clase = clase

    @staticmethod
    def registrar_log_info(clase, codigo, evento, detalle):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __info = "Codigo: " + codigo + " | Evento: " + evento + " | Detalle: " + detalle
        logger.info(__info)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #    print(__info)

    @staticmethod
    def registrar_log_exception(clase, argumento):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __exception = " ** EXCEPTION: " + argumento
        logger.exception(__exception)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #   print(__exception)

    @staticmethod
    def registrar_log_debug(clase, codigo, evento, detalle):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __debug = "Codigo: " + codigo + " | Evento: " + evento + " | Detalle: " + detalle
        logger.debug(__debug)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #    print(__debug)

    @staticmethod
    def registrar_log_warning(clase, codigo, evento, detalle):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __warning = "Codigo: " + codigo + " | Evento: " + evento + " | Detalle: " + detalle
        logger.warning(__warning)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #    print(__warning)

    @staticmethod
    def registrar_log_error(clase, codigo, evento, detalle):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __error = "Codigo: " + codigo + " | Evento: " + evento + " | Detalle: " + detalle
        logger.error(__error)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #    print(__error)

    @staticmethod
    def registrar_log_critical(clase, codigo, evento, detalle):
        # Creacion del Logger
        logger = logging.getLogger(clase)
        # Se registra el texto en el log
        __critical = "Codigo: " + codigo + " | Evento: " + evento + " | Detalle: " + detalle
        logger.critical(__critical)

        # imprimir en la consola
        #if cfg.logger_print_console:
        #    print(__critical)
