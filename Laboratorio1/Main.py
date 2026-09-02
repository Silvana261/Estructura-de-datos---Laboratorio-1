import os

from GenerarMatriz import generar_matriz
from LeerMatriz import MatrizArchivo


CARPETA = os.path.dirname(os.path.abspath(__file__))

ARCHIVO = os.path.join(
    CARPETA,
    "matriz.txt"
)



def main():

    # 1. Generar la matriz
    print("=== GENERACIÓN DE LA MATRIZ ===")

    generar_matriz(
        ARCHIVO,
        filas=100_000,
        columnas=100_000
    )

    print("\nMatriz generada correctamente.\n")


    # 2. Abrir la matriz desde el archivo
    print("=== LECTURA Y VERIFICACIÓN ===")

    m = MatrizArchivo(ARCHIVO)

    try:

        # Detectar dimensiones
        print(
            "Dimensiones detectadas SOLO a partir del archivo:"
        )

        print(f"  Columnas: {m.columnas:,}")
        print(f"  Filas: {m.filas:,}")
        print(f"  Bytes por fila: {m.bytes_por_fila:,}")


        # Verificar las comas
        print(
            "\nContando comas en TODO el archivo..."
        )

        resultado = m.contar_filas_por_comas()

        print(
            f"  Comas encontradas: "
            f"{resultado['comas_encontradas']:,}"
        )

        print(
            f"  Filas esperadas: "
            f"{resultado['filas_esperadas']:,}"
        )

        print(
            f"  Coincide: "
            f"{resultado['coincide']}"
        )


        # Verificar contenido
        print(
            "\nVerificando contenido..."
        )

        resultado = m.verificar_contenido()

        print(
            f"  Filas revisadas: "
            f"{resultado['filas_revisadas']:,}"
        )

        print(
            f"  Valores revisados: "
            f"{resultado['valores_revisados']:,}"
        )

        print(
            f"  Bytes inválidos: "
            f"{resultado['bytes_invalidos']}"
        )

        print(
            f"  Contenido válido: "
            f"{resultado['contenido_valido']}"
        )

        print(
            f"  Proporción de True: "
            f"{resultado['proporcion_true']:.2%}"
        )


        # Acceso aleatorio
        print("\n=== ACCESO ALEATORIO ===")

        print(
            "Primera fila "
            "(primeros 20 valores):"
        )
        print(m.obtener_fila(0)[:20])

        print(
            "\nÚltima fila "
            "(primeros 20 valores):"
        )
        print(m.obtener_fila(m.filas - 1)[:20])

        print(
            "\nValor en "
            "(fila=500, columna=999):"
        )
        print(m.obtener_valor(500, 999))


        # Guardar una fila como evidencia
        ruta_fila_0 = os.path.join(
            os.path.dirname(ARCHIVO),
            "fila_0.txt"
        )

        m.guardar_fila(
            0,
            ruta_fila_0
        )

        print(
            f"\nFila 0 guardada en: "
            f"{ruta_fila_0}"
        )

    finally:
        m.cerrar()


if __name__ == "__main__":
    main()