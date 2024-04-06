from Lectura import convert_input_toList
from Automatas import simular_afd_directo

def ejecutar_accion_token(token_actions, token):
    action = token_actions.get(token)
    if action is not None:
        if action.startswith("return "):
            value = action.split("return ")[1]
            print(f"El token '{token}' tiene el valor: {value}")
        else:
            print(f"Ejecutando la acción asociada al token '{token}':")
            exec(action)
    else:
        print(f"No se encontró ninguna acción para el token '{token}'.")


# Funcion que lea archivo txt linea por linea
def reconocedor_de_tokens( afd_directo, afd_dict, tokens_dict, token_actions):
    for value in tokens_dict.values():
        aceptado, token = simular_afd_directo(afd_directo, afd_dict, value)
        valor = ''.join(value)
        if aceptado:
            print(f"La cadena '{valor}' fue aceptada por el autómata '{token}'.")
            ejecutar_accion_token(token_actions, token)
        else:
            print(f"La cadena '{valor}' no fue aceptada por ningún autómata.")
    
            


def leer_tokens(operandos):
    archivo = input('Ingrese el nombre del archivo de entrada: ')

    #hacer diccionario con todos tokens en el archivo
    tokens_dict = {}

    with open(archivo) as f:
        contador = 1
        for line in f:
            print(f"\nCadena {contador}: {line.strip()}")
            listCadena = convert_input_toList(line)

            #asignar a cada token su valor
            contador2 = 1
            for i in listCadena:
                tokens_dict[f'token {contador2} de la linea {contador}'] = i
                contador2 += 1
    
            contador += 1
    
    updated_dict = convertTokens_toList(tokens_dict, operandos)
    
    return updated_dict
                

def convertTokens_toList(tokens_dict, operandos):
    updated_dict = {}

    #si el valor de un token pertenece a operandos se agrega a la lista de tokens de lo contrario se le hace split caracter por caracter y se agrega al diccionario 
    for key, value in tokens_dict.items():
        if value in operandos:
            updated_dict[key] = [value]
        else:
            updated_dict[key] = list(value) 

    return updated_dict


    

