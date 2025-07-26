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

- PySide6
- pydicom
- pynetdicom

## Zelf builden .exe in Windows

```bash
py -m PyInstaller --noconfirm --onefile --windowed --icon=resources/icon.ico main.py
```

## Gebruik
- In de releases staat een release_bundle.zip, deze bevat de applicatie, mock server en resources map. Pak deze uit op je lokale pc naar bijv C:\DMWL-tool
- Main.exe kan op Windows gestart worden (geef wel SmartScreen melding, omdat de applicatie niet ondertekend is), zorg er voor dat de resources map in dezelfde map staat.
- Er kan gezocht worden op een aantal velden, wildcards zijn ook toegestaan
- Door te dubbelklikken op een regel in de tabel krijg je meer DICOM details te zien

### Mock Server
De mock_dmwl_server.exe kan gestart worden om te testen, deze start een simpele DMWL service op met 4 voorbeeld patiënten. De terminal geeft ook volledige debug output, zodat je kunt zien wat de DMWL tool opvraagt.

## Licentie & Rechten
Deze applicatie is ontwikkeld voor gebruik in een ziekenhuis/testomgeving. Gebruik op eigen risico.

Auteursrechten:
© 2025 Bob van Mierlo. Alle rechten voorbehouden.

Je mag de code en applicatie vrij gebruiken, aanpassen en delen voor niet-commerciële doeleinden. Voor commerciële toepassing of distributie is toestemming vereist.
