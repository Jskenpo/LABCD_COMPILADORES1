import re

# Estructuras de datos para almacenar los elementos del lenguaje
symbols = {}
regular_elements = []

def read_var(filename):
    with open(filename) as f:
        is_tokens_section = False  # Variable para indicar si estamos en la sección de tokens
        
        for line in f:
            line = line.strip()
            
            # Eliminar comentarios
            line = re.sub(r'\(\*.*?\*\)', '', line)
            
            # Analizar variables 
            if line.startswith("let"):
                name, value = re.search(r"let\s+(\w+)\s*=\s*(.*)", line).groups()
                symbols[name] = value.strip()

    return symbols


def read_regdef(filename):
    with open(filename) as f:
        is_tokens_definition = False  # Variable para indicar si estamos en la definición de tokens
        
        for line in f:
            line = line.strip()
            
            # Eliminar comentarios
            line = re.sub(r'\(\*.*?\*\)', '', line)
            
            # Buscar la definición de tokens
            if line.startswith("rule tokens ="):
                is_tokens_definition = True
                continue
            
            # Procesar la definición de tokens
            if is_tokens_definition:
                # Ignorar líneas en blanco
                if not line:
                    continue
                
                # Romper si alcanzamos el final de la definición de tokens
                if line.startswith("rule") or line.startswith("}"):
                    break
                
                # Dividir la línea y obtener la parte derecha de la definición del token
                elements = line.split('|')
                for element in elements:
                    if element.strip():
                        regular_elements.append(element.strip())

# Llamar a las funciones para leer los datos

archivo = "slr-1.yal"

symbols = read_var(archivo)
read_regdef(archivo)

# Imprimir resultados                   
print("Símbolos:")
print(symbols)

print("Elementos de la definición regular:")
print(regular_elements)
