import re
from  prepare import *
from AST import *
from Automatas import *
from Lectura import *

operandos = [
    'multi',
    'div',
    'igual',
    'lparen',
    'rparen',
    'suma',
    'resta',
    'punto',
    'barra_vertical',
    'interrogacion',
    'corchete_abierto',
    'corchete_cerrado',
    'llave_abierta',
    'llave_cerrada'
]


# Llamar a las funciones para leer los datos

archivo = "slr-4.yal"

symbols = read_var(archivo)
read_regdef(archivo)

print(symbols)

regular_dict = convert_to_dictionary(regular_elements)

print(regular_dict)

definicion_regular = regdef(regular_dict)
print(definicion_regular)

# Expresión regular de ejemplo
regex_example = 'letter(letter|digit)*'



symbols_keys = list(symbols.keys())

print('expresiones regulares de los tokens')
print(symbols_keys)

new_regex = convert_regex_to_list(definicion_regular, symbols_keys, operandos)

print('expresion regular convertida a lista')
print(new_regex)


infix,alfabeto = convertir_expresion(new_regex)

print('La expresión regular en notación infix es:', infix)

explicit = implicit_to_explicit(new_regex,symbols_keys, operandos)

print('La expresión regular en notación explicit es:', explicit)

postfix = infix_postfix(explicit)

print('La expresión regular en notación postfix es:', postfix)


ast = construir_AST(postfix)
calcular_nulabilidad(ast)
nulables = obtener_nulables(ast)
obtener_primera_pos(ast)
obtener_ultima_pos(ast)
calcular_followpos(ast, ast)

dot = dibujar_AST(ast)
dot.render('ast', format='png', view=True)








