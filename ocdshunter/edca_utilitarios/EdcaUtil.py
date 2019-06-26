# Portal EDCA-HN
# Name :
# Description :
#
# MM/DD/YYYY    Collaborators   Descriptions
# 05/07/2019    Alla Duenas     Initial Code    

import hashlib
import os
import shutil
import ntpath

from pathlib import Path
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_logs.EdcaLogger import EdcaLogger as log


class EdcaUtil:

    @staticmethod
    def armar_nombre_archivo(nombre_archivo):
        return nombre_archivo

    def string_to_hash(self, cadena):
        return self.__convert_str_to_md5(cadena)

    # funcion para convertir el string en un hash
    @staticmethod
    def __convert_str_to_md5(cadena):
        h = hashlib.md5()
        h.update(cadena.encode('utf-8'))
        return h.hexdigest()

    # funcion para validar si el directorio existe, si no existe lo crea
    @staticmethod
    def validar_directorio(directorio):
        if not os.path.exists(directorio):
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_PUBLISHER_DIR_NOT_EXIST,
                                    "VALIDAR PUBLICADOR",
                                    msg.EdcaMensajes.obt_mensaje(
                                        err.EdcaErrores.ERR_PUBLISHER_DIR_NOT_EXIST) % directorio)
            os.makedirs(directorio)
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_PUBLISHER_DIR_CREATED,
                                   "VALIDAR PUBLICADOR",
                                   msg.EdcaMensajes.obt_mensaje(
                                       err.EdcaErrores.INFO_PUBLISHER_DIR_CREATED) % directorio)

    # Funcion para validar si el archivo descargado existe
    @staticmethod
    def validar_existe_archivo(archivo):
        __archivo = Path(archivo)
        if __archivo.is_file():
            return True
        else:
            return False

    # Funcion para valida si el archivo descargado es 0 bytes
    @staticmethod
    def validar_cerobytes_archivo(archivo):
        if os.stat(archivo).st_size == 0:
            return True
        else:
            return False

    # Funcion para borrar un archivo
    @staticmethod
    def borrar_archivo(archivo):
        os.remove(archivo)
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ZIPTOOL_CLEAN_FILES,
                               "LIMPIAR ZIP",
                               msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_ZIPTOOL_CLEAN_FILES) % archivo)

    # funcion para obtener el listado de archivos de un directorio
    @staticmethod
    def obtener_lista_archivos(directorio, extension):
        # Se inicializa el arreglo
        __archivos = []

        # Se obtiene la lista de archivos del directorio
        for archivo in os.listdir(directorio):
            # Se busca unicamente con la extension JSON
            if archivo.endswith(extension):
                __archivos.append(os.path.join(directorio, archivo))
                return __archivos
        # se manda limpio el arreglo en caso de no encontrar archivos
        __archivos = None

    # funcion para obtener el listado de archivos de un directorio
    @staticmethod
    def obtener_lista_solo_archivos(directorio, extension):
        # Se inicializa el arreglo
        __archivos = []
        # Se obtiene la lista de archivos del directorio
        for archivo in os.listdir(directorio):
            # Se busca unicamente con la extension JSON
            if archivo.endswith(extension):
                __archivos.append(os.path.join(directorio, archivo))
                return __archivos

    # funcion para obtener el listado de archivos de un directorio
    @staticmethod
    def move_file_to(archivo, origen, destino):
        # print("mover : " + origen + " --> " + destino)
        if archivo != "*":
            shutil.move(origen + archivo, destino + archivo)

        # si el directorio origen tiene archivos para mover.
        if len(os.listdir(origen)) != 0:
            for file in EdcaUtil.obtener_lista_archivos(origen, ".json"):
                print("mover : " + file + " --> " + destino + EdcaUtil.path_leaf(file))
                shutil.move(file, destino + EdcaUtil.path_leaf(file))

    # Existen archivos JSon en directorio
    @staticmethod
    def existen_archivos_json(directorio):
        l = 0
        # Se obtiene la lista de archivos del directorio
        for archivo in os.listdir(directorio):
            # Se busca unicamente con la extension JSON
            if archivo.endswith(".json"):
                l = l + 1
        if l == 0:
            return False
        
        return True

    # funcion para obtener el listado de archivos de un directorio
    @staticmethod
    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)