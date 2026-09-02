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
- Verificacion completa: se cuentan TODAS las comas del archivo (por
  bloques, sin cargarlo entero en RAM) y se confirma que ese total
  coincide con las filas calculadas. Esa coincidencia es la prueba de
  que, sin conocer de antemano el contenido del archivo, se puede
  determinar que es una matriz y con que dimensiones.
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

    def contar_filas_por_comas(self, tam_bloque=1 << 20):
        """
        Cuenta el numero TOTAL de comas en el archivo completo, leyendolo
        por bloques (por defecto de 1 MB) para no cargarlo entero en RAM.

        Como cada fila termina en EXACTAMENTE una coma, el numero total de
        comas encontradas debe coincidir con el numero de filas que ya
        habiamos calculado con tamano_archivo / bytes_por_fila.

        Esta es la prueba central de que el archivo es una matriz: sin
        saber de antemano que contiene, contamos cuantas veces aparece el
        separador de fila, y si ese conteo coincide con las filas
        esperadas (y estas, multiplicadas por las columnas detectadas por
        la posicion de la primera coma, dan el total de valores), queda
        demostrado que el archivo tiene la estructura de una matriz de
        'filas' x 'columnas' booleanos.
        """
        self.f.seek(0)
        total_comas = 0
        while True:
            bloque = self.f.read(tam_bloque)
            if not bloque:
                break
            total_comas += bloque.count(b',')

        return {
            "comas_encontradas": total_comas,
            "filas_esperadas": self.filas,
            "columnas_detectadas": self.columnas,
            "coincide": total_comas == self.filas,
        }

    def verificar_contenido(self, muestras=500):
        """
        Verifica el CONTENIDO de la matriz (no solo la estructura):
        - Todos los bytes de valores deben ser '0' o '1' (ningun caracter raro,
          senal de que el archivo no se corrompio).
        - Reporta la proporcion de True/False encontrada, que deberia rondar
          el 50% cada uno si la generacion aleatoria fue correcta.
        Revisa una muestra de filas para no tener que leer archivos enormes
        por completo.
        """
        n_chequear = min(muestras, self.filas)
        indices = (random.sample(range(self.filas), n_chequear)
                   if self.filas > n_chequear else range(self.filas))

        total_valores = 0
        total_verdaderos = 0
        bytes_invalidos = 0

        for i in indices:
            self.f.seek(i * self.bytes_por_fila)
            fila = self.f.read(self.columnas)
            for b in fila:
                if b == ord('1'):
                    total_verdaderos += 1
                elif b != ord('0'):
                    bytes_invalidos += 1
            total_valores += len(fila)

        proporcion_verdaderos = total_verdaderos / total_valores if total_valores else 0

        return {
            "filas_revisadas": n_chequear,
            "valores_revisados": total_valores,
            "bytes_invalidos": bytes_invalidos,
            "contenido_valido": bytes_invalidos == 0,
            "proporcion_true": round(proporcion_verdaderos, 4),
        }

    def obtener_fila(self, i):
        """Devuelve la fila i como lista de booleanos, con un solo seek+read."""
        if not (0 <= i < self.filas):
            raise IndexError("Fila fuera de rango")
        self.f.seek(i * self.bytes_por_fila)
        valores = self.f.read(self.columnas)
        return [b == ord('1') for b in valores]

    def guardar_fila(self, i, ruta_salida):
        """
        Extrae la fila i (usando obtener_fila, sin leer el archivo
        completo) y la guarda en un archivo de texto aparte, separada
        por comas. Sirve como evidencia concreta: un archivo chiquito
        que contiene solo una fila de la matriz gigante, extraida
        directamente por posicion (offset), sin recorrer el archivo
        original.
        """
        valores = self.obtener_fila(i)
        contenido = ",".join("1" if v else "0" for v in valores)
        with open(ruta_salida, "w") as f_salida:
            f_salida.write(contenido)
        return ruta_salida

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


