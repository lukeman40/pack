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
        
    def ReturnAmount(self, length):
        
        return self.amount[length]
    
    def ReturnSum(self, length):
        
        return self.totalsum[length]
    
    def LengthsAvailable(self):
        
        return self.lengths_available
        
            # T.insert(END, "\nStock Code for " + Item + " is "  + str(Stock[i][j+4]))                        
        # T.insert(END, "\nStockcodes for " + self.material + "Are:" + str(Stock[i][5]))

#Below is for Ui
root = Tk()
#T = Text(root, height=200, width=200)
#T.pack()

def ESGYES():
    print("Yes!!")

def ESGNO():
    print ("No")
    ESGButtonNo.unpack()




Stock_ = {}

wb = xw.Book('TWF 076 - ML production pack - Issue 16.xlsm')

shtDoNotEdit = wb.sheets['DO NOT EDIT']
shtPressingforPaint = wb.sheets['Pressings for Paint']
shtWorksOrder = wb.sheets['Works Order']

Stock = shtDoNotEdit.range("AJ73:AM80").value

# sets a array with all the data we require
Pressings_List = shtPressingforPaint.range("C10:P45").value

stocklengths = []

# ## Fucntion below removed all the test in the list. Its fucks getting my stock code up tho
# for i in range (6,0, -1):
#     
#     for j in range (6,0, -1):
#         if Stock[i][j] == "test":
#             del Stock[i][j]

# TODO: Check for which stock codes to use and then decide whether or not to use them. Search for them in the table and decide whether true or false, if to use them or not
# Pre-Requesite, gets all the stockcodes that we requirea

NumberOfItems = len(Stock)-1

StockList = []

for i in range (0, NumberOfItems):
    StockList.append(Stock[i][0])

for i in range (0, NumberOfItems):
    
    for j in range (1, 4):
        if Stock[i + 1][j] != None:
            stocklengths.append(Stock[0][j])

    Stock_[i] = Material(str(Stock[i + 1][0]), Stock[i + 1], stocklengths)
    stocklengths = []
    
# Define all the variables
TwoFive = 1
ThreeMeter = 0
FourMeter = 0
Offcuts = 0
WorksOrderRow = 16
Quantity = 0
Dims = 0


for i in range (0, 10):
    
    # Checks if we're onto a new material

    if Pressings_List[i][0] == None:

        # if we are onto a new material, set all the variables back to 0
        Dims = 0
        FourMeter = 0
        SixMeter = 0
        Offcuts = 0

    # check length and see what lengths are availble to tuse to put in algorithm below
# below is the algorithim to check what material we should use

# Doesnt check the empty cells
    if Pressings_List[i][0] != None:

        ESGLabel = Label(root, text="Do you want ESG with this with " + Pressings_List[i][0])

        ESGButtonYes = Button(root, text="Yes", command=ESGYES)
        ESGButtonNo = Button(root, text="No", command=ESGNO)

        ESGLabel.pack()
        ESGButtonYes.pack()
        ESGButtonNo.pack()
        
        Quantity = int(Pressings_List[i][9])

        Dims = int(Pressings_List[i][8])

        Quantity = round(Quantity /(1250/int(Pressings_List[i][4])))

        ThreeMeter = ThreeMeter + (1 * float(Quantity))
        # we plus the 10 because its the tenth row
        shtPressingforPaint.cells(i + 10, 15).value = str(1 * int(Quantity)) + " x 3m"


        Stock_[4].AddAmount(float(Quantity), 0, Dims)

        Dims = 0

#Blanks Works Order
for i in range (13, 30):

    shtWorksOrder.cells(i, 2).value = None
    shtWorksOrder.cells(i, 6).value = None
    shtWorksOrder.cells(i, 11).value = None
    shtWorksOrder.cells(i, 20).value = None


for i in range(0, NumberOfItems):

    for length in range(0, 8):
        # T.insert(END, "\nStock Code      " + str(Stock_[i].ReturnAmount(length)) + "  " + str(Stock_[i].material))
        if Stock_[i].ReturnAmount(length) != 0:
            shtWorksOrder.cells(WorksOrderRow, 2).value = str(Stock_[i].FindStockCode(length))
            shtWorksOrder.cells(WorksOrderRow, 6).value = str(length) + "m " + Stock_[i].material
            shtWorksOrder.cells(WorksOrderRow, 11).value = Stock_[i].ReturnAmount(length)
            shtWorksOrder.cells(WorksOrderRow, 20).value = "Total Length of all parts are: " + str(Stock_[i].totalsum[length])

            WorksOrderRow = WorksOrderRow + 1



#T.insert(END, "ESG?")
# # This is for the Ui As it above 
  
mainloop()