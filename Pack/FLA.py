'''
Created on 22 Mar 2017

@author: Luke
'''
import xlwings as xw

from tkinter import *


class Material:

#TODO add ESG if required
#TODO add gutter bits
#TODO add more types of stock
           
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

    def FindStockCode (self, length):
        
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

    for i in range(0, NumberOfItems+15):

        for length in range(0, 5):
            # T.insert(END, "\nStock Code      " + str(Stock_[i].ReturnAmount(length)) + "  " + str(Stock_[i].material))
            if Stock_[i].ReturnAmount(length) != 0:
                shtWorksOrder.cells(WorksOrderRow, 2).value = str(Stock_[i].FindStockCode(length))
                shtWorksOrder.cells(WorksOrderRow, 6).value = Stock_[i].material
                shtWorksOrder.cells(WorksOrderRow, 11).value = Stock_[i].ReturnAmount(length)
                shtWorksOrder.cells(WorksOrderRow, 20).value = "Total Length of all parts are: " + str(Stock_[i].totalsum[length])

                WorksOrderRow = WorksOrderRow + 1

#Below is for Ui
root = Tk()
#T = Text(root, height=200, width=200)
#T.pack()

# Define all the variables
TwoFive = 1
ThreeMeter = 0
FourMeter = 0
Offcuts = 0
Quantity = 0
Dims = 0
ESGButtonYes = {}
ESGButtonNo = {}
Thickness = 0

def ESGYES(i, Amount):
    print("Yes!!")
    shtPressingforPaint.cells(i + 10, 16).value = "Yes - " + Pressings_List[i][0]
    Stock_[5].AddAmount(float(Amount), 0, 3000)
    PrintWorksOrder()

    #Hide the button
    ESGButtonYes[i].pack_forget()
    ESGButtonNo[i].pack_forget()

def ESGNO(i):
    print ("No")
    shtPressingforPaint.cells(i + 10, 16).value = "No - " + Pressings_List[i][0]
    PrintWorksOrder()

    #Hides the button
    ESGButtonYes[i].pack_forget()
    ESGButtonNo[i].pack_forget()

Stock_ = {}

wb = xw.Book('TWF 076 - ML production pack - Issue 16.xlsm')

shtDoNotEdit = wb.sheets['DO NOT EDIT']
shtPressingforPaint = wb.sheets['Pressings for Paint']
shtWorksOrder = wb.sheets['Works Order']
shtInfo = wb.sheets['Info']

Stock = shtDoNotEdit.range("AJ73:AM80").value

# sets a array with all the data we require
Pressings_List = shtPressingforPaint.range("C10:P45").value
Info = shtInfo.range("C17").value

stocklengths = []

# TODO: Check for which stock codes to use and then decide whether or not to use them. Search for them in the table and decide whether true or false, if to use them or not
# Pre-Requesite, gets all the stockcodes that we requirea

NumberOfItems = len(Stock)-1

for i in range (0, NumberOfItems):

    for j in range (1, 4):
        if Stock[i + 1][j] != None:
            stocklengths.append(Stock[0][j])

    Stock_[i] = Material(str(Stock[i + 1][0]), Stock[i + 1], stocklengths)
    stocklengths = []

#Below adds all the information for the extruded gutter into the class

if Info == "extruded aluminium":
    for i in range (NumberOfItems, NumberOfItems+15):

        if Pressings_List[i+NumberOfItems+4][9] != None:

            if int(Pressings_List[i+NumberOfItems+4][9]) > 0:

                Quantity = int(Pressings_List[i+NumberOfItems+4][9])

                Stock_[i] = Material(str(Pressings_List[i+NumberOfItems+4][0]), "StockCode", 0)
                Stock_[i].AddAmount(Quantity, 1, 1)


#Makes sure something still gets added to the Stock class in icremental order, otherwise the pritnworksroder funcation will not work, as it checks the stock in icremental order
            else:

                Stock_[i] = Material(str(Pressings_List[i + NumberOfItems + 4][0]), "StockCode", 0)
                Stock_[i].AddAmount(0, 0, 0)
        else:

            Stock_[i] = Material(str(Pressings_List[i + NumberOfItems + 4][0]), "StockCode", 0)
            Stock_[i].AddAmount(0, 0, 0)

for i in range (0, 15):
    
    # Checks if we're onto a new material

    if Pressings_List[i][1] == None:

        # if we are onto a new material, set all the variables back to 0
        Dims = 0
        FourMeter = 0
        SixMeter = 0
        Offcuts = 0

    # check length and see what lengths are availble to tuse to put in algorithm below
# below is the algorithim to check what material we should use

# Doesnt check the empty cells
    if Pressings_List[i][1] != None:

        Quantity = int(Pressings_List[i][9])

        Dims = int(Pressings_List[i][8])

        Quantity = round(Quantity /(1250/int(Pressings_List[i][4])))

        ThreeMeter = ThreeMeter + (1 * float(Quantity))
        # we plus the 10 because its the tenth row
        shtPressingforPaint.cells(i + 10, 15).value = str(1 * int(Quantity)) + " x 3m"

        if Pressings_List[i][0] == "2mm":
            Stock_[1].AddAmount(float(Quantity), 0, Dims)

        elif Pressings_List[i][0] == "3mm":
            Stock_[4].AddAmount(float(Quantity), 0, Dims)
        else:
            shtPressingforPaint.cells(i + 10, 15).value = "Error - No Thickness Indicated"

        Dims = 0

        ESGLabel = Label(root, text="Do you want ESG with this with " + str(Pressings_List[i][0]) + " " + Pressings_List[i][1])

        # the i=i lambda is only declared after all the code is ran, therefore 'i' takes the last value of the while statement
        # therefore we need to declare i after lambda
        ESGButtonYes[i] = Button(root, text="Yes", command=lambda i=i: ESGYES(i, Quantity))
        ESGButtonNo[i] = Button(root, text="No", command=lambda i=i: ESGNO(i))

        ESGLabel.pack()

        ESGButtonYes[i].pack()
        ESGButtonNo[i].pack()

#Aluminium Gutter
#if Info == "extruded aluminium":

    #Stock_[6].AddAmount(1, 0, 4000)

PrintWorksOrder()

#T.insert(END, "ESG?")
# # This is for the Ui As it above 

mainloop()

