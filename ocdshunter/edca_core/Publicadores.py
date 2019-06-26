"""
PROYECTO : Portal EDCA-HN
NOMBRE : Publicadores
Descripcion : Clase que maneja todas las propiedades de los publicadores
    validaciones, configuraciones, etc.

MM/DD/YYYY    Colaboradores   Descripcion
05/07/2019    Alla Duenas     Creacion.    
"""   

from config import publicadores_config

class Publicadores:
    def __init__(self):
        self.__publicadores = publicadores_config.publicadores

    # Busca un publicador si esta registrado en el archivo de configuracion
    # retorna TRUE si existe y FALSE en caso contrario
    def existe_publicador(self, publicador):
        return publicador in self.__publicadores
    
    # Retorna el listado los origenes o sistemas de los publicadores
    @staticmethod
    def origenes(publicador):
        return publicadores_config.publicadores_sources.get(publicador)
    
    # url para descargar los archivos de los publicadores
    @staticmethod
    def origen_urls(origen):
        return publicadores_config.publicadores_sources_url.get(origen)
    
    # nombre del archivo json o zip publicado
    @staticmethod
    def origen_nombre_archivo(origen):
        return publicadores_config.publicadores_sources_file.get(origen)
    
    #
    @staticmethod
    def origen_directorio(origen):
        return publicadores_config.publicadores_sources_path.get(origen)
    
    # 
    @staticmethod
    def origen_archivo_destino(origen):
        return publicadores_config.publicadores_format_download_file.get(origen)

    # Obtener el tipo de archivo JSON del Publicador
    @staticmethod
    def publicador_tipo_archivo_json(origen):
        return publicadores_config.publicadores_origen_tipo_archivo_json.get(origen)

    # Obtener el directorio HASH del Publicador
    @staticmethod
    def publicador_directorio_hash(origen):
        return publicadores_config.publicadores_origen_directorio_hash.get(origen)

    # Obtener el nombre del archivo HASH del Publicador
    @staticmethod
    def publicador_archivo_hash(origen):
        return publicadores_config.publicadores_origen_hash_json.get(origen)

    # Obtener el directorio de Kingfisher del Publicador
    @staticmethod
    def publicador_directorio_kingfisher(origen):
        return publicadores_config.publicadores_origen_directorio_kf_json.get(origen)

    # Obtener el directorio de historico del origen o sistema
    @staticmethod
    def publicador_directorio_historico(origen):
        return publicadores_config.publicadores_origen_historico.get(origen)

    # Obtener el archivo JSON del Publicador para ser procesado a Kingfisher
    @staticmethod
    def publicador_archivo_json_kingfisher(origen):
        return publicadores_config.publicadores_origen_tipo_archivo_json.get(origen)

    # Obtener el ID Collection del publicador en el King Fisher
    @staticmethod
    def publicador_kf_id_collection(publicador):
        return publicadores_config.publicadores_id_collection.get(publicador)

    # Obtener el ID Collection del publicador en el King Fisher
    @staticmethod
    def publicador_kf_id_collection_record(publicador):
        return publicadores_config.publicadores_id_collection_record.get(publicador)
