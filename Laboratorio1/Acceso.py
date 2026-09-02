'''
Esta parte permite trabajar con matriz sin tener que cargarla por completo a RAM
Aprovechando que todas las filas tienen el mismo tamaño y los elementos son de longitud fija
podemos calcular las posiciones directamente de cualquier elemento del archivo (offset).
'''


import os
import random


class MatrizArchivo:
    
    ''' Esta clase representa la matriz almacenada en el disco'''
    
    def __init__(self, ruta):
        # Se guarda la ruta del archivo y también se abre el archivo en modo lectura binaria "rb"
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