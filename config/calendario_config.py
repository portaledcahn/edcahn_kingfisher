"""
PROYECTO : Portal EDCA-HN
NOMBRE : edca_global_config
Descripcion : Archivo de configuraciones de los calendarios de los publicadores
    perimte realizar la programacion y/o calendarizacion de las cargas automaticas.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

# Parametro que indica quien es el Publicador
publicador = {'ONCAE': 'HN.ONCAE',
              'SEFIN': 'HN.SEFIN',
              'SISOCS': 'HN.SISOCS'}

# Parametrizacion del Job de Descarga del Publicador
publicador_job_horario = {'HN.SISOCS': '23:00',
                          'HN.SEFIN': '23:00',
                          'HN.ONCAE': '23:00'}

# Parametrizacion del Job para indicar si debe ser diaria, semanal, mensual.
publicador_job_calendario = {'HN.SISOCS': 'DIARIA', 'HN.SEFIN': 'SEMANAL', 'HN.ONCAE': 'DIARIA'}

# Parametro de Prueba
publicador_prueba_horario = {'HN.ONCAE': '5'}
