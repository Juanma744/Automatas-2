import tkinter as tk
from tkinter import scrolledtext
import re

# --- 1. Definición de Tokens (Aliases) y Lexer ---

# Mapeo de palabras reservadas y símbolos a sus alias (tipos de token)
TOKEN_MAP = {
    r'programa': 'PROGRAMA',
    r'finprograma': 'FINPROGRAMA',
    r'entero': 'ENTERO_TIPO',
    r'booleano': 'BOOL_TIPO',
    r'si': 'SI',
    r'entonces': 'ENTONCES',
    r'sino': 'SINO',
    r'finsi': 'FINSI',
    r'mientras': 'MIENTRAS',
    r'hacer': 'HACER',
    r'finmientras': 'FINMIENTRAS',
    r'leer': 'LEER',
    r'escribir': 'ESCRIBIR',
    r'verdadero': 'LITERAL_BOOL',
    r'falso': 'LITERAL_BOOL',
    r'=': 'ASIGNACION',
    r'\+': 'OP_ARITMETICO',
    r'-': 'OP_ARITMETICO',
    r'\*': 'OP_ARITMETICO',
    r'/': 'OP_ARITMETICO',
    r'<=': 'OP_COMPARACION',
    r'>=': 'OP_COMPARACION',
    r'==': 'OP_COMPARACION',
    r'!=': 'OP_COMPARACION',
    r'<': 'OP_COMPARACION',
    r'>': 'OP_COMPARACION',
    r'y': 'OP_LOGICO',
    r'o': 'OP_LOGICO',
    r'no': 'OP_LOGICO',
    r'\(': 'PARENTESIS_IZQ',
    r'\)': 'PARENTESIS_DER',
    r';': 'PUNTO_Y_COMA',
    # --- Patrones que deben ir después de palabras reservadas ---
    r'[a-zA-Z_][a-zA-Z0-9_]*': 'IDENTIFICADOR', # Nombres de variables
    r'[0-9]+': 'LITERAL_ENTERO',      # Números enteros
    # --- Otros ---
    r'\s+': 'ESPACIO',             # Espacios en blanco (ignorar usualmente)
    r'#.*': 'COMENTARIO',          # Comentarios (ignorar)
}

# Expresión regular combinada (el orden importa!)
token_regex = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in TOKEN_MAP.items())
# Corrección: Los patrones deben ser asociados con su nombre correcto en el regex final
token_regex = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in TOKEN_MAP.items())
# Reconstrucción correcta del regex (nombre de grupo debe ser el ALIAS)
# Usar alias directamente como nombre de grupo
regex_parts = []
for pattern, alias in TOKEN_MAP.items():
    # Evitar duplicados de alias si varios patrones mapean al mismo (ej. operadores)
    # ¡Importante! Asegurar que alias válidos como nombres de grupo en regex
    # Python permite números al inicio de nombres de grupo, pero es mejor evitarlos si es posible
    # Vamos a usar el alias tal cual
    regex_parts.append(f'(?P<{alias}>{pattern})')

# Añadir un grupo para errores al final
regex_parts.append(r'(?P<ERROR>.)') # Captura cualquier otro caracter como error

token_regex = '|'.join(regex_parts)


def lexer(code):
    """Genera tokens a partir del código fuente."""
    tokens = []
    line_num = 1
    line_start = 0
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup # El alias/tipo de token
        value = match.group()   # El texto que coincidió
        column = match.start() - line_start + 1

        if kind == 'ESPACIO':
            pass # Ignorar espacios
        elif kind == 'COMENTARIO':
            pass # Ignorar comentarios
        elif kind == 'ERROR':
            # Manejar error léxico
            tokens.append(('ERROR', value, line_num, column))
            # Podríamos detener el análisis aquí o continuar reportando errores
            # print(f"Error léxico en línea {line_num}, columna {column}: Caracter inesperado '{value}'")
        else:
            tokens.append((kind, value, line_num, column))

        # Actualizar número de línea si hay saltos de línea en el token (poco común excepto en espacios/comentarios multilinea)
        new_lines = value.count('\n')
        if new_lines > 0:
            line_num += new_lines
            line_start = match.end() - value.rfind('\n') -1


    tokens.append(('EOF', 'EOF', line_num, 0)) # Token especial de fin de archivo
    return tokens

