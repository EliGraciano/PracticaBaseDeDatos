TAMANIOAPELLIDO = 16
TAMANIONOMBRE = 16
TAMANIOCODIGO = 4
TAMANIODATO= TAMANIOCODIGO + TAMANIOAPELLIDO + TAMANIONOMBRE
CANTREGISTROS = 700
TAMANIOHASH = 701 * TAMANIODATO
PATH = "ArchivoHash.txt"
"""si multiplico 36 por la cantidad de datos,obtengo el tamaño del archivo"""

def getoffset(codigo):
    return (hashFunction(int(codigo))-1 ) * TAMANIODATO

def hashFunction(Codigo):
    return  Codigo % TAMANIOHASH

def insert(new_apellido,new_nombre,new_codigo):
    writeByPK(new_apellido, new_nombre, new_codigo)

def searchOverflow(codigo):
    i = TAMANIOHASH
    registro = readByOffset(i)
    while registro[2] != "":
        if registro[2] == str(codigo):
            return i
        i += TAMANIODATO
        registro = readByOffset(i)
    return ""

def searchbypk(codigo):
    pos = getoffset(codigo)
    old_registro = readByOffset(pos)
    if old_registro[2] == str(codigo):
        return pos
    else:
        return searchOverflow(codigo)


def readOverflow(codigo):
    i = TAMANIOHASH
    registro = readByOffset(i)
    while registro[2] != "":
        if registro[2] == codigo:
            return registro
        i += TAMANIODATO
        registro = readByOffset(i)
    return ""

def readByPK(codigo):
    pos = getoffset(codigo)
    dato = readByOffset(pos)
    if dato[2] == str(codigo):
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
    old_registro = readByOffset(pos)
    if old_registro[2].isspace():
        writeByOffset(pos,new_apellido,new_nombre,new_codigo)
    else:
        if readOverflow(new_codigo) == "":
            writeinOverflow(new_apellido,new_nombre,new_codigo)
        else:
            return


def writeByOffset(pos,apellido,nombre,codigo):
    #escribe donde le ordeno
    with open(PATH,"r+") as archivo:
        archivo.seek(int(pos))
        archivo.write(apellido.ljust(TAMANIOAPELLIDO))
        archivo.write(nombre.ljust(TAMANIONOMBRE))
        archivo.write(codigo.ljust(TAMANIOCODIGO))


def delete(old_codigo):
    writeByOffset(searchbypk(old_codigo),"","","")
    garbageCollector()


#como hago para hacer que mi update tambien borre(pasarle to.do vacio,ya que el codigo no puedo)
def update(new_apellido, new_nombre, new_codigo,codigo_registro):
    old_registro = readByPK(codigo_registro)
    if new_apellido.isspace():
        new_apellido = old_registro[0]
    if new_nombre.isspace():
        new_nombre = old_registro[1]
    if new_codigo.isspace():
        new_codigo = old_registro[2]
    delete(codigo_registro)
    insert(new_apellido,new_nombre, new_codigo)

def mostrarcliente(codigo):
    apellido,nombre,old_codigo = readByPK(codigo)
    print("----------------------")
    print("Apellido: ", apellido)
    print("Nombre: ", nombre)
    print("Código: ", old_codigo)
    print("----------------------")


def listaClientes():
    pos = 0
    apellido,nombre,codigo = readByOffset(pos)
    while codigo != "":
        if not codigo.isspace():
            print("Apellido:", apellido)
            print("Nombre:", nombre)
            print("Código:", codigo)
            print("----------------------")
        pos += 36
        apellido,nombre,codigo = readByOffset(pos)

def garbageCollector():
    pos = TAMANIOHASH
    with open(PATH,"r+b") as archivo:
        archivo.seek(pos)
        registro = archivo.read(TAMANIODATO)
        while registro != "".encode("utf-8"):
            if registro.isspace():
                archivo.seek(-TAMANIODATO,2)
                ultimoRegistro = archivo.read(TAMANIODATO)
                archivo.seek(pos)
                archivo.write(ultimoRegistro)
                archivo.seek(-TAMANIODATO,2)
                archivo.truncate()
            else:
                pos += 36
            archivo.seek(pos)
            registro = archivo.read(TAMANIODATO)



def main():
    #crearArchivo()
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
            insert(apellido.ljust(TAMANIOAPELLIDO), nombre.ljust(TAMANIONOMBRE), codigo.ljust(TAMANIOCODIGO))
            print("Registro agregado correctamente.")

        elif opcion == '2':
            # Eliminar datos
            codigo = input("Ingrese el codigo del registro a eliminar: ").ljust(TAMANIOCODIGO)
            delete(codigo)
            print(f"Registro en índice {codigo} eliminado correctamente.")

        elif opcion == '3':
            # Modificar datos
            codigo = input("Ingrese el codigo del registro a modificar: ").ljust(TAMANIOCODIGO)
            apellidoaux,nombreaux,codigoaux = readByPK(codigo)
            print("Datos a modificar: ")
            print("apellido: ",apellidoaux)
            print("Nombre: ",nombreaux)
            print("Codigo: ",codigoaux)
            apellido = input("Ingrese el nuevo apellido (dejar en blanco para no modificar): ").ljust(TAMANIOAPELLIDO)
            nombre= input("Ingrese el nuevo nombre (dejar en blanco para no modificar): ").ljust(TAMANIONOMBRE)
            codigoaux = input("Ingrese el nuevo código (dejar en blanco para no modificar): ").ljust(TAMANIOCODIGO)

            update(apellido, nombre, codigoaux,codigo)

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
if __name__ == '__main__':
    main()