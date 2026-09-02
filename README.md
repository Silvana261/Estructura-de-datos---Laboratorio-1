# Matriz almacenada en disco

## Laboratorio 1

**Estudiante:** Silvana Saavedra Londoño 

## Descripción

Este laboratorio consiste en la generación, almacenamiento y lectura de una matriz de valores booleanos `0` y `1` de gran tamaño, utilizando el disco duro como medio de almacenamiento.

La matriz utilizada tiene unas dimensiones de **100.000 filas × 100.000 columnas**, lo que representa **10.000 millones de valores**.

Debido al gran tamaño de la matriz, no resulta conveniente mantenerla completa en la memoria RAM. Por esta razón, la matriz se genera y almacena directamente en un archivo, trabajando por bloques.

El archivo utiliza un formato sencillo en el que cada valor ocupa un byte y cada fila termina con una coma como separador.



El programa permite:

* Generar la matriz por bloques.
* Almacenar la matriz directamente en el disco.
* Determinar las dimensiones de la matriz a partir del archivo.
* Verificar la estructura del archivo mediante el número de comas.
* Verificar que los valores almacenados sean únicamente `0` o `1`.
* Acceder directamente a una fila específica.
* Acceder directamente a un elemento específico mediante su fila y columna.
* Extraer una fila y guardarla en un archivo independiente.

## Formato del archivo

La matriz se almacena en un archivo binario con la siguiente estructura:


Cada valor de la matriz se almacena como el carácter `0` o `1`, ocupando un byte.

Cada fila termina con una única coma como separador de filas:

```text
1010010110,
```

Por lo tanto, si una fila tiene `n` columnas, ocupa:

```text
n + 1 bytes
```

El byte adicional corresponde a la coma que funciona como separador de filas.

## Organización del proyecto

El repositorio contiene los siguientes archivos:

### `GenerarMatriz.py`

Contiene la función `generar_matriz()`, encargada de crear la matriz y almacenarla directamente en el disco.

La matriz no se genera completa en la memoria RAM. En su lugar, se generan bloques de filas y cada bloque se escribe inmediatamente en el archivo.

Para generar los valores se utiliza **NumPy**, que permite generar múltiples valores `0` y `1` simultáneamente.

También se utiliza este archivo para:

* Medir el tiempo de generación.
* Crear el archivo en modo binario.
* Escribir los bloques de datos en el disco.
* Mostrar información sobre el progreso de la generación.

### `LeerMatriz.py`

Contiene la clase `MatrizArchivo`, encargada de leer, verificar y acceder a la matriz almacenada en el archivo.

Las dimensiones de la matriz no se proporcionan al momento de abrir el archivo. Estas se obtienen directamente a partir de su estructura.

Primero se busca la primera coma del archivo. La posición de esta coma permite determinar la cantidad de columnas.

Después se calcula el tamaño de una fila:

```text
bytes_por_fila = columnas + 1
```

Finalmente, la cantidad de filas se obtiene dividiendo el tamaño total del archivo entre el tamaño de una fila.

La clase también permite:

* Verificar que la cantidad de comas corresponda con la cantidad de filas.
* Verificar que los valores almacenados sean `0` o `1`.
* Obtener una fila específica mediante acceso directo.
* Obtener un elemento específico de la matriz.
* Guardar una fila en un archivo de texto.
* Cerrar el archivo.

### `main.py`

Es el archivo principal del proyecto y controla la ejecución de las diferentes funciones.

En este archivo se realiza el siguiente proceso:

1. Se genera la matriz.
2. Se abre el archivo generado.
3. Se verifica que la cantidad de comas coincida con la cantidad de filas.
4. Se verifica que el contenido de la matriz sea válido.
5. Se demuestra el acceso directo a la primera fila.
6. Se demuestra el acceso directo a la última fila.
7. Se obtiene un elemento específico de la matriz.
8. Se extrae la primera fila y se almacena en `fila_0.txt`.

### `matriz.txt`

Es el archivo que contiene la matriz generada.

Para la matriz de `100.000 × 100.000`, el archivo ocupa aproximadamente **9,31 GiB**, debido a que cada valor utiliza un byte y cada fila tiene un byte adicional correspondiente a la coma.

### `fila_0.txt`

Es un archivo generado por el programa que contiene únicamente la primera fila de la matriz.

Se utiliza como evidencia de que es posible extraer una fila específica de la matriz almacenada en disco.

## Acceso directo a la matriz

Una de las características principales del programa es que no es necesario recorrer todas las filas anteriores para acceder a una fila determinada.

La posición de una fila se calcula mediante:

```text
posición = fila × bytes_por_fila
```

Por ejemplo, para acceder a una fila determinada, el programa utiliza `seek()` para desplazarse directamente hasta su posición dentro del archivo.

De manera similar, para acceder a un único elemento se calcula:

```text
posición = fila × bytes_por_fila + columna
```

Esto permite obtener un valor específico leyendo únicamente un byte del archivo.

## Verificación de la matriz

Se realizan dos verificaciones principales.

### Verificación mediante las comas

Como cada fila termina exactamente con una coma, se recorren los datos del archivo por bloques y se cuentan las comas.

Si:

```text
número de comas = número de filas
```

se confirma que la cantidad de separadores de fila coincide con la cantidad de filas calculada a partir del tamaño del archivo.

### Verificación del contenido

Se selecciona una muestra aleatoria de filas y se comprueba que sus valores sean únicamente:

```text
0
1
```

No es necesario revisar toda la matriz para realizar esta comprobación, lo que evita recorrer los 10.000 millones de valores.

## Uso de memoria

La generación de la matriz se realiza por bloques.

Por ejemplo, utilizando:

```python
filas_por_bloque=500
```

solo un bloque de 500 filas se mantiene temporalmente en RAM mientras se genera y posteriormente se escribe en el disco.

Esto permite trabajar con matrices cuyo tamaño completo sería demasiado grande para mantenerlas en memoria RAM.

## Ejecución

Para ejecutar el proyecto se debe ejecutar:

```bash
python main.py
```

El programa generará la matriz y posteriormente realizará las verificaciones y demostraciones de acceso.

## Resultado esperado

Al finalizar, el programa muestra información relacionada con:

* La generación de la matriz.
* La verificación de las comas.
* La validez del contenido.
* El acceso a la primera y última fila.
* El acceso a un elemento específico.
* La creación del archivo `fila_0.txt`.

De esta manera se demuestra que una matriz de gran tamaño puede almacenarse en disco y consultarse mediante acceso directo, sin necesidad de cargar toda la matriz en la memoria RAM.
