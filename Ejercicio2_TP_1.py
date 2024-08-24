from os import write
import os
TAMANIOAPELLIDO = 16
TAMANIONOMBRE = 16
TAMANIOCODIGO = 4
TAMANIODATO= TAMANIOCODIGO + TAMANIOAPELLIDO + TAMANIONOMBRE
CANTREGISTROS = 700 # TODO: para luego implementar funcion que calcule el primer numero primo despues de cantidad registros
TAMANIOHASH = 701 * TAMANIODATO
PATH = "ArchivoHash.txt"
"""si multiplico 36 por la cantidad de datos,obtengo el tamaño del archivo"""
def crearArchivo():
    # TODO: crear en un file a parte la funcion
    with open(PATH,"wt") as archivo:
        archivo.write(" " * TAMANIOHASH)

def getoffset(codigo):
    return (hashFunction(int(codigo))-1 ) * TAMANIODATO

def hashFunction(Codigo):
    return Codigo % 701

def insert(new_apellido,new_nombre,new_codigo):
    writeByPK(new_apellido, new_nombre, new_codigo)

def readOverflow(codigo):
    i = TAMANIOHASH
    dato = readByOffset(i)
    while dato[2] != "":
        dato = readByOffset(i)
        if dato[2] == codigo:
            return dato
        i += TAMANIODATO
    return None

def readByPK(codigo):
    pos = getoffset(codigo)
    dato = readByOffset(pos)
    if dato[2] == codigo:
        return dato
    else:
        return readOverflow(codigo)

def readByOffset(pos):
    with open(PATH,"rt") as archivo:
        archivo.seek(pos)
        apellido = archivo.read(TAMANIOAPELLIDO)
        nombre = archivo.read(TAMANIONOMBRE)
        codigo = archivo.read(TAMANIOCODIGO)
        return apellido,nombre,codigo

def writeByPK(apellido,nombre,codigo):
    pos = getoffset(codigo)
    dato = readByPK(codigo)
    if dato is not None:
        if readByOffset(codigo)[2] != "":
            pass #TODO:  escribirlo en la zona overflow(apend porque es al final)
        writeByOffset(pos,apellido,nombre,codigo)
    else: #tirar error
        return  None


def writeByOffset(pos,apellido,nombre,codigo):
    #escribe donde le ordeno
    with open(PATH,"r+") as archivo:
        archivo.seek(pos)
        archivo.write(apellido.ljust(TAMANIOAPELLIDO).encode("utf-8"))
        archivo.write(nombre.ljust(TAMANIONOMBRE).encode("utf-8"))
        archivo.write(codigo.ljust(TAMANIOCODIGO).encode("utf-8"))


def delete(index):
    #corregido
    pos = offset(index)
    with open(PATH,"r+b") as archivo:
        archivo.seek(-TAMANIODATO,2)
        resto = archivo.read()
        archivo.seek(pos)
        archivo.write(resto)
        archivo.seek(-TAMANIODATO,2)
        archivo.truncate()

def update(index, new_apellido, new_nombre, new_codigo):
    pos = offset(index)
    old_apellido,old_nombre,old_codigo = readByPK(index)
    if new_apellido is None:
        new_apellido = old_apellido

    if new_nombre is None:
        new_nombre = old_nombre

    if new_codigo is None:
        new_codigo = old_codigo

    writeByPK(index,new_apellido,new_nombre,new_codigo)



def listaClientes():
    index = 1
    while True:
        apellido,nombre,codigo = readByPK(index)
        if not codigo:
            break
        print("Cliente ", index)
        print("Apellido: ", apellido)
        print("Nombre: ", nombre)
        print("Código: ", codigo)
        print("----------------------")
        index += 1

def main():
    while True:
        print("\nMenú de Opciones")
        print("0. Salir")
        print("1. Cargar datos (Alta)")
        print("2. Eliminar datos (Baja)")
        print("3. Modificar datos")
        print("4. Mostrar Lista de Clientes")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Cargar datos
            apellido = input("Ingrese el apellido: ")
            nombre = input("Ingrese el nombre: ")
            codigo = input("Ingrese el código: ")
            insert(apellido, nombre, codigo)
            print("Registro agregado correctamente.")

        elif opcion == '2':
            # Eliminar datos
            index = int(input("Ingrese el índice del registro a eliminar: "))
            delete(index)
            print(f"Registro en índice {index} eliminado correctamente.")

        elif opcion == '3':
            # Modificar datos
            index = int(input("Ingrese el índice del registro a modificar: "))
            apellidoaux,nombreaux,codigoaux = readByPK(index)
            print("Datos a modificar: ")
            print("apellido: ",apellidoaux)
            print("Nombre: ",nombreaux)
            print("Codigo: ",codigoaux)
            apellido = input("Ingrese el nuevo apellido (dejar en blanco para no modificar): ")
            nombre = input("Ingrese el nuevo nombre (dejar en blanco para no modificar): ")
            codigo = input("Ingrese el nuevo código (dejar en blanco para no modificar): ")

            # Convertir entradas vacías en None para evitar modificar
            apellido = apellido if apellido != "" else None
            nombre = nombre if nombre != "" else None
            codigo = codigo if codigo != "" else None

            update(index, apellido, nombre, codigo)
            print(f"Registro en índice {index} modificado correctamente.")

        elif opcion == '4':
            print("Listado de Clientas:")
            print("----------------------")
            listaClientes()

        elif opcion == '0':
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, elija una opción del 0 al 4.")
    return

main()