import re
from  prepare import *
from AST import *
from Automatas import *

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


def convert_to_dictionary(elements):
    # Creamos un diccionario vacío
    regular_dict = {}
    
    # Asignamos 'ws' con un valor de 0
    regular_dict['ws'] = 0
    
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


# Llamar a las funciones para leer los datos

archivo = "slr-1.yal"

symbols = read_var(archivo)
read_regdef(archivo)

print(symbols)

regular_dict = convert_to_dictionary(regular_elements)

definicion_regular = regdef(regular_dict)

# Expresión regular de ejemplo
regex_example = 'letter(letter|digit)*'

symbols_keys = list(symbols.keys())

print('expresiones regulares de los tokens')
print(symbols_keys)

# Aplicar concatenación explícita
new_regex_example = implicit_to_explicit(regex_example, symbols_keys)

print(new_regex_example)

# Convertir la expresión regular a postfijo
postfix= infix_postfix(new_regex_example)

print(postfix)

ast = construir_AST(postfix,symbols_keys)
calcular_nulabilidad(ast)
nulables = obtener_nulables(ast)
obtener_primera_pos(ast)
obtener_ultima_pos(ast)
calcular_followpos(ast)

dot = dibujar_AST(ast)
dot.render('ast', format='png', view=True)





