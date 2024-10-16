# main.py
import sys
import os

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sheet_template import Sheet_Template  # Import the class
from equipment_template import Weapon_Template
from equipment_template import Usable_Template
from equipment_template import Permanent_Template


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
character_sheet = Sheet_Template("Aragorn", 20, 15, 10)
weapon = Weapon_Template("ARMA", 10, 2, 2, 0)
usable = Usable_Template("Potion", 10, 2, 3, 2)
usable2 = Usable_Template("Potion2", 10, 5, 4, 3)
permanent = Permanent_Template("Ring", 10, 2, 5)

character_sheet.addUsable(usable, 2)
character_sheet.addUsable(usable2, 1)


Potion = character_sheet.getUsables()[0][0]
Potion2 = character_sheet.getUsables()[1][0]

Potion.use()
Potion.use()
Potion2.use()
Potion2.use()
Potion2.use()



# Call the Display method to print the character's details
character_sheet.Display()





        
    