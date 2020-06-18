"""
PROYECTO : Portal EDCA-HN
NOMBRE : KingFisherInterface
Descripcion :

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.
"""

import subprocess
import datetime

from config import  kinfisher_config as cfg

class KingFisherInterface:

    # Tag para identificar el evento del log
    __event_log = "KingFisher Interface"

    @staticmethod
    def ejecutar(id_coleccion, directorio_json, tipo_json, id_record):
        # crear coleccion
        __stmt = KingFisherInterface.interperte() + " " \
                 + KingFisherInterface.kingfisher_directorio() \
                 + KingFisherInterface.cmd_crear_coleccion()
        __stmt = KingFisherInterface.__armar_stmt(__stmt)
        #print(__stmt)
        #__shell = subprocess.run([__stmt], shell=True)
        #print("Mensaje Kingfisher: " + str(__shell.stdout))

        # cargar los archivos json al king fisher
        __stmt = KingFisherInterface.interperte() + " " + KingFisherInterface.kingfisher_directorio() + KingFisherInterface.cmd_cargar_json().format(str(id_coleccion) + " " + directorio_json + " " + tipo_json)
        print(__stmt)
        __shell = subprocess.run([__stmt], shell=True)
        print("Mensaje Kingfisher: " + str(__shell.stdout))

        # cerrar la coleccion
        __stmt = KingFisherInterface.interperte() + " " + KingFisherInterface.kingfisher_directorio() + KingFisherInterface.cmd_cerrar_coleccion().format(str(id_coleccion))
        print(__stmt)
        __shell = subprocess.run([__stmt], shell=True)
        print("Mensaje Kingfisher: " + str(__shell.stdout))

        # Crear coleccion de Tipo RECORD
        __stmt = KingFisherInterface.interperte() + " " + KingFisherInterface.kingfisher_directorio() + KingFisherInterface.cmd_crear_record().format(
            str(id_coleccion))
        print(__stmt)
        __shell = subprocess.run([__stmt], shell=True)
        print("Mensaje Kingfisher: " + str(__shell.stdout))

        # Transformar a releases package
        __stmt = KingFisherInterface.interperte() + " " + KingFisherInterface.kingfisher_directorio() + KingFisherInterface.cmd_convertir_releases().format(str(id_record))
        print(__stmt)
        __shell = subprocess.run([__stmt], shell=True)
        print("Mensaje Kingfisher: " + str(__shell.stdout))

    @staticmethod
    def nombre_coleccion():
        return cfg.kf_nombre_coleccion

    @staticmethod
    def interperte():
        return cfg.kf_interprete

    @staticmethod
    def kingfisher_directorio():
        return cfg.kf_directorio

    @staticmethod
    def cmd_crear_coleccion():
        return cfg.kf_comando_crear_coleccion

    @staticmethod
    def cmd_cargar_json():
        return cfg.kf_comando_cargar_json

    @staticmethod
    def cmd_crear_record():
        return cfg.kf_comando_crear_records

    @staticmethod
    def cmd_cerrar_coleccion():
        return  cfg.kf_comando_cerrar_coleccion

    @staticmethod
    def cmd_convertir_releases():
        return cfg.kf_comando_convertir_releases

    @staticmethod
    def __armar_stmt(sentencia):
        # Reemplazar el formato por los atributos.
        __stmt = sentencia
        __stmt = __stmt.replace("{0}", str(cfg.kf_nombre_coleccion))
        __stmt = __stmt.replace("{yyyy}", str(datetime.date.today().year))
        __stmt = __stmt.replace("{mm}", str(datetime.date.today().month))
        __stmt = __stmt.replace("{dd}", str(datetime.date.today().day))
        __stmt = __stmt.replace("{hh24}", str(datetime.datetime.today().hour))
        __stmt = __stmt.replace("{mi}", str(datetime.datetime.today().minute))
        __stmt = __stmt.replace("{ss}", str(datetime.datetime.today().second))
        return __stmt
