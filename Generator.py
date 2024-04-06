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
def leer_tokens( afd_directo, afd_dict, regular_dict):
    archivo = input('Ingrese el nombre del archivo de entrada: ')
    with open(archivo) as f:
        contador = 1
        for line in f:
            print(f"\nCadena {contador}: {line.strip()}")
            listCadena = convert_input_toList(line)

            result, token = simular_afd_directo(afd_directo, afd_dict, listCadena)

            ejecutar_accion_token(regular_dict, token)
            contador += 1



