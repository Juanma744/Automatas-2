from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QMessageBox, QTabWidget, QHeaderView
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
        self.primeros_siguientes = PrimerosSiguientes()
        self.tabla_sintactica = TablaSintactica()

        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        # Crear un widget de pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Inicializar todas las pestañas
        self.inicializar_editor_tab()
        self.inicializar_analisis_tab()
        self.inicializar_vector_tab()
        self.inicializar_gramatica_tab()
        self.inicializar_primeros_siguientes_tab()
        self.inicializar_tabla_sintactica_tab()

    # ------------------------- Métodos de inicialización de pestañas -------------------------
    def inicializar_editor_tab(self):
        layout = QVBoxLayout()
        self.editor = QTextEdit(self)
        self.editor.setPlaceholderText("Escribe tu código aquí...")
        layout.addWidget(self.editor)

        botones_layout = QVBoxLayout()
        self.boton_compilar = QPushButton("Compilar", self)
        self.boton_analizar = QPushButton("Analizar", self)
        self.boton_vector = QPushButton("Vector", self)

        self.boton_compilar.clicked.connect(self.mostrar_mensaje_compilacion)
        self.boton_analizar.clicked.connect(self.analizar_codigo)
        self.boton_vector.clicked.connect(self.generar_vector)

        botones_layout.addWidget(self.boton_compilar)
        botones_layout.addWidget(self.boton_analizar)
        botones_layout.addWidget(self.boton_vector)

        layout.addLayout(botones_layout)
        self.editor_tab = QWidget()
        self.editor_tab.setLayout(layout)
        self.tabs.addTab(self.editor_tab, "Editor")

    def inicializar_analisis_tab(self):
        layout = QVBoxLayout()
        self.tabla_analisis = QTableWidget(self)
        self.tabla_analisis.setColumnCount(5)
        self.tabla_analisis.setHorizontalHeaderLabels(["Palabra", "Tipo", "Alias", "Apariciones", "Línea"])
        layout.addWidget(self.tabla_analisis)

        self.analisis_tab = QWidget()
        self.analisis_tab.setLayout(layout)
        self.tabs.addTab(self.analisis_tab, "Análisis")

    def inicializar_vector_tab(self):
        layout = QVBoxLayout()
        self.salida_vector = QTextEdit(self)
        self.salida_vector.setPlaceholderText("Aquí aparecerá el código en una línea con alias...")
        self.salida_vector.setReadOnly(True)
        layout.addWidget(self.salida_vector)

        self.vector_tab = QWidget()
        self.vector_tab.setLayout(layout)
        self.tabs.addTab(self.vector_tab, "Vector")

    def inicializar_gramatica_tab(self):
        layout = QVBoxLayout()
        self.gramatica_texto = QTextEdit(self)
        self.gramatica_texto.setPlaceholderText("Aquí aparecerá la gramática...")
        self.gramatica_texto.setReadOnly(True)
        
        self.boton_gramatica = QPushButton("Cargar Gramática", self)
        self.boton_gramatica.clicked.connect(self.cargar_gramatica)
        
        layout.addWidget(self.gramatica_texto)
        layout.addWidget(self.boton_gramatica)
        
        self.gramatica_tab = QWidget()
        self.gramatica_tab.setLayout(layout)
        self.tabs.addTab(self.gramatica_tab, "Gramática")

    def inicializar_tabla_sintactica_tab(self):
        layout = QVBoxLayout()
        self.tabla_sintactica_widget = QTableWidget()
        layout.addWidget(self.tabla_sintactica_widget)
        
        self.boton_tabla_sintactica = QPushButton("Generar Tabla Sintáctica", self)
        self.boton_tabla_sintactica.clicked.connect(self.generar_tabla_sintactica)
        layout.addWidget(self.boton_tabla_sintactica)
        
        self.tabla_sintactica_tab = QWidget()
        self.tabla_sintactica_tab.setLayout(layout)
        self.tabs.addTab(self.tabla_sintactica_tab, "Tabla Sintáctica")

    def inicializar_primeros_siguientes_tab(self):
        layout = QVBoxLayout()
        
        self.tabla_primeros_siguientes = QTableWidget(self)
        self.tabla_primeros_siguientes.setColumnCount(3)
        self.tabla_primeros_siguientes.setHorizontalHeaderLabels(["No Terminal", "Primeros", "Siguientes"])
        self.tabla_primeros_siguientes.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.tabla_primeros_siguientes)
        
        self.boton_primeros_siguientes = QPushButton("Calcular Primeros y Siguientes", self)
        self.boton_primeros_siguientes.clicked.connect(self.calcular_primeros_siguientes)
        layout.addWidget(self.boton_primeros_siguientes)
        
        self.primeros_siguientes_tab = QWidget()
        self.primeros_siguientes_tab.setLayout(layout)
        self.tabs.addTab(self.primeros_siguientes_tab, "Primeros y Siguientes")

    # ------------------------- Funcionalidades principales -------------------------
    def mostrar_mensaje_compilacion(self):
        QMessageBox.information(self, "Compilar", "La compilación del código no es responsabilidad de esta parte del programa.")

    def generar_vector(self):
        try:
            codigo = self.editor.toPlainText()
            lineas = codigo.split("\n")
            patron_tokens = re.compile(r'\s|\t|[a-zA-Z_]\w*|\d+\.\d+|\d+|<=|>=|!=|\+\+|--|"[^"]*"|“[^”]*”|[(),:;{}\[\]+\-*/=<>]|.', re.VERBOSE)
            
            linea_vector = []
            for linea in lineas:
                tokens = patron_tokens.findall(linea)
                for token in tokens:
                    if token == " ": linea_vector.append("_")
                    elif token == "\t": linea_vector.append("___")
                    else: linea_vector.append(self.analizador.diccionario_alias.get(token, "DESCONOCIDO"))
            
            self.salida_vector.setPlainText(" ".join(linea_vector) + " $")
            self.tabs.setCurrentIndex(2)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar vector: {str(e)}")

    def analizar_codigo(self):
        try:
            codigo = self.editor.toPlainText()
            datos_palabras = self.analizador.analizar_codigo(codigo)
            
            self.tabla_analisis.setRowCount(len(datos_palabras))
            for fila, (palabra, datos) in enumerate(datos_palabras.items()):
                self.tabla_analisis.setItem(fila, 0, QTableWidgetItem("___" if palabra == "\t" else palabra))
                self.tabla_analisis.setItem(fila, 1, QTableWidgetItem(datos["tipo"]))
                self.tabla_analisis.setItem(fila, 2, QTableWidgetItem(datos["alias"]))
                self.tabla_analisis.setItem(fila, 3, QTableWidgetItem(str(datos["apariciones"])))
                
                lineas_str = ", ".join([f"línea {k}({v})" for k, v in datos["lineas"].items()])
                self.tabla_analisis.setItem(fila, 4, QTableWidgetItem(lineas_str))
            
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al analizar código: {str(e)}")

    def cargar_gramatica(self):
        try:
            codigo = self.editor.toPlainText()
            # LLAMAR AL NUEVO MÉTODO que devuelve la estructura
            gramatica_activa = self.gramatica.obtener_gramatica_activa(codigo)

            if not gramatica_activa:
                self.gramatica_texto.setPlainText("No se activaron reglas de la gramática para el código ingresado.")
                QMessageBox.warning(self, "Gramática", "No se encontraron reglas aplicables para este código.")
                return # Salir si no hay gramática activa

            # Formatear la gramática activa para mostrarla
            texto_gramatica = "Gramática Activa para el Código:\n\n"
            # Ordenar NTs para consistencia (opcional)
            nts_ordenados = sorted(gramatica_activa.keys())

            for nt in nts_ordenados:
                producciones = gramatica_activa[nt]
                # Formatear cada producción: ["Start", "A", "End"] -> "Start A End"
                prods_formateadas = []
                for prod_lista in producciones:
                    # Manejar el caso epsilon: ["ε"] -> "ε"
                    if prod_lista == ["ε"]:
                        prods_formateadas.append("ε")
                    else:
                        prods_formateadas.append(" ".join(prod_lista))

                # Unir las producciones con " | "
                lado_derecho = " | ".join(prods_formateadas)
                texto_gramatica += f"{nt} -> {lado_derecho}\n"

            self.gramatica_texto.setPlainText(texto_gramatica)
            QMessageBox.information(self, "Gramática", "Gramática activa generada exitosamente basada en el código.")
            self.tabs.setCurrentIndex(3) # Asegúrate que 3 es el índice correcto

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar gramática activa: {str(e)}")
            import traceback
            traceback.print_exc()

