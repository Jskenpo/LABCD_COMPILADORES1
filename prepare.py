
import re 

def convert_regex_to_list(regex, symbols_keys, operandos):
    regex_list = []
    i = 0
    while i < len(regex):
        found_key = False
        for key in symbols_keys:
            if regex.startswith(key, i):
                regex_list.append(key)
                i += len(key)
                found_key = True
                break
        if not found_key:
            for op in operandos:
                if regex.startswith(op, i):
                    regex_list.append(op)
                    i += len(op)
                    found_key = True
                    break
        if not found_key:
            regex_list.append(regex[i])
            i += 1
    return regex_list

def convertFirst(expr):
    # si hay un '?' en la lista lo reemplaza a '|E'
    while '?' in expr:
        expr = expr.replace('?', '|E')
    return  expr

def convertir_expresion(lista,keys_values,operadores):
    
    alfabeto = []
    operandos = ['+','.','*','|','(',')','[',']','{','}','?']
    nueva_lista = []

    for i in lista:
        if i not in operandos:
            if i not in alfabeto:
                alfabeto.append(i)

    alfabeto.append('')
    
    i = 0
    while i < len(lista):
        if i > 0:
            before = lista[i - 1]
            if lista[i] == '+':
                if before not in ')]}':
                    nuevo_valor = lista[i - 1] +lista[i - 1] + '*'
                    nuevo_valor = convert_regex_to_list(nuevo_valor, keys_values, operadores)
                    nueva_lista = nueva_lista[:i - 1] + nuevo_valor
                    i += len(nuevo_valor) - 2
                else:
                    almacen = []
                    aperturas = 0
                    for j in range(i - 1, -1, -1):
                        if lista[j] in ')]}':
                            aperturas += 1
                            almacen.append(lista[j])
                        elif lista[j] in '([{':
                            aperturas -= 1
                            almacen.append(lista[j])
                        else:
                            almacen.append(lista[j])
                        if aperturas == 0:
                            break
                    almacen.reverse()
                    predecesor = ''.join(almacen)
                    nuevo_valor = ''.join(almacen) + '*'
                    nuevo_valor = convert_regex_to_list(nuevo_valor, keys_values, operadores)
                    predecesor = convert_regex_to_list(predecesor, keys_values, operadores)
                    nueva_lista = nueva_lista[:j] + predecesor + nuevo_valor
                    i += len(nuevo_valor) + len(predecesor) - 2
            else:
                nueva_lista.append(lista[i])
        else:
            nueva_lista.append(lista[i])
        i += 1

    while '+' in nueva_lista:
        nueva_lista.remove('+')

    return nueva_lista, alfabeto

def implicit_to_explicit(regex: list, symbol_keys: list, operandos: list) -> list:
    # Convertir la lista de expresión regular a una cadena
    regex_str = ''.join(regex)

    # Une lista de símbolos y operandos
    symbol_keys += operandos

    
    # Aplicar concatenación explícita
    new_regex_list = []
    for i in range(len(regex) - 1):
        if regex[i] not in ['(', '|', '.', '{', '['] and regex[i + 1] not in [')', '|', '*', '.', ']', '}']:
            new_regex_list.append(regex[i])
            new_regex_list.append('.')
        else:
            new_regex_list.append(regex[i])

    new_regex_list.append(regex[-1])  # Agregar el último caracter


    return new_regex_list

def infix_postfix(infix):
    caracteres_especiales = {'*': 60, '.': 40, '|': 20}
    exp_postfix, stack = [], []  

    for c in infix:        
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack[-1] != '(':
                exp_postfix.append(stack.pop())
            stack.pop()
        elif c in caracteres_especiales:
            while stack and caracteres_especiales.get(c, 0) <= caracteres_especiales.get(stack[-1], 0):
                exp_postfix.append(stack.pop())
            stack.append(c)
        else:
            exp_postfix.append(c)

    while stack:
        exp_postfix.append(stack.pop())

    return exp_postfix

