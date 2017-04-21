'''
Created on 22 Mar 2017

@author: Luke
'''
import xlwings as xw

#from tkinter import *

class Material:

#TODO try and collate when there are multiple 3 quantities of 2.5m bits, e.g if we have a lot left over see if we can use another with a lot left over#
#TODO 292 it has 3m and 4m piece but code below only required either so it decides if its 6m aswell.
           
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

def LengthsToUse(Dims):
    
    if float(Dims) > 4050:
        return True
    if float(Dims) > 3025 and float(Dims) < 4050:
        return False
    else:
        return True
    
# Below is for Ui      
# root = Tk()
# T = Text(root, height=500, width=150)
# T.pack()

Stock_ = {}

wb = xw.Book('16594-1a-pack.xlsm')

shtDoNotEdit = wb.sheets['DO NOT EDIT']
shtStructureCutting = wb.sheets['Structure Cutting']
shtWorksOrder = wb.sheets['Works Order']

Stock = shtDoNotEdit.range("S74:AA85").value

# sets a array with all the data we require
Structure_List = shtStructureCutting.range("C10:I60").value

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
    
    for j in range (1, 8):
        if Stock[i + 1][j] != "n/a":
            stocklengths.append(Stock[0][j])

    Stock_[i] = Material(str(Stock[i + 1][0]), Stock[i + 1], stocklengths)
    stocklengths = []
    
# Define all the variables
ThreeMeter = 1
FourMeter = 0
SixMeter = 0
SevenMeter = 0
Offcuts = 0
WorksOrderRow = 16
Quantity = 0
Dims = 0


# Gets data from Structure Cutting Sheett
for i in range (0, 45):
    
    # Checks if we're onto a new material
    if Structure_List[i][0] != Structure_List[i - 1][0] and i > 0:
        if Structure_List[i + 1][0] == None:
            
            # if we are onto a new material, set all the variables back to 0               
            Dims = 0
            FourMeter = 0
            SixMeter = 0
            Offcuts = 0    

    # check length and see what lengths are availble to tuse to put in algorithm below
# below is the algorithim to check what material we should use

# Doesnt check the empty cells
    if Structure_List[i][3] != None:
        
        Quantity = Structure_List[i][6]


        # if less than 2 m but we can get them out of a 6m piece
        if Structure_List[i][3] < 2000 and Structure_List[i][3] > 1525:
            if Quantity > 1:
                Dims = 2 * int(Structure_List[i][3])
                Quantity = Quantity / 2
    
    # creates a Dims of the lenghts which we will use
        else:
            Dims = int(Structure_List[i][3])
            
            #if there are any small pieces, see if there is a big quantity of them and multiply them
            if Quantity > 1 and Dims < 1500:
                Dims = Quantity * Dims
                Quantity = Quantity/2
                
     
     
# we only use the following for equation for lengths between 4 & 6m       
    for n in range (0, NumberOfItems):

        if Structure_List[i][0] == Stock_[n].material:
            if 4050 in Stock_[n].LengthsAvailable() or 6050 in Stock_[n].LengthsAvailable():        
        # returns false if we can use a 4m piece
                if LengthsToUse(str(Dims)) == False:
                    
                    FourMeter = FourMeter + (1 * float(Quantity))
                    # we plus the 10 because its the tenth row
                    shtStructureCutting.cells(i + 10, 7).value = str(1 * int(Quantity)) + " x 4m"
                    
                    for m in range (0, NumberOfItems):                           
                        if Stock_[m].material == str(Structure_List[i][0]):
                            Stock_[m].AddAmount(float(Quantity), 4, Dims)
                    
                    Dims = 0 
                    
                    # return true if we can use a 6m piiece
                elif LengthsToUse(Dims) == True:
                        
                        # checks if we can use offcuts or not because it checks for stuff less than 3m as well as greater than 4m
                    if (Dims < 6050 and Dims > 4050): 
            
                        for m in range (0, NumberOfItems):                           
                            if Stock_[m].material == str(Structure_List[i][0]):
                                Stock_[m].AddAmount(float(Quantity), 6, Dims)
                
                        SixMeter = SixMeter + (1 * float(Quantity))
                        shtStructureCutting.cells(i + 10, 7).value = str(1 * int(Quantity)) + " x 6m"
                        
                        Dims = 0
                    
                    # #try to minimize the use of offcuts, if sum of quantity x length is bettween if statement, use 4m
                    elif (Dims * float(Quantity)) < 4050 and (Dims * float(Quantity)) > 3000:
                        
                        Quantity = round(Quantity / 2) 
            
                        FourMeter = FourMeter + (1 * float(Quantity))
                        shtStructureCutting.cells(i + 10, 7).value = str(1 * int(Quantity)) + " x 4m"
                        
                        for m in range (0, NumberOfItems):                           
                            if Stock_[m].material == str(Structure_List[i][0]):
                                Stock_[m].AddAmount(float(Quantity*2), 4, Dims)
                                
                        Dims = 0
                        
