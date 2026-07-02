import time # Libreria nativa NECESARIA para medir el tiempo de ejecucion

# UNICAS LIBRERIAS NATIVAS *PARA INTERFAZ GRAFICA Y SISTEMA*
import tkinter as tk 
from tkinter import filedialog 
import os   

from estructura_hash import TablaHash, TablaHashProbing # propia libreria que contiene la estructura de la tabla hash


def cargar_datos_desde_archivo(archivo, hash_table, hash_probing, lista_comun):
    cantidad = 0 # cantidad de contraseñas en el archivo
    try:
        with open(archivo, 'r', encoding='utf-8', errors='ignore') as f: # errors=ignore evita que el programa caiga
            for linea in f:   # recorre cada linea del archivo (cada contraseña)
                credencial = linea.strip()  # elimina espacios en blanco y saltos de linea
                if credencial: 
                    # 1. Inserta en la Tabla Hash O(1)
                    hash_table.insertar(credencial) 
                    # 2. Inserta en la Tabla Hash con Probing O(1)
                    hash_probing.insertar(credencial)
                    # 3. Inserta en la Lista Común de Python para la comparación O(n)
                    lista_comun.append(credencial)
                    
                    cantidad += 1   # aumenta la cantidad de contraseñas recorridas +1
        print("[OK] Base de datos cargada en memoria.")
        return cantidad
    
    except FileNotFoundError:   # si no existe archivo
        print("[ ERROR :( ] No se encontró el archivo") # no se encontro el archivo
        return 0

# abre una ventana para seleccionar la base de datos
def seleccionar_archivo_gui(titulo_ventana): # reutilizable
    
    root = tk.Tk() # ventana principal de tkinter
    root.withdraw() # oculta la fea ventana gris
    
    ruta_archivo = filedialog.askopenfilename( # abre explorador de archivos nativo del SO
        title=titulo_ventana,
        filetypes=[("Archivos de texto", "*.txt")]      # IMPORTANTE!!! verifica que el archivo sea .txt
    )
    return ruta_archivo # devuelve la ruta del archivo seleccionado

def analizar_y_reportar(ruta_consulta, hash_table, hash_probing, lista_comun, nombre_bd, largo_bd):
    nombre_consulta = os.path.basename(ruta_consulta) # utiliza os para solo obtener el nombre del archivo
    print(f"[OK] Archivo a revisar seleccionado: {nombre_consulta}\n")
    print("--- RESULTADOS DE ESCANEO---") # titulo
    
    try:
        with open(ruta_consulta, 'r', encoding='utf-8', errors='ignore') as archivo_consultas: 
            consultas = archivo_consultas.readlines() # lee todas las lineas de golpe
            largo_consulta = len(consultas) # cuenta la cantidad de contraseñas en el archivo 
            
            contrasenas_revisadas = 0 
            lista_vulneradas = [] # almacena contraseñas vulneradas encontradas por el Hash
            
            # 1. USANDO TABLA HASH...
            
            tiempo_inicio_hash = time.perf_counter() 
            
            for linea in consultas: 
                pwd_sus = linea.strip() 
                if pwd_sus:
                    contrasenas_revisadas += 1 
                    if hash_table.buscar(pwd_sus): # Búsqueda O(1)
                        lista_vulneradas.append(pwd_sus) 
            
            tiempo_fin_hash = time.perf_counter() 
            tiempo_ms_hash = (tiempo_fin_hash - tiempo_inicio_hash) * 1000 # diferencia de tiempo hash y *1000 para convertir a milisegundos

            # 2. USANDO TABLA HASH CON PROBING...

            tiempo_inicio_probing = time.perf_counter() 
            for linea in consultas: 
                pwd_sus = linea.strip() 
                if pwd_sus:
                    hash_probing.buscar(pwd_sus) 
            tiempo_fin_probing = time.perf_counter() 
            tiempo_ms_probing = (tiempo_fin_probing - tiempo_inicio_probing) * 1000 # diferencia de tiempo hash probing y *1000 para convertir a milisegundos
            
            
            # 3. USANDO LISTA COMUN...

            tiempo_inicio_lineal = time.perf_counter() 
            
            for linea in consultas: 
                pwd_sus = linea.strip() 
                if pwd_sus: 
                    # Búsqueda secuencial comun en un arreglo O(n)
                    if pwd_sus in lista_comun: 
                        pass # solo se mide el tiempo, pass 
            
            tiempo_fin_lineal = time.perf_counter() 
            tiempo_ms_lineal = (tiempo_fin_lineal - tiempo_inicio_lineal) * 1000 # diferencia de tiempo lineal y *1000 para convertir a milisegundos
            
            # GENERAR REPORTE Y COMPARAR TIEMPOS

            archivo_reporte = "REPORTE_FINAL.txt"
            with open(archivo_reporte, "w", encoding='utf-8') as f_reporte: # abre archivo de reporte ("w" para escribir/sobrescribir)
                
                f_reporte.write("[REPORTE Y EXPERIMENTACION]\n\n") # titulo
                
                f_reporte.write("[BASE DE DATOS USADA]\n")
                f_reporte.write(f"{nombre_bd}\n") # nombre de la base de datos q se uso
                f_reporte.write(f"CANTIDAD DE ELEMENTOS : {largo_bd}\n\n") # cantidad de contraseñas en bd
                
                f_reporte.write("[ARCHIVO DE CONTRASEÑAS A REVISAR]\n")
                f_reporte.write(f"{nombre_consulta}\n")
                f_reporte.write(f"CANTIDAD DE ELEMENTOS : {largo_consulta}\n\n")  # cantidad de contraseñas a revisar
                
                f_reporte.write("[CONTRASEÑAS REVISADAS]\n")
                f_reporte.write(f"{contrasenas_revisadas}\n\n") # cantidad de contraseñas revisadas
                
                f_reporte.write("[METRICAS DE RENDIMIENTO]\n")
                f_reporte.write(f"Tiempo Busqueda Lineal Comun O(n)            : {tiempo_ms_lineal:.4f} ms\n") # se usa :..4f para 4 decimales
                f_reporte.write(f"Tiempo Tabla Hash O(1) [Listas Enlazadas]    : {tiempo_ms_hash:.4f} ms\n") # se usa :..4f para 4 decimales
                f_reporte.write(f"Tiempo Tabla Hash O(1) [Linear Probing]      : {tiempo_ms_probing:.4f} ms\n\n") # se usa :..4f para 4 decimales
                
                if len(lista_vulneradas) > 0: # si la lista de vulneradas tiene elementos...

                    f_reporte.write("***ALERTA, SE ENCONTRARON CONTRASEÑAS VULNERADAS***\n\n")
                    f_reporte.write("[CONTRASEÑAS VULNERADAS]\n")
                    f_reporte.write(f"CANTIDAD : {len(lista_vulneradas)}\n\n")  # cantidad de contraseñas vulneradas (elementos en lista_vulneradas)    
                    
                    for pwd in lista_vulneradas:    # para cada contraseña vulnerada (pwd) en lista_vulneradas...
                        f_reporte.write(f"{pwd}\n")     # se imprime la contraseña
                else: # SI NO HAY ELEMENTOS EN lista_vulneradas...
                    f_reporte.write("***INFO: NO SE ENCONTRARON CONTRASEÑAS VULNERADAS***\n") # no se encontraron contraseñas vulneradas

            # EN LA CONSOLA SE IMPRIME...
            print(f"Total de vulnerabilidades halladas: {len(lista_vulneradas)}") 
            print(f">>> Tiempo Busqueda Lineal Comun      : {tiempo_ms_lineal:.4f} ms.")
            print(f">>> Tiempo Tabla Hash                 : {tiempo_ms_hash:.4f} ms.") 
            print(f">>> Tiempo Hash [Linear Probing]      : {tiempo_ms_probing:.4f} ms.")
            print(f"\n[nice] Todo el detalle se ha exportado al archivo '{archivo_reporte}'.") 
            
    except Exception as e: # si ocurre algun error durante la ejecucion
        print(f"[ ERROR :( ] Hubo un problema al leer el archivo consultado: {e}")

