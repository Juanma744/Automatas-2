# analisis_lark.py
from lark import Lark, Transformer
from graphviz import Digraph
from tkinter import filedialog  # Para filedialog

# Definir la gramática en Lark (fuera de la función)
GRAMMAR = """
    start: S
    S: "Start" A "End"
    A: B*
    B: C | D | F | G | H | I
    C: J K? ";"
    J: "Entero" | "Doble" | "Cadena"
    K: var ("," var)*
    D: var "=" L ";"
    L: M L'
    L': op M |
    M: var | "(" L ")" | num | STRING
    op: "+" | "-" | "*" | "/"
    H: "Si" "(" N ")" "{" A "}" Q
    Q: "SiNo" "{" A "}" |
    I: "Mientras" "(" N ")" "{" A "}"
    F: "Salida" "(" (var | STRING) ")" ";"
    G: "Entrada" "(" var ")" ";"
    N: M N'
    N': R M | 
    R: ">" | "<" "=" | "!"
    var: /[a-zA-Z_]\w*/
    num: /-?\d+(\.\d+)?/
    STRING: /"[^"]*"/  // Agrega una regla para cadenas de texto

    %import common.WS
    %ignore WS
"""

def analizar_con_lark(codigo):
    # Parser con Lark
    parser = Lark(GRAMMAR, start="start", parser="lalr")

    # Transformer para construir el AST
    class ASTTransformer(Transformer):
        def __default__(self, data, children, meta):
            return {"type": data, "children": children}

    # Función para imprimir AST usando pila
    def print_ast_with_stack(ast):
        stack = [("1", ast)]
        lines = []
        while stack:
            pos, node = stack.pop()
            if isinstance(node, dict):
                lines.append(f"{pos} -> {node['type']}")
                children = node.get("children", [])
                for i in reversed(range(len(children))):
                    child_pos = f"{pos}.{i + 1}"
                    stack.append((child_pos, children[i]))
            else:
                lines.append(f"{pos} -> {str(node)}")
        return "\n".join(lines)

    # Función para parsear el código
    def parse_code(codigo_entrada):
        try:
            tree = parser.parse(codigo_entrada)
            transformer = ASTTransformer()
            ast = transformer.transform(tree)
            return ast, print_ast_with_stack(ast)  # Devuelve el AST y su representación en texto
        except Exception as e:
            return None, f"Error: {str(e)}"

    # Analizar el código y obtener resultados
    ast, resultado = parse_code(codigo)

    if ast:
        #imagen = generate_ast_image(ast) <---SE ELIMINA
        return ast, resultado #Regresamos solo el ast y el resultado
    else:
        return None, resultado #Regresamos ast vacio

# Función para generar una imagen del AST, es diferente ahora
def generate_ast_image(ast, filename="ast"):
        if not ast:
            return "No se pudo generar el AST."
        dot = Digraph(comment='AST', format='png')

        def add_nodes_edges(tree, parent=None):
            if isinstance(tree, dict):
                node_label = tree.get("type", "node")
                node_id = str(id(tree))
                dot.node(node_id, label=node_label)
                if parent:
                    dot.edge(parent, node_id)
                for child in tree.get("children", []):
                    add_nodes_edges(child, node_id)
            else:
                node_id = str(id(tree))
                dot.node(node_id, label=str(tree))  # Imprimir el valor del terminal
                if parent:
                    dot.edge(parent, node_id)

        add_nodes_edges(ast)
        dot.render(filename, cleanup=True)
        return f"Imagen del AST generada como {filename}.png"