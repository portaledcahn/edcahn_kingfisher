"""
PROYECTO : Portal EDCA-HN
NOMBRE : edca_global_config
Descripcion : Archivo de configuraciones globales para el proceso de carga

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

# parametro para habilitar la auditoria
auditoria = True
# parametro para habilitar la bitacora
bitacora = False
# parametro para habilitar la logger
logger = True
# parametro para habilitar guardar historico
historico = True

# Archivo looger
logger_file = '/home/adminaedca/portaledcahn_database/edcahn_kingfisher/edcahn/logs/edcahn_app.log'
logger_config_ini = 'edca_logs/EdcaLoggerConfig.ini'
logger_print_console = True

# Catalogo Bitacora
catalogo_connection = 1
catalogo_file_notfound = 2
catalogo_download = 3
catalogo_prepare_kingfisher = 4
catalogo_load_data_kingfisher = 5

# Catalogo de tipo archivo json
tipo_archivo_json_line = "release_package_json_lines"
tipo_archivo_releasepackage = "release_package"

lap_timer_run_process = 48