"""
PROYECTO : Portal EDCA-HN
NOMBRE : ZipTools
Descripcion : Clase utilitaria para descomprimir archivos ZIP.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

import zipfile
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_logs.EdcaLogger import EdcaLogger as log


class ZipTools:

    # Funcion para cromprimir los archivos descargados
    @staticmethod
    def comprimir(archivo, dir_comprimir):
        __archivo_zip = archivo[:archivo.find(".")] + ".zip"
        try:
            with zipfile.ZipFile(__archivo_zip,'w', zipfile.ZIP_DEFLATED) as archivoZip:
                archivoZip.write(archivo)
            archivoZip.close()

        except PermissionError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_ZIPTOOL_UNZIP) % PermissionError.filename % PermissionError.strerror)
        except IOError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(
                                        err.EdcaErrores.ERR_ZIPTOOL_UNZIP) % IOError.filename % IOError.strerror)
    
    # Funcion para descromprimir los archivos descargados
    @staticmethod
    def descomprimir(archivo, dir_extraer):
        try:
            zip_ref = zipfile.ZipFile(archivo, 'r')
            zip_list = zip_ref.infolist()
            for contenido in zip_list:
                log.registrar_log_info(__name__, err.EdcaErrores.INFO_ZIPTOOL_PRINT_DIR,
                                       "EXTRAER ARCHIVO",
                                       msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_ZIPTOOL_PRINT_DIR) % contenido.filename)
            zip_ref.extractall(dir_extraer)
            zip_ref.close()
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                   msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_ZIPTOOL_UNZIP))
        except PermissionError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_ZIPTOOL_UNZIP) % PermissionError.filename % PermissionError.strerror)
        except IOError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(
                                        err.EdcaErrores.ERR_ZIPTOOL_UNZIP) % IOError.filename % IOError.strerror)

    @staticmethod
    def obtener_contenido_zip(archivo):
        global zp
        try:
            zip_ref = zipfile.ZipFile(archivo, 'r')
            zip_list = zip_ref.infolist()
            for contenido in zip_list:
                zp = contenido.filename
            zip_ref.close()
            return zp
        except PermissionError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.ERR_ZIPTOOL_UNZIP)
                                    % PermissionError.filename % PermissionError.strerror)
        except IOError:
            log.registrar_log_error(__name__, err.EdcaErrores.ERR_ZIPTOOL_UNZIP, "EXTRAER ARCHIVO",
                                    msg.EdcaMensajes.obt_mensaje(
                                        err.EdcaErrores.ERR_ZIPTOOL_UNZIP) % IOError.filename % IOError.strerror)

