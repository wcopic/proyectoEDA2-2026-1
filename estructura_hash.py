# Estructura de Nodo: 
class Nodo:
    def __init__(self, credencial): # self es como this en C++
        self.credencial = credencial  # texto de contraseña 
        self.siguiente = None         # puntero al siguiente nodo (inicia en None / nullptr en C++)

# Estructura de Tabla Hash con manejo de colisiones mediante listas enlazadas: 
class TablaHash: # estructura muy similar de tablahash en C++
    def __init__(self, capacidad):
        self.capacidad = capacidad # capacidad se especifica en main.py
        self.tabla = [None] * capacidad # se crea un arreglo de tamaño capacidad con valores None

    # Funcion hash: convierte una cadena de caracteres ASCII (de la contraseña) en un indice para la tabla hash
    def _funcion_hash(self, cadena):
        suma_ascii = 0
        for caracter in cadena: # recorre cada letra de la contraseña 
            suma_ascii += ord(caracter)
        return suma_ascii % self.capacidad # % asegura que el indice no supere la capacidad (residuo se convierte en el indice)

    # Funcion insertar: agrega una nueva contraseña a la tabla hash (con manejo de colisiones)
    def insertar(self, cadena):
        indice = self._funcion_hash(cadena) # llama a funcion hash para obtener el indice a partir de la contraseña
        nuevo_nodo = Nodo(cadena) # nuevo_nodo es un objeto Nodo que contiene la contraseña como cadena
        
        # Si el espacio del arreglo esta vacio
        if self.tabla[indice] is None:
            self.tabla[indice] = nuevo_nodo

        # Si hay un dato, se agrega al final de la lista
        else:
            actual = self.tabla[indice]
            while actual.siguiente is not None: # mientras nodo actual no sea None...
                actual = actual.siguiente # se avanza
            # cuando llega al final se agrega 
            actual.siguiente = nuevo_nodo

    # Funcion buscar: True si la contraseña existe y False si no
    def buscar(self, cadena):
        indice = self._funcion_hash(cadena) 
        actual = self.tabla[indice]
        
        # recorre la lista en el indice
        while actual is not None: # mientras nodo actual no sea None...
            if actual.credencial == cadena:
                return True # contraseña encontrada
            actual = actual.siguiente
            
        return False # si no se encuentra, bota False