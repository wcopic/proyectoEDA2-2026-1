# Sistema de Deteccion de Credenciales (Proyecto EDA2)

Este proyecto implementa un sistema para auditar credenciales y detectar contraseñas vulneradas. El programa realiza un experimento de rendimiento comparando el tiempo de ejecución entre una estructura de Tabla Hash (con complejidad O(1) mediante Separate Chaining) y una búsqueda lineal en un arreglo común (complejidad O(n)). 

[Aviso] Este proyecto no usa NINGUNA libreria externa, solo usa las nativas de Python.

## Requisitos

* Python 3.x instalado en el sistema.

## Archivos de Ejemplo

Para facilitar las pruebas, el repositorio incluye una carpeta llamada `archivos_ejemplo` con datos listos para el experimento:

* `[BD] 100k-most-used-passwords-NCSC.txt`: Actúa como la base de datos masiva de contraseñas comprometidas.
* `[PWD] Pwdb_top-10000.txt`: Actúa como el archivo de credenciales sospechosas que el sistema va a revisar.

## Como usar el programa

1. Abre la terminal en la carpeta principal del proyecto.
2. Ejecuta el archivo principal con el comando:
   python main.py
3. El programa abrirá una ventana emergente (Paso 1). Navega hasta la carpeta `archivos_ejemplo` y selecciona el archivo de la Base de Datos (ej. `[BD] 100k-most-used-passwords-NCSC.txt`).
4. A continuación, se abrirá una segunda ventana (Paso 2). Selecciona el archivo de contraseñas a revisar (ej. `[PWD] Pwdb_top-10000.txt`).
5. El sistema leerá los datos, ejecutará ambas búsquedas y mostrará en la consola las vulnerabilidades encontradas junto con los tiempos de ejecución comparativos.
6. Al finalizar, se generará automáticamente un archivo llamado `REPORTE_FINAL.txt` en el directorio principal con todo el detalle de las contraseñas vulneradas y las métricas de rendimiento.
