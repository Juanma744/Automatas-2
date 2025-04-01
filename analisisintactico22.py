from lark import Lark, Transformer
import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import ttk, messagebox, simpledialog
from graphviz import Digraph 

# Definir la gramática en Lark
grammar = """
    start: "INICIO" inst "FIN"
    inst: (ins ";" | block) inst_prime  // Permite instrucciones con ";" o bloques sin ";"
    inst_prime: | (ins ";" | block) inst_prime  // ε se representa omitiendo la regla
    ins: dec | asig | out | inp | if_stmt | whl
    
    // Permitir declaraciones con o sin asignación
    dec: tipo alias ("=" exp)?  // Agrega ("=" exp)? para permitir asignaciones opcionales
    tipo: "int" | "float" | "str"
    
    asig: alias "=" exp
    exp: term exp_prime
    exp_prime: | op term exp_prime  // ε se representa omitiendo la regla
    term: alias | "(" exp ")" | STRING | NUMBER  // Agrega STRING y NUMBER como términos
    op: "+" | "-" | "*" | "/"
    
    if_stmt: "if" "(" comp ")" block else_stmt
    else_stmt: | "else" block  // ε se representa omitiendo la regla
    whl: "while" "(" comp ")" block  // Agrega la regla para el bloque while
    out: "out" "(" (alias | STRING) ")"  // Modificado para aceptar alias o STRING
    inp: "in" "(" alias ")"
    
    comp: term comp_prime
    comp_prime: | scomp term comp_prime  // ε se representa omitiendo la regla
    scomp: ">" | "<" | "?" | "!"
    
    block: "{" inst "}"  // Define un bloque como { inst }
    
    alias: /[a-zA-Z_][a-zA-Z0-9_]*/
    STRING: /"[^"]*"/  // Agrega una regla para cadenas de texto
    NUMBER: /-?\d+(\.\d+)?/  // Agrega una regla para números

    %import common.WS
    %ignore WS
"""

# Parser con Lark
parser = Lark(grammar, start="start", parser="lalr")

# Transformer para construir el AST
class ASTTransformer(Transformer):
    def __default__(self, data, children, meta):
        return {"type": data, "children": children}

# Función para analizar sintácticamente una entrada
def parse_code(code):
    try:
        tree = parser.parse(code)
        transformer = ASTTransformer()
        ast = transformer.transform(tree)
        return ast
    except Exception as e:
        return f"Error: {str(e)}"


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


# Función para generar una imagen del AST
def generate_ast_image(ast, filename="ast"):
    dot = Digraph(comment='AST')
    
    def add_nodes_edges(tree, parent=None):
        if isinstance(tree, dict):
            node_label = tree.get("type", "node")
            node_id = str(id(tree))
            dot.node(node_id, label=node_label)
            if parent:
                dot.edge(parent, node_id)
            for child in tree.get("children", []):
                add_nodes_edges(child, node_id)
        elif isinstance(tree, list):
            for child in tree:
                add_nodes_edges(child, parent)
        else:
            node_id = str(id(tree))
            dot.node(node_id, label=str(tree))
            if parent:
                dot.edge(parent, node_id)
    
    add_nodes_edges(ast)
    dot.render(filename, format='png', cleanup=True)
    return f"Imagen del AST generada como {filename}.png"

# Función para cargar un archivo .txt
def cargar_archivo():
    archivo_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo_path:
        with open(archivo_path, 'r') as archivo:
            contenido = archivo.read()
            text_input.delete(1.0, tk.END)
            text_input.insert(tk.END, contenido)

# Función para analizar el código y mostrar el resultado
def analyze_code():
    code = text_input.get("1.0", tk.END).strip()
    result = parse_code(code)
    if isinstance(result, dict):  # Si el resultado es un AST
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, print_ast_with_stack(result))
        text_output.config(state=tk.DISABLED)
        global ast  # Guardar el AST para generar la imagen
        ast = result
    else:
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)
        text_output.config(state=tk.DISABLED)

# Función para generar la imagen del AST
def generate_ast_image_gui():
    if 'ast' in globals():
        result = generate_ast_image(ast)
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)
        text_output.config(state=tk.DISABLED)
    else:
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "No hay un AST generado para crear la imagen.")
        text_output.config(state=tk.DISABLED)

# Función para guardar el árbol como archivo .txt
def save_ast_to_txt():
    if 'ast' not in globals():
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "Primero debes generar el AST.")
        text_output.config(state=tk.DISABLED)
        return

    respuesta = messagebox.askyesno("Guardar AST", "¿Deseas guardar el árbol como archivo .txt?")
    if respuesta:
        archivo_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Archivo de texto", "*.txt")],
                                                     title="Guardar como")
        if archivo_path:
            contenido = print_ast_with_stack(ast)
            with open(archivo_path, 'w') as archivo:
                archivo.write(contenido)
            text_output.config(state=tk.NORMAL)
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, f"Archivo guardado en: {archivo_path}")
            text_output.config(state=tk.DISABLED)

