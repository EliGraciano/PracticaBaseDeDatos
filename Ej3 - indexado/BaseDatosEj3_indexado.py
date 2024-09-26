import math
import os.path
from math import trunc
from os import system

PATH = 'archivo.txt'
lenghtCantColumnas = 2
lenghtTitulo = 16
lenghtCaracteres = 4
lenghtColumna = lenghtTitulo + lenghtCaracteres
lenghtPunteroDato = 4
caracterJustificacion = " "

class Metadata:
    cc : int
    titulos = []
    caracteres = []
    lenghtDato : int
    root_index : int
    lenghtIndexEntry : int

    def __init__(self):
        file = open(PATH, "r")
        self.cc = int(file.read(lenghtCantColumnas))
        for i in range(self.cc):
            self.titulos.append(file.read(lenghtTitulo))
            self.caracteres.append(int(file.read(lenghtCaracteres)))
        self.lenghtIndexEntry = self.caracteres_pk() + lenghtPunteroDato
        self.root_index = lenghtCantColumnas + (lenghtColumna * self.cc)  # salto el header
        file.close()

        resultado = 0
        for i in range(self.cc):
            resultado += self.caracteres[i]
        self.lenghtDato = resultado

    def caracteres_pk(self):
        if self.caracteres is None or len(self.caracteres) == 0:
            return None

        return self.caracteres[0]

    def titulos_pk(self):
        if self.titulos is None or len(self.titulos) == 0:
            return None

        return self.titulos[0]


class IndexEntry:
    pk = None
    puntero : int
    posicion : int

    def __init__(self, pk,puntero,posicion = 0):
        self.pk = pk
        self.puntero = puntero
        self.posicion = posicion

    def isPK(self,pk):
        return self.pk == pk

    def next(self):
        return readIndex(self.posicion + metadata.lenghtIndexEntry + metadata.lenghtDato)

    def hasNext(self):
        return self.next().pk != ""

    def readDato(self):
        return readByOffset(self.puntero)

    def write(self):
        with open(PATH,"r+") as archivo:
            archivo.seek(self.posicion)
            archivo.write(str(self.pk).ljust(metadata.caracteres_pk(),caracterJustificacion))
            archivo.write(str(self.puntero).ljust(lenghtPunteroDato,caracterJustificacion))


class Dato:
    datos = None

    def __init__(self):
        self.datos = []

    def pk(self):
        if self.datos is None or len(self.datos) == 0:
            return None

        return self.datos[0]



def getOffset(pk):
    eOF = os.path.getsize(PATH)
    header = metadata.cc + metadata.cc * lenghtColumna
    inferior = header
    superior= eOF
    canRegistros = (superior - inferior) / (metadata.lenghtDato + metadata.lenghtIndexEntry)
    actual = math.floor(canRegistros / 2) * (metadata.lenghtDato + metadata.lenghtIndexEntry) + header
    index = readIndex(actual) # indice del dato del medio

    while index.pk != pk:
        if pk < index.pk:
            superior = actual
        else:
            inferior = actual + metadata.lenghtDato + metadata.lenghtIndexEntry

        canRegistros = (superior - inferior) / (metadata.lenghtDato + metadata.lenghtIndexEntry)

        if canRegistros == 0:
            return  None

        actual = math.floor(canRegistros / 2) * (metadata.lenghtDato + metadata.lenghtIndexEntry) + inferior
        index = readIndex(actual)
    return int(index.puntero)

def readByOffset(offset):
    with open(PATH, "rt") as archivo:
        archivo.seek(int(offset))
        dato = Dato()

        for caracteres in metadata.caracteres:
            dato.datos.append(archivo.read(caracteres))
    return dato

def readIndex(offset):
    with open(PATH, "rt") as archivo:
        archivo.seek(offset)
        pk = archivo.read(metadata.caracteres_pk())
        puntero = archivo.read(lenghtPunteroDato)
    return IndexEntry(pk, puntero, offset)

def readByPK(pk):
    return readByOffset(getOffset(pk))


def write(dato):
    with open(PATH,"at") as archivo:
        for i in range (metadata.cc):
            archivo.write(dato.datos[i].ljust(metadata.caracteres[i],caracterJustificacion))

