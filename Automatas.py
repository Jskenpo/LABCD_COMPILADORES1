import graphviz
class estado:
    label = None
    transicion1 = None 
    transicion2 = None 
    id = None


def seguimiento(estado, visitados=None):
    if visitados is None:
        visitados = set()

    estados = set()
    estados.add(estado)

    if estado.label is None:
        if estado.transicion1 is not None and estado.transicion1 not in visitados:
            visitados.add(estado.transicion1)
            estados |= seguimiento(estado.transicion1, visitados)
        if estado.transicion2 is not None and estado.transicion2 not in visitados:
            visitados.add(estado.transicion2)
            estados |= seguimiento(estado.transicion2, visitados)

    return estados

class AFD:
    def __init__(self):
        self.estados = set()
        self.transitions = {}
        self.inicial = None
        self.accept = set()

    def agregar_transicion(self, estado_origen, simbolo, estado_destino):
        if estado_origen not in self.transitions:
            self.transitions[estado_origen] = {}
        self.transitions[estado_origen][simbolo] = estado_destino

    def agregar_estado(self, estado):
        # Convertir el conjunto a una tupla antes de agregarlo
        self.estados.add(tuple(sorted(estado)))

    def establecer_estado_inicial(self, estado):
        self.inicial = tuple(sorted(estado))

    def agregar_estado_aceptacion(self, estado):
        self.accept.add(tuple(sorted(estado)))

def recorrer_ast(nodo, valores_ast=None):
    if valores_ast is None:
        valores_ast = {}

    if nodo is None:
        return valores_ast

    if nodo.follows != set():
        valores_ast[nodo.id] = {
            'PrimeraPos': nodo.PrimeraPos,
            'UltimaPos': nodo.UltimaPos,
            'nulable': nodo.nulable,
            'follows': nodo.follows
        }

    recorrer_ast(nodo.izquierda, valores_ast)
    recorrer_ast(nodo.derecha, valores_ast)

    # Ordenar el diccionario por el id de manera ascendente
    valores_ast = dict(sorted(valores_ast.items(), key=lambda item: item[0]))


    return valores_ast

def direct_afd(root,alfabeto):

    
    while 'E' in alfabeto:
        alfabeto.remove('E')

    # Obtener s0
    s0 = root.NodosPP
    
    # Crear el AFD
    afd = AFD()
    afd.agregar_estado(root.PrimeraPos)
    afd.establecer_estado_inicial(root.PrimeraPos)
    labels = [root.PrimeraPos]
    # Dstates es una lista de conjuntos de nodos
    Dstates = [s0]
    marked_states = set()  # Conjunto de estados marcados

    # Mientras haya estados no marcados en Dstates
    while Dstates:
        # Obtener un estado no marcado
        T = Dstates.pop()
        L = labels.pop()
        
        # Marcar el estado
        marked_states.add(tuple(sorted(T)))

        for symbol in alfabeto:
            U = set()
            U_labels = set()

            # Calcular la unión de followpos(p) para todas las posiciones p en T
            for node in T:
                if node.valor == symbol:
                    U |= node.NodosF
                    U_labels |= node.follows

            # Si U no está vacío y no está en Dstates ni en marked_states, agregarlo como estado no marcado a Dstates
            if U and tuple(sorted(U)) not in Dstates and tuple(sorted(U)) not in marked_states:
                afd.agregar_estado(U_labels)
                Dstates.append(U)
                labels.append(U_labels)

            # Establecer la transición desde T con el símbolo 'symbol' a U
            if U:
                afd.agregar_transicion(tuple(sorted(L)), symbol, tuple(sorted(U_labels)))

            for nodo in U:
                if nodo.valor == '#':
                    afd.agregar_estado_aceptacion(U_labels)
           

    # Establecer los estados de aceptación
    return afd

def graficar_direct_afd(afd):
    dot = graphviz.Digraph(format = 'png')

    # Agregar nodos
    for estado in afd.estados:
        if estado in afd.accept:
            dot.node(str(estado), shape='doublecircle')
        elif estado == afd.inicial:
            dot.node(str(estado), shape='circle', style='bold')
        else:
            dot.node(str(estado), shape='circle')

    # Agregar transiciones
    for origen, transiciones in afd.transitions.items():
        for simbolo, destino in transiciones.items():
            dot.edge(str(origen), str(destino), label=str(simbolo))

    # Añadir flecha indicando cual es el estado inicial 
    dot.node('inicial', shape='none')
    dot.edge('inicial', str(afd.inicial), label='inicio')
    
    
    return dot

def imprimir_afd(afd):
    print("Estados:")
    for estado in afd.estados:
        print(estado)
    
    print("\nTransiciones:")

    for origen, transiciones in afd.transitions.items():
        for simbolo, destino in transiciones.items():
            print(f"{origen} --{simbolo}--> {destino}")

    print("\nEstado inicial:")
    print(afd.inicial)

    print("\nEstados de aceptación:")
    for estado in afd.accept:
        print(estado)


def simulacion_direct_afd(afd, w):
    actual = afd.inicial

    for char in w:
        if actual not in afd.transitions or char not in afd.transitions[actual]:
            return False
        actual = afd.transitions[actual][char]

    return actual in afd.accept

