import re 

symbols = {}
regular_elements=[]

def read_var(filename):
    with open(filename) as f:
        try:
            
            for line in f:
                line = line.strip()
                
                # Eliminar comentarios
                line = re.sub(r'\(\*.*?\*\)', '', line)
                
                # Analizar variables 
                if line.startswith("let"):
                    name, value = re.search(r"let\s+(\w+)\s*=\s*(.*)", line).groups()
                    symbols[name] = value.strip()
        except:
            print('Error: No se encontraron variables o variable mal escrita en el archivo de entrada')
            exit()
            

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


def convert_to_dictionary(elements):
    # Creamos un diccionario vacío
    regular_dict = {}
    
    # Si el primer elemento no tiene un '{', entonces se le asigna 0 en el diccionario
    if not elements[0].__contains__('{'):
        regular_dict[elements[0]] = 0
    
    # Iteramos sobre los elementos de la definición regular
    for element in elements:
        # Separamos la expresión del retorno
        parts = element.split('{')
        
        # Verificamos si se puede dividir en dos partes
        if len(parts) > 1:
            # Eliminamos espacios en blanco y caracteres no deseados
            expr = parts[0].strip(" '")
            ret = parts[1].strip(" }")
            
            # Agregamos al diccionario
            regular_dict[expr] = ret
        else:
            # Si no se puede dividir, asignamos una cadena vacía como retorno
            expr = parts[0].strip(" '")
            ret = ''
            regular_dict[expr] = ret
    
    return regular_dict


def regdef(dictionary):
    keys = list(dictionary.keys())

    # Unir las claves usando '|' como separador
    regex_pattern = '|'.join(keys)

    return regex_pattern

