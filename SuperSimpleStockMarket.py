# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:09:10 2016

@author: Agustin Canavari
"""

class StockElement:
  symbol_=""
  properties_={} # key:value array
  
def calculateDividendYield(stockElement, price):
  if stockElement.properties_['Type'] == "Common":
      divYield = float(stockElement.properties_['Last Dividend'])/price
      print(stockElement.properties_['Last Dividend'])
  else:
    divYield = float(stockElement.properties_['Fixed Dividend'])*float(stockElement.properties_['Par Value'])/price
    print(stockElement.properties_['Fixed Dividend'])
    print("else")
  return divYield

def calculatePERatio(stockElement, price):
  return price/float(stockElement.properties_['Last Dividend'])

def parseLines(lines, propertyList):
  stockArray = []
  for line in lines:    
    lineContent = line.rstrip().split(";") #Parsing the line in an array     
    stockElementAux = StockElement() #Create object
    stockElementAux.symbol_ = (lineContent[0]) #Load symbol
    symbolArray.append(stockElementAux.symbol_) #Load symbol into a global array
    for i in range(1,len(lineContent)):
      stockElementAux.properties_[propertyList[i]] = lineContent[i] #Load properties
    print(stockElementAux.properties_)
    stockArray.append(stockElementAux)
  return stockArray
  
def loadStocks():
  StockInputs=input("Please select path for a stocks CSV file \n(test file's path is: './Inputs/Stock_inputs_test.csv'): ")
  with open(StockInputs, 'r') as f:
    #CSV file is assumed to contain no errors  
    propertyList = f.readline().rstrip().split(";") #Load list of properties
    stockArray = parseLines(f.readlines(),propertyList) #Load all stocks  
    print ("Stocks correctly loaded from file\n")
  return stockArray
          
   
if __name__ == '__main__':
    
    stockArray = None
    symbolArray = []
    tradeRecordArray = None    
    mainMenu = {}
    mainMenu['1']="Load stocks." 
    mainMenu['2']="Select stock to operate."
    mainMenu['3']="Calculate GBCE"
    mainMenu['4']="Exit"
    while True: 
      options=list(mainMenu.keys())
      options.sort()
      for entry in options: 
        print (entry, mainMenu[entry])
      selection=input("Please Select an option from the menu: ") 
      if selection =='1':
        #Load stocks  
        if stockArray == None:  
          stockArray=loadStocks()  
        else:
          while True:  
            answer=input("Loading a new file will erase previous information, do you want to continue? (y/n): ") 
            if answer=='y':
              stockArray=loadStocks()
            elif answer=='n':
              break
            else:
              print("Unkwon option selected!")    
      elif selection == '2':  
        #Select a stock to operate with  
        if stockArray==None:
          print ("First you must load stocks to operate with\n")
        else:
          selectedStock=input("Select a stock to operate on\n(test stocks are TEA/POP/ALE/GIN/JOE): ")  
          if selectedStock in symbolArray:
            operationsMenu = {}
            operationsMenu['1']="Calculate the dividend yield."
            operationsMenu['2']="Calculate the P/E Ratio."
            operationsMenu['3']="Record a trade."
            operationsMenu['4']="Calculate Volume Weighted Stock Price."
            operationsMenu['5']="Go back."
            while True: 
              options=list(operationsMenu.keys())
              options.sort()
              for entry in options: 
                print (entry, operationsMenu[entry])
              selection=input("Please Select an option from the menu: ")
          else:
            print("Entered symbol is non existent. Please try again")    
            
            
      elif selection == '3':
        #Calculate GBCE  
        print ("find") 
      elif selection == '4': 
        #End program  
        print("Program terminated")
        break
      else: 
        print ("Unknown option selected!") 
        
