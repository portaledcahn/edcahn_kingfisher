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

import datetime
import json
import time

txnId = 0


class TransaccionesBitacora:

    # Constructor
    def __init__(self, base, publicador, sistema, proceso, archivo):
        # Variable Protegida
        self.__tabla = 'EDCA_BITACORA'
        self.__publicador = publicador
        self.__sistema = sistema
        # Se instancia la clase database
        self.__base = base
        self.__obter_fecha_actual()
        self.__proceso = proceso
        self.__archivo = archivo

    # Metodo para obtener la sequencia anterior filtrado por tabla
    def __obt_sequencia_anterior(self, tabla):
        query = ("SELECT * FROM f_obtener_seq_anterior('" + tabla + "')")
        return self.__base.obt_registro(query)

    # Metodo para obtener la sequencia actual filtrado por tabla
    def __obt_sequencia_actual(self, tabla):
        query = ("SELECT * FROM f_obtener_seq_actual('" + tabla + "')")
        return self.__base.obt_registro(query)

    # Metodo para actualizar la sequencia filtrado por tabla
    def __upd_sequencia(self, tabla, seqanterior, seqactual):
        # Nombre de la funcion creada en la base de datos el cual es enviado como parametro
        funcion = 'f_upd_sequencia'
        return self.__base.actualizar_sequencia(funcion, tabla, str(seqanterior), str(seqactual))

    # Funcion para formatear la fecha en yyyymmdd
    @staticmethod
    def __txn_fecha(fecha):
        formato_fecha = "%Y%m%d"
        _formato_fecha = datetime.datetime.strftime(fecha, formato_fecha)
        _formato_hora = time.strftime("%H%M%S")
        _formato = (_formato_fecha + "." + _formato_hora)
        return _formato

    # Funcion para formatear la fecha en DD-MM-YYYY HH12:MI:SS
    @staticmethod
    def __json_fecha(fecha):
        formato_fecha = "%d/%m/%Y"
        _formato_fecha = datetime.datetime.strftime(fecha, formato_fecha)
        _formato_hora = time.strftime("%I:%M %p")
        _formato = (_formato_fecha + " " + _formato_hora)
        return _formato

    # Funcion para Obtener la fecha actual
    @staticmethod
    def __obter_fecha_actual():
        _fecha = datetime.date.today()
        return _fecha

    # Funcion para construir la transaccion
    def __construir_txnid(self):
        _fecha_actual = self.__obter_fecha_actual()
        _fecha = self.__txn_fecha(_fecha_actual)
        _actual = self.__obt_seq_actual()
        _txn = (self.__publicador + "." + str(_fecha) + "." + str(_actual[0]))
        self.__guardar_sequencia()
        return _txn

    # Metodo para obtener todos los codigos de la bitacora
    def _getCatalogoBitacora(self):
        query = "SELECT Codigo_Bitacora, Descripcion_Bitacora FROM edca.edca_catalogo_bitacora"
        return self.__base.obt_registro(query)

    def _obt_EdcaHistorico(self):
        query = "SELECT tabla FROM edca.edca_secuencias"
        return self.__base.obt_multiples_registros(query)

    # Se obtiene el valor de la sequencia anterior
    def __obt_seq_anterior(self):
        query = ("SELECT * FROM edca.f_obtener_seq_anterior('" + self.__tabla + "')")
        return self.__base.obt_registro(query)

    # Se obtiene el valor de la sequencia actual
    def __obt_seq_actual(self):
        query = ("SELECT * FROM edca.f_obtener_seq_actual('" + self.__tabla + "')")
        return self.__base.obt_registro(query)

    # Se procede actualizar la sequencia en la tabla
    def __guardar_sequencia(self):
        _funcion = 'edca.f_upd_sequencia'
        _anterior = self.__obt_seq_anterior()
        _actual = self.__obt_seq_actual()
        return self.__base.actualizar_sequencia(_funcion, self.__tabla, str(_anterior[0]), str(_actual[0]))

    def __obt_txnid(self):
        # Se obtiene el ID de la Transaccion
        txn = self.__construir_txnid()
        global txnId
        txnId = txn
        return txn

    @property
    def obtener_txn(self):
        return txnId

    def guardar_bitacora(self):
        _funcion = 'edca.f_insertar_bitacora'
        _txnId = self.__obt_txnid()
        _fecha_actual = self.__obter_fecha_actual()
        _json_fecha = self.__json_fecha(_fecha_actual)
        _proceso = self.__proceso
        _nombre_archivo = self.__archivo
        _tipo_alerta = 'INFO'
        _json_log = {"Publicador": str(self.__publicador),
                     "Sistema": self.__sistema,
                     "Fecha": str(_json_fecha),
                     "Tipo Alerta": str(_tipo_alerta),
                     "Proceso": str(_proceso),
                     "Mensaje": "El Archivo: " + str(_nombre_archivo) + ", descargado correctamente"
                     }
        log = json.dumps(_json_log)
        query = "SELECT * FROM " + 'edca.f_insertar_bitacora' \
                + "('" + str(_txnId) + "'," \
                + "'" + str(1) + "','" \
                + str(1) + "'," + "'" \
                + log + "','ocdskingfisher')"
        return self.__base.guardar_datos(query)


