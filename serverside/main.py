# main.py
import sys
import os

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sheet_template import Sheet_Template  # Import the class
from equipment_template import Weapon_Template
from equipment_template import Usable_Template
from equipment_template import Permanent_Template
from equipment_template import Permanent_Buff_Template
from table import Table

def testaDado():
    resultados = []  # Initialize an empty list to hold results
    
    weapons_matrix = character_sheet.getWeaponsBackpack()
    for i in range(1000):
        resultado = weapons_matrix[0][0].roll_Damage_TwoDicesMod(1, 2, 1, 20, 100)  # Roll the dice
        
        # Check if the result already exists in the list
        found = False
        for res in resultados:
            if res[0] == resultado:  # If the result is found, increase its count
                res[1] += 1
                found = True
                break
        
        if not found:  # If the result is not found, append it with a count of 1
            resultados.append([resultado, 1])
    
    resultados.sort()

    print(resultados)

# Create an instance of the Sheet_Template class
character_sheet = Sheet_Template("Aragorn", 20, 15, 90)
character_sheet2 = Sheet_Template("Legolas", 15, 20, 10)
character_sheet3 = Sheet_Template("Frodo", 5, 5, 5)
character_sheet4 = Sheet_Template("Gandalf", 20, 20, 20)
character_sheet5 = Sheet_Template("Sauron", 20, 20, 20)

weapon = Weapon_Template("ARMA", 10, 2, 2, 0)
usable = Usable_Template("Potion", 10, 2, 3, 2)
usable2 = Usable_Template("Potion2", 10, 5, 4, 3)
permanent = Permanent_Template("Ring", 10, 2, 5)



table = Table(1, "Table1")
table.addSheet(character_sheet)
table.addSheet(character_sheet2)
table.displayTable()



        
    