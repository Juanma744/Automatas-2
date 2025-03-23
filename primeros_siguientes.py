class PrimerosSiguientes:
    def __init__(self, gramatica):
        """
        Inicializa la clase con la gramática proporcionada.
        """
        self.gramatica = gramatica

    def calcular_primeros_siguientes(self):
        """
        Calcula los conjuntos de primeros y siguientes para la gramática.
        """
        primeros = self.calcular_primeros()
        siguientes = self.calcular_siguientes(primeros)
        return primeros, siguientes

    def calcular_primeros(self):
        """
        Calcula los conjuntos de primeros para cada no terminal.
        """
        primeros = {}
        for no_terminal in self.gramatica:
            primeros[no_terminal] = self.calcular_primeros_no_terminal(no_terminal)
        return primeros

    def calcular_primeros_no_terminal(self, no_terminal):
        """
        Calcula los primeros para un no terminal específico.
        """
        primeros_set = set()
        for produccion in self.gramatica[no_terminal]:
            simbolo = produccion.split()[0]  # Tomamos el primer símbolo de la producción
            if simbolo in self.gramatica:  # Si es un no terminal
                primeros_set.update(self.calcular_primeros_no_terminal(simbolo))
            else:  # Si es un terminal
                primeros_set.add(simbolo)
        return primeros_set

    def calcular_siguientes(self, primeros):
        """
        Calcula los conjuntos de siguientes para cada no terminal.
        """
        siguientes = {no_terminal: set() for no_terminal in self.gramatica}
        siguientes["S"].add("$")  # El símbolo de fin de cadena

        for no_terminal in self.gramatica:
            for produccion in self.gramatica[no_terminal]:
                simbolos = produccion.split()
                for i, simbolo in enumerate(simbolos):
                    if simbolo in self.gramatica:  # Si es un no terminal
                        if i < len(simbolos) - 1:
                            siguiente_simbolo = simbolos[i + 1]
                            if siguiente_simbolo in self.gramatica:
                                siguientes[simbolo].update(primeros[siguiente_simbolo])
                            else:
                                siguientes[simbolo].add(siguiente_simbolo)
                        else:
                            siguientes[simbolo].update(siguientes[no_terminal])
        return siguientes