# Recorrer el AST con generador recursivo
def recorrer_ast(ast):
    if isinstance(ast, dict):
        yield ast
        for child in ast.get("children", []):
            yield from recorrer_ast(child)

# Buscar nodos por tipo
def buscar_nodos_por_tipo(ast, tipo_buscado):
    encontrados = []
    stack = [ast]
    while stack:
        nodo = stack.pop()
        if isinstance(nodo, dict):
            if nodo.get("type") == tipo_buscado:
                encontrados.append(nodo)
            stack.extend(nodo.get("children", []))
    return encontrados

# Etiquetar nodos con IDs únicos para referencia directa
def etiquetar_nodos_con_id(ast, prefix="nodo"):
    contador = [0]
    def asignar_id(nodo):
        if isinstance(nodo, dict):
            nodo["id"] = f"{prefix}_{contador[0]}"
            contador[0] += 1
            for child in nodo.get("children", []):
                asignar_id(child)
    asignar_id(ast)

# Construir un índice
def construir_indice(ast):
    indice = {}
    for nodo in recorrer_ast(ast):
        if "id" in nodo:
            indice[nodo["id"]] = nodo
    return indice

# Indexar por ruta jerárquica
def indexar_por_ruta(ast):
    stack = [("1", ast)]
    indice = {}
    while stack:
        ruta, nodo = stack.pop()
        if isinstance(nodo, dict):
            indice[ruta] = nodo
            for i, child in enumerate(nodo.get("children", [])):
                child_ruta = f"{ruta}.{i+1}"
                stack.append((child_ruta, child))
    return indice



# Función para buscar y mostrar un nodo por ruta jerárquica
def mostrar_nodo_por_ruta():
    if 'ast' not in globals():
        messagebox.showerror("Error", "Primero analiza el código.")
        return
    ruta = simpledialog.askstring("Buscar por Ruta", "Ingresa la ruta (ej. 1.2.1):")
    if ruta:
        rutas = indexar_por_ruta(ast)
        nodo = rutas.get(ruta)
        if nodo:
            text_output.config(state=tk.NORMAL)
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, f"Nodo en ruta {ruta}:\n{nodo}")
            text_output.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No encontrado", f"No se encontró un nodo en la ruta {ruta}.")

# Función para buscar y mostrar nodos por tipo
def mostrar_nodos_por_tipo():
    if 'ast' not in globals():
        messagebox.showerror("Error", "Primero analiza el código.")
        return
    tipo = simpledialog.askstring("Buscar por Tipo", "Ingresa el tipo de nodo (ej. asig, dec, out):")
    if tipo:
        encontrados = buscar_nodos_por_tipo(ast, tipo)
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        if encontrados:
            for nodo in encontrados:
                text_output.insert(tk.END, f"{nodo}\n\n")
        else:
            text_output.insert(tk.END, f"No se encontraron nodos de tipo '{tipo}'.")
        text_output.config(state=tk.DISABLED)


# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Analizador Sintáctico con AST")
root.geometry("800x600")  # Hacer la interfaz más grande

label = tk.Label(root, text="Ingrese el código para analizar:")
label.pack(pady=10)

text_input = scrolledtext.ScrolledText(root, width=80, height=20)
text_input.pack(padx=10, pady=10)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

# Botón para cargar archivo
boton_cargar = ttk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo)
boton_cargar.grid(row=0, column=0, padx=5)

# Botón de análisis
analyze_button = ttk.Button(frame_botones, text="Analizar", command=analyze_code)
analyze_button.grid(row=0, column=1, padx=5)

# Botón para generar la imagen del AST
generate_image_button = ttk.Button(frame_botones, text="Generar Imagen del AST", command=generate_ast_image_gui)
generate_image_button.grid(row=0, column=2, padx=5)

save_button = ttk.Button(frame_botones, text="Guardar AST como .txt", command=save_ast_to_txt)
save_button.grid(row=0, column=3, padx=5)

# Botón para mostrar nodo por ruta jerárquica
ruta_button = ttk.Button(frame_botones, text="Buscar por Ruta", command=mostrar_nodo_por_ruta)
ruta_button.grid(row=1, column=0, padx=5, pady=5)

# Botón para buscar nodos por tipo
tipo_button = ttk.Button(frame_botones, text="Buscar por Tipo", command=mostrar_nodos_por_tipo)
tipo_button.grid(row=1, column=1, padx=5, pady=5)



text_output = scrolledtext.ScrolledText(root, width=80, height=10, state=tk.DISABLED)
text_output.pack(padx=10, pady=10)

root.mainloop()