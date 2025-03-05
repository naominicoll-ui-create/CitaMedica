import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QCalendarWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt

DATA_FILE = "appointments.json"

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Citas Médicas - Admin")
        self.setGeometry(100, 100, 700, 500)
        self.center_window()  # Centrar la ventana
        self.appointments = []
        self.init_ui()
        self.load_appointments()
        self.show_appointments()

    def center_window(self):
        """Centra la ventana en la pantalla."""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()

        # Sección para agregar o editar cita
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.patient_input = QLineEdit(self)
        self.patient_input.setPlaceholderText("Nombre del paciente")
        layout.addWidget(self.patient_input)

        self.doctor_combo = QComboBox(self)
        self.doctor_combo.addItems(["Dr. Pérez - Cardiología", "Dra. Gómez - Pediatría"])
        layout.addWidget(self.doctor_combo)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Hora (HH:MM)")
        layout.addWidget(self.time_input)

        btn_schedule = QPushButton("Agendar Cita", self)
        btn_schedule.clicked.connect(self.schedule_appointment)
        layout.addWidget(btn_schedule)

        # Sección para la lista de citas y operaciones CRUD
        layout.addWidget(QLabel("Citas Agendadas:"))
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Paciente", "Médico", "Fecha", "Hora"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_edit = QPushButton("Editar Cita", self)
        btn_edit.clicked.connect(self.edit_appointment)
        btn_layout.addWidget(btn_edit)

        btn_cancel = QPushButton("Cancelar Cita", self)
        btn_cancel.clicked.connect(self.cancel_appointment)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_appointments(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.appointments = json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo cargar el archivo: {e}")
        else:
            self.appointments = []

    def save_appointments(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.appointments, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la información: {e}")

    def schedule_appointment(self):
        patient = self.patient_input.text().strip()
        doctor = self.doctor_combo.currentText()
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        time = self.time_input.text().strip()

        if not patient or not time:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")
            return

        appointment = {"patient": patient, "doctor": doctor, "date": date, "time": time}
        self.appointments.append(appointment)
        self.save_appointments()
        self.show_appointments()
        QMessageBox.information(self, "Éxito", "Cita agendada correctamente.")

        self.patient_input.clear()
        self.time_input.clear()

    def show_appointments(self):
        self.table.setRowCount(len(self.appointments))
        for i, app in enumerate(self.appointments):
            self.table.setItem(i, 0, QTableWidgetItem(app["patient"]))
            self.table.setItem(i, 1, QTableWidgetItem(app["doctor"]))
            self.table.setItem(i, 2, QTableWidgetItem(app["date"]))
            self.table.setItem(i, 3, QTableWidgetItem(app["time"]))
        self.table.resizeColumnsToContents()

    def edit_appointment(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Selecciona una cita para editar.")
            return

        appointment = self.appointments[row]
        new_patient = self.patient_input.text().strip() or appointment["patient"]
        new_time = self.time_input.text().strip() or appointment["time"]
        new_date = self.calendar.selectedDate().toString("yyyy-MM-dd") or appointment["date"]
        new_doctor = self.doctor_combo.currentText() or appointment["doctor"]

        self.appointments[row] = {
            "patient": new_patient,
            "doctor": new_doctor,
            "date": new_date,
            "time": new_time
        }
        self.save_appointments()
        self.show_appointments()
        QMessageBox.information(self, "Éxito", "Cita editada correctamente.")

    def cancel_appointment(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Selecciona una cita para cancelar.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "¿Estás seguro de cancelar la cita?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.appointments.pop(row)
            self.save_appointments()
            self.show_appointments()
            QMessageBox.information(self, "Éxito", "Cita cancelada.")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
