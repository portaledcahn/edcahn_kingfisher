"""
PROYECTO : Portal EDCA-HN
NOMBRE : PublicadoresTareas
Descripcion : PY principal que ejecuta la programacion de las tareas
    de los publicadores

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""

import logging.config
import time

import schedule

import PublicadoresTareas

logging.config.fileConfig(fname='edca_logs/EdcaLoggerConfig.ini', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

# Job para ejecutar los procesos de ONCAEHN
def job_oncae():
    print("***************************")
    print("* Publicador: ONCAE       *")
    print("* Programado: 03:00 AM    *")
    print("* Frecuencia: Diaria      *")
    print("***************************")
    # Se cargan las tareas de los publicadores
    try:
        PublicadoresTareas.PublicadoresTareas("HN.ONCAE").ejecutar()
    except Exception as ex:
        print(str(ex))
        #traceback.print_stack()

# Job para ejecutar los procesos de SEFINHN
def job_sefin():
    print("***************************")
    print("* Publicador: SEFIN       *")
    print("* Programado: 04:00 AM    *")
    print("* Frecuencia: Semanal     *")
    print("***************************")
    # Se cargan las tareas de los publicadores
    try:
        PublicadoresTareas.PublicadoresTareas("HN.SEFIN").ejecutar()
    except Exception as ex:
        print(str(ex))
        #traceback.print_stack()

# Job para ejecutar los procesos de SISOCSHN
def job_sisocs():
    print("***************************")
    print("* Publicador: SISOCS      *")
    print("* Programado: 05:00 AM    *")
    print("* Frecuencia: Diaria      *")
    print("***************************")
    # Se cargan las tareas de los publicadores
    try:
        PublicadoresTareas.PublicadoresTareas("HN.SISOCS").ejecutar()
    except Exception as ex:
        print(str(ex))

# Se calendariza cada horario para cada publicador
schedule.every().day.at("03:00").do(job_oncae)
schedule.every().monday.at("04:00").do(job_sefin)
schedule.every().day.at("05:00").do(job_sisocs)

# Ciclo para validar
while True:
    # Revisa si hay jobs agendados
    # pendientes de ejecutar
    schedule.run_pending()
    time.sleep(1)
    # create logger

