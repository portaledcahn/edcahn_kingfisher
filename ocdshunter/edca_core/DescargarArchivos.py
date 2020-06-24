"""
PROYECTO : Portal EDCA-HN
NOMBRE : DescargarArchivos
Descripcion : Clase para la descarga de los origenes o sistemas
    de los Publicadores, realizar el proceso de descarga y descomprension
    y listo para preprocesar los archivos.

    1. Recuperar los URL para descargar los archivos zip de los JSon de los publicadores
    2. Descargar los archivos ZIP en la carpeta descaga
    3. Descomprimir los archivos ZIP y dejar los archivos json para su analisis
    4. Eliminar los archivos ZIP
    
    se registra en Log y bitacoras de todos los movimientos en el proceso.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

import sys
import datetime
import requests
from config import edca_global_config as glb
from edca_core import Publicadores as pb
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_utilitarios import EdcaUtil as util, ZipTools as zp
from edca_logs.EdcaLogger import EdcaLogger as log
from edca_bitacora.da_bitacora import DaBitacora
from edca_bitacora.transacciones_bitacora import TransaccionesBitacora
from config import edca_global_config as cfg


# Clase Principal para la descarga de los archivos del publicador
# y preparacion de los mismo para la carga a la base de datos EDCA
class DescargarArchivos:

    def __init__(self, publicador, nro_transaccion):
        # inicializar variables 
        self.__publicador = publicador 
        self.__nro_transaccion = nro_transaccion
        # recuperar todos los origenes o sistemas del publicador.
        self.__origenes = self.__obtener_origenes(self.__publicador)

    # Ejecutar el proceso de descarga de los archivos del publicador
    def ejecutar(self):
        try:
            # Validaciones basicas.
            self.__validar_origenes()
            
            # recorre todos los origenes del publicador
            for origen in self.__origenes:
                # construir la url donde se encuentra el archivo para descargar del publicador
                __url = self.__obtener_url_origen(origen) + self.__armar_nombre_archivo_origen(origen)

                # construir el directorio y nombre del archivo destino descargado.
                __directorio = self.__obtener_ruta_descarga(origen)
                __archivo_destino = __directorio + self.__armar_nombre_archivo_destino(origen)
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_DOWNLOAD_URL_FILE, "DESCARGAR",
                                       "URL del archivo a descargar: %s" % __url)

                # Se valida si el directorio destino si existe
                self.__validar_directorio(__directorio)

                # Ejecuta herramienta utilitario para descargar archivo.
                self.__descargar_archivo(__url, __archivo_destino)
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_DOWNLOAD_DIR_FILE,
                                       "DESCARGAR",
                                       "Archivo descargado en directorio: %s" % __archivo_destino)

                # Se guarda el registro en la bitacora
                self.__registrar_bitacora(__archivo_destino)

                # Se procede a extraer el archivo json del zip descargado del publicador
                self.__descomprimir_zip(__archivo_destino, __directorio)

                # Se elimina el archivo ZIP para liberar espacio
                self.__eliminar_archivo_zip(__archivo_destino)

        except Exception as ex:
            log.registrar_log_exception(__name__, str(ex))

    # funcion GET del atributo Publicador
    def publicador(self):
        return self.__publicador

    # funcion GET del atributo Publicador
    def origen(self):
        return self.__origenes

    # Armar el nombre del archivo del origen para descargar.
    # esto permite renombrar los archivo ZIP descargados del publicador
    @staticmethod
    def __armar_nombre_archivo_origen(origen):
        archivo = str(pb.Publicadores.origen_nombre_archivo(origen))
        if archivo is None:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_PUBLISHER_NOFILENAME, "DESCARGAR",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_PUBLISHER_NOFILENAME))
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOFILENAME)
        return archivo.replace("{0}", str(datetime.date.today().year))

    # Armar el nombre del archivo del origen para descargar.
    # esto permite renombrar los archivo ZIP descargados del publicador
    def __armar_nombre_archivo_destino(self, origen):
        # {publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip
        archivo = str(pb.Publicadores.origen_archivo_destino(origen))
        if archivo is None:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_DOWNLOAD_NOFORMATFILE, "DESCARGAR",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_DOWNLOAD_NOFORMATFILE))
            raise Exception(err.EdcaErrores.ERR_DOWNLOAD_NOFORMATFILE)

        # Reemplazar el formato por los atributos.
        archivo = archivo.replace("{publisher}", self.__publicador.replace(".", "_"))
        archivo = archivo.replace("{source}", origen)
        archivo = archivo.replace("{yyyy}", str(datetime.date.today().year))
        archivo = archivo.replace("{mm}", str(datetime.date.today().month))
        archivo = archivo.replace("{dd}", str(datetime.date.today().day))
        archivo = archivo.replace("{hh24}", str(datetime.datetime.today().hour))
        archivo = archivo.replace("{mi}", str(datetime.datetime.today().minute))
        archivo = archivo.replace("{ss}", str(datetime.datetime.today().second))

        return archivo

    # Descargar archivo, proceso para descargar el archivo ZIP del origen del publicador
    @staticmethod
    def __descargar_archivo(url, file):
        try:
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_DOWNLOAD_BEGIN, "DESCARGAR",
                                   msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DOWNLOAD_BEGIN))
            with open(file, 'wb') as f:
                response = requests.get(url, stream=True)
                total = response.headers.get('content-length')

                if total is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50 * downloaded / total)
                        sys.stdout.write('\r[{}{}]'.format('=' * done, '.' * (50 - done)))
                        sys.stdout.flush()

            log.registrar_log_info(__name__, err.EdcaErrores.INFO_DOWNLOAD_END, "DESCARGAR",
                                   msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DOWNLOAD_END))

        except ConnectionRefusedError as refu:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_DOWNLOAD_CONNECTION_REFUSED, "CONNECTION REFUSED",
                                    refu.strerror)
        except ConnectionAbortedError as abor:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_DOWNLOAD_CONNECTION_ABORT, "CONNECTION ABORT",
                                    abor.strerror)
        except ConnectionResetError as rest:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_DOWNLOAD_CONNECTION_RESET, "CONNECTION RESET",
                                    rest.strerror)
        except ConnectionError as errs:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_DOWNLOAD_CONNECTION_ERROR, "CONNECTION ERROR",
                                    errs.strerror)

    # Recuperar los origenes o sistemas de los Publicadores
    @staticmethod
    def __obtener_origenes(publicador):
        return pb.Publicadores.origenes(publicador)

    # Recuperar la Url del origen del publicador donde se encuentran los archivos para descarga
    @staticmethod
    def __obtener_url_origen(origen):
        url = pb.Publicadores.origen_urls(origen)
        if url is None:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_PUBLISHER_SOURCE_NOURL, "DESCARGAR",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_PUBLISHER_SOURCE_NOURL))
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_SOURCE_NOURL)
        return url

    # Recuperar la ruta o direccion donde se guardara los archivo descargados
    @staticmethod
    def __obtener_ruta_descarga(origen):
        __directorio = pb.Publicadores.origen_directorio(origen)
        if __directorio is None:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_PUBLISHER_NOPATH, "DESCARGAR",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_PUBLISHER_NOPATH))
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOPATH)
        return __directorio

    # Validaciones de origen o sistemas del publicador
    def __validar_origenes(self):
        if self.__origenes is None:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_PUBLISHER_NOSOURCE, "DESCARGAR",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_PUBLISHER_NOSOURCE))
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOSOURCE)

    # Funcion para validar el directorio
    @staticmethod
    def __validar_directorio(directorio):
        util.EdcaUtil.validar_directorio(directorio)

    # Funcion para validar si el archivo descargado existe
    @staticmethod
    def __descomprimir_zip(archivo, directorio):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_ZIPTOOL_UNZIP_FILE, "EXTRAER ARCHIVO",
                               msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_ZIPTOOL_UNZIP_FILE).format(archivo,
                                                                                                            directorio))

        if not util.EdcaUtil.validar_existe_archivo(archivo):
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_FILE_NOTFOUND, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_ZIPTOOL_FILE_NOTFOUND))
            raise Exception(err.EdcaErrores.ERR_FILE_NOT_FOUND)

        # if not util.EdcaUtil.validar_cerobytes_archivo(archivo):
        #    log.registrar_log_error(__name__, err.EdcaErrores.ERR_FILE_CERO_BYTES, "EXTRAER ARCHIVO",
        #                            msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_FILE_CERO_BYTES))
        #    raise Exception(err.EdcaErrores.ERR_FILE_CERO_BYTES)

        # Se llama el metodo para extraer el archivo zip
        zp.ZipTools().descomprimir(archivo, directorio)

    # Eliminar archivos
    @staticmethod
    def __eliminar_archivo_zip(archivo):
        util.EdcaUtil.borrar_archivo(archivo)

    # Registrar Bitacora
    def __registrar_bitacora(self, archivo):
        # El archivo de configuracion indica si se gruarda bitacora.
        if not cfg.bitacora:
            return
            
        self.db = DaBitacora()

        __bitacora = TransaccionesBitacora(self.db,
                                           self.publicador(),
                                           self.origen(),
                                           glb.catalogo_download,
                                           zp.ZipTools.obtener_contenido_zip(archivo))
        __bitacora.guardar_bitacora()
        __txnid = __bitacora.obtener_txn
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN,
                               "BITACORA",
                               msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN).format(__txnid))
