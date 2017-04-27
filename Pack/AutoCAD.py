from pyautocad import Autocad, APoint
import xlwings as xw

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print (acad.doc.Name)

wb = xw.Book('TWF 076 - ML production pack - Issue 16.xlsm')

shtStructureCutting = wb.sheets['Structure Cutting']

Structure_List = shtStructureCutting.range("C10:I60").value

i=0
o=10
TextPosition = []
TextContent = []

for text in acad.iter_objects(['Text','Dimension']):
    if text.Layer == "Fab Details":

        if "Dimension" in text.EntityName:
            print (text.TextOverride , "\n")

            TextContent.append(text.TextOverride)
            TextPosition.append(text.TextPosition[1])
            i = i + 1

        if "Text" in text.EntityName:

            string = text.TextString

            j = string.find("No.") - 2
            l = string.find("No.") + 4

            printtext = string[j]
            Material = string[l:l + 8]

            print (printtext + "No.\n")

            print (text.TextString + "\n")



for text in acad.iter_objects('Text'):
    for n in range(0,i):
        if text.Layer == "Fab Details":
            if text.InsertionPoint[1] < TextPosition[n] and text.InsertionPoint[1]+600 > TextPosition[n]:
                print (TextContent[n])
                print (text.TextString, " -------- This is new bit \n")

                string = text.TextString

                j = string.find("No.") - 2
                l = string.find("No.") + 4

                printtext = string[j]
                Material = string

                shtStructureCutting.cells(o, 3).value = Material

                shtStructureCutting.cells(o, 6).value = TextContent[n]

                shtStructureCutting.cells(o, 9).value = printtext

                o=o+1
                n=n+1



