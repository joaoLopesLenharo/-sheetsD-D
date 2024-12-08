D&D 5.5E Character Sheet Application
This repository contains a Python application designed to create and manage character sheets for Dungeons & Dragons 5.5 Edition. The application provides a user-friendly GUI for managing character stats, inventory, spells, and features, along with exporting data to JSON and PDF formats.

Features
Create and edit character sheets, including basic info, classes, attributes, and resources.
Manage spells, abilities, and inventory items with detailed descriptions.
Export and import character data in JSON format.
Generate formatted PDFs of character sheets.
Responsive and interactive GUI built with Tkinter.
Requirements
To run this project, you will need:

Python 3.7 or higher
The following Python libraries:
tkinter (standard Python library)
reportlab (for PDF generation)
json (standard Python library)
pyinstaller (optional, for creating standalone executables)
Install the dependencies using:

bash
Copiar código
pip install reportlab pyinstaller
How to Run
Clone the repository:

bash
Copiar código
git clone https://github.com/joaoLopesLenharo/-sheetsD-D.git
cd -sheetsD-D
Run the main application:

bash
Copiar código
python ficha.py
To generate a standalone executable:

Run the build_exe.py script:
bash
Copiar código
python build_exe.py
The executable file will be created in the dist directory.
Usage
GUI Overview
Basic Info: Input the character's name, race, and level.
Attributes: Manage core stats like STR, DEX, CON, etc., and automatically calculate modifiers.
Proficiencies: Select skills and calculate their bonuses.
Combat Stats: Define AC, spell DC, and passive perception.
Resources: Track hit points, mana, and stamina.
Modules:
Spells: Add, edit, and filter spells by level and description.
Abilities: Manage character abilities or features.
Inventory: Add items, track bonuses, and describe equipment.
Export/Import Options
Save or load character sheets using JSON files.
Export formatted character sheets as PDFs.
License
This project is licensed under the MIT License. Feel free to use and modify it.

Acknowledgements
Developed by João Lopes Lenharo.
Special thanks to the Python community for the tools and libraries used in this project.