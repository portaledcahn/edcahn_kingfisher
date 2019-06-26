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

from edca_core import Publicadores as pb
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_utilitarios import EdcaUtil as util
from edca_logs.EdcaLogger import EdcaLogger as log


class PrepararArchivosKF:
    # Constructor
    def __init__(self, publicador, nro_transaccion):
        self.__publicador = publicador
        self.__nro_transaccion = nro_transaccion
        self.__origenes = self.__obtener_origenes(self.__publicador)
        self.__msg = msg.EdcaMensajes

    # Metodo para obtener los Sistemas de un Publicador
    @staticmethod
    def __obtener_origenes(publicador):
        return pb.Publicadores.origenes(publicador)

    # Metodo para obtener el directorio del archivo JSON del Publicador
    @staticmethod
    def __obtener_publicador_directorio_json(origen):
        __directorio = pb.Publicadores.origen_directorio(origen)
        if __directorio is None:
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOPATH)
        return __directorio

    # Metodo para obtener el archivo JSON del Publicador
    @staticmethod
    def __obtener_publicador_archivo_json(directorio):
        return util.EdcaUtil.obtener_lista_archivos(directorio, '.json')

    # Metodo para obtener el directorio HASH del Publicador
    @staticmethod
    def __obtener_publicador_directorio_hash(publicador):
        return pb.Publicadores.publicador_directorio_hash(publicador)

    # Metodo para generar un HASH del archivo JSON del Publicador
    @staticmethod
    def _generar_publicador_hash(cadena):
        return util.EdcaUtil().string_to_hash(cadena)

    # Metodo para obtener el archivo HASH del Publicador
    @staticmethod
    def __obtener_publicador_archivo_hash(origen):
        archivo = pb.Publicadores.publicador_archivo_hash(origen)
        if util.EdcaUtil.validar_existe_archivo(archivo):
            return True
        return False

    # Metodo para obtener el directorio Kingfisher del Publicador

    @staticmethod
    def __obtener_publicador_directorio_kingfisher(origen):
        return pb.Publicadores.publicador_directorio_kingfisher(origen)

    # Metodo para obtener el archivo JSON del Publicador a ser procesado por Kingfisher
    @staticmethod
    def __obtener_publicador_archivo_json_kingfisher(directorio):
        return util.EdcaUtil.obtener_lista_archivos(directorio, '.json')

    # Metodo para obtener el tipo de JSON del Publicador
    @staticmethod
    def __obtener_publicador_tipo_archivo_json(origen):
        return pb.Publicadores.publicador_tipo_archivo_json(origen)

    # Metodo para leer el archivo JSON del Publicador para el tipo de archivo release-package
    def __leer_archivo_json_tipo_release(self, origen, archivo):
        print("******* ABRIENDO ARCHIVO JSON DE TIPO RELEASE ********")
        # abrir el archivo json descargado del origen
        with open(archivo, "r") as archivojson:
            data = archivojson.read()
            # deserializando del string a json
            js = json.loads(data)
            # copia del archivo
            jx = json.loads(data)
            # limpiar el arreglo de releases del archivo para carga king fisher
            jx["releases"] = []
            # archivo hash para agregar los nuevos hash
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                   "ARMAR JSON RELEASE",
                                   "Cantidad de Releases en el Archivo JSON: " + str(len(js["releases"])))
            lineas = len(js["releases"])

            # Se valida si el archivo HASH existe o no
            if not util.EdcaUtil.validar_existe_archivo(pb.Publicadores.publicador_archivo_hash(origen)):
                # archivo hash para agregar los nuevos hash
                archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "w", encoding='utf-8')
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       "ARMAR JSON RELEASE",
                                       "Archivo HASH: " + str(archivo_hash) + ", creado exitosamente.")
                # contador para saber si hay nuevos releases para cargar
                x = 0
                # ciclo para analizar el arreglos de json de los releases
                for index, p in enumerate(js["releases"]):
                    print("Releases: " + str(p))
                    # convertir el json string a un hash md5
                    hash_datos = self._generar_publicador_hash(json.dumps(p))
                    print("HASH: " + hash_datos)
                    print("Index: " + str(index) + " X: " + str(lineas))
                    if index != (lineas - 1):
                        archivo_hash.writelines(hash_datos + '\n')
                    else:
                        archivo_hash.writelines(hash_datos)
                    # Acumulador
                    x = x + 1
                archivo_hash.close()
            else:
                print("ARCHIVO HASH EXISTE")

    # Metodo para leer el archivo JSON del Publicador de Tipo release-package
    def __preparar_json_release(self, origen, archivo):
        # Se valida si el archivo HASH existe o no
        if not util.EdcaUtil.validar_existe_archivo(pb.Publicadores.publicador_archivo_hash(origen)):
            # archivo hash para agregar los nuevos hash
            archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a", encoding='utf-8')
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                   "ARMAR JSON RELEASE",
                                   "Archivo HASH: " + str(archivo_hash) + ", creado exitosamente.")

            print("******* ABRIENDO ARCHIVO JSON DE TIPO RELEASE ********")
            # abrir el archivo json descargado del origen
            with open(archivo, "r") as archivojson:
                data = archivojson.read()
                # deserializando del string a json
                js = json.loads(data)
                # copia del archivo
                jx = json.loads(data)
                # limpiar el arreglo de releases del archivo para carga king fisher
                jx["releases"] = []
                # archivo hash para agregar los nuevos hash
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       "ARMAR JSON RELEASE",
                                       "Cantidad de Releases en el Archivo JSON: " + str(len(js["releases"])))
                lineas = len(js["releases"])

                # contador para saber si hay nuevos releases para cargar
                x = 0
                # ciclo para analizar el arreglos de json de los releases
                for index, p in enumerate(js["releases"]):
                    print("Releases: " + str(p))
                    # convertir el json string a un hash md5
                    hash_datos = self._generar_publicador_hash(json.dumps(p))
                    print("HASH: " + hash_datos)
                    print("Index: " + str(index) + " X: " + str(lineas))
                    if index != (lineas - 1):
                        archivo_hash.writelines(hash_datos + '\n')
                    else:
                        archivo_hash.writelines(hash_datos)
                    # Acumulador
                    x = x + 1

            # Se cierra el archivo HASH
            archivo_hash.close()
        else:
            print("***ARCHIVO HASH EXISTE***")
            print("INICIANDO COMPARACION DE HASH PARA IDENTIFICAR QUE CAMBIO")
            print("******* ABRIENDO ARCHIVO JSON DE TIPO RELEASE ********")
            # abrir el archivo json descargado del origen
            with open(archivo, "r") as archivojson:
                data = archivojson.read()
                # deserializando del string a json
                js = json.loads(data)
                # copia del archivo
                jx = json.loads(data)
                # limpiar el arreglo de releases del archivo para carga king fisher
                jx["releases"] = []
                # archivo hash para agregar los nuevos hash
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       "ARMAR JSON RELEASE",
                                       "Cantidad de Releases en el Archivo JSON: " + str(len(js["releases"])))
                lineas2 = len(js["releases"])

                # ciclo para analizar el arreglos de json de los releases
                print("******* ABRIENDO ARCHIVO HASH ********")
                # abrir el archivo json descargado del origen
                with open(pb.Publicadores.publicador_archivo_hash(origen), "r") as archivohash:
                    hash_data = archivohash.readline()
                    # contador para saber si hay nuevos releases para cargar
                    y = 0
                    for index, p in enumerate(js["releases"]):
                        print("Releases: " + str(p))
                        # convertir el json string a un hash md5
                        hash_datos = self._generar_publicador_hash(json.dumps(p))
                        print("HASH ARCHIVO JSON: " + hash_datos)
                        # ciclo para analizar el arreglos de json de los releases
                        #while hash_data:
                        print("LINEA ARCHIVO HASH {}: {} ".format(y, hash_data.rstrip()))
                        if not str(hash_data).rstrip() == str(hash_datos):
                               print("NO SON IGUALES")
                             #if index != (lineas2 - 1):
                                #archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a", encoding='utf-8')
                                #archivo_hash.writelines(hash_datos + '\n')
                        else:
                            print("RELEASE HASH YA EXISTE, NO TIENE CAMBIOS")
                        hash_data = archivohash.readline()
                        # Acumulador
                        y = y + 1
                        # Se cierra el archivo HASH
                archivohash.close()

    # Metodo que ejecuta el flujo de Armar Archivos para Procesar en Kingfisher
    def ejecutar(self):
        # ser recorren todos los origenes del publicador
        for origen in self.__origenes:
            # Se obtiene el directorio de descarga del archivo JSON del Publicador y Sistema
            __directorio = self.__obtener_publicador_directorio_json(origen)
            log.registrar_log_info(__name__,
                                   err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                   'ARMAR ARCHIVOS',
                                   'Directorio del Archivo JSON: '
                                   + __directorio)

            # Se obtiene el archivo JSON del Publicador y Sistema
            __archivo_json = self.__obtener_publicador_archivo_json(__directorio)
            log.registrar_log_info(__name__,
                                   err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                   'ARMAR ARCHIVOS',
                                   'Archivo JSON a preparar: '
                                   + str(__archivo_json[0]))

            # Se obtiene el directorio HASH del Publicador y Sistema
            __directorio_hash = self.__obtener_publicador_directorio_hash(origen)
            util.EdcaUtil.validar_directorio(__directorio_hash)
            log.registrar_log_info(__name__,
                                   err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                   'ARMAR ARCHIVOS',
                                   'Directorio del Archivo HASH: '
                                   + str(__directorio_hash))

            # Se procesa la lista de archivos
            for archivo in __archivo_json:
                log.registrar_log_info(__name__,
                                       err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       'ARMAR ARCHIVOS',
                                       'Iniciando a preparar Archivo JSON: '
                                       + str(__archivo_json[0]))

                # Se obtiene el tipo de JSON del archivo del Publicador
                __tipo = self.__obtener_publicador_tipo_archivo_json(origen)
                log.registrar_log_info(__name__,
                                       err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       'ARMAR ARCHIVOS', 'El Tipo de Archivo JSON es: '
                                       + __tipo)

                # Se evalua el tipo de archivo JSON del Publicador
                if 'release-package' == __tipo:
                    self.__preparar_json_release(origen, archivo)
                log.registrar_log_info(__name__,
                                       err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO,
                                       'ARMAR ARCHIVOS',
                                       'Preparacion de Archivo JSON: ' + archivo
                                       + ', Finalizado.')
