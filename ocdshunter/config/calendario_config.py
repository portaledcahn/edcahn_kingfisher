"""
PROYECTO : Portal EDCA-HN
NOMBRE : calendario_config
Descripcion : Archivo de configuraciones de los calendarios de los publicadores
    perimte realizar la programacion y/o calendarizacion de las cargas automaticas.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

# Parametro que indica quien es el Publicador
publicador = {
    'ONCAE': 'HN.ONCAE',
    'SEFIN': 'HN.SEFIN',
    'SISOCS': 'HN.SISOCS'
    }

# Parametrizacion del Job de Descarga del Publicador
publicador_job_horario = {
    'HN.SISOCS': '23:00',
    'HN.SEFIN': '23:00',
    'HN.ONCAE': '23:00'
    }

# Parametrizacion del Job para indicar si debe ser diaria, semanal, mensual.
publicador_job_periodo = {
    'HN.SISOCS': 'DIARIA', 
    'HN.SEFIN': 'SEMANAL',
    'HN.ONCAE': 'DIARIA'
    }

# SEMANAL : 0 Monday, 1 Tuesday, 2 Wednesday, 3 Thursday, 4 Friday, 5 Saturday, 6 Sunday
# DIARIA : 1 All days
# MENSUAL : Numero del dia del mes
# Indica el periodo que debe ejecutarse, ejemplo SEMANAL valor 7 (domingo), DIARIA valor 1
publicador_job_periodo_valor = {
    'HN.SISOCS': '1', 
    'HN.SEFIN': '4',
    'HN.ONCAE': '1'
    }

# Parametro de Prueba
publicador_prueba_horario = {'HN.ONCAE': '5'}

periodo_diaria = 'DIARIA'
periodo_semanal = 'SEMANAL'
periodo_mensual = 'MENSUAL'

minutos_tolerancia = 5
