from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QTextEdit, QHBoxLayout
)
from PyQt6.QtGui import QIcon
from dmwl_client import query_worklist
from gui.settings_dialog import SettingsDialog
import json
import traceback
import os
import sys
from pathlib import Path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM DMWL Query")
        self.setMinimumSize(900, 600)
        self.results = []

        layout = QVBoxLayout()

        icon_path = self.get_resource_path("icon.png")
        self.setWindowIcon(QIcon(str(icon_path)))

        # Dutch labels mapped to DICOM query keys
        labels = {
            "Achternaam": "PatientName",
            "Patiëntnummer": "PatientID",
            "Accessionnummer": "AccessionNumber",
            "Modaliteit": "Modality"
        }

        self.inputs = {}
        for label_text in labels.keys():
            lbl = QLabel(label_text)
            inp = QLineEdit()
            self.inputs[label_text] = inp
            layout.addWidget(lbl)
            layout.addWidget(inp)
            inp.returnPressed.connect(self.perform_query)

        # Buttons layout
        button_layout = QHBoxLayout()

        self.query_btn = QPushButton("Zoeken")
        self.query_btn.clicked.connect(self.perform_query)
        button_layout.addWidget(self.query_btn)

        self.settings_btn = QPushButton("Instellingen")
        self.settings_btn.clicked.connect(self.open_settings)
        button_layout.addWidget(self.settings_btn)

        layout.addLayout(button_layout)

        # Results table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Achternaam", "Patiëntnummer", "Accessienummer", "Modaliteit", "Startdatum"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.cellDoubleClicked.connect(self.show_full_dataset)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Map Dutch labels to DICOM tags for query
        self.label_to_tag = labels

    def get_base_path(self):
        if getattr(sys, 'frozen', False):
            # Executable mode
            return Path(sys.executable).parent
        else:
            # Script mode
            return Path(__file__).parent

    def get_resource_path(self, filename):
        base_path = self.get_base_path()
        return base_path / "resources" / filename

    def get_config_path(self):
        base_path = self.get_base_path()
        resources_dir = base_path / "resources"
        resources_dir.mkdir(exist_ok=True)  # Maak resources map als die nog niet bestaat
        return resources_dir / "settings.json"

    def load_config(self):
        config_path = self.get_config_path()
        print(f"Loading config from {config_path}")
        if not config_path.exists():
            # Maak een standaard settings.json aan als die er niet is
            default_config = {
                "server_ip": "",
                "server_port": 11112,
                "calling_ae_title": "",
                "called_ae_title": "DMWL_AE"
            }
            self.save_config(default_config)
            return default_config

        with open(config_path, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        config_path = self.get_config_path()
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Settings saved to {config_path}")

    def perform_query(self):
        self.query_btn.setEnabled(False)

        # Clear previous results before new query
        self.table.setRowCount(0)
        self.results = []

        try:
            # Load config fresh every query to get latest saved settings
            config = self.load_config()

            # Validate essential config entries, raise if missing
            required_keys = ["server_ip", "server_port", "calling_ae_title", "called_ae_title"]
            for key in required_keys:
                if key not in config or not config[key]:
                    raise ValueError(f"Configuratie ontbreekt: '{key}' moet ingevuld zijn in instellingen.")

            # Build query dict with DICOM keys and non-empty inputs only
            query_data = {}
            for label, line_edit in self.inputs.items():
                val = line_edit.text().strip()
                if val:
                    query_data[self.label_to_tag[label]] = val

            # Pass only config params, no hardcoded values
            kwargs = {
                "calling_ae_title": config["calling_ae_title"],
                "called_ae_title": config["called_ae_title"],
                "server_ip": config["server_ip"],
                "server_port": config["server_port"]
            }

            print("Query parameters:", kwargs)  # Debug print to terminal
            print("Query data:", query_data)

            results = query_worklist(query_data, **kwargs)

            if not results:
                QMessageBox.information(self, "Geen resultaten", "Geen resultaten gevonden voor deze query.")
                return

            self.table.setRowCount(len(results))
            self.results = results

            for i, ds in enumerate(results):
                self.table.setItem(i, 0, QTableWidgetItem(str(ds.get("PatientName", ""))))
                self.table.setItem(i, 1, QTableWidgetItem(str(ds.get("PatientID", ""))))
                self.table.setItem(i, 2, QTableWidgetItem(str(ds.get("AccessionNumber", ""))))

                modality = ""
                date = ""
                if hasattr(ds, "ScheduledProcedureStepSequence"):
                    sps = ds.ScheduledProcedureStepSequence[0]
                    modality = str(sps.get("Modality", ""))
                    date = str(sps.get("ScheduledProcedureStepStartDate", ""))

                self.table.setItem(i, 3, QTableWidgetItem(modality))
                self.table.setItem(i, 4, QTableWidgetItem(date))

        except ConnectionError as ce:
            QMessageBox.critical(self, "Verbindingsfout", f"Verbinding met DMWL-server mislukt:\n{ce}")
            print("ConnectionError:", ce)
            traceback.print_exc()
        except Exception as e:
            QMessageBox.critical(self, "Query Fout", f"Er is een fout opgetreden bij de query:\n{e}")
            print("Error during query:", e)
            traceback.print_exc()
        finally:
            self.query_btn.setEnabled(True)

    def show_full_dataset(self, row, col):
        ds = self.results[row]

        dlg = QDialog(self)
        dlg.setWindowTitle("Volledig DICOM Object")
        dlg.setMinimumSize(700, 500)
        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setFontFamily("Courier New")  # Monospace font
        text_edit.setReadOnly(True)

        dicom_dump = str(ds)
        text_edit.setPlainText(dicom_dump)

        layout.addWidget(text_edit)
        dlg.setLayout(layout)
        dlg.exec()

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            # Hier kun je settings opslaan, b.v.:
            new_config = dlg.get_settings()  # Stel dat je zoiets hebt in SettingsDialog
            if new_config:
                self.save_config(new_config)
