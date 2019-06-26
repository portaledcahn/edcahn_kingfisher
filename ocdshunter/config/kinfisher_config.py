"""
PROYECTO : Portal EDCA-HN
NOMBRE : edca_global_config
Descripcion : Archivo de configuraciones globales para el proceso de carga

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.
"""

# Parametros por defecto
kf_interprete = 'python'
kf_directorio = '/home/dba/kingfisher-process/'
kf_nombre_coleccion = 'OCDSHN'

# Comando para crear una collection
kf_comando_crear_coleccion = 'ocdskingfisher-process-cli new-collection {0} "{yyyy}-{mm}-{dd} {hh24}:{mi}:{ss}"'

# Comando para cargar los datos
kf_comando_cargar_json = 'ocdskingfisher-process-cli local-load {0}'

# Comando para cerrar la coleccion
kf_comando_cerrar_coleccion = 'ocdskingfisher-process-cli end-collection-store {0}'

# Comando para crear una coleccion de tipo RECORD
kf_comando_crear_records = 'ocdskingfisher-process-cli new-transform-record {0}'

# Comando para convertir los releases a records
kf_comando_convertir_releases = 'ocdskingfisher-process-cli transform-collection {0}'