# --- 2. Analizador Sintáctico Basado en Pila ---

def analyze_syntax(tokens):
    """
    Analiza la secuencia de tokens usando una pila para verificar estructura básica
    y balanceo de bloques. Devuelve (True, "OK") o (False, "Error message").
    """
    stack = []
    token_iterator = iter(tokens)
    current_token = next(token_iterator, None)
    last_token = None # Para ciertas verificaciones contextuales simples

    # Mapeo de tokens de apertura a sus correspondientes de cierre
    block_pairs = {
        'PROGRAMA': 'FINPROGRAMA',
        'SI': 'FINSI',
        'MIENTRAS': 'FINMIENTRAS',
        'PARENTESIS_IZQ': 'PARENTESIS_DER',
        # 'ENTONCES': 'FINSI', # 'entonces' no abre bloque, 'si' lo hace
        # 'HACER': 'FINMIENTRAS' # 'hacer' no abre bloque, 'mientras' lo hace
    }
    openers = list(block_pairs.keys())
    closers = list(block_pairs.values())

    # Tokens que esperan un bloque después (simplificado)
    expects_block_after = ['ENTONCES', 'SINO', 'HACER']

    # Estado simple para verificar secuencias
    inside_programa = False
    expected_tokens = [] # Pila de expectativas (ej: después de SI viene '(')

    while current_token and current_token[0] != 'EOF':
        token_type, token_value, line, col = current_token

        # --- Verificación de Errores Léxicos ---
        if token_type == 'ERROR':
            return False, f"Error Léxico en Línea {line}, Col {col}: Caracter inesperado '{token_value}'"

        # --- Lógica principal de la Pila y Secuencia ---

        # 1. Manejo de Inicio/Fin de Programa
        if token_type == 'PROGRAMA':
            if inside_programa:
                return False, f"Error Sintáctico en Línea {line}, Col {col}: 'programa' anidado no permitido."
            if stack: # No debería haber nada en la pila antes de 'programa'
                 return False, f"Error Sintáctico en Línea {line}, Col {col}: Código encontrado antes de 'programa'."
            stack.append(token_type)
            inside_programa = True
        elif token_type == 'FINPROGRAMA':
            if not stack or stack[-1] != 'PROGRAMA':
                return False, f"Error Sintáctico en Línea {line}, Col {col}: 'finprograma' sin 'programa' correspondiente o bloque no cerrado."
            stack.pop()
            if stack: # Si queda algo, es un bloque no cerrado
                return False, f"Error Sintáctico en Línea {line}, Col {col}: Bloque '{stack[-1]}' no cerrado antes de 'finprograma'."
            inside_programa = False # Terminó el programa principal

        # 2. Manejo de Bloques (Si, Mientras, Paréntesis)
        elif token_type in openers:
             if not inside_programa and token_type != 'PARENTESIS_IZQ': # Bloques deben estar dentro de programa (excepto paréntesis en expresiones globales?)
                 # Permitiremos paréntesis fuera por si acaso, aunque la gramática lo limita
                 # return False, f"Error Sintáctico en Línea {line}, Col {col}: Bloque '{token_value}' fuera de 'programa'."
                 pass # Relajamos esta regla por ahora
             stack.append(token_type)

             # --- Verificaciones de secuencia básicas ---
             if token_type == 'SI' or token_type == 'MIENTRAS':
                 expected_tokens.append('PARENTESIS_IZQ') # Espera un '(' después
             # No añadimos expectativa para '(' porque puede aparecer en muchos sitios

        elif token_type in closers:
            if not stack:
                return False, f"Error Sintáctico en Línea {line}, Col {col}: Se encontró '{token_value}' de cierre sin bloque de apertura."
            
            expected_opener = None
            for opener, closer in block_pairs.items():
                 if closer == token_type:
                     expected_opener = opener
                     break
            
            if not expected_opener: # No debería ocurrir si closers está bien definido
                 return False, f"Error Interno: No se encontró par para '{token_type}'."

            if stack[-1] == expected_opener:
                stack.pop()
                # Verificaciones post-cierre
                if token_type == 'PARENTESIS_DER' and expected_tokens and expected_tokens[-1] == 'PARENTESIS_IZQ':
                    expected_tokens.pop() # Se cumplió la expectativa del '('
                    # Ahora, después de 'si (...)' esperamos 'entonces'
                    # Si el paréntesis cerraba un 'si' o 'mientras', añadir expectativa
                    # Necesitamos saber qué abrió el paréntesis. ¡La pila actual no lo dice directamente!
                    # Este enfoque de pila simple tiene limitaciones aquí.
                    # Solución simple: No imponer expectativas tan estrictas con esta pila.

            else:
                return False, f"Error Sintáctico en Línea {line}, Col {col}: Se encontró '{token_value}' pero se esperaba cierre para '{stack[-1]}'."

        # 3. Manejo de Keywords Intermedias (entonces, sino, hacer)
        elif token_type == 'ENTONCES':
            if not stack or stack[-1] != 'SI': # Debe seguir a un bloque SI (implícito después del ')' )
                 # Esta verificación es débil porque no sabemos si el ')' cerró la condición del SI
                 # Podríamos requerir que el token *anterior* sea 'PARENTESIS_DER'
                 if not last_token or last_token[0] != 'PARENTESIS_DER':
                      return False, f"Error Sintáctico en Línea {line}, Col {col}: 'entonces' debe seguir a la condición 'si (...)'. Falta ')'?"
                 # No se pushea 'ENTONCES', solo se valida el contexto.
                 # Podríamos cambiar el SI en la pila a SINO_ALLOWED? Complicado.
            pass # Ok contextual (simplificado)

        elif token_type == 'SINO':
             # Debería estar dentro de un bloque SI, y no anidado directamente en otro SINO
             # La pila debería tener SI en algún lugar, pero no inmediatamente? Difícil con pila simple.
             # Verificación simple: ¿Estamos dentro de un bloque SI no cerrado?
             if 'SI' not in stack:
                  return False, f"Error Sintáctico en Línea {line}, Col {col}: 'sino' fuera de un bloque 'si'."
             # Idealmente, verificar que no estamos ya dentro de un 'sino' del mismo 'si'.
             pass # Ok contextual (muy simplificado)

        elif token_type == 'HACER':
            if not stack or stack[-1] != 'MIENTRAS': # Similar a ENTONCES
                 if not last_token or last_token[0] != 'PARENTESIS_DER':
                      return False, f"Error Sintáctico en Línea {line}, Col {col}: 'hacer' debe seguir a la condición 'mientras (...)'. Falta ')'?"
            pass # Ok contextual (simplificado)


        # 4. Verificaciones de Sentencias Simples (simplificado)
        elif token_type == 'PUNTO_Y_COMA':
            # Verifica si el token anterior permite un ';' (ej: expresion, asignacion, llamada, declaracion)
            if not last_token or last_token[0] in ['PROGRAMA', 'ENTONCES', 'HACER', 'SINO', 'PUNTO_Y_COMA', 'ASIGNACION', 'OP_ARITMETICO', 'OP_COMPARACION', 'OP_LOGICO', 'PARENTESIS_IZQ']:
                return False, f"Error Sintáctico en Línea {line}, Col {col}: ';' inesperado después de '{last_token[1] if last_token else 'inicio'}'. "
            pass # Ok contextual (muy simplificado)

        elif token_type == 'ASIGNACION':
            # Debe seguir a un IDENTIFICADOR
             if not last_token or last_token[0] != 'IDENTIFICADOR':
                 return False, f"Error Sintáctico en Línea {line}, Col {col}: Asignación '=' debe seguir a un identificador."
        pass # Ok

        # --- Manejo de Expectativas (ejemplo básico) ---
        if expected_tokens and token_type == expected_tokens[-1]:
            expected_tokens.pop()
        # elif expected_tokens and token_type not in ['IDENTIFICADOR', 'LITERAL_ENTERO', ...]: # Si se esperaba algo específico y no llega...
            # return False, f"Error Sintáctico: Se esperaba {expected_tokens[-1]} pero se encontró {token_type}"
            # Desactivado porque es difícil manejar todas las posibilidades con esta estructura


        # --- Actualizar último token y avanzar ---
        last_token = current_token
        current_token = next(token_iterator, None)

    # --- Verificación Final ---
    if not inside_programa and last_token and last_token[0] == 'FINPROGRAMA':
         # Si el último token fue FINPROGRAMA y no estamos 'inside', significa que cerró bien
         pass
    elif inside_programa and not stack:
         # Si estamos 'inside' pero la pila está vacía (quizás solo hubo 'programa' y EOF)
         return False, f"Error Sintáctico: Falta 'finprograma' al final del código."
    elif stack: # Si queda algo en la pila, hay bloques sin cerrar
        return False, f"Error Sintáctico: Fin de archivo inesperado. Bloque '{stack[-1]}' no fue cerrado."
    elif not last_token and not inside_programa: # Código vacío
        return False, "Error Sintáctico: El código está vacío o no contiene 'programa'."
    elif not inside_programa and last_token[0] != 'FINPROGRAMA':
         # Terminó el código, no estamos en programa, pero lo último no fue finprograma
         return False, f"Error Sintáctico: Código encontrado después de 'finprograma' o falta 'finprograma'."


    return True, "Análisis Sintáctico Básico: OK (Estructura de bloques correcta)"