def update(pk):
    dato = ingresarDatos(pk)
    offset = getOffset(dato.pk())
    with open(PATH,"r+b") as archivo:
        archivo.seek(offset)

        archivo.seek(metadata.caracteres_pk(),1)

        for i in range (1,metadata.cc):
            archivo.write(dato.datos[i].ljust(metadata.caracteres[i],caracterJustificacion).encode("utf-8"))


def updateIndex(newIndex):
    posicion = metadata.root_index
    for i in range(len(newIndex)):
        newIndex[i].posicion = posicion
        newIndex[i].write()
        posicion += metadata.lenghtIndexEntry + metadata.lenghtDato


def delete(pk):
    puntero = getOffset(pk)
    eOF = os.path.getsize(PATH)

    index = readIndex(metadata.root_index)
    newIndex = []



    with open(PATH,"r+") as file:
        file.seek(eOF - metadata.lenghtDato)
        ultimoRegistro = file.read(metadata.lenghtDato)

        if index.pk != pk:
            newIndex.append(index)
            if index.pk == ultimoRegistro[:metadata.caracteres_pk()]:
                index.puntero = puntero

        while index.hasNext():
            index = index.next()
            if index.pk != pk:

                if index.pk == ultimoRegistro[:metadata.caracteres_pk()]:
                    index.puntero = puntero

                newIndex.append(index)

        file.seek(puntero)
        file.write(ultimoRegistro)
        file.seek(eOF - metadata.lenghtDato - metadata.lenghtIndexEntry)
        file.truncate()

    updateIndex(newIndex)

def mostrarlista():
    for i in range(metadata.cc):
        print(metadata.titulos[i].ljust(metadata.caracteres[i] if metadata.caracteres[i] > lenghtTitulo else lenghtTitulo,caracterJustificacion),end="")
    print("")
    index = readIndex(metadata.root_index)

    if index.pk != "":
        dato = index.readDato()
        for i in range(metadata.cc):
            print(dato.datos[i].ljust(metadata.caracteres[i] if metadata.caracteres[i] > lenghtTitulo else lenghtTitulo,caracterJustificacion),end="")
        print("")
        while index.hasNext():
            index = index.next()
            dato = index.readDato()
            for i in range(0,metadata.cc):
                print(dato.datos[i].ljust(metadata.caracteres[i] if metadata.caracteres[i] > lenghtTitulo else lenghtTitulo,caracterJustificacion),end="")
            print("")

def ingresarDatos(pk = None):
    dato = Dato()
    j = 0
    if pk is not None:
        j = 1
        dato.datos.append(pk.ljust(metadata.caracteres_pk(),caracterJustificacion))
    for i in range(j,metadata.cc):
        dato.datos.append(input(f"{metadata.titulos[i].strip()}: ").ljust(metadata.caracteres[i],caracterJustificacion))
    return dato

def main():
    accion = input("Ingrese una de las siguientes opciones: \n A(altas) | B(bajas) | M(modificaciones) | C(cerrar el programa) | S(mostrar la lista)\n").lower()
    if accion == "a":
        alta()

    elif accion == "b":
        baja()

    elif accion == "m":
        pk = input("Ingrese la pk del cliente a modificar: ")
        update(pk)

    elif accion == "s":
        mostrarlista()

    if accion != "c":
        main()


def alta():
    dato = ingresarDatos()
    eOF = os.path.getsize(PATH)
    new_index = IndexEntry(dato.pk(), eOF + metadata.lenghtIndexEntry)

    index = readIndex(metadata.root_index)
    agregue = False

    if index.pk != "":
        if new_index.pk < index.pk:
            indexs = [new_index,index]
            agregue = True
        else:
            indexs = [index]

        while index.hasNext():

            index = index.next()

            if not agregue and new_index.pk < index.pk:
                indexs.append(new_index)
                agregue = True

            indexs.append(index)
    else:
        indexs = [new_index]
        agregue = True

    if not agregue:
        indexs.append(new_index)

    with open(PATH,"at") as f:
        f.write("".ljust(metadata.lenghtIndexEntry))

    updateIndex(indexs)
    write(dato)


def baja():
    pk = input("pk: ").ljust(metadata.caracteres_pk(),caracterJustificacion)
    delete(pk)


if __name__ == '__main__':
    print("Bienvenido al Sistema\n     Altas/Bajas/Modificaciones J.N.E\n")
    metadata = Metadata()
    main()
    # getOffset("Romero")
