from bisect import insort
from os import write

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
    return TAMANIOHASH % Codigo

def insert(new_apellido,new_nombre,new_codigo):
    writeByPK(new_apellido, new_nombre, new_codigo)

def readOverflow(codigo):
    i = TAMANIOHASH
    registro = readByOffset(i)
    while registro[2] != "":
        registro = readByOffset(i)
        if registro[2] == codigo:
            return registro
        i += TAMANIODATO
    return ""

def readByPK(codigo):
    pos = getoffset(codigo)
    dato = readByOffset(pos)
    if dato[2] != codigo:
        return dato
    elif dato[2] == "    ":
        return None
    else:
        return readOverflow(codigo)

def writeinOverflow(apellido,nombre,codigo):
    with open(PATH,"at") as archivo:
        archivo.write(apellido.ljust(TAMANIOAPELLIDO))
        archivo.write(nombre.ljust(TAMANIONOMBRE))
        archivo.write(codigo.ljust(TAMANIOCODIGO))

def readByOffset(pos):
    with open(PATH,"rt") as archivo:
        archivo.seek(pos)
        apellido = archivo.read(TAMANIOAPELLIDO)
        nombre = archivo.read(TAMANIONOMBRE)
        codigo = archivo.read(TAMANIOCODIGO)
        return apellido,nombre,codigo

def writeByPK(new_apellido,new_nombre,new_codigo):
    pos = getoffset(new_codigo)
    old_registro = readByPK(new_codigo)
    if old_registro is None:
        writeByOffset(pos,new_apellido,new_nombre,new_codigo)
    else:
        if readOverflow(new_codigo) == "":
            writeinOverflow(new_apellido,new_nombre,new_codigo)
        else:
            return


def writeByOffset(pos,apellido,nombre,codigo):
    #escribe donde le ordeno
    with open(PATH,"r+") as archivo:
        archivo.seek(pos)
        archivo.write(apellido.ljust(TAMANIOAPELLIDO))
        archivo.write(nombre.ljust(TAMANIONOMBRE))
        archivo.write(codigo.ljust(TAMANIOCODIGO))


def delete(old_codigo):
    pos = getoffset(old_codigo)
    registro = readByPK(old_codigo)
    empty_apellido = "".ljust(TAMANIOAPELLIDO)
    empty_nombre = "".ljust(TAMANIONOMBRE)
    writeByOffset(pos, empty_apellido, empty_nombre, old_codigo)

#como hago para hacer que mi update tambien borre(pasarle to.do vacio,ya que el codigo no puedo)
def update(new_apellido, new_nombre, new_codigo,codigo_registro):
    pos = getoffset(codigo_registro)
    old_registro = readByPK(new_codigo)
    if new_apellido == "":
        new_apellido = "".ljust(TAMANIOAPELLIDO)
    elif new_apellido is None:
        new_apellido = old_registro[0]

    if new_nombre == "":
        new_nombre = "".ljust(TAMANIONOMBRE)
    elif new_nombre is None:
        new_nombre = old_registro[1]

    if new_codigo == "":
        new_codigo = old_registro[2]

    if new_codigo == old_registro[2]:
        writeByPK(new_apellido, new_nombre, new_codigo)
    else:
        #actualiza el mismo Registro si el código no se cambia
        delete(codigo_registro)
        writeByOffset(pos, new_apellido, new_nombre, new_codigo)


def mostrarcliente(codigo):
    apellido,nombre,old_codigo = readByPK(codigo)
    print("----------------------")
    print("Apellido: ", apellido)
    print("Nombre: ", nombre)
    print("Código: ", old_codigo)
    print("----------------------")


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
    #crearArchivo()
    while True:
        print("\nMenú de Opciones")
        print("0. Salir")
        print("1. Cargar datos (Alta)")
        print("2. Eliminar datos (Baja)")
        print("3. Modificar datos")
        print("4. Mostrar Lista de Clientes")
        print("5. Mostrar cliente")

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
            codigo = int(input("Ingrese el codigo del registro a modificar: "))
            apellidoaux,nombreaux,codigoaux = readByPK(codigo)
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

            update(apellido, nombre, codigo)
            print(f"Registro en índice {index} modificado correctamente.")

        elif opcion == '4':
            print("Listado de Clientas:")
            print("----------------------")
            listaClientes()

        elif opcion == '5':
            codigo = input("ingrese codigo: ")
            mostrarcliente(codigo)

        elif opcion == '0':
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, elija una opción del 0 al 4.")

    return
main()
# insort()
# #update("Gimenez","Juancruz","1234","1234")
# delete(1234)