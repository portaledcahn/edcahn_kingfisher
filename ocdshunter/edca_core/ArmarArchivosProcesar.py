"""
PROYECTO : Portal EDCA-HN
NOMBRE : ArmarArchivosProcesar
Descripcion : Clase destinada para procesar los archivos descargados
del origen de los Publicadores, armar los archivos listos para la cargar
a la base de datos.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

import json
import uuid
from builtins import hasattr, Exception

from config import edca_global_config as cfg
from edca_core import Publicadores as pb
from edca_logs.EdcaLogger import EdcaLogger as log
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_utilitarios import EdcaUtil as util


class ArmarArchivosProcesar:
    releases_nuevos: int
    __event_log = "Praparar Achivos para KF"

    def __init__(self, publicador, nro_transaccion):
        self.__publicador = publicador
        self.__nro_transaccion = nro_transaccion
        self.__origenes = self.__obtener_origenes(self.__publicador)
        self.__msg = msg.EdcaMensajes()

    def ejecutar(self):
        try:
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_BUILD_FILEFROMKF_BEGIN, self.__event_log,
                                   "======= ETAPA 2 =======")

            # ser recorren todos los origenes del publicador
            for origen in self.__origenes:
                __directorio = self.__obtener_ruta_descarga(origen)  # se obtiene el directorio donde estan los archivos
                __archivos = self.__obtener_archivos(__directorio)  # se obtiene la lista de los archivos json
                # se lee la lista de archivos.
                for archivo in __archivos:
                    log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                                           "Leyendo Archivo: " + archivo)
                    # se recupera el tipo de archivo json
                    __tipo = self.__obtener_tipo_archivo_json(origen)
                    if cfg.tipo_archivo_json_line == __tipo:  # funcion para evaluar json line
                        self.__evaluar_archivo_tipo_jsonline(origen, archivo)
                    if cfg.tipo_archivo_releasepackage == __tipo:  # funcion para evaluar release package
                        self.__evaluar_archivo_tipo_release(origen, archivo)
                    log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                                           "Archivo leido : " + archivo)
        except Exception as ex:
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                                   str(ex.with_traceback()))

    # Recuperar los origenes o sistemas de los Publicadores
    @staticmethod
    def __obtener_origenes(publicador):
        return pb.Publicadores.origenes(publicador)

    # Recuperar la ruta o direccion donde se guardara los archivo descargados
    @staticmethod
    def __obtener_ruta_descarga(origen):
        __directorio = pb.Publicadores.origen_directorio(origen)
        if __directorio is None:
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOPATH)
        return __directorio

    # funcion para recupera todos los archivos de un directorio
    @staticmethod
    def __obtener_archivos(directorio):
        return util.EdcaUtil.obtener_lista_archivos(directorio, '.json')

    # se evalua el archivo, extraendo los releases para ser validados por un hash
    def __evaluar_archivo_tipo_jsonline(self, origen, archivo):
        l = 0
        js = []
        # abrir el archivo json descargado del origen
        with open(archivo, "r", encoding="utf8") as archivojson:
            for line in archivojson:
                js.append(json.loads(line))

        # archivo destino para cargar los json al king fisher
        outfile_name = self.__obtener_directorio_kingfisher(origen) + origen + "_" + str(uuid.uuid4()) + ".json"

        # archivo hash para agregar los nuevos hash
        archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a")

        # ciclo para analizar cada linea json
        for p in js:
            hs = self.__obtener_hash(json.dumps(p))  # convertir el json string a un hash md5
            # buscar el hash en el archivo hash
            if not self.__buscar_hash(origen, hs):  # de no existir el hash
                if l == 0:
                    outfile = open(outfile_name, "w")
                    l = l + 1
                # guardar el nuevo hash
                archivo_hash.writelines(hs + "\n")
                # pasar el json string al nuevo archivo para cargarlo al king fisher
                outfile.writelines(str(json.dumps(p)) + "\n")

        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                               "Release a Procesar en KingFisher= " + str(l))
        archivo_hash.close()  # cerrar archivo de hash
        outfile.close()  # cerrar archivo de json para el king fisher
        archivojson.close()  # cerrar archivo json origen

    # se evalua el archivo, extraendo los releases para ser validados por un hash
    def __evaluar_archivo_tipo_release(self, origen, archivo):
        # print("evaluar archivo tipo release")
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                               "evaluar archivo tipo release")

        # abrir el archivo json descargado del origen
        with open(archivo, "r") as archivojson:
            data = archivojson.read()
        # deserializando el string a json
        js = json.loads(data)
        jx = json.loads(data)  # copia del archivo.

        jx["releases"] = []  # limpiar el arreglo de releases del archivo para carga king fisher

        # archivo hash para agregar los nuevos hash
        archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a")

        l = 0  # contador para saber si hay nuevos releases para cargar
        # ciclo para analizar el arreglos de json de los releases
        for p in js["releases"]:
            hs = self.__obtener_hash(json.dumps(p))  # convertir el json string a un hash md5
            if not self.__buscar_hash(origen, hs):
                l = l + 1  # contando cada releases nuevo
                archivo_hash.writelines(hs + "\n")  # guardar el nuevo hash
                jx["releases"].append(p)  # agregando el releases nuevo

        # Se guarda el valor
        self.releases_nuevos = str(l)

        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                               "Release a Procesar en KingFisher= " + str(l))

        if l != 0:  # hay nuevos releases?
            # guardar el release package en el archivo destino para cargar al king fisher
            outfile_name = self.__obtener_directorio_kingfisher(origen) + origen + "_" + str(uuid.uuid4()) + ".json"
            with open(outfile_name, 'w') as outfile:
                json.dump(jx, outfile)
            # print("Listo para cargar : " + outfile_name)
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log,
                                   "Listo para cargar : " + outfile_name)
            outfile.close()  # cerrar archivo de json para el king fisher

        archivo_hash.close()  # cerrar archivo de hash
        archivojson.close()  # cerrar archivo json origen

    # Obtener si hay releases
    @property
    def get_existe_releases_nuevos(self):
        return self.releases_nuevos

    # buscar el hash en el archivo de hash
    @staticmethod
    def __buscar_hash(origen, hsh):
        archivo = pb.Publicadores.publicador_archivo_hash(origen)
        if hsh in open(archivo, "r").read():
            return True
        return False

    # convierte el json string en un hash md5
    @staticmethod
    def __obtener_hash(cadena):
        return util.EdcaUtil().string_to_hash(cadena)

    # obtener el tipo de archivos json del origen
    @staticmethod
    def __obtener_tipo_archivo_json(origen):
        return pb.Publicadores.publicador_tipo_archivo_json(origen)

    # Obtener el directorio para colocar los archivos y cargar al king fisher
    @staticmethod
    def __obtener_directorio_kingfisher(origen):
        return pb.Publicadores.publicador_directorio_kingfisher(origen)

    # recupera el archivo archivo de los json hash
    @staticmethod
    def __obtener_archivo_hash(origen):
        return pb.Publicadores.publicador_archivo_hash(origen)

    # Registrar bitacora del main o clase princial
    @staticmethod
    def __registrar_bitacora(code, event, detail):
        # print("Code : " + code + " Event : " + event + " Detail : " + detail)
        log.registrar_log_info(__name__, code, event, detail)
