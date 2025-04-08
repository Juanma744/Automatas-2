# gramatica.py

import re

class Gramatica:
    def __init__(self):
        # Gramática COMPLETA estructuralmente
        self.gramatica_completa = {
            "S": [["Start", "A", "End"]],
            "A": [["B", "A'"]],
            "A'": [["ε"], ["B", "A'"]],
            "B": [["C"], ["D"], ["F"], ["G"], ["H"], ["I"]],
            "C": [["J", "K"]],
            "J": [["Entero"], ["Doble"], ["Cadena"]],
            "K": [["var", "K'"]],
            "K'": [["ε"], [",", "var", "K'"]],
            "D": [["var", "=", "L"]],
            "L": [["M", "L'"]],
            "L'": [["ε"], ["OP", "M", "L'"]],
            "M": [["var"], ["(", "L", ")"], ["num"]],
            "OP": [["+"], ["-"], ["*"], ["/"]],
            "H": [["Si", "(", "N", ")", "{", "A", "}", "Q"]],
            "Q": [["ε"], ["SiNo", "{", "A", "}"]],
            "I": [["Mientras", "(", "N", ")", "{", "A", "}"]],
            "F": [["Entrada", "(", "var", ")"]],
            "G": [["Salida", "(", "var", ")"]],
            "N": [["M", "N'"]],
            "N'": [["ε"], ["R", "M"]],
            "R": [[">"], ["<"], ["="], ["!"], ["<="], [">="], ["!="], ["++"]]
        }

        self.mapeo_palabra_a_nt = {
            "Start": "S", "End": "S", "Entero": "J", "Doble": "J", "Cadena": "J",
            "var": ["K", "D", "M", "F", "G"], "=": "D", "+": "OP", "-": "OP", "*": "OP", "/": "OP",
            "Si": "H", "SiNo": "Q", "Mientras": "I", "Entrada": "F", "Salida": "G",
            ">": "R", "<": "R", "<=": "R", ">=": "R", "!=": "R", "++": "R", "!": "R",
            "(": ["M", "H", "I", "F", "G"],
        }

    def obtener_gramatica_activa(self, codigo):
        print("\n--- Iniciando obtención de gramática activa (SIN PROPAGACIÓN) ---")
        nts_activos = set()
        tokens_encontrados = set(re.findall(r'[a-zA-Z_]\w*|\d+\.\d+|\d+|<=|>=|!=|\+\+|--|[-+*/=(){}<>,:;!]', codigo))
        print(f"Tokens encontrados: {tokens_encontrados}")

        nts_iniciales = set()
        if "Start" in tokens_encontrados and "End" in tokens_encontrados:
            print("Activando S, A, A', B por Start/End")
            nts_iniciales.update({"S", "A", "A'", "B"})

        print("Activando NTs por tokens específicos:")
        for token in tokens_encontrados:
            mapeo = self.mapeo_palabra_a_nt.get(token)
            if mapeo:
                nts_a_agregar = mapeo if isinstance(mapeo, list) else [mapeo]
                for nt in nts_a_agregar:
                    if nt not in nts_iniciales:
                        print(f"  Token '{token}' activa NT: {nt}")
                        nts_iniciales.add(nt)

        if "=" in tokens_encontrados and "var" in tokens_encontrados:
            if "D" not in nts_iniciales: print("Activando D por asignación (=)")
            nts_iniciales.add("D")
        if any(decl in tokens_encontrados for decl in ["Entero", "Doble", "Cadena"]):
            if "C" not in nts_iniciales: print("Activando C por declaración")
            nts_iniciales.add("C")
        if any(op in tokens_encontrados for op in ["+", "-", "*", "/"]):
            if "OP" not in nts_iniciales: print("Activando OP por aritmética")
            nts_iniciales.add("OP")
        if "Si" in tokens_encontrados:
            if "H" not in nts_iniciales: print("Activando H por Si")
            nts_iniciales.add("H")
            if "SiNo" in tokens_encontrados:
                if "Q" not in nts_iniciales: print("Activando Q por SiNo")
                nts_iniciales.add("Q")
        if "Mientras" in tokens_encontrados:
            if "I" not in nts_iniciales: print("Activando I por Mientras")
            nts_iniciales.add("I")
        if "Entrada" in tokens_encontrados:
            if "F" not in nts_iniciales: print("Activando F por Entrada")
            nts_iniciales.add("F")
        if "Salida" in tokens_encontrados:
            if "G" not in nts_iniciales: print("Activando G por Salida")
            nts_iniciales.add("G")
        if any(op_rel in tokens_encontrados for op_rel in [">", "<", "<=", ">=", "!=", "==", "!", "++", "="]):
            if "R" not in nts_iniciales: print("Activando R por operador relacional/comparación/++")
            nts_iniciales.add("R")

        nts_activos = nts_iniciales

        print(f"\nNTs activos finales (SIN PROPAGACIÓN): {nts_activos}")

        # 3. Construir el diccionario de gramática activa
        gramatica_activa = {}
        for nt in nts_activos:
            # Asegurarse que el NT realmente existe en la definición completa
            if nt in self.gramatica_completa:
                gramatica_activa[nt] = self.gramatica_completa[nt]
        print("--- Gramática Activa Construida (SIN PROPAGACIÓN) ---")
        if not gramatica_activa:
            print("ADVERTENCIA: No se activó ninguna regla de la gramática.")
        return gramatica_activa

    def es_variable_o_numero(self, palabra):
        return re.match(r'^[a-zA-Z_]\w*$', palabra) or re.match(r'^\d+$', palabra) or re.match(r'^\d+\.\d+$', palabra)