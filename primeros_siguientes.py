class PrimerosSiguientes:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.primeros = {}
        self.siguientes = {}

    def calcular_primeros_siguientes(self):
        # Conjuntos de Primeros (ajustados a tus imágenes)
        self.primeros = {
            "S": {"Inicio"},
            "A": {"Entero", "Doble", "Cadena", "var", "Entrada", "Salida", "Si", "Mientras", "ε"},
            "A'": {"Entero", "Doble", "Cadena", "var", "Entrada", "Salida", "Si", "Mientras", "ε"},
            "B": {"Entero", "Doble", "Cadena", "var", "Entrada", "Salida", "Si", "Mientras"},
            "C": {"Entero", "Doble", "Cadena"},
            "D": {"var"},
            "F": {"Entrada"},
            "G": {"Salida"},
            "H": {"Si"},
            "I": {"Mientras"},
            "J": {"Entero", "Doble", "Cadena"},
            "K": {"var"},
            "K'": {"ε", ","},
            "L": {"var", "(", "num"},
            "L'": {"ε", "+", "-", "*", "/"},
            "M": {"var", "(", "num"},
            "N": {"var", "(", "num"},
            "N'": {"ε", ">", "<", "=", "!"},
            "OP": {"+", "-", "*", "/"},
            "Q": {"ε", "SiNo"},
            "R": {">", "<", "=", "!"}
        }

        # Conjuntos de Siguientes (ajustados a tus imágenes)
        self.siguientes = {
            "S": {"$"},
            "A": {"Fin", "}"},
            "A'": {"Fin", "}"},
            "B": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "C": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "D": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "F": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "G": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "H": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "I": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "J": {"var"},
            "K": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "K'": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "L": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}", ")"},
            "L'": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "M": {"+", "-", "*", "/", "var", "(", "num"},
            "N": {")"},
            "N'": {")"},
            "OP": {"var", "(", "num"},
            "Q": {"Fin", "Entrada", "Doble", "Cadena", "var", "Salida", "Si", "Mientras", "SiNo", "}"},
            "R": {"var", "(", "num"}
        }

        return self.primeros, self.siguientes