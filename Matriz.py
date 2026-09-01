
'''
Este programa genera una matriz de valores booleanos (0 y 1) y la almacena 
directamente en un archivo de texto. La cual se genera por bloques de filas y cada bloque
se escribe de una vez al disco, para no tener la necesidad de una RAM equivalente al tamaño de
la matriz.
'''


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
            bloque[:, :columnas] = valores + ord('0')  # '0' o '1' ya que ord('0') = 0 


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

    total = time.time() - inicio
    tam_real = os.path.getsize(ruta_salida)
    print(f"\nListo. Archivo creado: {ruta_salida}")
    print(f"Tamano real: {tam_real:,} bytes ({tam_real / 1024**3:.2f} GB)")
    print(f"Tiempo total: {total:.1f} s")


if __name__ == "__main__":
    # ---- AJUSTA AQUI EL TAMANO DE LA MATRIZ ----
    # Recomendado: probar primero con valores pequenos, ej. 100 x 100
    FILAS = 100_000
    COLUMNAS = 100_000
    ARCHIVO = "matriz.txt"

    generar_matriz(ARCHIVO, FILAS, COLUMNAS, filas_por_bloque=500, semilla=42)
    
    
    

"""
Lee y verifica la matriz de booleanos generada por generar_matriz.py,
SIN asumir de antemano el numero de filas ni columnas: todo se deduce
leyendo el propio archivo.

FORMATO ESPERADO
-----------------
    v0v1v2...v(n-1),v0v1v2...v(n-1),...,v0v1v2...v(n-1),

- Cada valor booleano ocupa 1 caracter ('1' o '0'), sin separador entre
  valores de la misma fila.
- Cada fila termina con una unica coma.

COMO SE DEDUCEN LAS DIMENSIONES
---------------------------------
- Columnas: posicion de la PRIMERA coma en el archivo.
- Bytes por fila: columnas + 1 (la coma).
- Filas: tamano del archivo / bytes por fila (debe ser division exacta).
- Verificacion extra: la coma debe aparecer exactamente cada
  (columnas + 1) bytes en TODAS las filas, no solo en la primera.
"""

import os
import random


class MatrizArchivo:
    def __init__(self, ruta):
        self.ruta = ruta
        self.f = open(ruta, 'rb')

        # Leemos solo un fragmento inicial para encontrar la primera coma,
        # NO hace falta leer el archivo completo para esto.
        fragmento = self.f.read(1 << 20)  # 1 MB de muestra
        pos_coma = fragmento.find(b',')
        if pos_coma == -1:
            raise ValueError(
                "No se encontro ninguna coma en el fragmento inicial: "
                "el archivo no parece tener el formato esperado."
            )

        self.columnas = pos_coma
        self.bytes_por_fila = self.columnas + 1

        tam_archivo = os.path.getsize(ruta)
        if tam_archivo % self.bytes_por_fila != 0:
            raise ValueError(
                "El tamano del archivo no es multiplo exacto del tamano "
                "de una fila: no parece ser una matriz bien formada."
            )

        self.filas = tam_archivo // self.bytes_por_fila

    def verificar_separadores(self, muestras=500):
        """
        Comprueba que la coma aparezca exactamente en la posicion esperada
        en varias filas (no solo en la primera). Por defecto revisa una
        muestra aleatoria de filas para no tener que leer todo el archivo
        cuando la matriz es enorme.
        """
        n_chequear = min(muestras, self.filas)
        indices = (random.sample(range(self.filas), n_chequear)
                   if self.filas > n_chequear else range(self.filas))
        for i in indices:
            self.f.seek(i * self.bytes_por_fila + self.columnas)
            if self.f.read(1) != b',':
                return False
        return True

    def obtener_fila(self, i):
        """Devuelve la fila i como lista de booleanos, con un solo seek+read."""
        if not (0 <= i < self.filas):
            raise IndexError("Fila fuera de rango")
        self.f.seek(i * self.bytes_por_fila)
        valores = self.f.read(self.columnas)
        return [b == ord('1') for b in valores]

    def obtener_valor(self, i, j):
        """Devuelve el valor (i, j) leyendo un unico byte del archivo."""
        if not (0 <= i < self.filas):
            raise IndexError("Fila fuera de rango")
        if not (0 <= j < self.columnas):
            raise IndexError("Columna fuera de rango")
        self.f.seek(i * self.bytes_por_fila + j)
        return self.f.read(1) == b'1'

    def cerrar(self):
        self.f.close()


if __name__ == "__main__":
    ARCHIVO = "matriz.txt"

    m = MatrizArchivo(ARCHIVO)
    print("Dimensiones detectadas SOLO a partir del archivo (sin conocerlas de antemano):")
    print(f"  Columnas: {m.columnas:,}  (= posicion de la primera coma)")
    print(f"  Filas:    {m.filas:,}     (= tamano_archivo / bytes_por_fila)")
    print(f"  Bytes por fila: {m.bytes_por_fila:,}\n")

    print("Verificando que la coma cae en la posicion correcta en varias filas...")
    print("  Resultado:", "OK, es una matriz valida" if m.verificar_separadores() else "FALLA")

    # Demostracion de acceso aleatorio sin leer todo el archivo
    print("\nPrimera fila (primeros 20 valores):", m.obtener_fila(0)[:20])
    print("Ultima fila (primeros 20 valores):", m.obtener_fila(m.filas - 1)[:20])
    print("Valor en (fila=500, columna=999):", m.obtener_valor(500, 999))

    m.cerrar()