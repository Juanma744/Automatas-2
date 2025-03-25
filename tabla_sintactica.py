from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


class TablaSintactica:
    def __init__(self, gramatica=None):
        # ... (resto del constructor y métodos anteriores)
        self.terminales = [
            "INICIO", "FIN", "Entero", "Doble", "Cadena", "num", "Var", "=",
            "+", "-", "Si", "(", ")", "{", "}", "SiNo", "Mientras", "Salida",
            "Entrada", ">", "<", "!", ","
        ]
        self.no_terminales = [
            "S", "A", "A'", "B", "C", "K", "K'", "J", "D", "L", "L'", "M",
            "OP", "H", "Q", "I", "G", "F", "N", "N'", "R"
        ]
        self.tabla = self._crear_tabla_numerica()  # Método que realmente genera la tabla
         # Si este es el método correcto

    def _crear_tabla_numerica(self):
        tabla = {}
        for nt in self.no_terminales:
            tabla[nt] = [""] * len(self.terminales)  # Inicializa cada NT con una lista vacía
        return tabla


    def generar_tabla_sintactica(self):
        try:
            # Obtener el código ingresado en el editor
            codigo = self.editor.toPlainText()

            # Obtener gramática basada en el código escrito
            gramatica_generada = self.gramatica.obtener_gramatica_desde_codigo(codigo)

            if not gramatica_generada:
                QMessageBox.warning(self, "Tabla Sintáctica", "No se pudo generar la tabla, revisa la gramática.")
                return

            # Generar tabla sintáctica basada en la gramática obtenida
            self.tabla_sintactica = TablaSintactica(gramatica_generada)
            tabla, encabezados = self.tabla_sintactica.generar_tabla_sintactica()

            # Configurar la tabla en la interfaz
            self.tabla_sintactica_widget.setRowCount(len(tabla))
            self.tabla_sintactica_widget.setColumnCount(len(encabezados))
            self.tabla_sintactica_widget.setHorizontalHeaderLabels(encabezados)

            # Llenar la tabla con los valores generados
            for fila_idx, (no_terminal, valores) in enumerate(tabla.items()):
                self.tabla_sintactica_widget.setItem(fila_idx, 0, QTableWidgetItem(no_terminal))  # No Terminal
                for col_idx, valor in enumerate(valores, start=1):
                    self.tabla_sintactica_widget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

            # Ajustar tamaño de las columnas para mejor presentación
            self.tabla_sintactica_widget.resizeColumnsToContents()
            self.tabla_sintactica_widget.resizeRowsToContents()

            QMessageBox.information(self, "Tabla Sintáctica", "Tabla generada correctamente basada en el código ingresado.")
            self.tabs.setCurrentIndex(5)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la tabla sintáctica: {str(e)}")


    def mostrar_en_qtablewidget(self, tabla_qt: QTableWidget):
        """
        Recibe un QTableWidget y lo llena con los datos de la tabla sintáctica.
        Se realizan ajustes de estética: se activa la cuadrícula, se usan estilos para bordes y se redimensionan celdas.
        """
        # Configurar encabezados
        columnas = len(self.terminales) + 1  # +1 para la columna de No Terminal
        tabla_qt.setColumnCount(columnas)
        tabla_qt.setHorizontalHeaderLabels(["No Terminal"] + self.terminales)
        
        # Activar la cuadrícula (grid lines)
        tabla_qt.setShowGrid(True)
        
        # Opcional: aplicar un stylesheet para definir bordes en las celdas
        tabla_qt.setStyleSheet("""
            QTableWidget {
                gridline-color: #d3d3d3;
                font: 12px;
            }
            QTableWidget::item {
                border: 1px solid #d3d3d3;
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #d3d3d3;
            }
        """)
        
        # Configurar que la última columna se estire para ocupar espacio extra
        header = tabla_qt.horizontalHeader()
        header.setStretchLastSection(True)
        
        # Definir número de filas y establecer alineación central para cada celda
        tabla_qt.setRowCount(len(self.no_terminales))
        alineacion = int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        
        for i, nt in enumerate(self.no_terminales):
            item_nt = QTableWidgetItem(nt)
            item_nt.setTextAlignment(alineacion)
            tabla_qt.setItem(i, 0, item_nt)
            fila = self.tabla.get(nt, [""] * len(self.terminales))
            for j, valor in enumerate(fila):
                texto = str(valor) if valor != "" else ""
                item = QTableWidgetItem(texto)
                item.setTextAlignment(alineacion)
                tabla_qt.setItem(i, j + 1, item)
        
        # Redimensionar columnas y filas para ajustarse al contenido
        tabla_qt.resizeColumnsToContents()
        tabla_qt.resizeRowsToContents()