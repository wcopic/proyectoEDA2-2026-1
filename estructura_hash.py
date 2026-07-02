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

# Estructura de Tabla Hash con manejo de colisiones mediante linear probing:   
class TablaHashProbing:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.tabla = [None] * capacidad

    def _funcion_hash(self, cadena):
        hash_val = 0
        for caracter in cadena:
            hash_val = (hash_val * 31 + ord(caracter)) % self.capacidad # aqui el hash function es distinto para evitar clustering (que todas las contraseñas caigan en los mismos indices)
        return hash_val

    def insertar(self, cadena):
        indice = self._funcion_hash(cadena)
        
        # Linear Probing: busca el siguiente espacio vacío
        while self.tabla[indice] is not None: # mientras que el nodo en el indice no sea None...
            if self.tabla[indice] == cadena: # si la contraseña ya existe no se inserta
                return # Evita duplicados
            indice = (indice + 1) % self.capacidad # se mueve al siguiente indice 
            
        self.tabla[indice] = cadena # Inserta directamente el string

    def buscar(self, cadena):
        indice = self._funcion_hash(cadena)
        indice_inicial = indice
        
        while self.tabla[indice] is not None:
            if self.tabla[indice] == cadena:
                return True
            indice = (indice + 1) % self.capacidad
            if indice == indice_inicial: # si ya dio la vuelta entera a la tabla
                break
                
        return False   