#TODO Merge cells with the one below it if it equals 0.5
                    #use 6 for case below   
                    elif (Dims) < 3025 and (Dims) > 2025:
                        
                        Quantity = round(Quantity / 2) + 0.5
                        
                        if Quantity > 0.99:
                            Quantity -= 0.5
            
                        SixMeter = SixMeter + (1 * float(Quantity))
                        shtStructureCutting.cells(i + 10, 7).value = str(1 * float(Quantity)) + " x 6m"
                        
                        for m in range (0, NumberOfItems):                           
                            if Stock_[m].material == str(Structure_List[i][0]):
                                Stock_[m].AddAmount(float(Quantity), 6, Dims)
                                
                        Dims = 0
                        
                    else:
                        
                        Offcuts = Offcuts + Dims
                        shtStructureCutting.cells(i + 10, 7).value = "Offcut"
                        
# everything below here will be for different lengths           
            else:
                
                # Seven Meters
                
                for m in range (0, NumberOfItems):                           
                    if Stock_[m].material == str(Structure_List[i][0]):
                        
                        # if we can get 2 out of a 7m piece
                        if Dims < 3535:
                            Quantity = Quantity / 2
                            
                        Stock_[m].AddAmount(float(Quantity), 7, Dims)
                        shtStructureCutting.cells(i + 10, 7).value = str(1 * int(Quantity)) + " x 7m"

        elif  Structure_List[i][0] != None and   Structure_List[i][0] not in StockList:
            shtStructureCutting.cells(i + 10, 7).value = "Item not in Stock List"

#Blanks Works Order
for i in range (13, 30):

    shtWorksOrder.cells(i, 2).value = None
    shtWorksOrder.cells(i, 6).value = None
    shtWorksOrder.cells(i, 11).value = None
    shtWorksOrder.cells(i, 20).value = None

for i in range (0, NumberOfItems):

    for length in range (0, 8):
        #T.insert(END, "\nStock Code      " + str(Stock_[i].ReturnAmount(length)) + "  " + str(Stock_[i].material))     
        if Stock_[i].ReturnAmount(length) != 0:

                                   
            shtWorksOrder.cells(WorksOrderRow, 2).value = str(Stock_[i].FindStockCode(length))
            shtWorksOrder.cells(WorksOrderRow, 6).value = str(length) + "m " + Stock_[i].material
            shtWorksOrder.cells(WorksOrderRow, 11).value = Stock_[i].ReturnAmount(length)
            shtWorksOrder.cells(WorksOrderRow, 20).value = "Total Length of all parts are: " + str(Stock_[i].totalsum[length])       
            
            WorksOrderRow = WorksOrderRow + 1
            

#T.insert(END, "Stock Code for 75x75 Aluminium Box is " + str(Stock))
# # This is for the Ui As it above 
  
#ainloop()
