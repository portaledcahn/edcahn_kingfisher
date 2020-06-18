"""
PROYECTO : Portal EDCA-HN
NOMBRE : EdcaErrores
Descripcion : Clase con las constantes o catologo de errores
    manejados por el negocio o proceso.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""


class EdcaErrores(object):
    ERR_PUBLISHER_NOTFOUND = "EDCA-00001"
    ERR_PUBLISHER_ISNULL = "EDCA-00002"

    # Codigos para el modulo de descarga
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_SCHEDULER_START = "EDCA-J0001"

    # Codigos para el modulo de descarga
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_DOWNLOAD_BEGIN = "EDCA-D0002"
    INFO_DOWNLOAD_URL_FILE = "EDCA-D0001"
    INFO_DOWNLOAD_END = "EDCA-D0003"
    INFO_DOWNLOAD_DIR_FILE = "EDCA-D0004"
    ERR_DOWNLOAD_CONNECTION_REFUSED = "EDCA-D0005"
    ERR_DOWNLOAD_CONNECTION_ABORT = "EDCA-D0006"
    ERR_DOWNLOAD_CONNECTION_RESET = "EDCA-D0007"
    ERR_DOWNLOAD_CONNECTION_ERROR = "EDCA-D0008"
    ERR_DOWNLOAD_NOFORMATFILE = "EDCA-D00009"

    # Codigos para el modulo de Bitacora
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_BITACORA_SUCCESS_TXN = "EDCA-B0003"
    INFO_BITACORA_FAIL_TXN = "EDCA-B0004"
    INFO_BITACORA_OPEN_CONNECTION = "EDCA-B0001"
    INFO_BITACORA_CLOSE_CONNECTION = "EDCA-B0002"
    INFO_BITACORA_UPD_SEQ = "EDCA-B0005"

    # Codigos para el modulo de Publicadores
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_PUBLISHER_DIR_CREATED = "EDCA-P0001"
    ERR_PUBLISHER_DIR_NOT_EXIST = "EDCA-P0002"

    ERR_PUBLISHER_NOSOURCE = "EDCA-00004"
    ERR_PUBLISHER_SOURCE_NOURL = "EDCA-00005"
    ERR_PUBLISHER_NOPATH = "EDCA-00007"
    ERR_PUBLISHER_NOFILENAME = "EDCA-00006"
    ERR_ZIPTOOL_UNZIP = "EDCA-Z0004"
    ERR_ZIPTOOL_FILE_NOTFOUND = "EDCA-Z0005"
    # ERR_DOWNLOAD_NOFORMATFILE = "EDCA-00010"
    ERR_FILE_NOT_FOUND = "EDCA-00012"
    ERR_FILE_CERO_BYTES = "EDCA-00013"

    INFO_ZIPTOOL_UNZIP = "EDCA-Z0001"
    INFO_ZIPTOOL_UNZIP_FILE = "EDCA-Z0002"
    INFO_ZIPTOOL_PRINT_DIR = "EDCA-Z0003"
    INFO_ZIPTOOL_CLEAN_FILES = "EDCA-Z0006"
    INFO_BUILD_FILEFROMKF_BEGIN = "EDCA-00016"
    INFO_BUILD_FILEFROMKF_END = "EDCA-00017"
    INFO_LOAD_FILEFROMKF_BEGIN = "EDCA-00018"
    INFO_LOAD_FILEFROMKF_END = "EDCA-00019"

    # Codigos para el modulo de Base de Datos
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_DATABASE_CONN_OPEN = "EDCA-DB001"
    INFO_DATABASE_CONN_CLOSE = "EDCA-DB002"
    INFO_DATABASE_TXN_START = "EDCA-DB003"
    INFO_DATABASE_TXN_END = "EDCA-DB004"
    INFO_DATABASE_TXN_COMMIT = "EDCA-DB005"
    INFO_DATABASE_TXN_ROLLBACK = "EDCA-DB006"
    ERR_DATABASE_MESSAGE = "EDCA-DB007"

    # Codigos para el modulo de Base de Datos
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_ARMAR_ARCHIVOS_GENERICO = "EDCA-AK001"

    # Codigos para el modulo de descarga
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_CARGAR_ARCHIVOS_GENERICO = "EDCA-CK001"

    # Codigo de Finalizacion Carga de KingFisher
    # Tipos de Eventos: Informativo (INFO)
    #                   Error (ERR)
    INFO_FIN_KF = "EDCA-KF002"


    # Codigo de Mensajes para los Threads
    # Tipos de Eventos : Informativo (INFO)
    #                    Error (ERR)
    INFO_OCDS_HUNTER_THREAD_START = "EDCA-TH001"
    INFO_OCDS_HUNTER_THREAD_LOCK = "EDCA-TH002"
    INFO_OCDS_HUNTER_THREAD_UNLOCK = "EDCA-TH003"
    INFO_OCDS_HUNTER_THREAD_FINISH = "EDCA-TH004"
    INFO_OCDS_HUNTER_THREAD_GENERAL = "EDCA-TH005"

