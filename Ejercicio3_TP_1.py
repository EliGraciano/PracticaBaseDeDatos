
TAMANIOCANTCOLUMNAS = 2
TAMANIOTITULO = 16
TAMANIOCARACTERES = 4
TAMANIOCOLUMNA = TAMANIOTITULO + TAMANIOCARACTERES
caracterJustificacion = " "
PATH = 'archivo.txt'

class MetaData:
    with open(PATH,"r+") as archivo:
        archivo.seek(0)








# def busquedabinaria(lista,inicio,tamaniofinal,dato):
#     if (inicio > tamaniofinal):
#         return
#     i = int((tamaniofinal - inicio) / 2)
#     if (dato == lista[i]):
#         return lista[i]
#     elif (dato < lista[i]):
#         return busquedabinaria(lista,inicio,i-1,dato)
#     else:
#         return busquedabinaria(lista,i+1,tamaniofinal,dato)