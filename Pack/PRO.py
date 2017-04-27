'''
Created on 22 Mar 2017

@author: Luke
'''
import xlwings as xw

from tkinter import *


class Material:
    # TODO add ESG if required - ADD ALERT when window pops up
    # TODO add gutter bits
    # TODO add more types of stock


    def __init__(self, material, stockcode, lengths_available):
        self.material = material
        self.stockcode = stockcode
        self.length = 0
        self.lengths_available = lengths_available

        self.amount = {}
        self.totalsum = {}

        for i in range(0, 50):
            self.amount[i] = 0
            self.totalsum[i] = 0

    def FindStockCode(self, length):
        return self.stockcode[length]

    def AddAmount(self, quantity, length, Dims):
        self.amount[length] = self.amount[length] + (1 * quantity)
        self.totalsum[length] = self.totalsum[length] + (Dims * quantity)

    def RemoveAmount(self, length):
        self.amount[length] = 0

    def ReturnAmount(self, length):
        return self.amount[length]

    def ReturnSum(self, length):
        return self.totalsum[length]

    def LengthsAvailable(self):
        return self.lengths_available

        # T.insert(END, "\nStock Code for " + Item + " is "  + str(Stock[i][j+4]))                        
        # T.insert(END, "\nStockcodes for " + self.material + "Are:" + str(Stock[i][5]))


def PrintWorksOrder():
    WorksOrderRow = 16

    # Blanks Works Order
    for i in range(13, 30):
        shtWorksOrder.cells(i, 2).value = None
        shtWorksOrder.cells(i, 6).value = None
        shtWorksOrder.cells(i, 11).value = None
        shtWorksOrder.cells(i, 20).value = None

    for i in range(0, NumberOfItems + 15):

        for length in range(0, 5):
            # T.insert(END, "\nStock Code      " + str(Stock_[i].ReturnAmount(length)) + "  " + str(Stock_[i].material))
            if Stock_[i].ReturnAmount(length) != 0:
                shtWorksOrder.cells(WorksOrderRow, 2).value = str(Stock_[i].FindStockCode(length))
                shtWorksOrder.cells(WorksOrderRow, 6).value = Stock_[i].material
                shtWorksOrder.cells(WorksOrderRow, 11).value = Stock_[i].ReturnAmount(length)
                shtWorksOrder.cells(WorksOrderRow, 20).value = "Total Length of all parts are: " + str(
                    Stock_[i].totalsum[length])

                WorksOrderRow = WorksOrderRow + 1


# Below is for Ui
root = Tk()
# T = Text(root, height=200, width=200)
# T.pack()

# Define all the variables
TwoFive = 1
ThreeMeter = 0
FourMeter = 0
Offcuts = 0
Quantity = 0
Dims = 0
Thickness = 0

Stock_ = {}

wb = xw.Book('TWF 076 - ML production pack - Issue 16.xlsm')

shtDoNotEdit = wb.sheets['DO NOT EDIT']
shtGlazingBarCutting = wb.sheets['Glazing Bar Cutting']
shtGlazingForPaint = wb.sheets['Glazing for Paint']
shtWorksOrder = wb.sheets['Works Order']
shtInfo = wb.sheets['Info']

Stock = shtDoNotEdit.range("AJ73:AM80").value

# sets a array with all the data we require
Production_List = shtGlazingBarCutting.range("C10:P45").value
Info = shtInfo.range("C17").value

stocklengths = []

# Pre-Requesite, gets all the stockcodes that we requirea

NumberOfItems = len(Stock) - 1

for i in range(0, NumberOfItems):

    for j in range(1, 4):
        if Stock[i + 1][j] != None:
            stocklengths.append(Stock[0][j])

    Stock_[i] = Material(str(Stock[i + 1][0]), Stock[i + 1], stocklengths)
    stocklengths = []

for i in range(0, 15):

    # Checks if we're onto a new material

    if Production_List[i][1] == None:
        # if we are onto a new material, set all the variables back to 0
        Dims = 0
        FourMeter = 0
        SixMeter = 0
        Offcuts = 0

        # check length and see what lengths are availble to tuse to put in algorithm below
    # below is the algorithim to check what material we should use

    # Doesnt check the empty cells
    if Production_List[i][1] != None:

        Quantity = int(Production_List[i][9])

        Dims = int(Production_List[i][8])

        Quantity = round(Quantity / (1250 / int(Production_List[i][4])))

        ThreeMeter = ThreeMeter + (1 * float(Quantity))
        # we plus the 10 because its the tenth row
        shtGlazingBarCutting.cells(i + 10, 15).value = str(1 * int(Quantity)) + " x 3m"

        if Production_List[i][0] == "2mm":
            Stock_[1].AddAmount(float(Quantity), 0, Dims)

        elif Production_List[i][0] == "3mm":
            Stock_[4].AddAmount(float(Quantity), 0, Dims)
        else:
            shtGlazingBarCutting.cells(i + 10, 15).value = "Error - No Thickness Indicated"

        Dims = 0

        # Aluminium Gutter
        # if Info == "extruded aluminium":

        # Stock_[6].AddAmount(1, 0, 4000)

PrintWorksOrder()

# T.insert(END, "ESG?")
# # This is for the Ui As it above 

mainloop()

