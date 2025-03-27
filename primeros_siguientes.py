class PrimerosSiguientes:
    def __init__(self, gramatica=None):
        # Gramática completa de referencia
        self.gramatica_completa = {
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
        self.gramatica_activa = {}
        self.primeros = {}
        self.siguientes = {}
        self.terminales = set()
        self.no_terminales = set()

    def actualizar_gramatica_activa(self, reglas_aplicadas):
        """Actualiza la gramática activa basada en las reglas aplicadas encontradas en el código"""
        self.gramatica_activa = {}
        
        # Mapeo de reglas simplificadas a las completas
        reglas_mapeo = {
            "S → Inicio A Fin": "S",
            "C → J K": "C",
            "J → Entero | Doble | Cadena": "J",
            "K → var K'": "K",
            "G → Salida(var)": "G",
            "F → Entrada(var)": "F",
            "I → Mientras(N) {A}": "I",
            "D → var = L": "D",
            "L → M L'": "L",
            "M → var | num": "M",
            "OP → + | - | * | /": "OP",
            "H → Si(N) {A} Q": "H",
            "Q → ε | SiNo {A}": "Q",
            "A → B A'": "A",
            "A' → ε | B A'": "A'",
            "B → C | D | F | G | H | I": "B",
            "K' → ε | , var K'": "K'",
            "L' → ε | OP M L'": "L'",
            "N → M N'": "N",
            "N' → ε | R M": "N'",
            "R → > | < | = | !": "R"
        }
        
        # Activar solo las reglas que aparecen en el código
        for regla in reglas_aplicadas:
            if regla in reglas_mapeo:
                nt = reglas_mapeo[regla]
                self.gramatica_activa[nt] = self.gramatica_completa[nt]
        
        # Incluir dependencias necesarias
        self._agregar_dependencias()
        
        return self.gramatica_activa

    def _agregar_dependencias(self):
        """Agrega reglas dependientes necesarias para las reglas activas"""
        # Siempre incluir S si hay otras reglas
        if "S" not in self.gramatica_activa and any(nt in self.gramatica_activa for nt in ["A", "B", "C", "D", "F", "G", "H", "I"]):
            self.gramatica_activa["S"] = self.gramatica_completa["S"]
        
        # Incluir A y A' si hay B
        if "B" in self.gramatica_activa and "A" not in self.gramatica_activa:
            self.gramatica_activa["A"] = self.gramatica_completa["A"]
            self.gramatica_activa["A'"] = self.gramatica_completa["A'"]
        
        # Incluir J si hay C
        if "C" in self.gramatica_activa and "J" not in self.gramatica_activa:
            self.gramatica_activa["J"] = self.gramatica_completa["J"]
        
        # Incluir K' si hay K
        if "K" in self.gramatica_activa and "K'" not in self.gramatica_activa:
            self.gramatica_activa["K'"] = self.gramatica_completa["K'"]
        
        # Incluir L y L' si hay D
        if "D" in self.gramatica_activa and "L" not in self.gramatica_activa:
            self.gramatica_activa["L"] = self.gramatica_completa["L"]
            self.gramatica_activa["L'"] = self.gramatica_completa["L'"]
        
        # Incluir OP si hay L'
        if "L'" in self.gramatica_activa and "OP" not in self.gramatica_activa:
            self.gramatica_activa["OP"] = self.gramatica_completa["OP"]

    def calcular_primeros_siguientes(self, reglas_aplicadas):
        """Calcula primeros y siguientes basado en las reglas activas encontradas en el código"""
        # Actualizar gramática activa primero
        self.actualizar_gramatica_activa(reglas_aplicadas)
        
        if not self.gramatica_activa:
            return {}, {}
        
        # Inicializar conjuntos
        self._inicializar_conjuntos()
        
        # Calcular primeros
        self.calcular_primeros()
        
        # Calcular siguientes
        self.calcular_siguientes()
        
        # Aplicar correcciones especiales
        self._aplicar_correcciones_especiales()
        
        # Formatear resultados para coincidir con tus imágenes
        primeros = {k: {v.replace("ε", "€") for v in vs} for k, vs in self.primeros.items()}
        siguientes = {k: {v.replace("SiNo", "SINo") for v in vs} for k, vs in self.siguientes.items()}
        
        return primeros, siguientes

    def _inicializar_conjuntos(self):
        """Inicializa los conjuntos de terminales, no terminales, primeros y siguientes"""
        self.terminales = set()
        self.no_terminales = set(self.gramatica_activa.keys())
        self.primeros = {nt: set() for nt in self.no_terminales}
        self.siguientes = {nt: set() for nt in self.no_terminales}
        self.siguientes["S"].add("$")  # Regla especial para S
        
        # Identificar terminales válidos
        terminales_temporales = set()
        for producciones in self.gramatica_activa.values():
            for produccion in producciones:
                for simbolo in produccion.split():
                    if simbolo not in self.no_terminales and simbolo != "ε":
                        terminales_temporales.add(simbolo)
        
        # Filtrar terminales (eliminar símbolos especiales)
        simbolos_invalidos = {"(", ")", "{", "}", "=", ",", ":", ";", "+", "-", "*", "/", ">", "<", "!"}
        self.terminales = terminales_temporales - simbolos_invalidos

    def calcular_primeros(self):
        """Calcula los conjuntos de primeros para cada no terminal"""
        cambiado = True
        while cambiado:
            cambiado = False
            for no_terminal, producciones in self.gramatica_activa.items():
                for produccion in producciones:
                    simbolos = produccion.split()
                    
                    # Caso ε
                    if simbolos[0] == "ε":
                        if "ε" not in self.primeros[no_terminal]:
                            self.primeros[no_terminal].add("ε")
                            cambiado = True
                        continue
                    
                    # Procesar cada símbolo en la producción
                    todos_tienen_epsilon = True
                    for simbolo in simbolos:
                        if simbolo in self.terminales:
                            # Terminal - agregar a primeros
                            if simbolo not in self.primeros[no_terminal]:
                                self.primeros[no_terminal].add(simbolo)
                                cambiado = True
                            todos_tienen_epsilon = False
                            break
                        else:
                            # No terminal - agregar sus primeros (excepto ε)
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
        """Calcula los conjuntos de siguientes para cada no terminal"""
        cambiado = True
        while cambiado:
            cambiado = False
            for no_terminal, producciones in self.gramatica_activa.items():
                for produccion in producciones:
                    simbolos = produccion.split()
                    for i, simbolo in enumerate(simbolos):
                        if simbolo not in self.no_terminales:
                            continue
                        
                        # Regla 1: Hay símbolos después
                        if i < len(simbolos) - 1:
                            siguiente = simbolos[i+1]

                        if siguiente in self.terminales:
                                # Terminal - agregar a siguientes
                                if siguiente not in self.siguientes[simbolo]:
                                    self.siguientes[simbolo].add(siguiente)
                                    cambiado = True
                        else:
                                # No terminal - agregar primeros (excepto ε)
                                primeros_siguiente = self.primeros.get(siguiente, set()) - {"ε"}
                                nuevos_siguientes = primeros_siguiente - self.siguientes[simbolo]
                                if nuevos_siguientes:
                                    self.siguientes[simbolo].update(nuevos_siguientes)
                                    cambiado = True
                                
                                # Si puede ser ε, agregar siguientes del no terminal
                                if "ε" in self.primeros.get(siguiente, set()):
                                    siguientes_nt = self.siguientes.get(no_terminal, set())
                                    nuevos_siguientes = siguientes_nt - self.siguientes[simbolo]
                                    if nuevos_siguientes:
                                        self.siguientes[simbolo].update(nuevos_siguientes)
                                        cambiado = True
                        
                        # Regla 2: Es el último símbolo o todo lo que sigue puede ser ε
                        if i == len(simbolos) - 1 or all(
                            "ε" in self.primeros.get(s, set()) 
                            for s in simbolos[i+1:] 
                            if s in self.no_terminales
                        ):
                            siguientes_nt = self.siguientes.get(no_terminal, set())
                            nuevos_siguientes = siguientes_nt - self.siguientes[simbolo]
                            if nuevos_siguientes:
                                self.siguientes[simbolo].update(nuevos_siguientes)
                                cambiado = True
        
        # Aplicar correcciones especiales después del cálculo principal
        self._aplicar_correcciones_especiales()

    def _aplicar_correcciones_especiales(self):
        """Aplica correcciones especiales para casos específicos"""
        # Corrección para C → J K
        if "C" in self.gramatica_activa:
            self.siguientes["K"].update(self.siguientes.get("C", set()))
        
        # Corrección para K → var K'
        if "K" in self.gramatica_activa and "K'" in self.gramatica_activa:
            self.siguientes["K'"].update(self.siguientes.get("K", set()))
        
        # Corrección para L → M L'
        if "L" in self.gramatica_activa and "L'" in self.gramatica_activa:
            self.siguientes["M"].update(self.primeros.get("L'", set()) - {"ε"})
            if "ε" in self.primeros.get("L'", set()):
                self.siguientes["M"].update(self.siguientes.get("L", set()))
        
        # Corrección para L' → OP M L'
        if "L'" in self.gramatica_activa and "OP" in self.gramatica_activa:
            self.siguientes["OP"].update(self.primeros.get("M", set()) - {"ε"})