def verify_regex(expresion):
    pila = []
    parentesis_abiertos = {'(', '[', '{'}
    parentesis_cerrados = {')', ']', '}'}
    parentesis_complementarios = {'(': ')', '[': ']', '{': '}'}

    for char in expresion:
        if char in parentesis_abiertos:
            pila.append(char)
        elif char in parentesis_cerrados:
            if not pila:
                return False
            ultimo_abierto = pila.pop()
            if parentesis_complementarios[ultimo_abierto] != char:
                return False

    return len(pila) == 0

def expandir_rango(rango):
    inicio, fin = rango
    return '|'.join([f'({chr(i)})' for i in range(ord(inicio), ord(fin) + 1)])

def expandir_extensiones(expresion, operandos):
    expresion = reemplazar_caracteres(expresion)

    patron_extension = '[^\]]+'
    inicio = expresion.find('[')
    while inicio != -1:
        fin = expresion.find(']', inicio)
        coincidencia = expresion[inicio+1:fin]
        rangos = coincidencia.split(' ')
        expresion_rangos = []
        for rango in rangos:
            if rango in operandos:  # Si es un operando, tratarlo como un solo carácter
                expresion_rangos.append(rango)
            elif '-' in rango:
                inicio_rango, fin_rango = rango.split('-')
                if len(inicio_rango) == 1 and len(fin_rango) == 1:
                    expresion_rangos.append(expandir_rango((inicio_rango, fin_rango)))
                elif len(inicio_rango) == 3 and inicio_rango[0] == "'" and inicio_rango[2] == "'" and len(fin_rango) == 3 and fin_rango[0] == "'" and fin_rango[2] == "'":
                    expresion_rangos.append(expandir_rango((inicio_rango[1], fin_rango[1])))
            elif rango[0] == "'" and rango[-1] == "'":
                palabra = rango[1:-1]
                expresion_rangos.append(f'({"|".join(palabra)})') 
            else:
                expresion_rangos.append(rango)
        
        expresion = expresion.replace(f'[{coincidencia}]', f'({"|".join(expresion_rangos)})')
        inicio = expresion.find('[', fin)
    
    return expresion


def preprocess_regex_dict(regex_dict, symbols_keys, operandos):
    keys = list(regex_dict.keys())
    for key in keys:
        valor_actual = regex_dict[key]
        nuevo_valor = convertFirst(valor_actual)
        nuevo_valor = expandir_extensiones(nuevo_valor, operandos)
        nuevo_valor = convert_regex_to_list(nuevo_valor, symbols_keys, operandos)
        infix, alfabeto = convertir_expresion(nuevo_valor, symbols_keys, operandos)
        explicit = implicit_to_explicit(infix, symbols_keys, operandos)
        postfix = infix_postfix(explicit)
        regex_dict[key] = postfix
    return regex_dict

def reemplazar_caracteres(expresion):
    expresion = expresion.replace("'\\t'", "'\t'").replace("'\\n'", "'\n'").replace("'\\s'", "'\s'")
    caracteres_reemplazar = {'\t': 'Tab', '\n': 'Enter', '\s': 'Espacio'}

    if expresion.find("['+' '-']") != -1:
        expresion = expresion.replace("['+' '-']", "[suma resta]")
    elif expresion.find("['-' '+']") != -1:
        expresion = expresion.replace("['-' '+']", "[resta' suma]")
    elif expresion.find("['+']") != -1:
        expresion = expresion.replace("['+']", "[suma]")
    elif expresion.find("['-']") != -1:
        expresion = expresion.replace("['-']", "[resta]")
    elif expresion.find("(_)") != -1:
        expresion = expresion.replace('(_)', '苦')

    for caracter, special in caracteres_reemplazar.items():
        expresion = expresion.replace(caracter, special)
        #eliminar las comillas 
        expresion = expresion.replace("'", "")

        
    return expresion

def revertir_caracteres(expresion):
    caracteres_revertir = {'Tab': 't', 'Enter': 'n', 'Espacio': 's', 'suma': '+', 'resta': '-', '苦': '_'}
    for special, caracter in caracteres_revertir.items():
        expresion = expresion.replace(special, caracter)
    return expresion