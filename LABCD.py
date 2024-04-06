import re
from  prepare import *
from AST import *
from Automatas import *
from Lectura import *
from Errores import *
from Generator import *

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


# ---------------------LECTURA DE DATOS ----------------------------

archivo = "slr-4.yal"

symbols = read_var(archivo)

errores = verificarErrores(symbols, operandos, archivo)

if not errores:
    exit()

read_regdef(archivo)

regular_dict = convert_to_dictionary(regular_elements)

definicion_regular = regdef(regular_dict)

tokens = regdefKeys(regular_dict)

symbols_keys = list(symbols.keys())

#---------------------PREPROCESAMIENTO DE DATOS ----------------------------

new_regex = convertFirst(definicion_regular)
new_regex = convert_regex_to_list(new_regex, symbols_keys, operandos)

infix,alfabeto = convertir_expresion(new_regex,symbols_keys,operandos)

explicit = implicit_to_explicit(infix,symbols_keys, operandos)

postfix = infix_postfix(explicit)

processed_symbols=preprocess_regex_dict(symbols, symbols_keys, operandos)

dict_regdef = get_regex_byregdef(tokens, processed_symbols)



#---------------------CONSTRUCCION DE AST ----------------------------
ast = construir_AST(postfix, processed_symbols)
ast = ast_final(ast)
calcular_nulabilidad(ast)
obtener_primera_pos(ast)
obtener_ultima_pos(ast)
calcular_followpos(ast,ast)


#dot = dibujar_AST(ast)
#dot.render('ast', format='png', view=True)

#obtener alfabeto de ast 
alfabeto = obtener_alfabeto(ast)

#---------------------CONSTRUCCION DE AFD ----------------------------


afd_directo = direct_afd(ast,alfabeto)


#graficar afd directo
#dot = graficar_direct_afd(afd_directo)
#dot.render('afd_directo', format='png', view=True)

#imprimir afd directo
#imprimir_afd(afd_directo)

#---------------------CONSTRUCCION DE AFD POR TOKENS ----------------------------

ast_dict = get_ast_by_regdefDict(dict_regdef, processed_symbols)



afd_dict = get_afd_byASTDict(ast_dict)

tokens_dict=leer_tokens(operandos)

#---------------------RECONOCIMIENTO DE TOKENS ----------------------------

reconocedor_de_tokens(afd_directo, afd_dict, tokens_dict, regular_dict)

#graph_DFA_by_DFADict(afd_dict)