# --- 3. Interfaz Gráfica (GUI) ---

def analyze_code_gui():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        result_display.config(text="Resultado: Por favor, inserte código.", fg="orange")
        return

    # 1. Lexer
    tokens = lexer(code)
    # Opcional: Mostrar tokens para depuración
    # print(tokens)

    # Mostrar errores léxicos primero si existen
    lexical_errors = [t for t in tokens if t[0] == 'ERROR']
    if lexical_errors:
         error_msg = f"Error Léxico en Línea {lexical_errors[0][2]}, Col {lexical_errors[0][3]}: Caracter inesperado '{lexical_errors[0][1]}'"
         result_display.config(text=f"Resultado: {error_msg}", fg="red")
         return # Detener análisis si hay error léxico

    # 2. Analizador Sintáctico
    is_correct, message = analyze_syntax(tokens)

    if is_correct:
        result_display.config(text=f"Resultado: {message}", fg="green")
    else:
        result_display.config(text=f"Resultado: {message}", fg="red")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Analizador Sintáctico Simplex")
root.geometry("700x500")

# Etiqueta para la entrada de código
input_label = tk.Label(root, text="Inserte su código Simplex aquí:")
input_label.pack(pady=(10, 0))

# Área de texto para insertar código
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Courier New", 10))
code_input.pack(pady=5, padx=10)

# Botón para iniciar el análisis
analyze_button = tk.Button(root, text="Analizar Código", command=analyze_code_gui, width=20, height=2)
analyze_button.pack(pady=10)

# Etiqueta para mostrar el resultado del análisis
result_display = tk.Label(root, text="Resultado:", wraplength=650, justify=tk.LEFT, font=("Arial", 11))
result_display.pack(pady=(5, 10), padx=10)

# Iniciar el bucle principal de la GUI
root.mainloop()