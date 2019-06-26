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

from edca_core import ArmarArchivosProcesar as bf
from edca_core import CargarArchivosKF as pf
from edca_core import DescargarArchivos as dl
from edca_core import Publicadores as pb
from edca_mensajes import EdcaErrores as err


# Clase principal para todo el proceso de carga de los publicadores


class Edca:

    # Constructor para configurar el publicador
    def __init__(self, publicador, nro_transaction):
        self.__publicador = publicador
        self.__nro_transaction = nro_transaction

    # Ejecutar el proceso general de descarga publicador y cargar a base datos edca
    def ejecutar(self):
        try:
            self.__validar_publicador()
            self.__descargar_archivos()
            self.__preparar_archivos()
            #self.__PrepararArchivosKF()
            self.__cargar_king_fisher()
        except Exception as ex:
            print(str(ex))

    # Funcion principal para la descarga de los releases del publicador
    def __descargar_archivos(self):
        dl.DescargarArchivos(self.__publicador, self.__nro_transaction).ejecutar()

    def __preparar_archivos(self):
        bf.ArmarArchivosProcesar(self.__publicador, self.__nro_transaction).ejecutar()

    # Funcion principal para preparar los archivos descargados del publicador
    #def __PrepararArchivosKF(self):
    #    kf.PrepararArchivosKF(self.__publicador, self.__nro_transaction).ejecutar()

    # Proceso principal para la carga de los releases al king Fisher (edca)
    def __cargar_king_fisher(self):
        pf.CargarArchivosKF(self.__publicador, self.__nro_transaction).ejecutar()

    # Valida si el publicador existe
    def __validar_publicador(self):
        # Validar que el publicador no sea nulo o este vacio
        if self.__publicador is None:
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_ISNULL)

        # Validar si el publicador existe.
        if not pb.Publicadores().existe_publicador(self.__publicador):
            raise Exception(err.EdcaErrores.ERR_PUBLISHER_NOTFOUND)

    # Registrar bitacora del main o clase princial
    @staticmethod
    def __registrar_bitacora(evento):
        return evento
