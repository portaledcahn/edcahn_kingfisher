import psycopg2
import psycopg2.extras
from edca_bitacora.conector_bitacora import ConectorBitacora
from edca_logs.EdcaLogger import EdcaLogger as log
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg


class DaBitacora:
    # Constructor
    def __init__(self):
        cfg = ConectorBitacora()
        self.__servidor = cfg.obt_servidor()
        self.__bd = cfg.obt_bd()
        self.__esquema = cfg.obt_esquema()
        self.__usuario = cfg.obt_usuario()
        self.__pwd = cfg.obt_pwd()
        self.conn = psycopg2.connect(dbname=self.__bd, user=self.__usuario, host=self.__servidor, password=self.__pwd)

        # Creacion del objeto cursor el cual permite ejecutar querys en la base de datos
        # cur = self.conn.cursor()

        # Validacion del esquema
        # if self.__esquema is not None and self.__esquema != '':
        #    cur.execute("Esquema de Base de Datos No Encontrado {}".format(self.__esquema))

    # Metodo para obtener la conexion a la base de datos
    def obt_conexion(self):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_DATABASE_CONN_OPEN,
                               "DATABASE", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DATABASE_CONN_OPEN))
        return self.conn

    # Metodo para obtener todos los registros
    def obt_multiples_registros(self, query):
        cur = self.__ejecutar_sql(query)
        rows = cur.fetchall()
        return rows

    # Metodo para obtener un solo registro
    def obt_registro(self, query):
        cur = self.__ejecutar_sql(query)
        rows = cur.fetchone()
        return rows

    # Execute the query and return the cursor object
    def __ejecutar_sql(self, query):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        return cur

    # Metodo privado para confirmar la transaccion
    def __confirmar_transaccion(self):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_DATABASE_TXN_COMMIT,
                               "DATABASE", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DATABASE_TXN_COMMIT))
        return self.conn.commit()

    # Metodo privado para reversar la transaccion
    def __revertir_transaccion(self):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_DATABASE_TXN_ROLLBACK,
                               "DATABASE", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DATABASE_TXN_ROLLBACK))
        return self.conn.rollback()

    # Metodo para cerrar la conexion obtenida
    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_DATABASE_CONN_CLOSE,
                                   "DATABASE", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_DATABASE_CONN_CLOSE))

    # Metodo para Actualizar la sequencia de la tabla enviada para registrar
    # las transacciones en la bitacora
    def actualizar_sequencia(self, funcion, tabla, seq_anterior, seq_actual):
        cur = self.conn.cursor()
        try:
            cur.callproc(funcion, (tabla, seq_anterior, seq_actual))
            self.__confirmar_transaccion()
            # log.registrar_log_info(__name__, err.EdcaErrores.INFO_BITACORA_UPD_SEQ,
            #                       "BITACORA", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_BITACORA_UPD_SEQ))
            return cur
        except psycopg2.Error as dbError:
            log.registrar_log_exception(__name__,
                                        ("Codigo Error: " + str(dbError.pgcode) + " Mensaje: " + dbError.pgerror))

    # Insertar
    def guardar_datos(self, query):
        cur = self.conn.cursor()
        try:
            cur.execute(query=query)
            # log.registrar_log_info(__name__, err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN,
            #                       "BITACORA", msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN))
            self.__confirmar_transaccion()
            return cur
        except psycopg2.Error as dbError:
            log.registrar_log_exception(__name__,
                                        ("Codigo Error: " + str(dbError.pgcode) + " Mensaje: " + dbError.pgerror))