# --- Fin del método ---

    # En Interfaz.py
    def calcular_primeros_siguientes(self):
        try:
            codigo = self.editor.toPlainText()

            # 1. Obtener la gramática activa basada en el código
            gramatica_activa = self.gramatica.obtener_gramatica_activa(codigo)

            if not gramatica_activa:
                 QMessageBox.warning(self, "Advertencia", "No se detectaron suficientes elementos en el código para activar reglas de la gramática.")
                 # Limpiar la tabla si se desea
                 self.tabla_primeros_siguientes.setRowCount(0)
                 return

            # 2. Calcular Primeros y Siguientes para esa gramática activa
            self.primeros_siguientes.calcular_para_gramatica(gramatica_activa)

            # 3. Obtener los conjuntos formateados
            primeros, siguientes = self.primeros_siguientes.obtener_primeros_siguientes_formateados()

            # 4. Mostrar en la tabla (igual que antes)
            self.tabla_primeros_siguientes.setRowCount(0) # Limpiar tabla
            # Asegúrate que PrimerosSiguientes tiene este atributo o ajústalo
            orden_interfaz = self.primeros_siguientes.no_terminales_interfaz_orden

            for row, nt in enumerate(orden_interfaz):
                self.tabla_primeros_siguientes.insertRow(row)
                item_nt = QTableWidgetItem(nt)
                # Usar .get(nt, "-") para manejar NTs no activos
                item_pr = QTableWidgetItem(primeros.get(nt, "-"))
                item_sg = QTableWidgetItem(siguientes.get(nt, "-"))

                # Opcional: Alinear texto (necesitas importar Qt: from PyQt6.QtCore import Qt)
                # alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                # item_nt.setTextAlignment(alignment)
                # item_pr.setTextAlignment(alignment)
                # item_sg.setTextAlignment(alignment)

                self.tabla_primeros_siguientes.setItem(row, 0, item_nt)
                self.tabla_primeros_siguientes.setItem(row, 1, item_pr)
                self.tabla_primeros_siguientes.setItem(row, 2, item_sg)

            # Ajustar columnas (necesitas importar QHeaderView: from PyQt6.QtWidgets import QHeaderView)
            self.tabla_primeros_siguientes.resizeColumnsToContents()
            header = self.tabla_primeros_siguientes.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

            QMessageBox.information(self, "Éxito", "Tabla de Primeros y Siguientes generada basada en el código actual!")
            # Asegúrate que el índice 4 corresponde a la pestaña de Primeros/Siguientes
            self.tabs.setCurrentIndex(4)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular Primeros/Siguientes: {str(e)}")
            import traceback
            traceback.print_exc() # Ayuda a depurar viendo el error completo en consola

# --- FIN DEL MÉTODO ---
            
    def generar_tabla_sintactica(self):
        try:
            # Obtener conjuntos necesarios
            primeros, _ = self.primeros_siguientes.primeros, self.primeros_siguientes.siguientes
            
            # Generar y mostrar tabla
            self.tabla_sintactica.construir_tabla(primeros)
            self.tabla_sintactica.mostrar_en_qtablewidget(self.tabla_sintactica_widget)
            
            QMessageBox.information(self, "Tabla Sintáctica", "Tabla generada exitosamente!")
            self.tabs.setCurrentIndex(5)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar tabla: {str(e)}")