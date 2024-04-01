import sys

from src import Gui
import argparse

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        parser = argparse.ArgumentParser(
            description="""
            To Run "python main.py".
            
            Xel Spreadsheet.
            Just like excel but programmed in a week and by me alone.
            Please use the gui which should be opening right about now.
            
            To edit a cell double click a cell.
            To enter a formula first type `=` into the cell.
            Example: `=8*8` is a formula, but `8*8` is not a formula, the first will show `64.0` and the second `8*8`.
            
            To save/export the current workbook please use export/save in the file menu.
            To import a file into the current workbook please use import in the file menu.
            
            To add/rename/delete a sheet right click on the current sheets buttons.
            
            To add/remove more columns/rows please right use append/add/delete rows/columns when right clicking the columns
                titles.
             
            To see documentation about the functions/operands in Xel choose the operation you wish to learn about 
                in the relevant menus in the upper left side of the window.
            
            Font, font size and font annotation are for the entire workbook.
            Alignments and colors are per cell.
            
            P.S. Xel mostly uses floats so weird operations will cause floating point error.
            To Combat it Xel offers the amazing Round Function which can turn a float back into an int.
            """,
            epilog="""Have a great time using Xel :)""")
        args = parser.parse_args()
    else:
        gui: Gui = Gui()
        
        gui.run()
