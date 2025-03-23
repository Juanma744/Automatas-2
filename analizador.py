import re
from PyQt6.QtWidgets import QMessageBox  # Importación necesaria para QMessageBox

class AnalizadorLexico:
    def __init__(self):
        # Definimos las palabras y símbolos del lenguaje
        self.palabras_reservadas = {"Start", "Entero", "Salida", "Entrada", "Mientras", "Si", "SiNo", "FinSi", "FinMientras", "End"}
        self.signos_puntuacion = {",", ":", ";"}
        self.signos_aritmeticos = {"+", "-", "*", "/", "="}
        self.signos_agrupacion = {"(", ")", "[", "]", "{", "}", "“", "”", "\""}
        self.operadores = {">", "<", ">=", "<=", "!=", "++", "--"}

        # Contadores para alias
        self.contador_variables = 1
        self.contador_numeros = 1
        self.contador_dobles = 1
        self.contador_mensajes = 1
        self.contador_desconocidos = 1

        # Diccionario para almacenar los alias
        self.diccionario_alias = {}

    def analizar_codigo(self, codigo):
        lineas = codigo.split("\n")
        datos_palabras = {}
        
        # Patrón para capturar espacios, tabs, símbolos y otros tokens
        patron_tokens = re.compile(r'\s|\t|[a-zA-Z_]\w*|\d+\.\d+|\d+|<=|>=|!=|\+\+|--|"[^"]*"|“[^”]*”|[(),:;{}\[\]+\-*/=<>]|.', re.VERBOSE)

        for numero_linea, linea in enumerate(lineas, start=1):
            tokens = patron_tokens.findall(linea)
            for token in tokens:
                if token == " ":  # Espacio simple
                    tipo_token = "ESPACIO"
                    alias = "_"
                elif token == "\t":  # Tab
                    tipo_token = "TAB"
                    alias = "___"  # Cambiado de "__" a "___"
                elif token == '"':  # Comilla doble
                    tipo_token = "SAG"
                    alias = '"'
                elif re.match(r'^".*"$', token) or re.match(r'^“.+”$', token):  # Cadena entre comillas
                    tipo_token = "CADENA"
                    alias = f"CADENA{self.contador_mensajes}"
                    self.contador_mensajes += 1
                else:
                    tipo_token = self.obtener_tipo_token(token)
                    alias = self.generar_alias(token, tipo_token)

                if token not in datos_palabras:
                    datos_palabras[token] = {
                        "tipo": tipo_token,
                        "alias": alias,
                        "apariciones": 0,
                        "lineas": {}
                    }
                    self.diccionario_alias[token] = alias

                if numero_linea not in datos_palabras[token]["lineas"]:
                    datos_palabras[token]["lineas"][numero_linea] = 1
                else:
                    datos_palabras[token]["lineas"][numero_linea] += 1

                datos_palabras[token]["apariciones"] += 1

        return datos_palabras

    def calcular_primeros_siguientes(self):
        try:
            primeros, siguientes = self.primeros_siguientes.calcular_primeros_siguientes()
            
            # Crear tabla con formato alineado
            resultado = "| NO TERMINALES  | PRIMEROS                                  | SIGUIENTES                                |\n"
            resultado += "|----------------|-------------------------------------------|-------------------------------------------|\n"
            
            # Ordenar no terminales para consistencia
            no_terminales = [
                "S", "A", "A'", "B", "C", "D", "F", "G", 
                "H", "I", "J", "K", "K'", "L", "L'", "M", 
                "N", "N'", "OP", "Q", "R"
            ]

            for nt in no_terminales:
                # Formatear primeros
                pr = ", ".join(sorted(primeros.get(nt, set())))
                pr = pr.replace("ε", "€")  # Mantener símbolo de la imagen
                
                # Formatear siguientes
                sg = ", ".join(sorted(siguientes.get(nt, set())))
                sg = sg.replace("SiNo", "SINo_")  # Mantener formato de la imagen
                
                # Añadir fila
                resultado += f"| {nt.ljust(14)} | {pr.ljust(41)} | {sg.ljust(41)} |\n"

            self.primeros_siguientes_texto.setPlainText(resultado)
            QMessageBox.information(self, "Primeros y Siguientes", "Tabla generada exitosamente!")
            self.tabs.setCurrentIndex(4)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular: {str(e)}")

    def obtener_tipo_token(self, token):
        if token in self.palabras_reservadas:
            return "PR"
        elif re.match(r'^".*"$', token) or re.match(r'^“.+”$', token):  # Cadena entre comillas
            return "CADENA"
        elif token in self.signos_puntuacion:
            return "SP"
        elif token in self.signos_aritmeticos:
            return "SA"
        elif token in self.signos_agrupacion:
            return "SAG"
        elif token in self.operadores:
            return "OP"
        elif re.match(r"^\d+\.\d+$", token):
            return "DOBLE"
        elif re.match(r"^\d+$", token):
            return "NUM"
        elif re.match(r"^[a-zA-Z_]\w*$", token):
            return "VAR"
        else:
            return "DESCONOCIDO"

    def generar_alias(self, token, tipo_token):
        if tipo_token == "CADENA":
            alias = f"CADENA{self.contador_mensajes}"
            self.contador_mensajes += 1
            return alias
        elif tipo_token == "PR":
            return token
        elif tipo_token in {"SP", "SA", "SAG", "OP"}:
            return token
        elif tipo_token == "DOBLE":
            alias = f"d{self.contador_dobles}"
            self.contador_dobles += 1
            return alias
        elif tipo_token == "NUM":
            alias = f"NUM{self.contador_numeros}"
            self.contador_numeros += 1
            return alias
        elif tipo_token == "VAR":
            alias = f"VAR{self.contador_variables}"
            self.contador_variables += 1
            return alias
        elif tipo_token == "DESCONOCIDO":
            alias = f"DESCONOCIDO{self.contador_desconocidos}"
            self.contador_desconocidos += 1
            return alias
        else:
            return "-"