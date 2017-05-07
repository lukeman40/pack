from pyautocad import Autocad, APoint
import xlwings as xw

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

            #gets the coordinates of the texts
            if text.TextOverride != "":
                TextContent.append(text.TextOverride)
            else:
                TextContent.append(text.Measurement)


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

        if n == len(TextPosition):
            break
        if text.Layer == "Fab Details":

            x = text.InsertionPoint[0]
            y = text.InsertionPoint[1]

            if x-200 < TextPosition[n][0] and x + 600 > TextPosition[n][0]:
                if y < TextPosition[n][1] and y + 1000 > TextPosition[n][1]:

                    print (TextContent[n])
                    print (text.TextString, " -------- This is new bit \n")

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


                    #string manipulation
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



