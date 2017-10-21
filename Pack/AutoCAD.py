from pyautocad import Autocad, APoint
import xlwings as xw
import re

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print (acad.doc.Name)

wb = xw.Book('TWF 076 - ML production pack - Issue 17.xlsm')

shtStructureCutting = wb.sheets['Structure Cutting']

Structure_List = shtStructureCutting.range("C10:I60").value

o=10
TextPosition = []
TextContent = []


for text in acad.iter_objects(['Text','Dimension']):
    if text.Layer == "Fab Details":

        if "Dimension" in text.EntityName:
            print (text.TextOverride , "\n")

            #gets the coordinates of the measurements/dimensions
            if text.TextOverride != "":
                TextContent.append(text.TextOverride)
            else:
                TextContent.append(str(text.Measurement))

            #makes dimension in the same array
            TextPosition.append(text.TextPosition)

        # if "Text" in text.EntityName:
        #
        #     string = text.TextString
        #
        #     j = string.find("No.") - 2
        #     l = string.find("No.") + 4
        #
        #     printtext = string[j]
        #     Material = string[l:l + 8]
        #
        #     print (printtext + "No.\n")
        #
        #     print (text.TextString + "\n")



for text in acad.iter_objects('Text'):

    #cylcles through the text position, if it is within a range, its gets the dimension length
    for n in range(0,len(TextPosition)):

        if text.Layer == "Fab Details":

            x = text.InsertionPoint[0]
            y = text.InsertionPoint[1]

        #if the text is within a certain box around dimension, we know this text is associated with the dimension
            if x-200 < TextPosition[n][0] and x + 600 > TextPosition[n][0]:
                if y < TextPosition[n][1] and y + 1000 > TextPosition[n][1]:

                    print (TextContent[n])
                    print (text.TextString, " -------- This is new bit \n")



                    #//////////////////////////// region Adds box around text were looking at
                    p1 = APoint(x-200,y)
                    p2 = APoint(x+600,y+1000)

                    p1 = APoint(x-200,y)
                    p2 = APoint(x-200,y+1000)

                    acad.model.AddLine(p1,p2)

                    p1 = APoint(x-200,y+1000)
                    p2 = APoint(x+600,y+1000)

                    acad.model.AddLine(p1,p2)

                    p1 = APoint(x + 600, y + 1000)
                    p2 = APoint(x + 600, y)

                    acad.model.AddLine(p1, p2)

                    p1 = APoint(x + 600, y)
                    p2 = APoint(x - 200, y)

                    acad.model.AddLine(p1, p2)
                    #///////////////////////////////////// endregion


                    #string manipulation
                    Title = text.TextString
                    Dimensions = TextContent[n]

                    j = Title.index("No.") - 3
                    l = Title.find("No.") + 4

                    #quantity
                    printtext = Title[j:j+2]

                    Material = Title

                    #Finds Reference
                    Reference = Title[(Title.find("<") + 1):(Title.find("<") + 3)]

                    # Adds to excel///////////////////////////////////

                    shtStructureCutting.cells(o, 2).value = Reference

                    # If Dimensions contains aluminium, find print out that section
                    # description column
                    if 'ALUMINIUM' in Dimensions:
                        shtStructureCutting.cells(o, 3).value = Dimensions[(Dimensions.find("Aluminium") - 27):(Dimensions.find("Aluminium") - 7)].title()

                    # if re.search('150x75', TextContent[n]):
                    #     shtStructureCutting.cells(o, 3).value = re.search('150x75 Aluminium Box', TextContent[n]).group()

                    # length column
                    shtStructureCutting.cells(o, 6).value = re.search(r'\d+', TextContent[n]).group()

                    #quantity column
                    shtStructureCutting.cells(o, 9).value = printtext

                    o=o+1
                    n=n+1



