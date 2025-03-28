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
        
        # Cambiar QTextEdit por QTableWidget
        self.tabla_sintactica_widget = QTableWidget()
        layout.addWidget(self.tabla_sintactica_widget)
        
        # Mantener el botón existente
        self.boton_tabla_sintactica = QPushButton("Generar Tabla Sintáctica", self)
        self.boton_tabla_sintactica.clicked.connect(self.generar_tabla_sintactica)
        layout.addWidget(self.boton_tabla_sintactica)
        
        self.tabla_sintactica_tab = QWidget()
        self.tabla_sintactica_tab.setLayout(layout)
        self.tabs.addTab(self.tabla_sintactica_tab, "Tabla Sintáctica")
    def inicializar_primeros_siguientes_tab(self):
        layout = QVBoxLayout()
        
        # Crear tabla con 3 columnas
        self.tabla_primeros_siguientes = QTableWidget(self)
        self.tabla_primeros_siguientes.setColumnCount(3)
        self.tabla_primeros_siguientes.setHorizontalHeaderLabels(["No Terminal", "Primeros", "Siguientes"])
        self.tabla_primeros_siguientes.horizontalHeader().setStretchLastSection(True)  # Ajustar ancho automático
        
        layout.addWidget(self.tabla_primeros_siguientes)
        
        # Botón para calcular
        self.boton_primeros_siguientes = QPushButton("Calcular Primeros y Siguientes", self)
        self.boton_primeros_siguientes.clicked.connect(self.calcular_primeros_siguientes)
        layout.addWidget(self.boton_primeros_siguientes)
        
        self.primeros_siguientes_tab = QWidget()
        self.primeros_siguientes_tab.setLayout(layout)
        self.tabs.addTab(self.primeros_siguientes_tab, "Primeros y Siguientes")
    def generar_tabla_sintactica(self):
        try:
            # Obtener referencia al QTableWidget de la pestaña
            tabla_qt = self.tabs.widget(5).findChild(QTableWidget)
            
            # Mostrar en la tabla gráfica
            self.tabla_sintactica.mostrar_en_qtablewidget(tabla_qt)
            
            QMessageBox.information(self, "Tabla Sintáctica", "Tabla generada exitosamente!")
            self.tabs.setCurrentIndex(5)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
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
                # Corregir paréntesis faltante en la línea siguiente
                self.tabla_analisis.setItem(fila, 0, QTableWidgetItem("___" if palabra == "\t" else palabra))
                self.tabla_analisis.setItem(fila, 1, QTableWidgetItem(datos["tipo"]))
                self.tabla_analisis.setItem(fila, 2, QTableWidgetItem(datos["alias"]))
                self.tabla_analisis.setItem(fila, 3, QTableWidgetItem(str(datos["apariciones"])))  # <-- Paréntesis cerrado
                
                lineas_str = ", ".join([f"línea {k}({v})" for k, v in datos["lineas"].items()])
                self.tabla_analisis.setItem(fila, 4, QTableWidgetItem(lineas_str))
            
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al analizar código: {str(e)}")

    def cargar_gramatica(self):
        try:
            codigo = self.editor.toPlainText()
            reglas_aplicadas = self.gramatica.obtener_reglas_aplicadas(codigo)
            
            if reglas_aplicadas:
                self.gramatica_texto.setPlainText("\n".join(reglas_aplicadas))
                QMessageBox.information(self, "Gramática", "Reglas aplicadas generadas exitosamente.")
            else:
                QMessageBox.warning(self, "Gramática", "No se encontraron reglas aplicables.")
            
            self.tabs.setCurrentIndex(3)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar gramática: {str(e)}")

    def calcular_primeros_siguientes(self):
        try:
            # Obtener las reglas aplicadas del código
            codigo = self.editor.toPlainText()
            reglas_aplicadas = self.gramatica.obtener_reglas_aplicadas(codigo)
            
            # Calcular primeros y siguientes basados en las reglas activas
            primeros, siguientes = self.primeros_siguientes.calcular_primeros_siguientes(reglas_aplicadas)
            
            # Limpiar tabla existente
            self.tabla_primeros_siguientes.setRowCount(0)
            
            # Orden preferido para mostrar los no terminales
            orden_no_terminales = [
                "S", "A", "A'", "B", "C", "D", "F", "G", 
                "H", "I", "J", "K", "K'", "L", "L'", "M", 
                "N", "N'", "OP", "Q", "R"
            ]
            
            # Llenar la tabla solo con los no terminales activos
            no_terminales_activos = set(self.primeros_siguientes.gramatica_activa.keys())
            
            for nt in orden_no_terminales:
                if nt not in no_terminales_activos:
                    continue
                    
                row_position = self.tabla_primeros_siguientes.rowCount()
                self.tabla_primeros_siguientes.insertRow(row_position)
                
                # Obtener y formatear datos
                pr = ", ".join(sorted(primeros.get(nt, set())))
                sg = ", ".join(sorted(siguientes.get(nt, set())))
                
                # Añadir celdas
                self.tabla_primeros_siguientes.setItem(row_position, 0, QTableWidgetItem(nt))
                self.tabla_primeros_siguientes.setItem(row_position, 1, QTableWidgetItem(pr))
                self.tabla_primeros_siguientes.setItem(row_position, 2, QTableWidgetItem(sg))
            
            # Ajustar el ancho de las columnas
            self.tabla_primeros_siguientes.resizeColumnsToContents()
            QMessageBox.information(self, "Éxito", "Tabla de Primeros y Siguientes generada correctamente!")
            self.tabs.setCurrentIndex(4)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular Primeros y Siguientes: {str(e)}")
    def generar_tabla_sintactica(self):
        try:
            # Usar la referencia directa al widget
            self.tabla_sintactica.mostrar_en_qtablewidget(self.tabla_sintactica_widget)
            QMessageBox.information(self, "Tabla Sintáctica", "Tabla generada exitosamente!")
            self.tabs.setCurrentIndex(5)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar tabla: {str(e)}")