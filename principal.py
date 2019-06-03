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
from config import edca_global_config as cfg


logging.config.fileConfig(fname='edca_logs/EdcaLoggerConfig.ini', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

#Recibimos el Publicador
#pub = sys.argv[1]
pub = "HN.ONCAE"


def job():
    PublicadoresTareas.PublicadoresTareas(pub).ejecutar()


schedule.every(10).seconds.do(job)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
    # create logger

