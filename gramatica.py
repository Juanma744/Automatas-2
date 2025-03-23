class Gramatica:
    def __init__(self):
        # Definimos las reglas gramaticales
        self.reglas = {
            "S": [["Inicio", "A", "Fin"]],
            "A": [["B", "A'"]],
            "A'": [["ε"], ["B", "A'"]],
            "B": [["C"], ["D"], ["F"], ["G"], ["H"], ["I"]],
            "C": [["J", "K"]],
            "K": [["var", "K'"]],
            "K'": [["ε"], [",", "var", "K'"]],
            "J": [["Entero"], ["Doble"], ["Cadena"]],
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
            "R": [[">"], ["<"], ["="], ["!"]]
        }

    def validar_codigo(self, codigo):
        tokens = codigo.split()  # Dividir el código en tokens
        try:
            self.validar_regla("S", tokens, 0)
            return "El código es válido según la gramática."
        except Exception as e:
            return f"Error de sintaxis: {str(e)}"

    def validar_regla(self, regla, tokens, indice):
        if regla in self.reglas:
            for opcion in self.reglas[regla]:
                try:
                    indice_actual = indice
                    for simbolo in opcion:
                        if simbolo == "ε":
                            continue
                        indice_actual = self.validar_regla(simbolo, tokens, indice_actual)
                    return indice_actual
                except:
                    continue
            raise Exception(f"No se pudo aplicar la regla {regla} en el token {tokens[indice]}")
        else:
            if indice < len(tokens) and tokens[indice] == regla:
                return indice + 1
            else:
                raise Exception(f"Token inesperado: {tokens[indice]}. Se esperaba: {regla}")