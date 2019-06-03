"""
PROYECTO : Portal EDCA-HN
NOMBRE : publicadores_config
Descripcion : Archivo de configuraciones de los publicadores

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

# Publicadores para el portal EDCA Honduras.
publicadores = ['HN.SEFIN', 'HN.ONCAE', 'HN.SISOCS']

# Sistemas origen de los publicadores.
publicadores_sources = {
    'HN.SEFIN': ['SIAFI2'],
    'HN.ONCAE': ['DDC'],
    # 'HN.ONCAE': ['HC1','DDC','CE'],
    'HN.SISOCS': ['SISOCS']
}

# Sistemas origen de los publicadores.
publicadores_sources_url = {
    'SIAFI2': 'http://....',
    'HC1': 'http://181.210.15.175/datosabiertos/HC1/',
    'DDC': 'http://181.210.15.175/datosabiertos/DDC/',
    'CE': 'http://181.210.15.175/datosabiertos/CE/',
    'SISOCS': 'http://....'
}

# Formato del archivo a descargar del origen de los publicadores.
publicadores_sources_file = {
    'SIAFI2': 'ocid_{0}.zip',
    'HC1': 'HC1_datos_2018_json.zip',
    'DDC': 'DDC_datos_2018_json.zip',
    'CE': 'CE_datos_2018_json.zip',
    'SISOCS': 'SISOCS_{0}.zip'
}

# Directorio destino para la descarga de los archivos de los publicadores
publicadores_sources_path = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\descargas\\',
    'HC1': 'C:\\edcahn\\hn_oncae\\hc1\\descargas\\',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\descargas\\',
    'CE': 'C:\\edcahn\\hn_oncae\\ce\\descargas\\',
    # 'HC1': '/home/aduenas/edcahn/hn_oncae/HC1/descargas',
    # 'DDC': '/home/aduenas/edcahn/hn_oncae/DDC/descargas',
    # 'CE': '/home/aduenas/edcahn/hn_oncae/CE/descargas',
    'SISOCS': '/home/aduenas/edcahn/hn_sisocs/sisocs/descargas'
}

publicadores_format_download_file = {
    'SIAFI2': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'HC1': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'DDC': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'CE': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip',
    'SISOCS': '{publisher}_{source}_{yyyy}{mm}{dd}_{hh24}{mi}{ss}.zip'
}

publicadores_origen_tipo_archivo_json = {
    'SIAFI2': 'json-line',
    'HC1': 'release-package',
    'DDC': 'release-package',
    'CE': 'release-package',
    'SISOCS': 'json-line'
}

publicadores_origen_directorio_kf_json = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\kingfisher\\',
    'HC1': 'C:\\edcahn\\hn_oncae\\hc1\\kingfisher\\',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\kingfisher\\',
    'CE': 'C:\\edcahn\\hn_oncae\\ce\\kingfisher\\',
    # 'HC1': '/home/aduenas/Publicadores_Edca/ONCAE/HC1/kingfisher\\',
    # 'DDC': '/home/aduenas/Publicadores_Edca/ONCAE/DDC/kingfisher\\',
    # 'CE': '/home/aduenas/Publicadores_Edca/ONCAE/CE/kingfisher\\',
    'SISOCS': '/home/aduenas/Publicadores_Edca/SISOCS/SISOCS/kingfisher\\'
}

# Parametro para la configuracion del directorio para almacenar los HASH
publicadores_origen_directorio_hash = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\hash',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\hash\\'
}

publicadores_origen_hash_json = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\hash\\SIAFI2_json.hash',
    'HC1': 'C:\\edcahn\\hn_oncae\\hc1\\hash\\hc1_json.hash',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\hash\\ddc_json.hash',
    'CE': 'C:\\edcahn\\hn_oncae\\ce\\hash\\ce_json.hash',
    # 'HC1': '/home/aduenas/Publicadores_Edca/ONCAE/HC1/hash/HC1_json.hash',
    # 'DDC': '/home/aduenas/Publicadores_Edca/ONCAE/DDC/hash/DDC_json.hash',
    # 'CE': '/home/aduenas/Publicadores_Edca/ONCAE/CE/hash/CE_json.hash',
    'SISOCS': '/home/aduenas/Publicadores_Edca/SISOCS/SISOCS/hash/SISOCS_json.hash'
}

publicadores_origen_historico = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\historico\\',
    'HC1': 'C:\\edcahn\\hn_oncae\\hc1\\historico\\',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\historico\\',
    'CE': 'C:\\edcahn\\hn_oncae\\ce\\historico\\',
    # 'HC1': '/home/aduenas/Publicadores_Edca/ONCAE/HC1/historico/',
    # 'DDC': '/home/aduenas/Publicadores_Edca/ONCAE/DDC/historico/',
    # 'CE': '/home/aduenas/Publicadores_Edca/ONCAE/CE/historico/',
    'SISOCS': '/home/aduenas/edcahn/hn_sisocs/sisocs/historico/'
}

publicadores_origen_logger = {
    'SIAFI2': 'C:\\edcahn\\hn_sefin\\siafi2\\logger\\',
    'HC1': 'C:\\edcahn\\hn_oncae\\hc1\\logger\\',
    'DDC': 'C:\\edcahn\\hn_oncae\\ddc\\logger\\',
    'CE': 'C:\\edcahn\\hn_oncae\\ce\\logger\\',
    # 'HC1': '/home/aduenas/Publicadores_Edca/ONCAE/HC1/logger/',
    # 'DDC': '/home/aduenas/Publicadores_Edca/ONCAE/DDC/logger/',
    # 'CE': '/home/aduenas/Publicadores_Edca/ONCAE/CE/logger/',
    'SISOCS': '/home/aduenas/edcahn/hn_sisocs/sisocs/historico/'
}

# Sistemas origen de los publicadores.
publicadores_id_collection = {
    'HN.SEFIN': 2,
    'HN.ONCAE': 1,
    'HN.SISOCS': 3
}

# Sistemas origen de los publicadores.
publicadores_id_collection_record = {
    'HN.SEFIN': 2,
    'HN.ONCAE': 1,
    'HN.SISOCS': 3
}
