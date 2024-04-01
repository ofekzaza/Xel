# Xel

Xel is a spreadsheet app, created using python and tkinter,
for the final project of the introduction to computer science course.

## Extensions

### list of extensions

1. Gui - Xel is fully operable from the graphical interface.
2. Advanced Operations - Xel offers the use of around 30 functions and operands.
3. Sheets - allow for creation, renaming, and deletion of cells, also cell pointers between sheets.
4. Auto filling - create simple auto fills for cells based on selected sells.
5. Text editing - Xel allows to change the font, size, annotation of the text within the workbook.
6. Cell customization - set alignment and colors of background and text of cells.
7. Export - allows to export your Workbook to any of the following formats Json, Yaml, Xlsx, ~csv.
8. Import - allow to import any of the following formats into your workbook: Json, Yaml, Xlsx, ~csv.
9. Save - fast export to the last exported file or only imported file, allows for fast saving of progress.
10. Table operations - Hide, add, delete rows and columns.
11. basic undo - basic text undo per worksheet.
12. fast links - To Xel video, and  Introduction to Microsoft Excel 1990, found under the file menu.
13. Mypy - mypy main.py returns no errors.

note - csv export import supports only one sheet, and only evaluation without the formulas.

### Gui

graphical user interface is the only way to use xel.
when running xel a tkinter window will open with all the functions of xel.
Xel is heavily influenced by excel and tries to be similar as possible. (under the time constraints of the development)
So ui is very similar and the formulas work pretty similar too.

the ui have 3 main parts:
1. the menus - upper buttons which allow metadata operations:
    - file menu:
        - export: like Save as functionality in Office.
        - import: import a selected file into the existing worksheet,
                    warning if the imported workbook have worksheet with the same name of an existing worksheet,
                    the imported will overwrite the existing.
        - save: fast export to a known workbook file.
        - youtube video: open xel up to 7 min video
        - Excel video: my spreadsheet doesnt do that
    - font menu: allows to select the font of the text within the workbook
    - size menu: allows to select/change the size on the cells in the workbook
    - font annotation: select if you want normal / bold or italic text in the workbook
    - font color: select the color of the text in selected cells.
    - background color: select the color for background in selected cells.
    - alignment: select the kind of alignment for text within selected cells.
    - function: shows all the options of reduce functions within Xel, pressing one opens his documentation.
    - function: shows all the options of operands within Xel, pressing one opens his documentation.
2. Table:
    - shows the existing data
    - to enter a formula first enter `=` when editing the cell.
      Example: `=8*8` is as formula and the cell will show `64`, `8*8` is not a formula and cell will show `8*8`
    - When entering a bad formula the Cell will state the error, bad pointer may mean an invalid function name.
    - formulas are not case sensitive but upper case is preferable.
    - to edit a cell double click him, to save the edition just exit him (with enter or click outside the cell)
    - To append cells, right click the sheet and choose append columns or rows, enter the amount you want and the sheet will grow.
    - To hide/Add/Delete row/column within the table right click the headers/index and choose the option you want.
    - To see hidden row/column right click index/headers and press show all row/columns
3. Sheets menu:
    - sheet name buttons: move you to the chosen sheet.
    - right click on sheets menu: allows for adding a sheet or renaming/deleting the chosen sheet.

### Advance Operations

Xel offers advance functions and operands
Here is the complete list of the offered operations:
- Functions:
    - Average
    - Max
    - Min
    - Median
    - Round
    - Sqrt
    - Summary
    - Log
    - Ln
    - Lookup
    - CountIf
    - Length
    - Count
    - If
    - Absolute
    - Concat
    - Truncate
- Operands:
    - Power
    - Multiplying
    - Divide
    - Modulo
    - Addition
    - Subtraction
    - Equality
    - GreaterEqual
    - Greater
    - SmallerEqual
    - Smaller
    - NotEqual
    - And
    - Or
    - Xor

For more detail on each one please see the documentation within xel, (Upper right buttons).

### Multiple Sheets

Xel is designed from the ground for multiple sheets
you can add new sheets
and rename and delete existing ones,
when deleting the only existing sheet, a new empty sheet with the default name will be created.

Moreover, you can reference in formulas cells in different sheets.
and when exporting or importing data it imports and exports sheets of data, not specific cells.

## Notes

### Formula Cells

To enter a formula first enter `=` when editing the cell.
Examples: `=8*8` is as formula and the cell will show `64`.
          `8*8` is not a formula and cell will show `8*8`.
When entering a bad formula the Cell will state the error, bad pointer may mean an invalid function name.
In addition formulas are not case sensitive but upper case is preferable.
If formula doesnt change value after based upon cells change value, it is probably because the formula you use is invalid.

#### Pointers
in formula cells xel offers to use values of different cells within the formula,
to use different cells with the formula you can reference them by Stating their point.
there are 3 different kinds of pointers:
1. Cell pointer: Just State his location, examples: A1, J7, F19 and so forth.
2. Rows or Columns pointers: Reference an entire column or row, Example: A:A, B:C, or 1:3, 6:6 and so forth.
3. Table pointers: Reference a sub-table, for reference state the start cell and end cell. examples: A1:C3, A3:A7, B9:C1 and so forth

to reference cells in a different sheet first state the sheet name of the referenced cells.

Example: SheetName:A7:J8, SheetName2:E9, NewSheet:E:E and so forth.

when a cell value is changed, all the cells which reference him, reevaluate their values.

**note** you cannot create a circular pointers,
Example: A1 cannot reference any cells which in the reference A1 in any way,
including if any cells they reference reference A1 and so forth.
this is done to avoid infinite loop of reevaluations.

### **Empty cells are treated as 0 in formulas**

This is for simplicity and safety.
TO avoid the undesired effects of many zeros, state close area of functions.
Example: instead of writing A:A write A1:A10 and so forth.

## final words

Enjoy using Xel,

Created by Ofek Eshet.
