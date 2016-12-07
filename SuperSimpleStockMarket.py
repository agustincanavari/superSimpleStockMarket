# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:09:10 2016

@author: Agustin Canavari
"""
import time
import csv
DEFAULT_TIME_MINUTES = 5

class StockElement:
  symbol_=""
  properties_={} # key:value array
  
  def __init__(self, symbol,properties):
    self.symbol_ = symbol
    self.properties_ = properties  
  
class Trade:
  symbol_=""
  timestamp_= None
  quantity_= None
  bs_= None
  price_= None

  def __init__(self, symbol, timestamp, quantity, bs, price):
    self.symbol_ = symbol
    self.timestamp_ = timestamp
    self.quantity_ = quantity
    self.bs_ = bs
    self.price_ = price    
  
def calculateDividendYield(stockElement, price):
  #Receives a StockElemente object and a price
  #Returns the value of Dividend Yield  
  if stockElement.properties_['Type'] == "Common":
      divYield = float(stockElement.properties_['Last Dividend'])/price
  else:
    divYield = float(stockElement.properties_['Fixed Dividend'].strip("%"))*float(stockElement.properties_['Par Value'])/(100*price)
  return divYield

def calculatePERatio(stockElement, price):
  #Receives a StockElemente object and a price
  #Returns the value of P/E Ratio 
  if float(stockElement.properties_['Last Dividend']) == 0:
    return ("Last Dividend is 0, P/E Ratio can not be computed\n")
  else:    
    return price/float(stockElement.properties_['Last Dividend'])
  
def calculateVWSP(tradesArray):
  #Receives an array with Trade objects
  #Returns the value of the VWSP
  num = den = 0  
  for i in range(0,len(tradesArray)):
    num+= tradesArray[i].quantity_*tradesArray[i].price_
    den+= tradesArray[i].quantity_
  return num/den   
    
def calculateGBCE(volumesArray):
  #Receives an array
  #Returns the geometric mean  
  n = len(volumesArray)
  p = 1
  for i in range(0, n):
    p *= volumesArray[i]
  return pow(p,1/n)           
    
def loadStocks():
  #Loads user's input for file path and calls parseLines() to save stocks to an array
  #Returns stockArray
  #Symbol's name is assumed to be 'Stock Symbol'
  stockArrayAux = []  
  StockInputs=input("Please select path for a stocks CSV file \n(test file's path is: './Inputs/Stock_inputs_test.csv'): ")
  with open(StockInputs, 'r') as inputFile:
    inputRows = csv.DictReader(inputFile, delimiter=';')
    for row in inputRows:
      symbol=row['Stock Symbol']
      symbolArray.append(symbol)
      del row['Stock Symbol']
      stockArrayAux.append(StockElement(symbol, dict(row)))  
    print("Stocks loaded succesfully\n")  
  return stockArrayAux  
  
def extractTradesSymbol(tradesArray, stock):
  #Receives an array of Trade objects and a stock's symbol
  #Returns an array of Trades corresponding to that stock's symbol  
  tradesAux = []
  showTradeArray(tradesArray)  
  for i in range(0, len(tradesArray)):
    if tradesArray[i].symbol_ == stock:
      tradesAux.append(tradesArray[i])
  showTradeArray(tradesAux)    
  return tradesAux 

def extractTradesTime(tradesArray, minutes):
  #Receives an array of Trade objects and a time in minutes
  #Returns an array of Trades in the last 'x' minutes     
  tradesAux = []
  showTradeArray(tradesArray)
  for i in range(0, len(tradesArray)):
    if (time.time() - tradesArray[i].timestamp_) <= minutes*60 :
      tradesAux.append(tradesArray[i])
  showTradeArray(tradesAux)    
  return tradesAux    
   
def showTradeArray(array):
  #Prints values of a trade array  
  for record in array:
    showTrade(record)    
  
def showTrade(record):
  #Prints values of a trade 
  print(record.symbol_)
  print(record.bs_)
  print(record.quantity_)
  print(record.price_)
  print(record.timestamp_)   

def showStockArray(stockArrayAux):
  #prints values of a stockElement array 
  for stockElement in stockArrayAux:
    showStock(stockElement)    
  
def showStock(stockElement):
  #Prints values of a stockElement  
  print (stockElement.symbol_)
  print (stockElement.properties_)    
   
if __name__ == '__main__':
    
    #Data arrays
    stockArray = []
    symbolArray = []
    tradeRecordArray = []    

    mainMenu = {}
    mainMenu['1']="Load stocks." 
    mainMenu['2']="Select stock to operate."
    mainMenu['3']="Calculate GBCE"
    mainMenu['4']="Exit"
    while True: 
      options=list(mainMenu.keys())
      options.sort()
      for entry in options:
        print("\n")  
        print (entry, mainMenu[entry])
      selection=input("Please Select an option from the menu: ") 
      if selection =='1':
        #Load stocks  
        if len(stockArray) == 0:  
          stockArray=loadStocks()  
        else:
          answer=input("Loading a new file will erase previous information, do you want to continue? (y/n): ")
          while answer not in ['y','n']:
            answer = input("Please enter only 'y' or 'n' for yess or no: ")
          if answer=='y':
            stockArray=loadStocks()
          elif answer=='n':
            break
      elif selection == '2':  
        #Select a stock to operate with  
        if len(stockArray) == 0:
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
                print("\n")  
                print (entry, operationsMenu[entry])
              selection=input("Please Select an operation from the menu: ")
              if selection == '1':
                #Calculate div.yield      
                for i in range(0,len(stockArray)):
                  if selectedStock == stockArray[i].symbol_:
                    stockElementAux = stockArray[i]
                    break
                while True:
                  try:
                    price = float(input("Enter price for the dividend yield calculation: "))    
                  except ValueError:
                    print("Please check the quantity you are entering is a float ")
                    continue
                  else:
                    if price <= 0:
                      print("Please enter a positive price")  
                      continue
                    else:
                      break    
                print("Result is: ",calculateDividendYield(stockElementAux, float(price)))
              elif selection == '2':
                #Calculate P/E Ratio
                for i in range(0,len(stockArray)):
                  if selectedStock == stockArray[i].symbol_:
                    stockElementAux = stockArray[i]
                    break
                while True:
                  try:
                    price = float(input("Enter price for the P/E Ratio calculation: "))    
                  except ValueError:
                    print("Please check the quantity you are entering is a float ")
                    continue
                  else:
                    if price <= 0:
                      print("Please enter a positive price")  
                      continue
                    else:
                      break    
                print("Result is: ",calculatePERatio(stockElementAux, float(price)))
              elif selection == '3':
                #Record a trade                
                bs = input("Enter 'b' for buy or 's' for sell: ")
                while bs not in ['b','s']:
                  bs = input("Please enter only 'b' or 's' for buy or sell: ")  
                while True:
                  try:
                    quantity = int(input("Enter the quantity to buy or sell: "))    
                  except ValueError:
                    print("Please check the quantity you are entering is an integer ")
                    continue
                  else:
                    if quantity <= 0:
                      print("Please check the quantity you are entering is positive")
                      continue
                    else:
                      break
                while True:
                  try:
                    price = float(input("Enter price of the operation: "))    
                  except ValueError:
                    print("Please check the quantity you are entering is a float ")
                    continue
                  else:
                    if price <= 0:
                      print("Please enter a positive price")  
                      continue
                    else:
                      break    
                tradeRecordArray.append(Trade(selectedStock, time.time(), quantity, bs, price))
                tradeAux = Trade(selectedStock, time.time(), quantity, bs, price)
                showTrade(tradeAux)
                print(len(tradeRecordArray))
                showTradeArray(tradeRecordArray)
                print("Recorded trade succesfully\n")
              elif selection == '4':  
                #Calculate VWSP
                tradesAux = extractTradesSymbol(tradeRecordArray, selectedStock)
                if len(tradesAux) == 0:
                  print("Please record trades for this stock before trying to obtain VWSP")
                else:
                  tradesAux = extractTradesTime(tradesAux,DEFAULT_TIME_MINUTES)
                  if len(tradesAux) == 0:
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
        if len(stockArray) == 0:
          print ("First you must load stocks to operate with\n")
        else:
          if len(tradeRecordArray) == 0:
            print("First you must record Trades\n")
          else:  
            volumeWSP = [] 
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
        
