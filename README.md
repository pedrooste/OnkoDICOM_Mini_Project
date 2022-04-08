# OnkoDICOM_Mini_Project
OnkoDICOM Introduction to DICOM and PySide6 Project.

## Overview
PySide6 program which 
- starts and determines if there is a preferences-configuration record, loading if present.
- proceed to opening a DICOM file in a fault tolerant way, checking all elements are present. If not, the programme must seek guidence from the user on how to proceed.
  - insert element list

## Requirements
The program must meet the following requirements
- Python logging enabled
- Pycodestyle
- Pylint
- Pytest (80% test code coverage)

## How To Run
Clone the repo to your desired location
- `git clone <url>`

Initialise your virtual environment (recommended)
- `python -m venv <venv>`

For Windows, in your project dir
- `<venv>\Scripts\activate.bat`

For Linux, in your project dir
- `source <venv>/bin/activate`

Install the requirements
- `pip install -r requirements.txt`

😀 You should be good to go! 😀
