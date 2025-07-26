# DICOM Modality Worklist (DMWL) Query Tool

This application is a simple Qt-based GUI that allows you to perform DICOM C-FIND queries on a Modality Worklist (DMWL) service. It helps test or verify modality integrations with a PACS/RIS system.

> 🇳🇱 This project is originally designed in Dutch, the GUI therefore is also Dutch. The README is also available in Dutch: [README_nl.md](README_nl.md)

## Features

- GUI with input fields for:
  - Last name (supports wildcards)
  - Patient ID
  - Accession Number
  - Modality
- Results are displayed in an interactive table
- Double-clicking a row shows the full DICOM object
- All connection settings are configurable in `resources/settings.json`:
  - PACS IP
  - Port
  - AE Titles (caller and called)

## Requirements

- PySide6
- pydicom
- pynetdicom

## Building a Windows .exe

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

## Usage
- In the releases section, you'll find a release_bundle.zip. Extract this locally, for example to C:\DMWL-tool.
- Run main.exe (Windows will show a SmartScreen warning because the app is unsigned). Make sure the resources folder is in the same directory as the executable.
- You can search using the fields; wildcards are allowed.
- Double-clicking a row in the table shows more DICOM details.

### Mock Server
You can run mock_dmwl_server.exe to test the application. This starts a simple DMWL SCP with 4 example patients. The terminal shows full debug output so you can see what is queried by the tool.

### License & Disclaimer
This application is intended for use in a hospital or test environment. Use at your own risk.

Copyright:
© 2025 Bob van Mierlo. All rights reserved.

You may freely use, modify, and share the code and application for non-commercial purposes. For commercial use or redistribution, permission is required.

### Third party licenses
This application uses PyQt6, which is licensed under the GPLv3. As such, the entire application is subject to the terms of the GPLv3 license.

- **PyQt6**  
  License: GNU General Public License v3 (GPLv3)  
  Source: https://www.riverbankcomputing.com/software/pyqt/  
  This application uses PyQt6 for the graphical user interface. As PyQt6 is licensed under the GPLv3, this means the entire application, when distributed in compiled form, is also subject to the terms of the GPLv3 license.

- **pynetdicom**  
  License: MIT  
  Source: https://github.com/pydicom/pynetdicom  
  Used to perform DICOM network communication, including C-FIND queries to a DMWL (Modality Worklist) SCP.

- **pydicom**  
  License: MIT  
  Source: https://github.com/pydicom/pydicom  
  Used to parse and handle DICOM files and datasets in Python.

- **PyInstaller**  
  License: GPLv2 with an exception (allows bundling non-GPL software)  
  Source: https://github.com/pyinstaller/pyinstaller  
  Used to package the application into standalone executable files. Note that PyInstaller's license allows bundling GPL and non-GPL software, but it does not override the GPLv3 requirement from PyQt6.

Please refer to each library’s repository for the full license text.