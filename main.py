import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PyQt6.QtGui import QIcon
import os
import platform
import requests
import uuid
import datetime

def log_install_once():
    appdata = os.getenv('APPDATA')  # bv: C:\Users\<user>\AppData\Roaming
    folder = os.path.join(appdata, 'DMWLTool')
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    flag_file = os.path.join(folder, '.install_logged')
    if os.path.exists(flag_file):
        return  # Al gelogd, niet opnieuw doen

    data = {
        "id": str(uuid.uuid4()),
        "ver": "1.2.0",  # Pas aan waar nodig
        "os": platform.system(),
        "host": platform.node(),
        "user": None,
        "installed_at": datetime.datetime.utcnow().isoformat() + "Z"
    }

    # Haal Windows gebruikersnaam veilig op
    try:
        data["user"] = os.getlogin()
    except Exception:
        data["user"] = os.environ.get("USERNAME", "unknown")

    # Probeer IP en locatie op te halen (optioneel, kan traag zijn)
    try:
        ip = requests.get("https://api.ipify.org", timeout=2).text
        data["ip"] = ip
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=2).json()
        data["country"] = geo.get("country_name", "")
        data["region"] = geo.get("region", "")
        data["city"] = geo.get("city", "")
    except Exception:
        pass

    try:
        requests.post("https://www.bobvmierlo.nl/logger.php", json=data, timeout=3)
    except Exception:
        pass

    with open(flag_file, 'w') as f:
        f.write('logged')

if __name__ == "__main__":
    log_install_once()

    app = QApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
    app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
