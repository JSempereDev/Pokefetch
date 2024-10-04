import subprocess
import os
import re

sprite = os.path.expanduser("~/Proyectos/Pokefetch/sprite.txt")
neofetch = os.path.expanduser("~/Proyectos/Pokefetch/neofetch.txt")
combinado = os.path.expanduser("~/Proyectos/Pokefetch/archivo_combinado.txt")

command = "touch " + sprite + " " + neofetch + " " + combinado
subprocess.run(command, shell=True)

command = "pokeget random --hide-name > " + sprite
subprocess.run(command, shell=True)

command = "neofetch --off > "+ neofetch
subprocess.run(command, shell=True)

#---------------------------------------------

# Expresión regular para los códigos de escape ANSI (códigos de color)
ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

# Función para eliminar los códigos de color ANSI y obtener la longitud real de la línea
def longitud_sin_ansi(linea):
    return len(ansi_escape.sub('', linea.rstrip()))

# Abre archivo1 y archivo2 para leer todas sus líneas
with open(neofetch, 'r') as archivo1, open(sprite, 'r') as archivo2:
    lineas1 = archivo1.readlines()
    lineas2 = archivo2.readlines()

# Encuentra la longitud máxima de las líneas de archivo2 (sin códigos ANSI)
longitud_maxima_archivo2 = max(longitud_sin_ansi(linea) for linea in lineas2)

# Asegúrate de que ambos archivos tengan el mismo número de líneas
if len(lineas2) < len(lineas1):
    lineas2.extend(['\n'] * (len(lineas1) - len(lineas2)))

# Combina las líneas de archivo2 (izquierda) con archivo1 (derecha)
lineas_modificadas = [
    linea2.rstrip() + ' ' * (longitud_maxima_archivo2 - longitud_sin_ansi(linea2)) + ' \t' + linea1
    for linea1, linea2 in zip(lineas1, lineas2)
]

# Escribe las líneas modificadas en un nuevo archivo o sobreescribe el original
with open(combinado, 'w') as archivo_modificado:
    archivo_modificado.writelines(lineas_modificadas)


#----------------------------------------
command = "head -n -1 " + combinado
subprocess.run(command, shell=True)

command = "rm " + sprite + " " + neofetch + " " + combinado
subprocess.run(command, shell=True)