def ejecutar_experimento():

    print("\n\n--- BIENVENIDO AL SISTEMA DE DETECCIÓN DE CREDENCIALES ---")
    
    print("\n[PASO 1] Selecciona la BASE DE DATOS en la ventana emergente (puedes usar el archivo [BD] que se encuentra en /archivos_ejemplo)")
    ruta_bd = seleccionar_archivo_gui("1. Selecciona tu base de datos principal") 
    
    if not ruta_bd: # si no se selecciona ninguna base de datos...
        print("[AVISO] No seleccionaste ninguna base de datos. Saliendo...")
        return # el programa te bota
    
    # calcular una cantidad realista para evitar exceso de consumo de memoria (esto asegura que el Factor de Carga (Load Factor) siempre sea = 0.5)
    cantidadlineas = 0
    with open(ruta_bd, 'r', encoding='utf-8', errors='ignore') as total: 
        for linea in total:
            if linea.strip(): # si la linea no es nulo o vacio
                cantidadlineas += 1 # aumenta en 1
    cap_variable = cantidadlineas * 2 # calcula la capacidad VARIABLE para la tabla hash

    hash_table = TablaHash(cap_variable) # crea tabla hash con capacdad variable
    hash_probing = TablaHashProbing(cap_variable) # crea tabla hash con probing con capacdad variable
    lista_comun_bd = [] # arreglo comun para comparar rendimiento

    nombre_bd = os.path.basename(ruta_bd) 
    # carga datos en la tabla hash y la lista comun
    largo_bd = cargar_datos_desde_archivo(ruta_bd, hash_table, hash_probing, lista_comun_bd) 
    
    print("\n[PASO 2] Selecciona el ARCHIVO A REVISAR en la ventana emergente (puedes usar el archivo [PWD] que se encuentra en /archivos_ejemplo)")
    consulta = seleccionar_archivo_gui("2. Selecciona el archivo de contraseñas a revisar")
    
    if consulta:
        # se llama a la funcion analizar_y_reportar pasándole ambas estructuras
        analizar_y_reportar(consulta, hash_table, hash_probing, lista_comun_bd, nombre_bd, largo_bd)
    else:
        print("[AVISO] No se seleccionó ningún archivo. Escaneo cancelado.")

if __name__ == "__main__": # ejecuta solo la funcion principal (ejecutar_experimento)
    ejecutar_experimento()