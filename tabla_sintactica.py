from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

class TablaSintactica:
    def __init__(self, gramatica=None, no_terminales_interfaz_orden=None): # Recibir orden
        self.terminales = [
            "Start", "End", "Entero", "Doble", "Cadena", "num", "var", "=",
            "+", "-", "*", "/", "(", ")", "{", "}", "Si", "SiNo", "Mientras", "Salida",
            "Entrada", ">", "<", "<=", ">=", "!=", "!", "++",  ","
        ]
        self.no_terminales = [
            "S", "A", "A'", "B", "C", "J", "K", "K'", "D", "L", "L'", "M",
            "OP", "H", "Q", "I", "G", "F", "N", "N'", "R"
        ]
        self.tabla = {nt: {t: "" for t in self.terminales} for nt in self.no_terminales}
        self.gramatica = gramatica
        self.no_terminales_orden = no_terminales_interfaz_orden # Guardar orden

    def construir_tabla(self, primeros, gramatica):
        """Construye la tabla sintáctica predictiva."""
        fila_por_nt = {nt: i + 1 for i, nt in enumerate(self.no_terminales_orden)}

        print("TablaSintactica.construir_tabla: Iniciando la construcción de la tabla...")
        for no_terminal, producciones in gramatica.items():
            print(f"TablaSintactica.construir_tabla: No Terminal = {no_terminal}")
            for produccion in producciones:
                print(f"TablaSintactica.construir_tabla: Producción = {produccion}")
                primeros_produccion = self.calcular_primeros_produccion(produccion, primeros)

                for terminal in primeros_produccion:
                    if terminal != "ε":
                        fila_numero = fila_por_nt[no_terminal]
                        print(f"TablaSintactica.construir_tabla: Terminal = {terminal}, Fila = {fila_numero}") # <----
                        if self.tabla[no_terminal][terminal] == "":
                            self.tabla[no_terminal][terminal] = str(fila_numero)
                        else:
                            print(f"TablaSintactica.construir_tabla: CONFLICTO: {no_terminal}, {terminal}")

    def calcular_primeros_produccion(self, produccion, primeros):
        conjunto_primeros = set()
        epsilon_en_primeros = True

        for simbolo in produccion:
            if simbolo in primeros:
                primeros_simbolo = primeros[simbolo]
                conjunto_primeros.update(primeros_simbolo - {"ε"})
                if "ε" not in primeros_simbolo:
                    epsilon_en_primeros = False
                    break
            elif simbolo != "ε":
                conjunto_primeros.add(simbolo)
                epsilon_en_primeros = False
                break
            else:
                break

        if epsilon_en_primeros:
            conjunto_primeros.add("ε")

        return conjunto_primeros

    def mostrar_en_qtablewidget(self, tabla_qt: QTableWidget):
        """Muestra los números de fila en la QTableWidget."""
        # Configurar encabezados
        columnas = len(self.terminales) + 1
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

            for j, terminal in enumerate(self.terminales):
                valor = self.tabla[nt].get(terminal, "") # <--- Usar .get aquí
                texto = str(valor) if valor != "" else ""
                item = QTableWidgetItem(texto)
                item.setTextAlignment(alineacion)
                tabla_qt.setItem(i, j + 1, item)

        # Redimensionar columnas y filas para ajustarse al contenido
        tabla_qt.resizeColumnsToContents()
        tabla_qt.resizeRowsToContents()