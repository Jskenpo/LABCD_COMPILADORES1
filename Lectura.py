import re 

symbols = {}
regular_elements = []

def read_var(filename):
    with open(filename) as f:
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


def manejar_errores_yalex(archivo_yalex, operandos):
    # Lista de palabras reservadas o operandos en YALex
    operandos_yalex = ['let', 'rule', 'eof']

    operandos_yalex += operandos

    # Secciones necesarias en el archivo YALex
    secciones_necesarias = ['rule']

    try:
        # Abre el archivo YALex para lectura
        with open(archivo_yalex, 'r') as f:
            contenido = f.read()
            # Realiza algunas verificaciones en el contenido del archivo YALex
            lineas = contenido.split('\n')
            secciones_presentes = set()
            for linea in lineas:
                # Verifica si las secciones necesarias están presentes
                for seccion in secciones_necesarias:
                    if seccion in linea:
                        secciones_presentes.add(seccion)

                # Verifica si la línea comienza con "let" seguido de un identificador
                if linea.strip().startswith('let'):
                    partes = linea.split()
                    if len(partes) >= 3:
                        nombre_expresion = partes[1]
                        if nombre_expresion in operandos_yalex:
                            return False, f"El nombre de la expresión regular '{nombre_expresion}' coincide con una palabra reservada de YALex."

            # Verifica si todas las secciones necesarias están presentes
            secciones_faltantes = set(secciones_necesarias) - secciones_presentes
            if secciones_faltantes:
                return False, f"Faltan las siguientes secciones necesarias en el archivo YALex: {', '.join(secciones_faltantes)}"
                
            # Si todas las verificaciones pasan, devuelve True
            return True, "El archivo YALex parece estar bien formateado y no tiene errores."
    except FileNotFoundError:
        return False, "El archivo YALex especificado no se encontró."
    except Exception as e:
        return False, f"Se produjo un error al procesar el archivo YALex: {str(e)}"
