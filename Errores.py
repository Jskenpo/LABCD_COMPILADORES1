
def verPalabrasReservadas (symbols, operandos):
    # Verificar si hay palabras reservadas
    operandos_yalex = ['let', 'rule', 'eof']
    operandos += operandos_yalex
    
    for key in symbols:
        if key in operandos:
            print('Error: El token', key, 'es una palabra reservada')
            return False
    return True


def ExistRules(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("rule"):
                return True
    return False


def sintaxisRegex(symbols):
    operands =['+', '-', '*', '?', '|', '(', ')', '[', ']', '{', '}', ' ', '\t', '\n', '\s']
    for key in symbols:
        if key in operands:
            print('Error: El token', key, 'contiene un operador')
            return False
    return True
