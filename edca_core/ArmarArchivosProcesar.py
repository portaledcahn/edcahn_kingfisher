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
import datetime
import uuid

from edca_core import Publicadores as pb
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_utilitarios import EdcaUtil as util, ZipTools as zp
from edca_logs.EdcaLogger import EdcaLogger as log
from config import edca_global_config as cfg

class ArmarArchivosProcesar():
    __event_log = "Praparar Achivos para KF"

    def __init__(self, publicador, nro_transaccion):
        self.__publicador = publicador
        self.__nro_transaccion = nro_transaccion
        self.__origenes = self.__obtener_origenes(self.__publicador)
        self.__msg = msg.EdcaMensajes()

    def ejecutar(self):
        try:
            # Log para informar que inicio el proceso de preparar archivos al king fisher
            # print("")
            # print("======= ETAPA 2 =======")
            # print(err.EdcaErrores.INFO_BUILD_FILEFROMKF_BEGIN + " : " + self.__msg.getMessageError(err.EdcaErrores.INFO_BUILD_FILEFROMKF_BEGIN))
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_BUILD_FILEFROMKF_BEGIN, self.__event_log, "======= ETAPA 2 =======")

            # ser recorren todos los origenes del publicador
            for origen in self.__origenes:
                __directorio = self.__obtener_ruta_descarga(origen) # se obtiene el directorio donde estan los archivos
                __archivos = self.__obtener_archivos(__directorio) # se obtiene la lista de los archivos json
                # se lee la lista de archivos.
                for archivo in __archivos:
                    #print("Leer : " + archivo)
                    log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log, "Leer : " + archivo)
                    # se recupera el tipo de archivo json
                    __tipo = self.__obtener_tipo_archivo_json(origen)
                    if cfg.tipo_archivo_json_line == __tipo: # funcion para evaluar json line
                        self.__evaluar_archivo_tipo_jsonline(origen, archivo)
                    if cfg.tipo_archivo_releasepackage == __tipo: # funcion para evaluar release package
                        self.__evaluar_archivo_tipo_release(origen, archivo)
                    # print("Archivo leido : " + archivo)
                    log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log, "Archivo leido : " + archivo)

            # mensaje de consola para informar que finalizo el proceso de preparar archivos al king fisher
            #print(err.EdcaErrores.INFO_BUILD_FILEFROMKF_END + " : " + self.__msg.getMessageError(err.EdcaErrores.INFO_BUILD_FILEFROMKF_END))
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_BUILD_FILEFROMKF_END, self.__event_log, None)
        except Exception as ex:
            self.__registrar_bitacora(ex)

    # Recuperar los origenes o sistemas de los Publicadores
    def __obtener_origenes(self, publicador):
        return pb.Publicadores.origenes(publicador)

    # Recuperar la ruta o direccion donde se guardara los archivo descargados
    def __obtener_ruta_descarga(self, origen):
        __directorio = pb.Publicadores.origen_directorio(origen)
        if __directorio is None:
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOPATH)
        return __directorio

    # funcion para recupera todos los archivos de un directorio
    def __obtener_archivos(self, directorio):
        return util.EdcaUtil.obtener_lista_archivos(directorio, '.json')

    # se evalua el archivo, extraendo los releases para ser validados por un hash
    def __evaluar_archivo_tipo_jsonline(self, origen, archivo):
        # abrir el archivo json descargado del origen
        with open(archivo, "r") as archivojson:
            data = archivojson.read()
        
        # deserializando el string a json
        js = json.loads(data)
        
        # archivo destino para cargar los json al king fisher
        outfile = open(self.__obtener_directorio_kingfisher(origen) + archivo, "a")
        # archivo hash para agregar los nuevos hash
        archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a")
        
        l = 0 # contador 

        # ciclo para analizar cada linea json
        for p in js:
            hs = self.__obtener_hash(json.dumps(p)) # convertir el json string a un hash md5
            # buscar el hash en el archivo hash
            if not self.__buscar_hash(origen, hs): # de no existir el hash
                # pasar el json string al nuevo archivo para cargarlo al king fisher
                outfile.writelines(json.dumps(p) + ",\n") 
                archivo_hash.writelines(hs + "\n") # guardar el nuevo hash
        
        outfile.close() # cerrar archivo de json para el king fisher
        archivo_hash.close() # cerrar archivo de hash
        archivojson.close() # cerrar archivo json origen

    # se evalua el archivo, extraendo los releases para ser validados por un hash
    def __evaluar_archivo_tipo_release(self, origen, archivo):
        #print("evaluar archivo tipo release")
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log, "evaluar archivo tipo release")

        # abrir el archivo json descargado del origen
        with open(archivo, "r") as archivojson:
            data = archivojson.read()
        # deserializando el string a json
        js = json.loads(data)
        jx = json.loads(data) # copia del archivo.
        
        jx["releases"] = [] # limpiar el arreglo de releases del archivo para carga king fisher
        
        # archivo hash para agregar los nuevos hash
        archivo_hash = open(pb.Publicadores.publicador_archivo_hash(origen), "a")

        l = 0 # contador para saber si hay nuevos releases para cargar
        # ciclo para analizar el arreglos de json de los releases
        for p in js["releases"]:
            hs = self.__obtener_hash(json.dumps(p)) # convertir el json string a un hash md5
            if not self.__buscar_hash(origen, hs):
                l = l + 1 # contando cada releases nuevo
                archivo_hash.writelines(hs + "\n") # guardar el nuevo hash
                jx["releases"].append(p) # agregando el releases nuevo
        
        #print("Cantidad de releases a cargar al kingFisher = " + str(l))
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log, "Cantidad de releases a cargar al kingFisher = " + str(l))

        if l != 0: # hay nuevos releases?
            # guardar el release package en el archivo destino para cargar al king fisher
            outfile_name = self.__obtener_directorio_kingfisher(origen) + origen + "_" + str(uuid.uuid4()) + ".json"
            with open(outfile_name, 'w') as outfile:  
                json.dump(jx, outfile)
            #print("Listo para cargar : " + outfile_name)
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ARMAR_ARCHIVOS_GENERICO, self.__event_log, "Listo para cargar : " + outfile_name)
            outfile.close() # cerrar archivo de json para el king fisher

        archivo_hash.close() # cerrar archivo de hash
        archivojson.close() # cerrar archivo json origen

    # buscar el hash en el archivo de hash
    def __buscar_hash(self, origen, hsh):
        archivo = pb.Publicadores.publicador_archivo_hash(origen)
        if hsh in open(archivo,"r").read():
            return True
        return False

    # convierte el json string en un hash md5
    def __obtener_hash(self, str):
        return util.EdcaUtil().string_to_hash(str)

    # obtener el tipo de archivos json del origen
    def __obtener_tipo_archivo_json(self, origen):
        return pb.Publicadores.publicador_tipo_archivo_json(origen)

    # Obtener el directorio para colocar los archivos y cargar al king fisher
    def __obtener_directorio_kingfisher(self, origen):
        return pb.Publicadores.publicador_directorio_kingfisher(origen)
        
    # recupera el archivo archivo de los json hash
    def __obtener_archivo_hash(self, origen):
        return pb.Publicadores.publicador_archivo_hash(origen)

    # Registrar bitacora del main o clase princial
    def __registrar_bitacora(self, code, event, detail):
        #print("Code : " + code + " Event : " + event + " Detail : " + detail) 
        log.registrar_log_info(__name__, code, event, detail)

    # Registrar bitacora del main o clase princial
    def __registrar_bitacora(self, ex):
        #print(ex) 
        if hasattr(ex, 'message'):
            log.registrar_log_exception(__name__, ex.mensaje)
        