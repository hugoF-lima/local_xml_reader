# Batch XML Invoice Automation (Python RPA)
Python-based RPA solution developed to automate invoice emission by replacing a manual PDF-based workflow with structured XML batch processing.

The system parses XML invoice data, extracts relevant fields, automates interaction with an external invoice management system, and updates structured Excel reports.

This reduced invoice processing time from **90 minutes to 40 minutes per 100 invoices (55% reduction / 2.25× throughput increase)**.

---
# Problem Context

Manual invoice emission required:
- Opening and processing ~100 PDF files individually
- Extracting and inputting invoice data manually
- Updating Excel reports manually

The process was repetitive, time-consuming, and error-prone.

---
## Solution

This project implements:
- Batch XML parsing and structured data extraction
- Automated interaction with external invoice software (GUI automation)
- Excel report generation
- Desktop interface built with PyQt5

Despite external system latency constraints, the automation significantly improved workflow efficiency.

---

## Tech Stack

- Python
- Pandas
- OpenPyXL
- ElementTree (XML parsing)
- PyAutoGUI (GUI automation)
- ctypes (system-level interaction)
- PyQt5 (GUI interface)

---
## Architecture Summary

1. XML files are batch-read and parsed.
2. Relevant invoice fields are extracted and structured.
3. GUI automation interacts with external invoice management software.
4. Processed data is exported into formatted Excel reports.
---

## External Dependency

The automation interacts with a third-party invoice management application (Synchro DFE Manager).

⚠ Note: For security reasons, the project cannot fully run without a compatible external target application. However, the window check can be disabled or adapted for integration with other systems. (Custom XML mapping and Excel table mapping for reports are required).

---
## Running the project and Packaging Notes
- Ensure `local_rfid.xlsx` is available as a template file for spreadsheet output.

- Ensure creating a fresh new virtual environment (venv):
```bash
python -m venv localvenv
```
- Ensure dependencies are properly installed: 
```bash
pip install -r requirements.txt
```
- Spreadsheet structure is expected to match the model template.

If building EXE with PyInstaller (version 3.6 required):
```bash
pyinstaller src/local_xml_reader.py --onefile --noconsole
```
if debugging, remove the --noconsole parameter.


To prevent compatibility issues, avoid modifying the Excel template using alternative editors that may alter embedded XML structures.
