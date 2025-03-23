from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QMessageBox, QTabWidget
)
from analizador import AnalizadorLexico
from gramatica import Gramatica
from primeros_siguientes import PrimerosSiguientes
from tabla_sintactica import TablaSintactica
import re


class AnalizadorCodigo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de Código")
        self.setGeometry(100, 100, 800, 600)

        # Instancias de las clases
        self.analizador = AnalizadorLexico()
        self.gramatica = Gramatica()
        self.primeros_siguientes = PrimerosSiguientes(self.gramatica.obtener_gramatica())
        self.tabla_sintactica = TablaSintactica(self.gramatica.obtener_gramatica())

        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        # Crear un widget de pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Pestaña 1: Editor de código
        self.editor_tab = QWidget()
        self.tabs.addTab(self.editor_tab, "Editor")
        self.inicializar_editor_tab()

        # Pestaña 2: Análisis
        self.analisis_tab = QWidget()
        self.tabs.addTab(self.analisis_tab, "Análisis")
        self.inicializar_analisis_tab()

        # Pestaña 3: Vector
        self.vector_tab = QWidget()
        self.tabs.addTab(self.vector_tab, "Vector")
        self.inicializar_vector_tab()

        # Pestaña 4: Gramática
        self.gramatica_tab = QWidget()
        self.tabs.addTab(self.gramatica_tab, "Gramática")
        self.inicializar_gramatica_tab()

        # Pestaña 5: Tabla de Primeros y Siguientes
        self.primeros_siguientes_tab = QWidget()
        self.tabs.addTab(self.primeros_siguientes_tab, "Primeros y Siguientes")
        self.inicializar_primeros_siguientes_tab()

        # Pestaña 6: Tabla Sintáctica
        self.tabla_sintactica_tab = QWidget()
        self.tabs.addTab(self.tabla_sintactica_tab, "Tabla Sintáctica")
        self.inicializar_tabla_sintactica_tab()

    def inicializar_editor_tab(self):
        layout = QVBoxLayout()

        self.editor = QTextEdit(self)
        self.editor.setPlaceholderText("Escribe tu código aquí...")
        layout.addWidget(self.editor)

        self.boton_compilar = QPushButton("Compilar", self)
        self.boton_compilar.clicked.connect(self.mostrar_mensaje_compilacion)
        layout.addWidget(self.boton_compilar)

        self.boton_analizar = QPushButton("Analizar", self)
        self.boton_analizar.clicked.connect(self.analizar_codigo)
        layout.addWidget(self.boton_analizar)

        self.boton_vector = QPushButton("Vector", self)
        self.boton_vector.clicked.connect(self.generar_vector)
        layout.addWidget(self.boton_vector)

        self.editor_tab.setLayout(layout)

    def inicializar_analisis_tab(self):
        layout = QVBoxLayout()

        self.tabla_analisis = QTableWidget(self)
        self.tabla_analisis.setColumnCount(5)
        self.tabla_analisis.setHorizontalHeaderLabels(["Palabra", "Tipo", "Alias", "Apariciones", "Línea"])
        layout.addWidget(self.tabla_analisis)

        self.analisis_tab.setLayout(layout)

    def inicializar_vector_tab(self):
        layout = QVBoxLayout()

        self.salida_vector = QTextEdit(self)
        self.salida_vector.setPlaceholderText("Aquí aparecerá el código en una línea con alias...")
        self.salida_vector.setReadOnly(True)
        layout.addWidget(self.salida_vector)

        self.vector_tab.setLayout(layout)

    def inicializar_gramatica_tab(self):
        layout = QVBoxLayout()

        self.gramatica_texto = QTextEdit(self)
        self.gramatica_texto.setPlaceholderText("Aquí aparecerá la gramática...")
        self.gramatica_texto.setReadOnly(True)
        layout.addWidget(self.gramatica_texto)

        self.boton_gramatica = QPushButton("Cargar Gramática", self)
        self.boton_gramatica.clicked.connect(self.cargar_gramatica)
        layout.addWidget(self.boton_gramatica)

        self.gramatica_tab.setLayout(layout)

    def inicializar_primeros_siguientes_tab(self):
        layout = QVBoxLayout()

        self.primeros_siguientes_texto = QTextEdit(self)
        self.primeros_siguientes_texto.setPlaceholderText("Aquí aparecerá la tabla de primeros y siguientes...")
        self.primeros_siguientes_texto.setReadOnly(True)
        layout.addWidget(self.primeros_siguientes_texto)

        self.boton_primeros_siguientes = QPushButton("Calcular Primeros y Siguientes", self)
        self.boton_primeros_siguientes.clicked.connect(self.calcular_primeros_siguientes)
        layout.addWidget(self.boton_primeros_siguientes)

        self.primeros_siguientes_tab.setLayout(layout)

    def inicializar_tabla_sintactica_tab(self):
        layout = QVBoxLayout()

        self.tabla_sintactica_texto = QTextEdit(self)
        self.tabla_sintactica_texto.setPlaceholderText("Aquí aparecerá la tabla sintáctica...")
        self.tabla_sintactica_texto.setReadOnly(True)
        layout.addWidget(self.tabla_sintactica_texto)

        self.boton_tabla_sintactica = QPushButton("Generar Tabla Sintáctica", self)
        self.boton_tabla_sintactica.clicked.connect(self.generar_tabla_sintactica)
        layout.addWidget(self.boton_tabla_sintactica)

        self.tabla_sintactica_tab.setLayout(layout)

    def mostrar_mensaje_compilacion(self):
        QMessageBox.information(self, "Compilar", "La compilación del código no es responsabilidad de esta parte del programa.")

    def generar_vector(self):
        try:
            codigo = self.editor.toPlainText()
            lineas = codigo.split("\n")

            # Patrón para capturar espacios, tabs, símbolos y otros tokens
            patron_tokens = re.compile(r'\s|\t|[a-zA-Z_]\w*|\d+\.\d+|\d+|<=|>=|!=|\+\+|--|"[^"]*"|“[^”]*”|[(),:;{}\[\]+\-*/=<>]|.', re.VERBOSE)

            linea_vector = []
            for linea in lineas:
                tokens = patron_tokens.findall(linea)
                for token in tokens:
                    if token == " ":  # Espacio simple
                        linea_vector.append("_")
                    elif token == "\t":  # Tab
                        linea_vector.append("__")
                    else:
                        alias = self.analizador.diccionario_alias.get(token, "DESCONOCIDO")
                        linea_vector.append(alias)

            codigo_vector = " ".join(linea_vector) + " $"
            self.salida_vector.setPlainText(codigo_vector)
            self.tabs.setCurrentIndex(2)  # Cambiar a la pestaña de Vector
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar el vector: {str(e)}")

    def analizar_codigo(self):
        try:
            codigo = self.editor.toPlainText()
            datos_palabras = self.analizador.analizar_codigo(codigo)

            self.tabla_analisis.setRowCount(len(datos_palabras))
            for fila, (palabra, datos) in enumerate(datos_palabras.items()):
                self.tabla_analisis.setItem(fila, 0, QTableWidgetItem(palabra))
                self.tabla_analisis.setItem(fila, 1, QTableWidgetItem(datos["tipo"]))
                self.tabla_analisis.setItem(fila, 2, QTableWidgetItem(datos["alias"]))
                self.tabla_analisis.setItem(fila, 3, QTableWidgetItem(str(datos["apariciones"])))

                info_lineas = [f"línea {num_linea}({contador})" for num_linea, contador in datos["lineas"].items()]
                self.tabla_analisis.setItem(fila, 4, QTableWidgetItem(", ".join(info_lineas)))

            self.tabs.setCurrentIndex(1)  # Cambiar a la pestaña de Análisis
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al analizar el código: {str(e)}")

    def cargar_gramatica(self):
        try:
            # Obtener el código del editor
            codigo = self.editor.toPlainText()

            # Obtener las reglas aplicadas
            reglas_aplicadas = self.gramatica.obtener_reglas_aplicadas(codigo)

            # Mostrar las reglas en la interfaz
            if reglas_aplicadas:
                gramatica_texto = "\n".join(reglas_aplicadas)
                self.gramatica_texto.setPlainText(gramatica_texto)
                QMessageBox.information(self, "Gramática", "Reglas aplicadas generadas exitosamente.")
            else:
                QMessageBox.warning(self, "Gramática", "No se encontraron reglas aplicables para el código.")

            self.tabs.setCurrentIndex(3)  # Cambiar a la pestaña de Gramática
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar la gramática: {str(e)}")

    def calcular_primeros_siguientes(self):
        try:
            primeros, siguientes = self.primeros_siguientes.calcular_primeros_siguientes()
            resultado = "Primeros:\n"
            for no_terminal, primeros_set in primeros.items():
                resultado += f"{no_terminal}: {', '.join(primeros_set)}\n"
            resultado += "\nSiguientes:\n"
            for no_terminal, siguientes_set in siguientes.items():
                resultado += f"{no_terminal}: {', '.join(siguientes_set)}\n"
            self.primeros_siguientes_texto.setPlainText(resultado)
            QMessageBox.information(self, "Primeros y Siguientes", "Primeros y siguientes calculados exitosamente.")
            self.tabs.setCurrentIndex(4)  # Cambiar a la pestaña de Primeros y Siguientes
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al calcular primeros y siguientes: {str(e)}")

    def generar_tabla_sintactica(self):
        try:
            resultado = self.tabla_sintactica.generar_tabla_sintactica()
            self.tabla_sintactica_texto.setPlainText(resultado)
            QMessageBox.information(self, "Tabla Sintáctica", "Tabla sintáctica generada exitosamente.")
            self.tabs.setCurrentIndex(5)  # Cambiar a la pestaña de Tabla Sintáctica
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar la tabla sintáctica: {str(e)}")