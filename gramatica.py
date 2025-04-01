# --- START OF FILE gramatica.py ---

import re

class Gramatica:
    def __init__(self):
        # Gramática COMPLETA estructuralmente
        self.gramatica_completa = {
            # ... (definición completa como la tenías) ...
             "S": [["Start", "A", "End"]], "A": [["B", "A'"]], "A'": [["ε"], ["B", "A'"]],
             "B": [["C"], ["D"], ["F"], ["G"], ["H"], ["I"]], "C": [["J", "K"]],
             "J": [["Entero"], ["Doble"], ["Cadena"]], "K": [["var", "K'"]],
             "K'": [["ε"], [",", "var", "K'"]], "D": [["var", "=", "L"]],
             "L": [["M", "L'"]], "L'": [["ε"], ["OP", "M", "L'"]],
             "M": [["var"], ["(", "L", ")"], ["num"]], "OP": [["+"], ["-"], ["*"], ["/"]],
             "H": [["Si", "(", "N", ")", "{", "A", "}", "Q"]], "Q": [["ε"], ["SiNo", "{", "A", "}"]],
             "I": [["Mientras", "(", "N", ")", "{", "A", "}"]], "F": [["Entrada", "(", "var", ")"]],
             "G": [["Salida", "(", "var", ")"]], "N": [["M", "N'"]],
             "N'": [["ε"], ["R", "M"]],
             "R": [[">"], ["<"], ["="], ["!"], ["<="], [">="], ["!="], ["++"]]
        }

        # Dependencias explícitas (pueden ayudar, pero la propagación por producción es más robusta)
        self.dependencias_nt = {
            # ... (definición como la tenías) ...
            "S": {"A"}, "A": {"B", "A'"}, "A'": {"B"}, "B": {"C", "D", "F", "G", "H", "I"},
            "C": {"J", "K"}, "K": {"K'"}, "D": {"L"}, "L": {"M", "L'", "OP"}, "L'": {"OP", "M"},
            "H": {"N", "A", "Q"}, "Q": {"A"}, "I": {"N", "A"}, "N": {"M", "N'"}, "N'": {"R", "M"},
        }

        # Mapeo token -> NTs que podrían introducirlo (para la activación inicial)
        self.mapeo_palabra_a_nt = {
             # ... (definición como la tenías) ...
             "Start": "S", "End": "S", "Entero": "J", "Doble": "J", "Cadena": "J",
             "var": ["K", "D", "M", "F", "G"], "=": "D", "+": "OP", "-": "OP", "*": "OP", "/": "OP",
             "Si": "H", "SiNo": "Q", "Mientras": "I", "Entrada": "F", "Salida": "G",
             ">": "R", "<": "R", "<=": "R", ">=": "R", "!=": "R", "++": "R", "!": "R",
             "(": ["M", "H", "I", "F", "G"],
        }

        # Definición original (para compatibilidad si se usa obtener_reglas_aplicadas)
        # PERO LO MODIFICAREMOS EN INTERFAZ.PY PARA NO USARLO EN EL BOTÓN
        self.reglas = { # Formato antiguo, por si acaso
            "S": ["Inicio A Fin"], "A": ["B A'"], "A'": ["ε", "B A'"],
            "B": ["C", "D", "F", "G", "H", "I"], "C": ["J K"], "K": ["var K'"],
            "K'": ["ε", ", var K'"], "J": ["Entero", "Doble", "Cadena"],
            "D": ["var = L"], "L": ["M L'"], "L'": ["ε", "OP M L'"],
            "M": ["var", "(L)", "num"], "OP": ["+", "-", "*", "/"],
            "H": ["Si(N) {A} Q"], "Q": ["ε", "SiNo {A}"], "I": ["Mientras(N) {A}"],
            "F": ["Entrada(var)"], "G": ["Salida(var)"], "N": ["M N'"],
            "N'": ["ε", "R M"], "R": [">", "<", "=", "!"]
        }
        self.tokens_reconocidos = { # También para compatibilidad con obtener_reglas_aplicadas
            "Start", "End", "Entero", "Doble", "Cadena", "Salida", "Entrada",
            "Mientras", "Si", "SiNo", "FinSi", "FinMientras", "var", "num",
            "+", "-", "*", "/", "=", ">", "<", ">=", "<=", "!=", "(", ")", "{", "}", ",", ";", ":"
        }
    # --- FIN DEL MÉTODO __init__ ---
