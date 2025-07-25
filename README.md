# DICOM Modality Worklist (DMWL) Query Tool

Deze applicatie is een eenvoudige Qt-gebaseerde GUI waarmee je DICOM C-FIND queries kunt uitvoeren op een Modality Worklist (DMWL) service. Dit helpt bij het testen of verifiëren van modality-integraties met een PACS/RIS-systeem.

## Functionaliteiten

- GUI met invoervelden voor:
  - Achternaam (ondersteunt wildcards)
  - Patient ID
  - Accession Number
  - Modality
- Resultaten worden getoond in een interactieve tabel
- Dubbelklikken op een regel toont het volledige DICOM-object (in JSON)
- Alle connectiegegevens configureerbaar in `resources/settings.json`:
  - PACS IP
  - Poort
  - AE Titles (zender en ontvanger)

## Vereisten

- Python 3.12
- PySide6
- pydicom
- pynetdicom

## Builden .exe in Windows

```bash
pyinstaller main.py --onefile --noconsole --name DMWL_CFinder
