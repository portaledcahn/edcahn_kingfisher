"""
PROYECTO : Portal EDCA-HN
NOMBRE : CargarArchivosKF
Descripcion : Clase destinada para la cargar de los archivos JSON Line
    a la base de datos del King Fisher
    consiste en las siguiente etapas.
        1. recuperar directorio, tipo archivo json y id collection
        2. cargar los archivo segun los parametros
        3. limipar y mover archivos a historico
        4. generar record package

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

import os

from edca_core import Publicadores as pb
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_utilitarios import EdcaUtil as util, ZipTools as zp
from edca_logs.EdcaLogger import EdcaLogger as log


class CargarArchivosKF:
    # Tag para identificar el evento del log
    __event_log = "Cargar KingFisher"

    # Constructor
    def __init__(self, publicador, nro_transaccion):
        self.__publicador = publicador
        self.__nro_transaccion = nro_transaccion
        self.__origenes = self.__obtener_origenes(self.__publicador)
        self.__msg = msg.EdcaMensajes()

    # Ejecutar el proceso o flujo de cargar al King Fisher
    def ejecutar(self):
        try:
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_LOAD_FILEFROMKF_BEGIN, self.__event_log, "======= ETAPA 3 =======")

            # Cursor para recorrer todos los origen o sistemas del publicador, 
            # el objetivo es por origen cargar los archivos JSon procesados al King Fisher
            for origen in self.__origenes:
                # se obtiene el directorio de carga king fisher del origen
                __directorio_carga = self.__obtener_directorio_kingfisher(origen)
                # se obtiene el formato del archivo json segun el origen o sistema
                __tipo_archvio_json = self.__obtener_tipo_archivo_json(origen)
                # se obtiene el numero ID Collection del publicador.
                __id_collection = self.__obtener_id_collection()
                
                # Log para ver los parametros
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "ID Collection = " + str(__id_collection) + ", Directorio = " + __directorio_carga + " Tipo Archivo = " + __tipo_archvio_json)

                # Cargar los archivos json al king fisher
                self.__cargar_kingfisher(__directorio_carga, __tipo_archvio_json, __id_collection)

                # Mover los archivos a la carpeta de historico
                self.__mover_archivos_historico(origen, __directorio_carga)

                # Eliminar los archivos JSon de la carpeta de carga
                #self.__limpiar_carpeta(__directorio_carga)

                # Generar el archivo de releases package para descarga masiva
                self.__generar_achivo_masivo()

            # log para indicar el inicio del proceso de cargar archivos al king fisher
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_LOAD_FILEFROMKF_END, self.__event_log, None)
        
        except Exception as ex:
            #self.__registrar_bitacora(ex)
            raise ex

    # Recuperar los origenes o sistemas de los Publicadores
    def __obtener_origenes(self, publicador):
        return pb.Publicadores.origenes(publicador)

    # Obtener el directorio king fisher del origen para la carga de los JSon
    def __obtener_directorio_kingfisher(self, origen):
        return pb.Publicadores.publicador_directorio_kingfisher(origen)

    # Obtener el directorio historial del origen o sistema.
    def __obtener_directorio_historico(self, origen):
        return pb.Publicadores.publicador_directorio_historico(origen)

    # obtener el tipo de archivos json del origen
    def __obtener_tipo_archivo_json(self, origen):
        return pb.Publicadores.publicador_tipo_archivo_json(origen)

    # Obtener el directorio king fisher del origen para la carga de los JSon
    def __obtener_id_collection(self):
        return pb.Publicadores.publicador_kf_id_collection(self.__publicador)

    # Obtener el directorio king fisher del origen para la carga de los JSon
    def __obtener_id_collection_record(self):
        return pb.Publicadores.publicador_kf_id_collection_record(self.__publicador)

    # Cargar los archivos JSon al King Fisher
    def __cargar_kingfisher(self, directorio, tipo, id):
        # Armar la sentensia para carcar el King Fisher segun los parametros
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "python ocdskingfisher-process-cli local-load " + str(id) + " " + directorio + " " + tipo)
        #os.system("python ocdskingfisher-process-cli local-load " + str(id) + " " + directorio + " " + tipo)        

        # Cerrar la collection
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "python ocdskingfisher-process-cli end-collection-store " + str(id))
        #os.system("python ocdskingfisher-process-cli end-collection-store " + str(id))
        
        # Recuperar los ID Collection tipo record
        __record_id_colletion = self.__obtener_id_collection_record()

        # Transformar a Releses Record Package
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "python ocdskingfisher-process-cli transform-collection " + str(__record_id_colletion))
        #os.system("python ocdskingfisher-process-cli transform-collection " + str(__record_id_colletion))
    
    def __mover_archivos_historico(self, origen, directorio):
        # obtener la carpeta historica del origen o sistema
        __directorio_historico = self.__obtener_directorio_historico(origen)
        
        # Copiar los archivos a la carpeta historica
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "Copiando JSON de " + directorio + " --> " + __directorio_historico)        
        util.EdcaUtil.move_file_to("*", directorio, __directorio_historico) # utilitario para mover los archivos json al una carpeta destino
        # Comprimir todos los archivos json en la carpeta historico
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "Comprimiendo los JSON historicos a ZIP")        
        for archivo in self.__obtener_archivos(__directorio_historico): # obtener todos los json file del historico
            # comprimir archivo
            zp.ZipTools.comprimir(archivo, __directorio_historico)
            # borrar todos los archviso JSon dejando exclusivo los ZIP
            util.EdcaUtil.borrar_archivo(archivo)
        
    # funcion que permite borrar o limpiar la carpeta de carga king fisher
    def __limpiar_carpeta(self, directorio):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_CARGAR_ARCHIVOS_GENERICO, self.__event_log, "Limpiar los archivos JSON de " + directorio)
        # Borrar todos los archivos
        for archivo in self.__obtener_archivos(directorio): # obtener todos los json file del historico
            # borrar todos los archviso JSon dejando exclusivo los ZIP
            util.EdcaUtil.borrar_archivo(archivo)
    
    # funcion para genera el archivo masivo de releses package
    def __generar_achivo_masivo(self):
        pass
    
    # funcion para recupera todos los archivos de un directorio
    def __obtener_archivos(self, directorio):
        return util.EdcaUtil.obtener_lista_archivos(directorio, '.json')

    # Registrar bitacora del main o clase princial
    def __registrar_bitacora(self, code, event, detail):
        #print("Code : " + code + " Event : " + event + " Detail : " + detail) 
        log.registrar_log_info(__name__, code, event, detail)

    # Registrar bitacora del main o clase princial
    def __registrar_bitacora(self, ex):
        #print(ex) 
        if hasattr(ex, 'message'):
            log.registrar_log_exception(__name__, ex.mensaje)
        