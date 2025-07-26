### Third-party licenses

This application uses several open-source libraries. The main license of this project is MIT, but due to the use of GPL-licensed components, the entire application must comply with the terms of the GPLv3 license when distributed in compiled form.

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