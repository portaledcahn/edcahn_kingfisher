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

from config import base_de_datos


class ConectorBitacora:

    def __init__(self):
        self.__servidor = base_de_datos.servidor
        self.__bd = base_de_datos.nombre_db
        self.__esquema = base_de_datos.nombre_schema
        self.__usuario = base_de_datos.usuario
        self.__pwd = base_de_datos.password

    def obt_servidor(self):
        return self.__servidor

    def obt_bd(self):
        return self.__bd

    def obt_esquema(self):
        return self.__esquema

    def obt_usuario(self):
        return self.__usuario

    def obt_pwd(self):
        return self.__pwd
