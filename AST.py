
# Clase para construir el árbol de sintaxis abstracta
from graphviz import Digraph 

class NodoAST:
    def __init__(self, valor, identificador ):
        self.id = identificador
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.nulable = False 
        self.PrimeraPos = set()
        self.UltimaPos = set()
        self.follows = set()
        self.NodosPP = set()
        self.NodosUP = set()
        self.NodosF = set()

    def __lt__(self,other):
        return self.id < other.id
        
identificador_global = 1

def construir_AST(exp_postfix, definitions):
    # Usar el contador global de identificadores
    global identificador_global

    stack = []
    for token in exp_postfix:
        if token in definitions:  # Verificar si el token es una definición previa
            # Expandir la definición
            nodo = construir_AST(definitions[token], definitions)
        elif token in ['.', '|', '*', '+', '?']:
            nodo = NodoAST(token, 'null')
        else:
            # Usar el identificador global y luego incrementarlo
            nodo = NodoAST(token, identificador_global)
            identificador_global += 1
        if token in ['.', '|', '*']:
            nodo.derecha = stack.pop()
            if token not in ['*']:
                nodo.izquierda = stack.pop()
        stack.append(nodo)

    if len(stack) != 1:
        raise ValueError("Expresión no válida")

    return stack[0]

def ast_final(ast):
    global identificador_global  # Asegurarse de usar el contador global de identificadores
      
    # Crear el nodo de concatenación
    nodo_concatenacion = NodoAST('.', 'null')
    nodo_concatenacion.izquierda = ast
    nodo_finalizacion = NodoAST('#', identificador_global)  # Crear el nodo de finalización
    # Incrementar el identificador global
    identificador_global += 1 

    # Asignar el nodo de finalización como hijo derecho del nodo de concatenación
    nodo_concatenacion.derecha = nodo_finalizacion

    return nodo_concatenacion


def dibujar_AST(nodo, dot=None):
    if dot is None:
        dot = Digraph()
    
    dot.node(str(id(nodo)), f"{nodo.valor}\nNulable:{nodo.nulable} \nID: {nodo.id}\nPP: {nodo.PrimeraPos}\nUP: {nodo.UltimaPos}\n FP: {nodo.follows}")
    if nodo.izquierda is not None:
        dot.node(str(id(nodo.izquierda)), nodo.izquierda.valor)
        dot.edge(str(id(nodo)), str(id(nodo.izquierda)))
        dibujar_AST(nodo.izquierda, dot)
    if nodo.derecha is not None:
        dot.node(str(id(nodo.derecha)), nodo.derecha.valor)
        dot.edge(str(id(nodo)), str(id(nodo.derecha)))
        dibujar_AST(nodo.derecha, dot)
    return dot

def calcular_nulabilidad(nodo):
    if nodo is None:
        return

    calcular_nulabilidad(nodo.izquierda)
    calcular_nulabilidad(nodo.derecha)

    if nodo.valor == 'E':
        nodo.nulable = True
    elif nodo.valor == '.':
        nodo.nulable = nodo.izquierda.nulable and nodo.derecha.nulable
    elif nodo.valor == '|':
        nodo.nulable = nodo.izquierda.nulable or nodo.derecha.nulable
    elif nodo.valor == '*':
        nodo.nulable = True

def obtener_nulables(nodo, nulables=None):
    if nulables is None:
        nulables = []

    if nodo is None:
        return

    obtener_nulables(nodo.izquierda, nulables)
    obtener_nulables(nodo.derecha, nulables)

    if nodo.nulable:
        nulables.append(nodo)

    return nulables

def obtener_nulables(nodo, nulables=None):
    if nulables is None:
        nulables = []

    if nodo is None:
        return

    obtener_nulables(nodo.izquierda, nulables)
    obtener_nulables(nodo.derecha, nulables)

    if nodo.nulable:
        nulables.append(nodo)

    return nulables

def obtener_primera_pos(nodo):
    if nodo is None:
        return set(),set()

    primera_pos = set()
    nodos_PP = set()

    if nodo.valor == '.':
        if nodo.izquierda is not None and nodo.derecha is not None:
            if nodo.izquierda.nulable:
                primera_pos |= nodo.izquierda.PrimeraPos | nodo.derecha.PrimeraPos
                nodos_PP |= nodo.izquierda.NodosPP | nodo.derecha.NodosPP
            else:
                primera_pos |= nodo.izquierda.PrimeraPos

                nodos_PP |= nodo.izquierda.NodosPP

    elif nodo.valor == '|':
        if nodo.izquierda is not None and nodo.derecha is not None:
            primera_pos |= nodo.izquierda.PrimeraPos | nodo.derecha.PrimeraPos
            nodos_PP |= nodo.izquierda.NodosPP | nodo.derecha.NodosPP

    elif nodo.valor == '*':
        if nodo.izquierda is not None:
            primera_pos |= nodo.izquierda.PrimeraPos
            nodos_PP |= nodo.izquierda.NodosPP

    # Regla para hoja con posición i
    elif nodo.id is not None:
        if nodo.valor != 'E':
            primera_pos.add(nodo.id)
            nodos_PP.add(nodo)

    primera_pos_izq, nodos_PP_izq = obtener_primera_pos(nodo.izquierda)
    if primera_pos_izq is not None and nodos_PP_izq is not None:
        primera_pos |= primera_pos_izq
        nodos_PP |= nodos_PP_izq

    primera_pos_der, nodos_PP_der= obtener_primera_pos(nodo.derecha)
    if primera_pos_der is not None and nodos_PP_der is not None:
        primera_pos |= primera_pos_der
        nodos_PP |= nodos_PP_der

    

    nodo.PrimeraPos = primera_pos
    nodo.NodosPP = nodos_PP

    #si el nodo es concatenacion y el nodo izquierdo no es nulable, eliminar la primera posicion del nodo derecho 
    if nodo.valor == '.':
        if not nodo.izquierda.nulable:
            nodo.PrimeraPos -= nodo.derecha.PrimeraPos
            nodo.NodosPP -= nodo.derecha.NodosPP

    return primera_pos, nodos_PP

