import json
import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)

DEFAULT_SETTINGS = {
    "calling_ae_title": "MY_AE",
    "called_ae_title": "DMWL_AE",
    "server_ip": "127.0.0.1",
    "server_port": 11112
}


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instellingen")
        self.setMinimumSize(400, 200)

        self.settings = self.load_settings()

        layout = QVBoxLayout()
        self.fields = {}

        # Map keys to Dutch labels
        field_info = {
            "server_ip": "Server IP",
            "server_port": "Server Poort",
            "calling_ae_title": "Calling AE Title",
            "called_ae_title": "Called AE Title"
        }

        for key, label_text in field_info.items():
            label = QLabel(label_text)
            input_field = QLineEdit(str(self.settings.get(key, "")))
            self.fields[key] = input_field
            layout.addWidget(label)
            layout.addWidget(input_field)

        btn_layout = QHBoxLayout()
        save_button = QPushButton("Opslaan")
        save_button.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_button)

        cancel_button = QPushButton("Annuleren")
        cancel_button.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_base_path(self):
        if getattr(sys, 'frozen', False):
            # Executable mode
            return Path(sys.executable).parent
        else:
            # Script mode
            return Path(__file__).parent

    def get_config_path(self):
        base_path = self.get_base_path()
        resources_dir = base_path / "resources"
        resources_dir.mkdir(exist_ok=True)  # Maak map resources als die nog niet bestaat
        return resources_dir / "settings.json"

    def load_settings(self):
        config_path = self.get_config_path()
        if not config_path.exists():
            return DEFAULT_SETTINGS.copy()
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        try:
            updated = {
                k: (int(f.text()) if k == "server_port" else f.text())
                for k, f in self.fields.items()
            }
            config_path = self.get_config_path()
            with open(config_path, "w") as f:
                json.dump(updated, f, indent=2)
            QMessageBox.information(self, "Opgeslagen", "Instellingen succesvol opgeslagen.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Fout", f"Instellingen konden niet worden opgeslagen:\n{e}")

    def get_settings(self):
        # Extra methode om actuele settings terug te geven (optioneel, handig voor main_window)
        return {
            k: (int(f.text()) if k == "server_port" else f.text())
            for k, f in self.fields.items()
        }
