# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:09:10 2016

@author: Agustin Canavari
"""

STOCK_INPUTS='./Inputs/Stock_inputs.csv'

class StockElement:
	symbol_=""
	properties_=[] # key:value array

def parseLines(lines):  
	stockArray=[]
	for line in lines:
		#Parsing the line in an array
		lineContent=line.strip("\n").split(";")
		print ("lineContent")
		#Create object 		
		stockElementAux = StockElement()
		stockElementAux.symbol_ = lineContent[0]
		for i in range(1,len(lineContent)):
			stockElementAux.properties_.push(lineContent[i])
           stockArray.push(stockElementAux)

if __name__ == '__main__':
	with open(STOCK_INPUTS, 'r') as f:
		parseLines(f.readlines())