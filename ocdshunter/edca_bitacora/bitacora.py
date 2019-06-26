"""
PROYECTO : Portal EDCA-HN
NOMBRE : Bitacora
Descripcion : 

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.
"""

from edca_bitacora.da_bitacora import DaBitacora
from edca_bitacora.transacciones_bitacora import TransaccionesBitacora
from config import edca_global_config as glb
from edca_utilitarios import ZipTools as zp
from edca_logs.EdcaLogger import EdcaLogger as log
from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from config import edca_global_config as cfn


class Bitacora:

    # Metodo para registrar en la bitacora
    @staticmethod
    def registrar_bitacora(publicador, origen, archivo):

        # Se valida si debe almacenar la transaccion en la base de datos
        if cfn.bitacora:
            db = DaBitacora()
            __bitacora = TransaccionesBitacora(db,
                                               publicador,
                                               origen,
                                               glb.catalogo_download,
                                               zp.ZipTools.obtener_contenido_zip(archivo))
            __bitacora.guardar_bitacora()
            __txnid = __bitacora.obtener_txn
            log.registrar_log_info(__name__, err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN,
                                   "BITACORA",
                                   msg.EdcaMensajes.obt_mensaje(err.EdcaErrores.INFO_BITACORA_SUCCESS_TXN).format(__txnid))
        else:
            log.registrar_log_info(__name__, "BT-0001",
                                   "BITACORA",
                                   "Registrar Bitacora esta: DESHABILITADO")