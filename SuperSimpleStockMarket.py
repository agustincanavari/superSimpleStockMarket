# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:09:10 2016

@author: Agustin Canavari
"""
import time
DEFAULT_TIME_MINUTES = 5

class StockElement:
  symbol_=""
  properties_={} # key:value array
  
class Trade:
  symbol_=""
  timestamp_= None
  quantity_= None
  bs_= None
  price_= None    
  
def calculateDividendYield(stockElement, price):
  #Receives a StockElemente object and a price
  #Returns the value of Dividend Yield  
  if stockElement.properties_['Type'] == "Common":
      divYield = float(stockElement.properties_['Last Dividend'])/price
  else:
    divYield = float(stockElement.properties_['Fixed Dividend'])*float(stockElement.properties_['Par Value'])/price
  return divYield

def calculatePERatio(stockElement, price):
  #Receives a StockElemente object and a price
  #Returns the value of P/E Ratio     
  return price/float(stockElement.properties_['Last Dividend'])
  
def calculateVWSP(tradesArray):
  #Receives an array with Trade objects
  #Returns the value of the VWSP
  num = den = 0  
  for i in range(0,len(tradesArray)):
    num+= tradesArray[i].quantity_*tradesArray[i].price_
    den+= tradesArray[i].quantity
  return num/den   
    
def calculateGBCE(volumesArray):
  #Receives an array
  #Returns the geometric mean  
  n = len(volumesArray)
  p = 1
  for i in range(0, n):
    p *= volumesArray(i)
  return p^(1/n)           

def parseLines(lines, propertyList):
  #Receives all lines in a file and a list of properties to save
  #Returns an array with all stocks  
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
  #Loads user's input for file path and calls parseLines() to save stocks to an array
  #Returns stockArray  
  StockInputs=input("Please select path for a stocks CSV file \n(test file's path is: './Inputs/Stock_inputs_test.csv'): ")
  with open(StockInputs, 'r') as f:
    #CSV file is assumed to contain no errors or duplicates 
    propertyList = f.readline().rstrip().split(";") #Read list of properties
    stockArray = parseLines(f.readlines(),propertyList) #Read all stocks  
    for element in stockArray:
      showStock(element)    
  return stockArray
  
def extractTradesSymbol(tradesArray, stock):
  #Receives an array of Trade objects and a stock's symbol
  #Returns an array of Trades corresponding to that stock's symbol  
  tradesAux = [None]  
  for i in range(0, len(tradesArray)):
    if tradesArray[i].symbol_ == stock:
      tradesAux.append(tradesArray[i])
  return tradesAux 

def extractTradesTime(tradesArray, minutes):
  #Receives an array of Trade objects and a time in minutes
  #Returns an array of Trades in the last 'x' minutes     
  tradesAux = [None]
  for i in range(0, len(tradesArray)):
    if (time.time() - tradesArray[i].timestamp_) <= minutes*60 :
      tradesAux.append(tradesArray[i])
  return tradesAux    
   
def showTrade(record):
  print(record.symbol_)
  print(record.bs_)
  print(record.quantity_)
  print(record.price_)
  print(record.timestamp_)   

def showStock(stockElement):
  print (stockElement.symbol_)
  print (stockElement.properties_)    
   
if __name__ == '__main__':
    
    stockArray = [None]
    symbolArray = [None]
    tradeRecordArray = [None]    
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
        if stockArray == [None]:  
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
        if stockArray == [None]:
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
              selection=input("Please Select an operation from the menu: ")
              if selection == '1':
                #Calculate div.yield      
                for i in range(0,len(stockArray)):
                  if selectedStock == stockArray[i].symbol_:
                    stockElementAux = stockArray[i]
                    break
                price = input("Enter the price for the dividend yield calculation: ")
                print("Result is: ",calculateDividendYield(stockElementAux, float(price)))
              elif selection == '2':
                #Calculate P/E Ratio
                for i in range(0,len(stockArray)):
                  if selectedStock == stockArray[i].symbol_:
                    stockElementAux = stockArray[i]
                    break
                price = input("Enter the price for the dividend yield calculation: ")
                print("Result is: ",calculatePERatio(stockElementAux, float(price)))
                print("peratio")
              elif selection == '3':
                #Record a trade
                tradeElementAux = Trade() #Create an object
                tradeElementAux.symbol_ = selectedStock
                bs = input("Enter 'b' for buy or 's' for sell: ")
                while bs != 'b' and bs != 's':
                  bs = input("Please enter only 'b' or 's' for buy or sell: ")  
                tradeElementAux.bs_ = bs #Assign value for buy or sell indicator  
                quantity = int(input("Enter the quantity to buy or sell: "))
                while (not isinstance(quantity,int)) or quantity <= 0:
                  quantity = input("Please enter only positive integers for this value: ")
                tradeElementAux.quantity_ = quantity #Assign value for quantity    
                price = float(input("Enter price of the operation: "))
                while (not isinstance(price,float)) or price <= 0:
                  price = input("Please enter only positive floats for this value: ")
                tradeElementAux.price_ = price #Assign value for price
                tradeElementAux.timestamp_ = time.time()
                tradeRecordArray.append(tradeElementAux)
                showTrade(tradeElementAux)
                showTrade(tradeRecordArray[0])
                print("Recorded trade succesfully\n")
              elif selection == '4':  
                #Calculate VWSP
                tradesAux = extractTradesSymbol(tradeRecordArray, selectedStock)
                if len(tradesAux) <= 0:
                  print("Please record trades for this stock before trying to obtain VWSP")
                else:
                  tradesAux = extractTradesTime(tradesAux,DEFAULT_TIME_MINUTES)
                  if len(tradesAux) <= 0:
                    print("There are no records in under 5 minutes for this stock")
                  else:
                    print("VWSP is: ", calculateVWSP(tradesAux))    
              elif selection == '5':
                break     
              else:
                print("Unkown option selected!")    
          else:
            print("Entered stock is not an option. Please try again")               
            
      elif selection == '3':
        #Calculate GBCE
        if stockArray == [None]:
          print ("First you must load stocks to operate with\n")
        else:
          if tradeRecordArray == [None]:
            print("First you must record Trades\n")
          else:  
            volumeWSP = [None] 
            for i in range(0, len(stockArray)):
              tradesAux = extractTradesSymbol(tradeRecordArray, stockArray[i].symbol_)
              if len(tradesAux) > 0:
                volumeWSP.append(calculateVWSP(tradesAux)) 
            print("GBCE is: ", calculateGBCE(volumeWSP))
      elif selection == '4': 
        #End program  
        print("Program terminated")
        break
      else: 
        print ("Unknown option selected!") 
        
