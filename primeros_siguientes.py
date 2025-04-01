# --- START OF FILE primeros_siguientes.py ---

from collections import defaultdict
import re # Import re (aunque no se usa directamente aquí ahora)

class PrimerosSiguientes:
    def __init__(self):
        # Gramática completa de REFERENCIA (no se usa directamente para cálculo ahora)
        # Se usa para el orden de la interfaz
        self.gramatica_completa_ref = {
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
        self.no_terminales_interfaz_orden = [
            "S", "A", "A'", "B", "C", "D", "F", "G", "H", "I",
            "J", "K", "K'", "L", "L'", "M", "N", "N'", "OP", "Q", "R"
        ]

        # Inicialización de conjuntos (se llenarán al calcular)
        self.primeros = defaultdict(set)
        self.siguientes = defaultdict(set)
        self.gramatica_usada = {} # Para guardar la gramática con la que se calcularon
        self.no_terminales = set()
        self.terminales = set()

    def calcular_para_gramatica(self, gramatica_activa):
        """Calcula Primeros y Siguientes para la gramática activa dada."""
        self.gramatica_usada = gramatica_activa
        self._identificar_simbolos() # Identificar NT y T de la gramática activa
        self._inicializar_conjuntos()
        self._calcular_primeros()
        self._calcular_siguientes()
        # No devuelve nada, modifica self.primeros y self.siguientes

    def _identificar_simbolos(self):
        """Identifica NT y T a partir de self.gramatica_usada."""
        self.no_terminales = set(self.gramatica_usada.keys())
        self.terminales = set()
        for nt in self.gramatica_usada:
            for produccion in self.gramatica_usada[nt]:
                for simbolo in produccion:
                    if simbolo not in self.no_terminales and simbolo != "ε":
                        self.terminales.add(simbolo)

# --- En primeros_siguientes.py, dentro de class PrimerosSiguientes ---
    def _inicializar_conjuntos(self):
        """Inicializa/limpia los conjuntos antes del cálculo."""
        self.primeros.clear()
        self.siguientes.clear()
        print("Conjuntos Primeros/Siguientes limpiados.") # DEBUG

        # Inicializar siguientes aquí porque _calcular_siguientes lo necesita
        # IMPORTANTE: Iterar sobre self.no_terminales (los activos), no sobre la lista completa fija
        for nt in self.no_terminales:
            self.siguientes[nt] = set() # Inicializa vacío para todos los NT activos

        start_symbol = "S" # Asumiendo S es el inicial
        if start_symbol in self.no_terminales: # Solo si S está en la gramática activa
             print(f"Añadiendo '$' a Siguientes({start_symbol})") # DEBUG
             self.siguientes[start_symbol].add("$")
        else:
             print(f"Símbolo inicial '{start_symbol}' no está en los NT activos.") # DEBUG


    def _calcular_primeros(self):
        # Algoritmo de Primeros (igual que antes, pero usa self.gramatica_usada)
        # Inicializar FIRST(T) = {T} para terminales T
        for terminal in self.terminales:
            self.primeros[terminal] = {terminal}
        # Inicializar FIRST(NT) = {} para no terminales NT
        for nt in self.no_terminales:
            self.primeros[nt] = set()

        cambiado = True
        while cambiado:
            cambiado = False
            # Usar self.gramatica_usada en lugar de self.gramatica
            for nt, producciones in self.gramatica_usada.items():
                for produccion in producciones:
                    # Caso: X -> ε
                    if not produccion or produccion == ["ε"]:
                        if "ε" not in self.primeros[nt]:
                            self.primeros[nt].add("ε")
                            cambiado = True
                        continue

                    # Caso: X -> Y1 Y2 ... Yk
                    produccion_contiene_epsilon = True # Asumir que puede derivar epsilon
                    for simbolo in produccion:
                        # Si el símbolo no está en primeros (podría ser terminal no visto antes)
                        if simbolo not in self.primeros:
                             if simbolo in self.terminales:
                                 self.primeros[simbolo] = {simbolo}
                             else: # Error: NT no definido en la gramática activa? Omitir?
                                 # print(f"Advertencia: Símbolo '{simbolo}' en producción de '{nt}' no encontrado en primeros.")
                                 produccion_contiene_epsilon = False # No podemos asumir epsilon
                                 break # No podemos continuar con esta producción

                        primeros_simbolo = self.primeros[simbolo]
                        nuevos_primeros = primeros_simbolo - {"ε"}

                        antes = len(self.primeros[nt])
                        self.primeros[nt].update(nuevos_primeros)
                        if len(self.primeros[nt]) > antes:
                            cambiado = True

                        if "ε" not in primeros_simbolo:
                            # Si Y_i no deriva ε, detenemos para esta producción
                            produccion_contiene_epsilon = False
                            break

                    # Si todos los símbolos de la producción derivaron epsilon
                    if produccion_contiene_epsilon:
                         if "ε" not in self.primeros[nt]:
                            self.primeros[nt].add("ε")
                            cambiado = True


    def _calcular_siguientes(self):
        # Algoritmo de Siguientes (igual que antes, pero usa self.gramatica_usada)
        # La inicialización ya se hizo en _inicializar_conjuntos

        cambiado = True
        while cambiado:
            cambiado = False
            # Usar self.gramatica_usada
            for nt_origen, producciones in self.gramatica_usada.items():
                for produccion in producciones:
                    if produccion == ["ε"]:
                        continue

                    # Para manejar FOLLOW(B) en A -> αB
                    trailer = set(self.siguientes[nt_origen])

                    # Iterar de derecha a izquierda
                    for i in range(len(produccion) - 1, -1, -1):
                        simbolo_actual = produccion[i]

                        if simbolo_actual in self.no_terminales:
                             # Calcular FIRST(beta) donde beta es produccion[i+1:]
                            primeros_beta = set()
                            epsilon_en_beta = True
                            for j in range(i + 1, len(produccion)):
                                simbolo_beta = produccion[j]
                                primeros_simbolo_beta = self.primeros.get(simbolo_beta, set())
                                primeros_beta.update(primeros_simbolo_beta - {"ε"})
                                if "ε" not in primeros_simbolo_beta:
                                    epsilon_en_beta = False
                                    break
                            
                            # Regla 2: A -> αBβ, añadir FIRST(β) - {ε} a FOLLOW(B)
                            antes = len(self.siguientes[simbolo_actual])
                            self.siguientes[simbolo_actual].update(primeros_beta)
                            if len(self.siguientes[simbolo_actual]) > antes:
                                cambiado = True
                                
                            # Regla 3: A -> αBβ donde ε está en FIRST(β), añadir FOLLOW(A) a FOLLOW(B)
                            # O Regla 3: A -> αB, añadir FOLLOW(A) a FOLLOW(B)
                            if epsilon_en_beta: # Si beta no existía (i es el último) o FIRST(beta) contiene ε
                                antes = len(self.siguientes[simbolo_actual])
                                self.siguientes[simbolo_actual].update(self.siguientes[nt_origen])
                                if len(self.siguientes[simbolo_actual]) > antes:
                                    cambiado = True


    def obtener_primeros_siguientes_formateados(self):
        """Devuelve los conjuntos formateados para la interfaz."""
        # Formateo (igual que antes, pero usa los conjuntos calculados por calcular_para_gramatica)
        # Orden de terminales para la salida (basado en la imagen y sentido común)
        # Usar los terminales encontrados en la gramática activa + $
        terminales_ordenados = sorted(list(self.terminales)) + ['$']
        custom_order = {t: i for i, t in enumerate([
            'Start', 'End', 'Entero', 'Doble', 'Cadena', 'var', 'num',
            '(', ')', '{', '}', '+', '-', '*', '/', '=',
            '>', '<', '<=', '>=', '!=', '!', '++',
            'Si', 'SiNo', 'Mientras', 'Entrada', 'Salida',
            ',', ';', ':', '$', 'ε'
        ])}
        def sort_key(x):
             return (custom_order.get(x, float('inf')), x)

        primeros_formateados = {}
        siguientes_formateados = {}

        # Mostrar siempre todos los NTs del orden de interfaz, aunque no estén activos
        for nt in self.no_terminales_interfaz_orden:
            if nt in self.no_terminales: # Si el NT estuvo en la gramática activa
                # Formatear Primeros
                p_list = sorted(list(self.primeros.get(nt, set())), key=sort_key)
                p_list_str = [item.replace("SiNo", "SINo_").replace("ε", "€") for item in p_list]
                primeros_formateados[nt] = ", ".join(p_list_str)

                # Formatear Siguientes
                s_list = sorted(list(self.siguientes.get(nt, set())), key=sort_key)
                s_list_str = [item.replace("SiNo", "SINo_") for item in s_list]
                siguientes_formateados[nt] = ", ".join(s_list_str)
            else: # Si el NT no se activó con el código actual
                primeros_formateados[nt] = "-" # O "" o "No aplica"
                siguientes_formateados[nt] = "-"

        return primeros_formateados, siguientes_formateados

# --- END OF FILE primeros_siguientes.py ---