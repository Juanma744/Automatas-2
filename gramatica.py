import re

class Gramatica:
    def __init__(self):
        # Definimos las reglas de la gramática
        self.reglas = {
            "S": ["Inicio A Fin"],
            "A": ["B A'"],
            "A'": ["ε", "B A'"],
            "B": ["C", "D", "F", "G", "H", "I"],
            "C": ["J K"],
            "K": ["var K'"],
            "K'": ["ε", ", var K'"],
            "J": ["Entero", "Doble", "Cadena"],
            "D": ["var = L"],
            "L": ["M L'"],
            "L'": ["ε", "OP M L'"],
            "M": ["var", "(L)", "num"],
            "OP": ["+", "-", "*", "/"],
            "H": ["Si(N) {A} Q"],
            "Q": ["ε", "SiNo {A}"],
            "I": ["Mientras(N) {A}"],
            "F": ["Entrada(var)"],
            "G": ["Salida(var)"],
            "N": ["M N'"],
            "N'": ["ε", "R M"],
            "R": [">", "<", "=", "!"]
        }

        # Definimos los tokens reconocidos por la gramática
        self.tokens_reconocidos = {
            "Start", "End", "Entero", "Doble", "Cadena", "Salida", "Entrada",
            "Mientras", "Si", "SiNo", "FinSi", "FinMientras", "var", "num",
            "+", "-", "*", "/", "=", ">", "<", ">=", "<=", "!=", "(", ")", "{", "}", ",", ";", ":"
        }

    def obtener_gramatica(self):
        """
        Devuelve las reglas de la gramática.
        """
        return self.reglas

    def obtener_reglas_aplicadas(self, codigo):
        """
        Analiza el código y devuelve las reglas de la gramática aplicadas.
        También detecta palabras no reconocidas.
        """
        reglas_aplicadas = []
        palabras_no_reconocidas = set()

        # Dividir el código en palabras y símbolos
        palabras = re.findall(r'\b\w+\b|[^\w\s]', codigo)

        # Verificar cada palabra o símbolo
        for palabra in palabras:
            if palabra not in self.tokens_reconocidos and not self.es_variable_o_numero(palabra):
                palabras_no_reconocidas.add(palabra)

        # Mostrar palabras no reconocidas
        if palabras_no_reconocidas:
            reglas_aplicadas.append(f"Palabras no reconocidas: {', '.join(palabras_no_reconocidas)}")

        # Reglas aplicadas (como antes)
        if "Start" in codigo and "End" in codigo:
            reglas_aplicadas.append("S → Inicio A Fin")

        if "Entero" in codigo or "Doble" in codigo or "Cadena" in codigo:
            reglas_aplicadas.append("C → J K")
            reglas_aplicadas.append("J → Entero | Doble | Cadena")
            reglas_aplicadas.append("K → var K'")

        if "Salida" in codigo:
            reglas_aplicadas.append("G → Salida(var)")

        if "Entrada" in codigo:
            reglas_aplicadas.append("F → Entrada(var)")

        if "Mientras" in codigo:
            reglas_aplicadas.append("I → Mientras(N) {A}")

        if "=" in codigo:
            reglas_aplicadas.append("D → var = L")
            reglas_aplicadas.append("L → M L'")
            reglas_aplicadas.append("M → var | num")

        if "+" in codigo or "-" in codigo or "*" in codigo or "/" in codigo:
            reglas_aplicadas.append("OP → + | - | * | /")

        if "Si" in codigo:
            reglas_aplicadas.append("H → Si(N) {A} Q")

        return reglas_aplicadas

    def es_variable_o_numero(self, palabra):
        """
        Verifica si una palabra es una variable o un número.
        """
        return re.match(r'^[a-zA-Z_]\w*$', palabra) or re.match(r'^\d+$', palabra) or re.match(r'^\d+\.\d+$', palabra)