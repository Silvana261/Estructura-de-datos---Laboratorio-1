
import os
import random

class MatrizArchivo:
    
    
    '''
    
    Esta parte del programa permite leer, verificar y acceder a una matriz almacenada en un
    archivo binario. 
    Identifica la matriz de manera que cada valor ocupa un byte correspondiente al carácter "0" o "1".
    Y cada fila termina con una coma como separador.
    Las dimensiones de la matriz no se reciben, por lo que no se sabe que es una matriz, sino que
    se deduce a partir del archivo.
    
    '''
    def __init__(self, ruta):
        '''
        Recibe la ruta del archivo que contiene la matriz.
        '''
        
        
        self.ruta = ruta
        
        # Se abre el archivo en modo lectura binaria.
        self.file = open(ruta, 'rb')


        # Aquí se lee el primer MB del archivo para encontrar la primera coma, o sea la primera fila.
        fragmento = self.file.read(1 << 20)  # 1 MB de muestra se guarda en fragmento.
        posicion_coma = fragmento.find(b',')  # find busca la primera aparición de la coma.
        if posicion_coma == -1:
            raise ValueError(
                "No se encontro ninguna coma en el fragmento inicial: "
                "El archivo no corresponde a la matriz a la estructura establecida."
            )

        #La posición de la primera coma corresponde a la cantidad de columnas de la matriz.
        self.columnas = posicion_coma
        
        # La cantidad total de bytes en cada fila es la cantidad de columnas ya que cada valor ocupa un byte + la coma que separa la fila.
        self.bytes_por_fila = self.columnas + 1

        # Se obtiene el tamaño total del archivo interactuando con el sistema operativo, obteniendo con getsize la cantidad exacta de bytes.
        tamanno_archivo = os.path.getsize(ruta)
        
        
        # COMPROBAR QUE COINCIDE CON UNA MATRIZ
        # El tamaño del archivo debería ser divisible exactamente entre el tamaño de una fila, para que tenga las filas completas.
        if tamanno_archivo % self.bytes_por_fila != 0:
            raise ValueError(
                "El tamano del archivo no es multiplo exacto del tamano "
                "de una fila: no parece ser una matriz bien formada."
            )

        #Se calcula la cantidad de filas dividiendo el tamaño total entre el tamaño de una fila
        self.filas = tamanno_archivo // self.bytes_por_fila
        
        

    def contar_filas_por_comas(self, tam_bloque=1 << 20):
        """
        Cuenta todas las comas existentes en el archivo. El cual se leerá por bloques
        para evitar cargarlo completo a memoria. La cantidad de comas deberá coincidir con la 
        cantidad de filas calculada a partir del tamaño del archivo.
        
        PARAMETER:
        - tam_bloque (int): Cantidad de bytes que se leen en cada bloque ( 1 MB)

        """
        # seek() es el método que desplaza la posición del cursor de lectura o escritura dentro del archivo
        # El cual ponemos en el byte incial.
        self.file.seek(0)
        total_comas = 0
        
        # El archivo se lee por bloques para no cargarlo todo de una vez.
        while True:
            bloque = self.file.read(tam_bloque)

            if not bloque:
                break

            # Se cuentan las comas encontradas en cada bloque.
            total_comas += bloque.count(b',')

        # Cada fila termina en una coma.
        # Por lo tanto, el número de comas debe ser igual
        # al número de filas calculadas.
        return total_comas == self.filas

    def verificar_contenido(self, muestras=500):
        """
       Verifica que los valores almacenados sean solo 0 y 1 
       Selecciona una muestra aleatoria de filas.
        """
        n_chequear = min(muestras, self.filas)
        indices = (random.sample(range(self.filas), n_chequear)
                   if self.filas > n_chequear else range(self.filas))

        # Se revisan las filas seleccionadas.
        for i in indices:

            # Se calcula directamente la posición donde comienza la fila.
            self.file.seek(i * self.bytes_por_fila)

            # Se leen los valores de la fila.
            fila = self.file.read(self.columnas)

            # Se verifica que todos los valores sean '0' o '1'.
            for b in fila:
                if b != ord('0') and b != ord('1'):
                    return False

        # Si ninguna posición presentó un valor inválido,
        # el contenido se considera válido.
        return True

    def obtener_fila(self, i):
        """
        Obtiene una fila específica de la matriz.

        El acceso se realiza directamente mediante su posición en el
        archivo, por lo que no es necesario recorrer las filas
        anteriores.
        
        PARAMETERS:
        - i (int): índice de la fila.
        """
        
        # Se verifica que la fila exista.
        if not (0 <= i < self.filas):
            raise IndexError("Fila fuera de rango")
        # Se calcula la posición exacta donde comienza la fila, sin necesidad de recorrerlas todas.
        self.file.seek(i * self.bytes_por_fila)
        valores = self.file.read(self.columnas)
        return [b == ord('1') for b in valores] # Se leen y convierten los caracteres a valores booleanos.

    def guardar_fila(self, i, ruta_salida):
        """
        Extrae una fila y la guarda en un archivo de texto.
        """
        # Se obtiene la fila con la función anterior, directamente del archivo
        valores = self.obtener_fila(i)
        
        # Se convierte a texto, utilizando comas entre los valores para ser mostrados
        contenido = ",".join("1" if v else "0" for v in valores)
        # Se crea un archivo independiente que contiene solo a la fila.
        with open(ruta_salida, "w") as f_salida:
            f_salida.write(contenido)
        return ruta_salida

    def obtener_valor(self, i, j):
        """
        Devuelve el valor (i, j) leyendo un unico byte del archivo.
        """
        # Se verifica que la fila y la columna estén dentro los límites.
        if not (0 <= i < self.filas):
            raise IndexError("Fila fuera de rango")
        if not (0 <= j < self.columnas):
            raise IndexError("Columna fuera de rango")
        
        # Se calcula la posición exacta del elemento dentro del archivo.
        # Se multiplica la fila por el tamaño de una fila y se suma
        # la posición de la columna.
        self.file.seek(i * self.bytes_por_fila + j)
        return self.file.read(1) == b'1'

    def cerrar(self):
        self.file.close() # Para liberar el recurso.