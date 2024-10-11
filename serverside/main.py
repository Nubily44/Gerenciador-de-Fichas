# main.py
import sys
import os

# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sheet_template import Sheet_Template  # Import the class
from equipment_template import Usable_Template


# Create an instance of the Sheet_Template class
character_sheet = Sheet_Template("Aragorn", 20, 15, 10)
# Call the Display method to print the character's details
character_sheet.Display()


# RESOLVER OS EQUIPMENT