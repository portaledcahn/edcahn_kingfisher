"""
PROYECTO : Portal EDCA-HN
NOMBRE : publicadores_config
Descripcion : Archivo de configuraciones de los publicadores

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

# Publicadores para el portal EDCA Honduras.
# El publicador es una institucion, entidad u organizacion que publicar informacion sobre 
# compras y contratacion en el estandar OCDS,  "publicadores" es un arreglo para guardar un 
# identificador para cada publicador, como estandar se recomienda usar como inicio el acornimo
# del pais de origen del publicador ej: HN y seguido de las siglas significativas que indentifiquen
# a la institucion publicadora ej: SEFIN = Secretaria de Finanzas de Honduras. 
publicadores = ['HN.SEFIN', 'HN.ONCAE', 'HN.SISOCS']

# Sistemas origen de los publicadores.
# Los publicadores pueden tener varios origen, fuentes o sistemas que generen informacion segun
# el standar OCDS, por lo cual "publicadores_sources" es un diccionario donde los publicadores
# lista todos las fuentes o sistemas que generen.  Esto permite tener la flexibilidad de los publicadores
# tengan la oportunidad de matricular mas de una fuente u origen.  Se recomienda usar las siglas
# o acronimos que puedan identificar el sistema u origne de la informacion ej: SIAFI2 = Sistema
# Administracion Financiero Integrado version 2.0
publicadores_sources = {
    'HN.SEFIN': ['SIAFI2'],
    'HN.ONCAE': ['HC1','CE'],
    'HN.SISOCS': ['SISOCS']
}

# Url o Uri Sistemas origen de los publicadores.
# Los sistemas u origen de los publicadores puede especificar la Url o Uri donde tienen publicado
# los archivos JSON masivos.
publicadores_sources_url = {
    'SIAFI2': 'http://192.100.171.32/edca/',
    'HC1': 'http://200.13.162.79/datosabiertos/HC1/',
    'CE': 'http://200.13.162.79/datosabiertos/CE/'
}

# Formato del archivo a descargar del origen de los publicadores.
# "publicadores_sources_file" es una lista de los prefijos o nombres de los archivos JSON, los 
# publicadores definin un prefijo para publicar los diferentes archivos, 
# para el caso de Honduras, los publicadores han convenido generar un 
# nuevo archivo de ocids por año.  Ejemplo SEFIN para su origen SIAFI2 ha definido sus archivos JSON
# en el siguiente formato "ocid_2018.zip", donde el 2018 es la variable que se ajusta cada año, segun
# lo convenido entre los publicadores para el portal.
publicadores_sources_file = {
    'SIAFI2': 'ocid_sefin_{0}.zip',
    'HC1': 'HC1_datos_{0}_json.zip',
    'CE': 'CE_datos_{0}_json.zip',
    'SISOCS': 'SISOCS_{0}.zip'
}

# Directorio destino para la descarga de los archivos de los publicadores.
# "publicadores_sources_path", es un diccionario para especificar el directorio o path destion
# donde se descargaran los archivos JSON publicados en las Url o Uri.
publicadores_sources_path = {
    'SIAFI2': 'C:\\EDCA\\sefinhn\\siafi2\\descargas\\',
    'HC1': 'C:\\EDCA\\oncae\\hc1\\descargas\\',
    'CE': 'C:\\EDCA\\oncae\\ce\\descargas\\'
}

# Formato en que el archivo a descargar del origen.
# "publicadores_format_download_file", es un diccionario de por sistema y origen donde especifica,
# como se deben de renombrar los archivos JSON descargados, con el proposito de ayudar guardar los 
# archivo con algun tipo de historico.
publicadores_format_download_file = {
    'SIAFI2': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'HC1': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'CE': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'SISOCS': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip'
}

# Tipo de formato JSON.
# "publicadores_origen_tipo_archivo_json", es un diccionario que ayuda a identificar el tipo de
# archvio JSON, existen dos formatos "json_line" y "release_package", esto es importante para el
# proceso de carga al KingFisher.
publicadores_origen_tipo_archivo_json = {
    'SIAFI2': 'release_package_json_lines',
    'HC1': 'release_package',
    'CE': 'release_package',
    'SISOCS': 'json_line'
}

# Directorio o path cargar KingFisher.
# "publicadores_origen_directorio_kf_json", es un diccionario con el fin de ayudar a mantener un
# order fisico de los archivos JSON a procesar y cargar al KingFisher.
publicadores_origen_directorio_kf_json = {
    'SIAFI2': 'C:\\EDCA\\sefinhn\\siafi2\\kingfisher\\',
    'HC1': 'C:\\EDCA\\oncae\\hc1\\kingfisher\\',
    'CE': 'C:\\EDCA\\oncae\\ce\\kingfisher\\'
}

# Parametro para la configuracion del directorio para almacenar los HASH
publicadores_origen_directorio_hash = {
    'SIAFI2': 'C:\\EDCA\\sefinhn\\siafi2\\hash\\',
    'HC1': 'C:\\EDCA\\oncae\\hc1\\hash\\',
    'CE': 'C:\\EDCA\\oncae\\ce\\hash\\'
}

# Directorio o path archivos Hash.
publicadores_origen_hash_json = {
    'SIAFI2': 'C:\\EDCA\\sefinhn\\siafi2\\hash\\siafi2_json.hash',
    'HC1': 'C:\\EDCA\\oncae\\hc1\\hash\\hc1_json.hash',
    'CE': 'C:\\EDCA\\oncae\\ce\\hash\\ce_json.hash'
}

# Directorio o path historicos.
# "publicadores_origen_historico", es un diccionario donde se vincular los sistemas u origen de
# los publicadoes, el proposito es para dar la oportunidad al portal EDCA de mantener un orden
# logico y fisico de un historial de todos los archivos descargados por el proceso descarga del hunter,
# esto permitira tener alguna auditoria.
publicadores_origen_historico = {
    'SIAFI2': 'C:\\EDCA\\sefinhn\\siafi2\\historico\\',
    'HC1': 'C:\\EDCA\\oncae\\hc1\\historico\\',
    'CE': 'C:\\EDCA\\oncae\\ce\\historico\\'
}

# Directorio o path log.
# "publicadores_origen_logger", es un diccionario donde se vincular los sistemas u origen de
# los publicadoes, el proposito es para dar la oportunidad al portal EDCA de mantener un orden
# logico y fisico de los archivos LOG que se generen en los diferentes procesos de la descarga,
# procesado y carga de los archivos JSON.
publicadores_origen_logger = {
    'SIAFI2': 'C:\EDCA\logs',
    'HC1': 'C:\EDCA\logs',
    'CE': 'C:\EDCA\logs'
}

# ID collection del publicador en el KingFisher.
# "publicadores_id_collection", un diccionario donde relaciona el publicador con su ID 
# collection en KingFisher, el ID collection es asignado por la base de datos de KingFisher, 
# por convension el portal EDCA asignara el mismo ID para todos los publicadores.
publicadores_id_collection = {
    'HN.SEFIN': 1,
    'HN.ONCAE': 1
}

# ID collection record del publicador en el KingFisher.
# "publicadores_id_collection_record", un diccionario donde relaciona el publicador con su ID 
# record en KingFisher, el ID record es asignado por la base de datos de KingFisher, por convension
# el portal EDCA asignara el mismo ID para todos los publicadores.
publicadores_id_collection_record = {
    'HN.SEFIN': 2,
    'HN.ONCAE': 2
}
