class TablaSintactica:
    def __init__(self, gramatica):
        """
        Inicializa la clase con la gramática proporcionada.
        """
        self.gramatica = gramatica

    def generar_tabla_sintactica(self):
        """
        Genera la tabla sintáctica basada en la gramática.
        """
        # Aquí puedes implementar la lógica para generar la tabla sintáctica
        # basada en la gramática cargada.
        tabla = {}
        for no_terminal, producciones in self.gramatica.items():
            tabla[no_terminal] = {}
            for produccion in producciones:
                primeros = self.calcular_primeros(produccion)
                for simbolo in primeros:
                    if simbolo != "ε":
                        tabla[no_terminal][simbolo] = produccion
                    else:
                        siguientes = self.calcular_siguientes(no_terminal)
                        for simbolo_siguiente in siguientes:
                            tabla[no_terminal][simbolo_siguiente] = produccion
        return tabla

    def calcular_primeros(self, produccion):
        """
        Calcula los primeros de una producción.
        """
        primeros = set()
        simbolo = produccion.split()[0]  # Tomamos el primer símbolo de la producción
        if simbolo in self.gramatica:  # Si es un no terminal
            primeros.update(self.calcular_primeros_no_terminal(simbolo))
        else:  # Si es un terminal
            primeros.add(simbolo)
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

    def calcular_siguientes(self, no_terminal):
        """
        Calcula los siguientes para un no terminal específico.
        """
        siguientes = set()
        if no_terminal == "S":  # El símbolo inicial
            siguientes.add("$")  # El símbolo de fin de cadena
        for nt, producciones in self.gramatica.items():
            for produccion in producciones:
                simbolos = produccion.split()
                for i, simbolo in enumerate(simbolos):
                    if simbolo == no_terminal:
                        if i < len(simbolos) - 1:
                            siguiente_simbolo = simbolos[i + 1]
                            if siguiente_simbolo in self.gramatica:
                                primeros_siguiente = self.calcular_primeros_no_terminal(siguiente_simbolo)
                                siguientes.update(primeros_siguiente)
                            else:
                                siguientes.add(siguiente_simbolo)
                        else:
                            siguientes.update(self.calcular_siguientes(nt))
        return siguientes