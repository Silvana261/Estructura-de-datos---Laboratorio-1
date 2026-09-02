"""
Este programa genera una matriz de valores booleanos (0 y 1) y la
almacena directamente en un archivo binario.

La matriz se genera por bloques de filas. Cada bloque se mantiene
temporalmente en la memoria RAM y, una vez generado, se escribe
directamente en el disco.

De esta manera, no es necesario disponer de una cantidad de memoria
RAM equivalente al tamaño completo de la matriz.
"""


# IMPORTS:
# Numpy que permite generar muchos valores simultáneamente
# time que permite medir cuánto tarda la generación de la matriz
# os que permite consultar información del archivo, como tamaño en bytes.
import numpy as np
import time
import os



def generar_matriz(ruta_salida, filas, columnas, filas_por_bloque=500, semilla=None):
    
    
    '''
    Esta función se encarga de generar una matriz de valores booleanos y alamacenarla en el disco.
    Teniendo como separador de cada fila de la columna una ","
    
    Parameters:
    - ruta_salida: Es un string con la ruta del archivo donde se almacenará la matriz.
    - filas: Es un entero con el número total de filas de la matriz
    - columnas: Es un entero con el número total de columnas de la matriz
    - filas_por_bloque: Es un parámetro que permite controlar la cantidad de filas qeu se 
    generan en cada operación. Un valor más pequeño utiliza menos RAM , pero aumenta el número de operaciones
    de escritura
    - semilla: semilla que utilizada para el generador de números aleatorios, que sirve para obtener los mismos números
    aleatorios para un mismo valor de la semilla

    '''
    
    # PLANTILLA PARA LA MATRIZ
    
    # Se crea un generador de números aleatorios, dandole una semilla, para obtener valores con los que podamos comparar
    rng = np.random.default_rng(semilla)

    bytes_por_fila = columnas + 1  # Cada fila contiene un byte por columna más el del separador de la fila: ","

    # Plantilla reutilizable: Se crea una matriz llena de comas de tamaño: filas_por_bloque x bytes_por_fila.
    # Luego, las demás columnas se llenaran de 0 y 1.
    plantilla = np.full((filas_por_bloque, bytes_por_fila), ord(','), dtype=np.uint8)   # unint8 significa que cada elemento ocupa 1 byte.
                                                                                        # ord convierte la coma al número 44 según su código ASCII ya que Numpy trabaja con números.
   
    
    # TAMAÑO DEL ARCHIVO
    
    # Se calcula cuánto espacio ocupará la matriz en el disco 
    tam_estimado_gb = (filas * bytes_por_fila) / (1024 ** 3)     # Dividir entre 1024**1 pasa de bytes a KB, entre 1024**2 pasa a MB y entre 1024**3 pasa a GB (En este laboratorio: 9.31 GB)
    print(f"Filas: {filas:,} | Columnas: {columnas:,}") 
    print(f"Tamano estimado del archivo: {tam_estimado_gb:.2f} GB")
    print("Ahora mismo se está generando...")

    
    # Se inicia el contador de tiempo para medir cuánto se demora en hacer la matriz.
    inicio = time.time()
    
    # Contador que indica cuántas filas han sido generadas y escritas.
    filas_escritas = 0
    
    # CREACIÓN DEL ARCHIVO:
    
    # 'wb' significa: w = escritura y b = modo binario. Sirve para crear o abrir un archivo y escribir datos en formato binario de forma segura.
    
    # El archivo se abre en modo binario porque cada valor es 0 ó 1.
    # f es el nombre de variable que se le va a asignar al archivo.

    with open(ruta_salida, 'wb') as f:
        
        # El ciclo termina cuando todas las filas estén llenas.
        while filas_escritas < filas:
            
            # n determina cuántas filas procesar en el bloque actual. Normalmente toma el bloque completo menos en la ultima interacción que son las restantes.
            n = min(filas_por_bloque, filas - filas_escritas)
            
            # Genera una matriz aleatoria de ceros y unos ya que el rango es [1,2) de tamaño del bloque (n, columnas).
            # Solo este bloque permanece en RAM.
            valores = rng.integers(0, 2, size=(n, columnas), dtype=np.uint8)

            # Se copia la plantilla de la matriz (llena de comas) para construir el bloque.
            # Es necesaria la copia para no modificar plantilla y poderla reutilizar.
            bloque = plantilla[:n].copy()
            # Se sobreescriben las columnas correspondientes a ceros y unos, menos la última que es el separador.
            bloque[:, :columnas] = valores + ord('0')  # '0' o '1' ya que ord('0') = 0. Entonces 0 + ord('0') = 0 y 1 + ord('0') = 1


            # ESCRITURA EN EL DISCO
            
            
            # tobytes() convierte el bloque de Numpy en una secuencia de bytes para escribirla directamente en el archivo.
            # Y como estamos usando wb, los nuevos datos se pegan al final de lo que ya se tenía antes.
            f.write(bloque.tobytes())
            # Se actualiza el contador.
            filas_escritas += n

            # Se muestra en pantalla cada 20 bloques pocesados el número de filas escritas y el tiempo transcurrido.
            if filas_escritas % (filas_por_bloque * 20) == 0 or filas_escritas == filas:
                transcurrido = time.time() - inicio
                print(f"  {filas_escritas:,}/{filas:,} filas escritas ({transcurrido:.1f} s)")

    
    # INFORMACIÓN ADICIONAL
    # Tiempo total para generar la matriz
    total = time.time() - inicio
    
    # Se obtiene el tamaño real de los datos.
    tam_real = os.path.getsize(ruta_salida)
    print(f"\nListo. Archivo creado: {ruta_salida}")
    print(f"Tamano real: {tam_real:,} bytes ({tam_real / 1024**3:.2f} GB)")
    print(f"Tiempo total: {total:.1f} s")

    