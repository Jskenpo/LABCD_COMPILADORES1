import re
from  prepare import *
from AST import *
from Automatas import *
from Lectura import *
from Errores import *

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
    'llave_cerrada',
    'Tab',
    'Espacio',
    'Enter'
]


# Llamar a las funciones para leer los datos

archivo = "slr-1.yal"

symbols = read_var(archivo)

errores = verificarErrores(symbols, operandos, archivo)

if not errores:
    exit()


read_regdef(archivo)

print(symbols)

print('elementos regulares')
print(regular_elements)
print ('elementos regulares')

regular_dict = convert_to_dictionary(regular_elements)

print(regular_dict)

definicion_regular = regdef(regular_dict)
print(definicion_regular)

symbols_keys = list(symbols.keys())

print('expresiones regulares de los tokens')
print(symbols_keys)

new_regex = convertFirst(definicion_regular)
new_regex = convert_regex_to_list(new_regex, symbols_keys, operandos)

print('expresion regular convertida a lista')
print(new_regex)



infix,alfabeto = convertir_expresion(new_regex,symbols_keys,operandos)

print('La expresión regular en notación infix es:', infix)

explicit = implicit_to_explicit(infix,symbols_keys, operandos)

print('La expresión regular en notación explicit es:', explicit)

postfix = infix_postfix(explicit)

print('La expresión regular en notación postfix es:', postfix)

##preprocesar simbolos 

processed_symbols=preprocess_regex_dict(symbols, symbols_keys, operandos)

print('Simbolos procesados')
print(processed_symbols)

ast = construir_AST(postfix, processed_symbols)
ast = ast_final(ast)
calcular_nulabilidad(ast)
obtener_primera_pos(ast)
obtener_ultima_pos(ast)
calcular_followpos(ast,ast)


dot = dibujar_AST(ast)
dot.render('ast', format='png', view=True)

#obtener alfabeto de ast 
alfabeto = obtener_alfabeto(ast)

print('alfabeto')
print(alfabeto)


#convertir a afd directo 

afd_directo = direct_afd(ast,alfabeto)

print('afd directo')
imprimir_afd(afd_directo)

#graficar afd directo
dot = graficar_direct_afd(afd_directo)
dot.render('afd_directo', format='png', view=True)



