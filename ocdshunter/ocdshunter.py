"""
PROYECTO : Portal EDCA-HN
NOMBRE : PublicadoresTareas
Descripcion : PY principal que ejecuta la programacion de las tareas
    de los publicadores

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Allan Duenas     Creacion.
14/06/2020    Allan Duenas     Modificacion
"""

import datetime
import logging.config
import threading
import time
import schedule
import PublicadoresTareas

from edca_mensajes import EdcaErrores as err, EdcaMensajes as msg
from edca_logs.EdcaLogger import EdcaLogger as log

# Se obtiene la configuracion del archivo de log
logging.config.fileConfig(fname='edca_logs/EdcaLoggerConfig.ini', disable_existing_loggers=False)


class OcdsHunterThread(threading.Thread):
    def __init__(self, threadID, name, publicador):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.publicador = publicador

    def run(self):
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_START, "THREADS", "Iniciando el Thread: %s" % self.name)

        # Se realiza el bloqueo para sincronizar el thread
        threadLock.acquire()
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_LOCK, "THREADS", "Thread Adquirio Bloqueo: %s" % self.name)

        # Se incia el proceso del publicador
        PublicadoresTareas.PublicadoresTareas(self.publicador).ejecutar()
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_FINISH, "THREADS", "Thread Finalizo Tarea: %s" % self.name)

        # Se libera el thread
        threadLock.release()
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_UNLOCK, "THREADS", "Se libera el Thread: %s" % self.name)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

print("***************************")
print("*    OCDS Hunter v1.0     *")
print("*     Status: Running     *")
print("***************************")
now = datetime.datetime.now()
print("Fecha-Hora: " + now.strftime("%Y-%m-%d %H:%M:%S"))


# Job para ejecutar los procesos de ONCAEHN
def job_oncae():
    print("***************************")
    print("* Publicador: ONCAE       *")
    print("* Programado: 05:00 AM    *")
    print("* Frecuencia: Diaria      *")
    print("***************************")
    # Se cargan las tareas de los publicadores
    try:
        threads = []
        # Create new threads
        thread1 = OcdsHunterThread(1, "Thread-Job-ONCAE", "HN.ONCAE")
        # Start new Threads
        thread1.start()
        # Add threads to thread list
        threads.append(thread1)

        # Wait for all threads to complete
        for t in threads:
            t.join()
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_GENERAL, "THREADS", "**** SIN JOBS PARA PROCESAR **** : %s")
    except Exception as ex:
        print(str(ex))



# Job para ejecutar los procesos de SEFINHN
def job_sefin():
    print("***************************")
    print("* Publicador: SEFIN       *")
    print("* Programado: 04:00 AM    *")
    print("* Frecuencia: Semanal     *")
    print("***************************")
    # Se cargan las tareas de los publicadores
    try:
        threads = []
        # Create new threads
        thread1 = OcdsHunterThread(2, "Thread-Job-SEFIN", "HN.SEFIN")
        # Start new Threads
        thread1.start()
        # Add threads to thread list
        threads.append(thread1)

        # Wait for all threads to complete
        for t in threads:
            t.join()
        log.registrar_log_info(__name__, err.EdcaErrores.INFO_OCDS_HUNTER_THREAD_GENERAL, "THREADS", "**** SIN JOBS PARA PROCESAR **** : %s")
    except Exception as ex:
        print(str(ex))


# Se calendariza cada horario para cada publicador
schedule.every().day.at("05:00").do(job_oncae)
schedule.every().saturday.at("20:00").do(job_sefin)

# Se inicializa el lock del thread
threadLock = threading.Lock()

# Ciclo para validar
while True:
    # Validar que tarea esta pendiente de ejecutar
    schedule.run_pending()
    time.sleep(1)
