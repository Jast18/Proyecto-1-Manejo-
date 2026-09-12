#Almacena los archivios
#No sabe nada sobre ellos solamente intercatura con la memoria y los guardad en el disco 
#Se almacenanran los archivos en binario

import struct #Struct nos permitira darnos la agilidad para empaquetar. y desempaquetar datos binarios
import shutil #Shutil nos dara la agiliad para poder pegar y copiar archivo(utilizados en el momento de guardar y elimnara archio) estos se copian y pegan en el disco
import os #AL implementar os nos ayuda a poder interactar con el sistema operaticvo y crear carpetas y arhchivos en el disco diro 

#strcut empaquetr y desempaquetr
#shutil pegar y copiar directamente en el disco duro
# os crear en el sistema operativo

RUTA_CONFIG = "data/config.bin"
RUTA_BACKUP = "data/config_backup.bin"
RUTA_TMP = "data/config.tmp"

Valores = {
    "nombre_Usuario" : "usuario",
    "tema_interfaz": "claro",
    "idioma": "es",
    "tamaño_fuente": 12, #La funete contempla 12 bits de tamaño por defecto y la fuente conformara el texto ezcrito en la aplicacion
    "color_barra": (255, 255, 255), #Color preseleccionado para la barra de herramientas, blanco en RGB = 255
    "color_letra": (0, 0, 0), #Color preseleccionado para la letra, negro en RGB
    "foto_perfil": "",
}


def empaquetar_string(texto: str) -> bytes: #str el texto permanecera en formato de bytes y str para especificar que permanecera en strings
    datos = texto.encode("utf-8")
    return struct.pack(">H", len(datos )) + datos #Leera sttring por string en datos y almacenara para cada uno 2 bytes ">H" e ira sumando los demas datos adjuntados 

def desempaquetar_string(datos : bytes, offset: int ):
    (longitud ,) = struct.unpack_from(">H", datos, offset) #Se almacenara las variables de datos en la longitud como tupla, contemplando los dos bytes pore cada datos, los dtatos y su posicion
    ofset += 2 #Cambiara cada 2 bytes
    texto = datos[offset:offset + longitud].decode("utf-8")
    offset += longitud
    return texto, offset

def _serializar(config: dict) -> bytes: #Almacenamos la informacion obteneida en diccionario de valores a bytes 
    partes = []
    partes.append(_empaquetar_string(config("nombre_Usuario")))
    partes.append(struct.pack(">B", 1 if config("tema_interfaz") == "oscuro" else 0))
    partes.append(_empaquetar_string(config("idioma")))
    partes.append(struct.pack(">i", config("tamaño_fuente"))) 
    partes.append(struct.pack(">BBB", *config["color_barra"]))
    partes.append(struct.pack(">BBB", *config["color_letra"]))
    partes.append(_empaquetar_string(config["foto_perfil"]))
    return b"".join(partes)
 
 
def _deserializar(datos: bytes) -> dict: #ALmacena la informacion obteneida en bytes nuevamente al diccionario de valores
    offset = 0
    config = {}
 
    config["nombre_usuario"], offset = _desempaquetar_string(datos, offset)
 
    (tema_byte,) = struct.unpack_from(">B", datos, offset)
    config["tema_interfaz"] = "oscuro" if tema_byte == 1 else "claro"
    offset += 1
 
    config["idioma"], offset = _desempaquetar_string(datos, offset)
 
    (config["tamaño_fuente"],) = struct.unpack_from(">i", datos, offset)
    offset += 4
 
    config["color_barra"] = struct.unpack_from(">BBB", datos, offset)
    offset += 3
 
    config["color_letra"] = struct.unpack_from(">BBB", datos, offset)
    offset += 3
 
    config["foto_perfil"], offset = _desempaquetar_string(datos, offset)

    #+= Cantidad de bytes que se van recorriendo por cada dato
 
    return config
 
 
def cargar_configuracion() -> dict:
    #Las modificaciones que se realizrn se guardaran en un mismo archivo binario desearizando para poder verlo
    try:
        with open(RUTA_CONFIG, "rb") as archivo: 
            datos = archivo.read()
        return _deserializar(datos)
 
    except FileNotFoundError:
        print("Aviso: no existe un archivo de configuración previo. Usando valores por defecto.")
        return dict(VALORES_POR_DEFECTO)
 
    except PermissionError:
        print("Aviso: sin permisos para leer el archivo de configuración. Usando valores por defecto.")
        return dict(VALORES_POR_DEFECTO)
 
    except (struct.error, UnicodeDecodeError, IndexError) as error:
        print(f"Aviso: el archivo de configuración está corrupto o tiene formato inválido ({error}). "
              f"Usando valores por defecto.")
        return dict(VALORES_POR_DEFECTO)
 
 
def guardar_configuracion(config: dict) -> bool:

    try:
        os.makedirs(os.path.dirname(RUTA_CONFIG), exist_ok=True)
 
        #1. respaldo del archivo actual, si existe
        if os.path.exists(RUTA_CONFIG): #os.path.exist() verifica en path si existe y es el que se guardara en el disco duro antes de modificarlo
            shutil.copy2(RUTA_CONFIG, RUTA_BACKUP)
 
        #2. escritura completa a archivo temporal
        datos = _serializar(config) #Todas las modificaciones se amacenaran un archivo temporal, conforme se vallan ingresando datos se serializaran en el temporal
        with open(RUTA_TEMPORAL, "wb") as archivo:
            archivo.write(datos)
 
        #3. reemplazo atómico
        os.replace(RUTA_TEMPORAL, RUTA_CONFIG) #Al finalizar se remplazar el temporal por el actual, y el que antes era actual se almacena como respaldo hasta que se vuelva a modificar, en ese entonces el actual sera descartado.
        return True
 
    except PermissionError:
        print("Error: sin permisos para escribir el archivo de configuración. Los cambios no se guardaron.")
        return False
 
    except OSError as error:
        print(f"Error al guardar la configuración: {error}")
        return False

        
 