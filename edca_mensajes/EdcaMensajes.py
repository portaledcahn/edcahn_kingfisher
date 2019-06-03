# Portal EDCA-HN
# Name :
# Description :
#
# MM/DD/YYYY    Collaborators   Descriptions
# 05/07/2019    Alla Duenas     Initial Code    


class EdcaMensajes:

    @staticmethod
    def obt_mensaje(cod_error):
        if cod_error == "EDCA-J0001":
            return "Se inicializa el calendario del Publicador."
        if cod_error == "EDCA-00001":
            return "El codigo del publicador no es valido o no existes."
        if cod_error == "EDCA-00002":
            return "El codigo del publicador no puede ser nulo."            
        if cod_error == "EDCA-00003":
            return "Error en la descarga del archivo del publicador" 
        if cod_error == "EDCA-00004":
            return "El publicador no tiene sistemas u origen registrados en el archivo de configuracion" 
        if cod_error == "EDCA-00005":
            return "El origen del publicador no tiene Url registrada en el archivo de configuracion" 
        if cod_error == "EDCA-00006":
            return "El origen del publicador no tiene nombre del archivo para descarga registrado en el archivo de configuracion"
        if cod_error == "EDCA-00007":
            return "El publicador no tiene path para la descarga de archivos."
        if cod_error == "EDCA-Z0001":
            return "Extraccion de archivo ZIP exitosa."
        if cod_error == "EDCA-Z0002":
            return "Archivo a extraer --> {0} , en directorio --> {1}"
        if cod_error == "EDCA-Z0003":
            return "Contenido del archivo ZIP: %s"
        if cod_error == "EDCA-Z0004":
            return "Archivo: %s, Error: %s"
        if cod_error == "EDCA-Z0005":
            return "Archivo ZIP no existe."
        if cod_error == "EDCA-Z0006":
            return "Archivo ZIP: %s eliminado."
        if cod_error == "EDCA-00010":
            return "No hay formato de archivo en la configuraciones"
        if cod_error == "EDCA-00011":
            return "El Directorio: %s no existe."
        if cod_error == 'EDCA-00012':
            return "El Archivo: %s no existe."
        if cod_error == 'EDCA-00013':
            return "El Archivo: %s tiene 0 bytes."
        if cod_error == 'EDCA-00014':
            return ""
        if cod_error == 'EDCA-00015':
            return ""
        if cod_error == 'EDCA-00016':
            return "Preparando archivos para el King Fisher"
        if cod_error == 'EDCA-00017':
            return "Archivos preparados para el King Fisher"
        if cod_error == 'EDCA-00018':
            return "Iniciando carga archivos JSON al KingFisher"
        if cod_error == 'EDCA-00019':
            return "Carga al King Fisher Finalizada"
        if cod_error == 'EDCA-D0002':
            return "Iniciando proceso de descarga de archivo"
        if cod_error == 'EDCA-D0003':
            return "Archivo descargado correctamente"
        if cod_error == 'EDCA-D0004':
            return "%s"
        if cod_error == 'EDCA-B0001':
            return "Conectado a la Base de Datos"
        if cod_error == 'EDCA-B0002':
            return "Desconectado de la Base de Datos"
        if cod_error == 'EDCA-B0003':
            return "Transaccion: {0} almacenada correctamente."
        if cod_error == 'EDCA-B0004':
            return "Transaccion Revertida"
        if cod_error == 'EDCA-B0005':
            return "Sequencia Bitacora actualizada correctamente."
        if cod_error == 'EDCA-P0002':
            return "Directorio: %s no existe."
        if cod_error == 'EDCA-P0001':
            return "Directorio: %s creado exitosamente."
        if cod_error == 'EDCA-DB001':
            return "Conexion Establecida a la Base de Datos."
        if cod_error == 'EDCA-DB002':
            return "Conexion Cerrada a la Base de Datos."
        if cod_error == 'EDCA-DB003':
            return "Iniciando Transaccion."
        if cod_error == 'EDCA-DB004':
            return "Transaccion Finalizada."
        if cod_error == 'EDCA-DB005':
            return "Transaccion Almacenada en la Base de Datos."
        if cod_error == 'EDCA-DB006':
            return "Deshaciendo Transaccion Almacenada en la Base de Datos."
        if cod_error == 'EDCA-DB007':
            return "Error de Base de Datos: %s"

        return "Codigo de error no definido"
