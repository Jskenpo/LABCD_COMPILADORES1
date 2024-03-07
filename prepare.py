
def convert_regex_to_list(regex, symbols_keys):
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
            regex_list.append(regex[i])
            i += 1
    return regex_list

def convertFirst(expresion):
    return expresion.replace('?', '|E')

def convertir_expresion(lista):
    
    alfabeto = []
    operandos = ['+','.','*','|','(',')','[',']','{','}','?']

    for i in lista:
        if i not in operandos:
            if i not in alfabeto:
                alfabeto.append(i)

    alfabeto.append('')
    
        
    for i in range(len(lista)):
        if i > 0:
            before = lista[i - 1]
            if lista[i] == '+':
                if before not in ')]}':
                    lista[i - 1] = lista[i - 1] +lista[i - 1] + '*'
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
                    lista[i] = ''.join(almacen) + '*'
    
    while '+' in lista:
        lista.remove('+')

    #vueva epxpresion 
    expr = ''.join(lista)

    return expr, alfabeto

import re

def implicit_to_explicit(regex: list, symbol_keys: list) -> str:
    # Convertir la lista de expresión regular a una cadena
    regex_str = ''.join(regex)

    # Generar patrón de búsqueda para encontrar tokens completos
    pattern = r'\b(?:' + '|'.join(map(re.escape, symbol_keys)) + r')\b'

    # Reemplazar tokens por caracteres especiales
    replaced_regex = re.sub(pattern, lambda match: str(symbol_keys.index(match.group(0))), regex_str)

    # Aplicar concatenación explícita
    new_regex = ''
    for i in range(len(replaced_regex) - 1):
        if replaced_regex[i] not in ['(', '|', '.','{','['] and replaced_regex[i + 1] not in [')', '|', '*', '.',']','}']:
            new_regex += replaced_regex[i] + '.'  # Agregar concatenación explícita
        else:
            new_regex += replaced_regex[i]  # Agregar el caracter normal
    new_regex += replaced_regex[-1]  # Agregar el último caracter

    # Restaurar estado original de los tokens
    for i, token in enumerate(symbol_keys):
        new_regex = new_regex.replace(str(i), token)

    new_regex = convert_regex_to_list(new_regex, symbol_keys)

    return new_regex


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