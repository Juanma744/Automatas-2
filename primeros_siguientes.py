class PrimerosSiguientes:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.primeros = {}
        self.siguientes = {}
        self.terminales = set()
        self.no_terminales = set()
        
        # Inicializar conjuntos
        self._inicializar_conjuntos()
        
    def _inicializar_conjuntos(self):
        # Identificar terminales y no terminales
        for no_terminal, producciones in self.gramatica.items():
            self.no_terminales.add(no_terminal)
            for produccion in producciones:
                for simbolo in produccion.split():
                    if simbolo not in self.gramatica and simbolo != "ε":
                        self.terminales.add(simbolo)
        
        # Inicializar primeros y siguientes
        for no_terminal in self.no_terminales:
            self.primeros[no_terminal] = set()
            self.siguientes[no_terminal] = set()
        
        # El símbolo inicial tiene $ en sus siguientes
        self.siguientes["S"].add("$")
    
    def calcular_primeros(self):
        cambiado = True
        while cambiado:
            cambiado = False
            for no_terminal, producciones in self.gramatica.items():
                for produccion in producciones:
                    simbolos = produccion.split()
                    # Caso 1: Producción vacía (ε)
                    if simbolos[0] == "ε":
                        if "ε" not in self.primeros[no_terminal]:
                            self.primeros[no_terminal].add("ε")
                            cambiado = True
                        continue
                    
                    # Caso 2: Primer símbolo es terminal
                    primer_simbolo = simbolos[0]
                    if primer_simbolo in self.terminales:
                        if primer_simbolo not in self.primeros[no_terminal]:
                            self.primeros[no_terminal].add(primer_simbolo)
                            cambiado = True
                        continue
                    
                    # Caso 3: Primer símbolo es no terminal
                    todos_tienen_epsilon = True
                    for simbolo in simbolos:
                        if simbolo in self.terminales:
                            if simbolo not in self.primeros[no_terminal]:
                                self.primeros[no_terminal].add(simbolo)
                                cambiado = True
                            todos_tienen_epsilon = False
                            break
                        
                        # Agregar primeros del no terminal (excepto ε)
                        primeros_simbolo = self.primeros.get(simbolo, set()) - {"ε"}
                        nuevos_primeros = primeros_simbolo - self.primeros[no_terminal]
                        if nuevos_primeros:
                            self.primeros[no_terminal].update(nuevos_primeros)
                            cambiado = True
                        
                        # Verificar si tiene ε
                        if "ε" not in self.primeros.get(simbolo, set()):
                            todos_tienen_epsilon = False
                            break
                    
                    # Si todos pueden ser ε, agregar ε
                    if todos_tienen_epsilon and "ε" not in self.primeros[no_terminal]:
                        self.primeros[no_terminal].add("ε")
                        cambiado = True
    
    def calcular_siguientes(self):
        cambiado = True
        while cambiado:
            cambiado = False
            for no_terminal, producciones in self.gramatica.items():
                for produccion in producciones:
                    simbolos = produccion.split()
                    for i, simbolo in enumerate(simbolos):
                        if simbolo not in self.no_terminales:
                            continue
                        
                        # Regla 1: Si hay algo después
                        if i < len(simbolos) - 1:
                            siguiente = simbolos[i+1]
                            
                            # Si es terminal, agregarlo a siguientes
                            if siguiente in self.terminales:
                                if siguiente not in self.siguientes[simbolo]:
                                    self.siguientes[simbolo].add(siguiente)
                                    cambiado = True
                            else:
                                # Si es no terminal, agregar sus primeros (excepto ε)
                                primeros_siguiente = self.primeros.get(siguiente, set()) - {"ε"}
                                nuevos_siguientes = primeros_siguiente - self.siguientes[simbolo]
                                if nuevos_siguientes:
                                    self.siguientes[simbolo].update(nuevos_siguientes)
                                    cambiado = True
                                
                                # Si el siguiente puede ser ε, aplicar regla 2
                                if "ε" in self.primeros.get(siguiente, set()):
                                    siguientes_no_terminal = self.siguientes.get(no_terminal, set())
                                    nuevos_siguientes = siguientes_no_terminal - self.siguientes[simbolo]
                                    if nuevos_siguientes:
                                        self.siguientes[simbolo].update(nuevos_siguientes)
                                        cambiado = True
                        
                        # Regla 2: Si es el último símbolo o todo lo que sigue puede ser ε
                        else:
                            siguientes_no_terminal = self.siguientes.get(no_terminal, set())
                            nuevos_siguientes = siguientes_no_terminal - self.siguientes[simbolo]
                            if nuevos_siguientes:
                                self.siguientes[simbolo].update(nuevos_siguientes)
                                cambiado = True
    
    def calcular_primeros_siguientes(self):
        # Calcular primeros
        self.calcular_primeros()
        
        # Calcular siguientes
        self.calcular_siguientes()
        
        # Reemplazar "ε" por "€" para coincidir con tus imágenes
        primeros = {k: {v.replace("ε", "€") for v in vs} for k, vs in self.primeros.items()}
        siguientes = {k: {v.replace("SiNo", "SINo") for v in vs} for k, vs in self.siguientes.items()}
        
        return primeros, siguientes