def obtener_ultima_pos(nodo):
    if nodo is None:
        return set(),set()

    ultima_pos = set()
    nodos_UP = set()

    if nodo.valor == '.':
        if nodo.izquierda is not None and nodo.derecha is not None:
            if nodo.derecha.nulable:
                ultima_pos |= nodo.izquierda.UltimaPos | nodo.derecha.UltimaPos
                nodos_UP |= nodo.izquierda.NodosUP | nodo.derecha.NodosUP
            else:
                ultima_pos |= nodo.derecha.UltimaPos
                nodos_UP |= nodo.derecha.NodosUP

    elif nodo.valor == '|':
        if nodo.izquierda is not None and nodo.derecha is not None:
            ultima_pos |= nodo.izquierda.UltimaPos | nodo.derecha.UltimaPos
            nodos_UP |= nodo.izquierda.NodosUP | nodo.derecha.NodosUP

    elif nodo.valor == '*':
        if nodo.izquierda is not None:
            ultima_pos |= nodo.izquierda.UltimaPos
            nodos_UP |= nodo.izquierda.NodosUP

    # Regla para hoja con posición i
    elif nodo.id is not None:
        if nodo.valor != 'E':
            ultima_pos.add(nodo.id)
            nodos_UP.add(nodo)

    ultima_pos_new, nodos_UP_new = obtener_ultima_pos(nodo.izquierda)
    if ultima_pos_new is not None and nodos_UP_new is not None:
        ultima_pos |= ultima_pos_new
        nodos_UP |= nodos_UP_new

    ultima_pos_new, nodos_UP_new = obtener_ultima_pos(nodo.derecha)
    if ultima_pos_new is not None and nodos_UP_new is not None:
        ultima_pos |= ultima_pos_new
        nodos_UP |= nodos_UP_new

    nodo.UltimaPos = ultima_pos
    nodo.NodosUP = nodos_UP

    #si el nodo es concatenacion y el nodo derecho no es nulable, eliminar la ultima posicion del nodo izquierdo
    if nodo.valor == '.':
        if not nodo.derecha.nulable:
            nodo.UltimaPos -= nodo.izquierda.UltimaPos
            nodo.NodosUP -= nodo.izquierda.NodosUP

    return ultima_pos, nodos_UP

def calcular_followpos(nodo, ast ):

    if nodo is None:
        return

    if nodo.valor == '.':
        for i in nodo.izquierda.UltimaPos:
            nodo_izquierda = obtener_nodo_por_id(ast, i)
            nodo_izquierda.follows |= nodo.derecha.PrimeraPos
            nodo_izquierda.NodosF |= nodo.derecha.NodosPP

    elif nodo.valor == '*':
        for i in nodo.UltimaPos:
            pos_node = obtener_nodo_por_id(ast, i)
            pos_node.follows |= nodo.PrimeraPos
            pos_node.NodosF |= nodo.NodosPP

    calcular_followpos(nodo.izquierda, ast)
    calcular_followpos(nodo.derecha, ast)

def obtener_nodo_por_id(nodo, id):
    if nodo is None:
        return None

    if nodo.id == id:
        return nodo

    nodo_izquierda = obtener_nodo_por_id(nodo.izquierda, id)
    if nodo_izquierda is not None:
        return nodo_izquierda

    nodo_derecha = obtener_nodo_por_id(nodo.derecha, id)
    if nodo_derecha is not None:
        return nodo_derecha

def obtener_alfabeto(nodo):
    # Definir los operadores
    operadores = ['.', '|', '*', '+', '?']

    # Usar un conjunto para almacenar el alfabeto (para evitar duplicados)
    alfabeto = set()

    # Definir una función recursiva para recorrer el árbol
    def recorrer(nodo):
        if nodo is None:
            return
        if nodo.valor not in operadores:
            alfabeto.add(nodo.valor)
        recorrer(nodo.izquierda)
        recorrer(nodo.derecha)

    # Iniciar el recorrido del árbol
    recorrer(nodo)

    # Devolver el alfabeto como una lista
    return list(alfabeto)

