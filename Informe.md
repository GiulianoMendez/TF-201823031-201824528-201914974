# *Informe Trabajo Final Complejidad Algoritmica*

### Integrantes:
* Leonardo Grau
* Bruno Palomino
* Giuliano Mendez

### Introduccion:
El trabajo surgio de la problematica en la perdida de tiempo para el traslado de las calles, por algunos motivos, como el trafico. Pero gracias a la informacion de las calles, nombre, una longitud, permite encontrar caminos mas cortos.

Con los datos ya mencionados, se crean interseccion de un mapa, y lo representamos mediante un grafo a traves de una interfaz, el cual consta de aristas y vertices que representaran con las imagen de calles y sus intersecciones.En el presente Proyecto elaboramos un grafo para representar una porcion de 1500 aristas de la ciudad, gracias a google masps.

### Ciudad Elegida :
Escogimos la ciudad de Buenos Aires por el orden y variedad de calles unidas

### Resumen Ejecutivo:
Se solicito elaborar un grafo con las intersecciones de las calles de una ciudad o parte de esta. Usamos un generador de calles (over pass turbo)
para obtener la informacion y google colab para implementar las funciones con la data.

Una vez se obtuvo la informacion necesaria para la lista de adyacencia, se procedio a implementarla en un los archivos de texto.

### Analisis de las intersecciones:
Para la creacion de las interseccion usamos una estructura de latitud, longitud, Ncalle horizontal y Ncalle vertical.

### Elaboracion del Grafo
Se leen los archivos streets.txt, nodes,txt y edges,txt.
Creamos una lista de adyasencia, simula los caminos existentes en cada una de las interscciones, con el conteo manual.

Posteriormente se hizo uso de las funciones, trafiweigth el cual permite cambiar el paso de las aristas a ciertas horas, genera perlin noise, el cual crea una matriz de distribucion, luego varperlin noise, que ayuda a encontrar un numero aleatorio y encontrar el peso de los caminos

### Conclusiones 
Pudimos implementar los algoritmos Dijkstra unos de los algoritmos mas conocidos y utlizados en grafos para la busqueda de un camino mas corto.
Habiendo desarrolado el grafo se ha incrementado el numero de posiblidades de rutas mas corta en funcion al tiempo o peso de la calle
En este sentido la inclusion de variables en el proceso como latitud y longitud ayudo a encontrar las rutas mas adecuadas.
