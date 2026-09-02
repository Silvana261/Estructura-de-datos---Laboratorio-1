import os

from GenerarMatriz import generar_matriz
from LeerMatriz import MatrizArchivo

# Se obtiene la carpeta donde se encuentra este archivo.
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Se define la ruta donde se almacenará la matriz.
ARCHIVO = os.path.join(CARPETA, "matriz.txt")


def main():

    # Primero se genera la matriz y se almacena en el disco duro directamente.
    print("\n=== GENERACIÓN DE LA MATRIZ ===\n")

    generar_matriz(ARCHIVO,filas=100_000,columnas=100_000)

    print("\nMatriz generada correctamente.\n")


    # Luego se abre el archivo para poder acceder y verificar la matriz.
    print("\n=== LECTURA Y VERIFICACIÓN ===\n")

    matriz = MatrizArchivo(ARCHIVO)

    try:
        print("\nDEMOSTRACIÓN DE MATRIZ A PARTIR DEL NÚMERO DE COMAS EN EL ARCHIVO:\n")
        
        # Primero se verifica que la cantidad de comas coincida con la cantidad 
        # de filas calculada a partir del archivo.
        print(
            "Dimensiones detectadas SOLO a partir del archivo:"
        )
        
        if matriz.contar_filas_por_comas():
                print("\nLa cantidad de comas coincide con la cantidad de filas. Si es una matriz con las dimensiones correctas.\n")
        else:
                print("\nLa cantidad de comas no coincide con la cantidad de filas. No es una matriz con las dimensiones correctas.\n")


        print("\nVERIFICACIÓN DE TIPO DE CONTENIDO DE LA MATRIZ \n") 

        # Luego se verifica que los valores almacenados sean únicamente 0 o 1.
        if matriz.verificar_contenido():
            print("\nEl contenido de la matriz es válido.\n")
        else:
            print("\nEl contenido de la matriz no es válido.\n")


        # ACCESO A LOS ELEMENTOS DE LA MATRIZ: 
        print("\n===  ACCESOS  A LA MATRIZ ===\n")

    
        print("\nPrimera fila (primeros 20 valores):" )
        print(matriz.obtener_fila(0)[:20])

        print("\nÚltima fila (primeros 20 valores):")
        print(matriz.obtener_fila(matriz.filas - 1)[:20])

        print("\nValor en (fila=500, columna=999):")
        print(matriz.obtener_valor(500, 999))


        # Se extrae la primera fila y se guarda en un archivo
        # independiente para evidenciar acceso a la matriz.
        ruta_fila_0 = os.path.join(
            os.path.dirname(ARCHIVO),
            "fila_0.txt"
        )

        matriz.guardar_fila(
            0,
            ruta_fila_0
        )

        print(
            f"\nFila 0 guardada en: "
            f"{ruta_fila_0}"
        )

    finally:
        matriz.cerrar()


if __name__ == "__main__":
    main()