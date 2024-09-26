
from BaseDatosEj3_indexado import *

cc = input("numero de columnas: ")
with open("archivo.txt","wt") as archivo:
    archivo.write(cc.ljust(lenghtCantColumnas,caracterJustificacion))
    for i in range(int(cc)):
        archivo.write(input(f"inserte el titulo de la columna numero {i + 1}: ").ljust(lenghtTitulo, caracterJustificacion))
        archivo.write(input(f"inserte la cantidad de caracteres utilizados por dato en la columna numero {i + 1}: ").ljust(lenghtCaracteres,caracterJustificacion))