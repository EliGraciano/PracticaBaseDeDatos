from Ejercicio2_TP_1 import *
def crearArchivo():
    with open(PATH,"wt") as archivo:
        archivo.write(" " * TAMANIOHASH)

crearArchivo()