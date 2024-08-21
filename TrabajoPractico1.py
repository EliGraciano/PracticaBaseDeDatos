from os import write

tamañoApellido = 16
tamañoNombre = 16
tamañoCodigo = 4
tamañoDato = 36
"""si multiplico 36 por la cantidad de datos,obtengo el tamaño del archivo"""
"""archivo =open("Archivo.txt","wt")"""
def altas(apellido,nombre,codigo):
    with open("Archivo.txt","a",encoding="utf-8") as archivo:
        archivo.write(apellido.ljust(tamañoApellido))
        archivo.write(nombre.ljust(tamañoNombre))
        archivo.write(codigo.ljust(tamañoCodigo))

def leerdatos(index):
    pos = offset(index)
    with open("Archivo.txt","rt",encoding="utf-8") as archivo:
        archivo.seek(pos)
        apellido = archivo.read(tamañoApellido).strip()
        nombre = archivo.read(tamañoNombre).strip()
        codigo = archivo.read(tamañoCodigo).strip()
        return apellido,nombre,codigo

def bajas(index):
    pos = offset(index)
    with open("Archivo.txt","r+",encoding="utf-8") as archivo:
        archivo.seek(pos + tamañoDato)
        resto = archivo.read()
        archivo.seek(pos)
        archivo.write(resto)
        archivo.truncate()

def offset(index):
    if index == 1:
        offset1 = 0
        return offset1
    else:
        offset1 = tamañoDato * index
        return offset1

def modificacion(index,apellido,nombre,codigo):
    pos = offset(index)
    with open('archivo.txt', 'r+b') as archivo:
        archivo.seek(pos)
        if apellido is not None:
            apellido = apellido.ljust(tamañoApellido)
            archivo.write(apellido.encode('utf-8'))
        else:
            archivo.seek(tamañoApellido,1)
        if nombre is not None:
            nombre = nombre.ljust(tamañoNombre)
            archivo.write(nombre.encode('utf-8'))
        else:
            archivo.seek(tamañoNombre,1)
        if codigo is not None:
            codigo = codigo.ljust(tamañoCodigo)
            archivo.write(codigo.encode('utf-8'))
        else:
            archivo.seek(tamañoCodigo,1)


def main():
    while True:
        print("\nMenú de Opciones")
        print("1. Cargar datos (Alta)")
        print("2. Eliminar datos (Baja)")
        print("3. Modificar datos")
        print("4. Leer datos")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Cargar datos
            apellido = input("Ingrese el apellido: ")
            nombre = input("Ingrese el nombre: ")
            codigo = input("Ingrese el código: ")
            altas(apellido, nombre, codigo)
            print("Registro agregado correctamente.")

        elif opcion == '2':
            # Eliminar datos
            index = int(input("Ingrese el índice del registro a eliminar: "))
            bajas(index)
            print(f"Registro en índice {index} eliminado correctamente.")

        elif opcion == '3':
            # Modificar datos
            index = int(input("Ingrese el índice del registro a modificar: "))
            apellidoaux,nombreaux,codigoaux = leerdatos(index)
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

            modificacion(index, apellido, nombre, codigo)
            print(f"Registro en índice {index} modificado correctamente.")

        elif opcion == '4':
            # Leer datos
            index = int(input("Ingrese el índice del registro a leer: "))
            apellido, nombre, codigo = leerdatos(index)
            print(f"Registro en índice {index}: Apellido: {apellido}, Nombre: {nombre}, Código: {codigo}")

        elif opcion == '5':
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, elija una opción del 1 al 5.")
    return

main()