# --- En gramatica.py, dentro de class Gramatica ---

    def obtener_gramatica_activa(self, codigo):
        """
        Analiza el código y devuelve un subconjunto de la gramática completa
        basado en heurísticas (palabras clave encontradas). NO PROPAGA DEPENDENCIAS.
        Retorna un diccionario con la estructura requerida por PrimerosSiguientes.
        """
        print("\n--- Iniciando obtención de gramática activa (SIN PROPAGACIÓN) ---") # DEBUG
        nts_activos = set()
        tokens_encontrados = set(re.findall(r'[a-zA-Z_]\w*|\d+\.\d+|\d+|<=|>=|!=|\+\+|--|[-+*/=(){}<>,:;!]', codigo))
        print(f"Tokens encontrados: {tokens_encontrados}") # DEBUG

        nts_iniciales = set()
        if "Start" in tokens_encontrados and "End" in tokens_encontrados:
            print("Activando S, A, A', B por Start/End") # DEBUG
            nts_iniciales.update({"S", "A", "A'", "B"})

        print("Activando NTs por tokens específicos:") # DEBUG
        for token in tokens_encontrados:
            mapeo = self.mapeo_palabra_a_nt.get(token)
            if mapeo:
                nts_a_agregar = mapeo if isinstance(mapeo, list) else [mapeo]
                for nt in nts_a_agregar:
                    if nt not in nts_iniciales:
                        print(f"  Token '{token}' activa NT: {nt}") # DEBUG
                        nts_iniciales.add(nt)

        # ... (Heurísticas adicionales como las tenías) ...
        if "=" in tokens_encontrados and "var" in tokens_encontrados:
            if "D" not in nts_iniciales: print("Activando D por asignación (=)") # DEBUG
            nts_iniciales.add("D")
        if any(decl in tokens_encontrados for decl in ["Entero", "Doble", "Cadena"]):
             if "C" not in nts_iniciales: print("Activando C por declaración") # DEBUG
             nts_iniciales.add("C")
        if any(op in tokens_encontrados for op in ["+", "-", "*", "/"]):
            if "OP" not in nts_iniciales: print("Activando OP por aritmética") # DEBUG
            nts_iniciales.add("OP")
        if "Si" in tokens_encontrados:
            if "H" not in nts_iniciales: print("Activando H por Si") # DEBUG
            nts_iniciales.add("H")
            if "SiNo" in tokens_encontrados:
                 if "Q" not in nts_iniciales: print("Activando Q por SiNo") # DEBUG
                 nts_iniciales.add("Q")
        if "Mientras" in tokens_encontrados:
             if "I" not in nts_iniciales: print("Activando I por Mientras") # DEBUG
             nts_iniciales.add("I")
        if "Entrada" in tokens_encontrados:
             if "F" not in nts_iniciales: print("Activando F por Entrada") # DEBUG
             nts_iniciales.add("F")
        if "Salida" in tokens_encontrados:
             if "G" not in nts_iniciales: print("Activando G por Salida") # DEBUG
             nts_iniciales.add("G")
        if any(op_rel in tokens_encontrados for op_rel in [">", "<", "<=", ">=", "!=", "==", "!", "++", "="]):
             if "R" not in nts_iniciales: print("Activando R por operador relacional/comparación/++") # DEBUG
             nts_iniciales.add("R")


        # --- SECCIÓN DE PROPAGACIÓN COMENTADA/ELIMINADA ---
        # print("Propagando dependencias...")
        # cola = list(nts_iniciales)
        # nts_activos.update(nts_iniciales) # Empezar con los iniciales
        # visitados_para_dependencia = set()
        # while cola:
        #    nt_actual = cola.pop(0)
        #    # ... (Lógica de propagación eliminada) ...
        # --------------------------------------------------

        # Usar SOLO los NTs activados inicialmente
        nts_activos = nts_iniciales # <-- Asignar directamente

        print(f"\nNTs activos finales (SIN PROPAGACIÓN): {nts_activos}") # DEBUG

        # 3. Construir el diccionario de gramática activa
        gramatica_activa = {}
        for nt in nts_activos:
            # Asegurarse que el NT realmente existe en la definición completa
            if nt in self.gramatica_completa:
                 gramatica_activa[nt] = self.gramatica_completa[nt]
            # Incluir NTs necesarios aunque no tengan producciones directas activadas?
            # Ejemplo: Si activamos D, necesitamos L, L', M, OP aunque no haya tokens para ellos?
            # -> Este es el dilema de la corrección vs el filtrado estricto.
            # -> Por ahora, solo incluimos los NTs directamente activados.

        print("--- Gramática Activa Construida (SIN PROPAGACIÓN) ---") # DEBUG
        if not gramatica_activa:
            print("ADVERTENCIA: No se activó ninguna regla de la gramática.") # DEBUG
        return gramatica_activa
    
    # --- Método antiguo (lo dejaremos pero no lo usaremos desde el botón) ---
    def obtener_reglas_aplicadas(self, codigo):
        # ... (código original de este método, que usa self.tokens_reconocidos) ...
        # Este método devuelve strings, no la estructura que necesitamos
        # y depende de self.tokens_reconocidos que puede causar el error si no está definido
        # en __init__ como lo hemos vuelto a poner ahora.
        reglas_aplicadas = []
        # ... (resto del código original) ...
        print("ADVERTENCIA: Llamando a obtener_reglas_aplicadas (método antiguo)") # DEBUG
        # Ejemplo simple para evitar error si tokens_reconocidos falta:
        if not hasattr(self, 'tokens_reconocidos'):
             return ["Error: self.tokens_reconocidos no definido"]

        palabras_no_reconocidas = set()
        palabras = re.findall(r'\b\w+\b|[^\w\s]', codigo)
        for palabra in palabras:
            # Corrección: usar hasattr para verificar si existe antes de usarlo
            if hasattr(self, 'tokens_reconocidos') and palabra not in self.tokens_reconocidos and not self.es_variable_o_numero(palabra):
                 palabras_no_reconocidas.add(palabra)

        if palabras_no_reconocidas:
            reglas_aplicadas.append(f"Palabras no reconocidas: {', '.join(palabras_no_reconocidas)}")

        if "Start" in codigo and "End" in codigo: reglas_aplicadas.append("S → Start A End")
        # ... (resto de la lógica original de este método) ...
        return reglas_aplicadas


    def es_variable_o_numero(self, palabra):
        return re.match(r'^[a-zA-Z_]\w*$', palabra) or re.match(r'^\d+$', palabra) or re.match(r'^\d+\.\d+$', palabra)

# --- Fin de gramatica.py ---