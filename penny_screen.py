import csv
import matplotlib.pyplot as plt
import datetime
import matplotlib
import matplotlib.dates as dates
import screen_helper
import stock_screener
import requests
import time
import random
import screen_helper
from requests.exceptions import Timeout



def p_screen(ticker):

    path = 'https://finance.yahoo.com/quote/' + ticker + '/?p=' + ticker
    Bool_except = 0
    try:
        
        x = requests.get(path, timeout=2)
        
    except Timeout as ex:
        
        print("Exception Riased: ", ticker)
        Bool_except = 1
    
    while Bool_except:
     
        try:
            x = requests.get(path, timeout=2)
            Bool_except = 0
            
        except Timeout as ex:
            
            print("Exception Raised: ", ticker)
            Bool_except = 1
        
        
        
        
        
    
    str_x = x.text
    
    find = str_x.find('Open')
    
    #makes a substring
    subx = str_x[find:find+8000]
    
    
    #looks for a unique identifyer in the code
    val = subx.find('data-test="OPEN-value')
    
    #makes a much smaller substring
    sub = subx[val+50:val+150]
    
    #finds the indexes for the value we are looking for
    begin = sub.find('>')
    
    begin+=1
    
    end = sub.find('<')
    
    str_price = sub[begin:end]
    
    price = str_price.replace(',','')
    
    #price = float(price)
    
    return(price)

def full_screen(price_limit = 10):
    
    file = open(r"NYSE.txt",'r')
    
    our_list = []
    
    penny_stocks = []
    
    print('Ticker, price')
    
    for line in file:
        
        #dont need the first line for our purposes
        if 'Symbol' in line:
            
            continue
        
        this_line = line
        
        ticker = this_line.rsplit('\t',1)[0]
        
        #gets a list of stock tickers
        our_list.append(ticker)    
    
    
    
    
        
    for tick in our_list:
        
        if '-' in tick or '.' in tick or 'ARA' in tick or 'PE' in tick or 'WOW' in tick:
            continue
        
        try:
            price = p_screen(tick)
        except:
            print("Exception Raised: ", tick)
        print(tick,price)
        
        try:
            if float(price) < 10:
                #print(tick,price)
                penny_stocks.append((tick, price))
        
        except:
            print('tick', 'fuck it')
            
    file1 = open(r"Penny_screen.txt",'w')
    
    for line in penny_stocks:
        
        file1.write(str(line)+'\n')   
    
    file1.close()
    file.close()
          
    
    
    
def options_screen(ticker):
    
    path = 'https://finance.yahoo.com/quote/' + ticker + '/options?p=' + ticker
    Bool_except = 0
    try:
        
        x = requests.get(path, timeout=5)
        
    except Timeout as ex:
        
        print("Exception Riased: ", ticker)
        Bool_except = 1
    
    while Bool_except:
     
        try:
            x = requests.get(path, timeout=2)
            Bool_except = 0
            
        except Timeout as ex:
            
            print("Exception Raised: ", ticker)
            Bool_except = 1
        
    
    str_x = x.text
    
    find = str_x.find('Contract Name</span>')
        
    
    return(find)




def full_options(price_limit = 10):
    
    file = open(r"Penny_screen.txt",'r')
    
    our_list = []
    
    penny_options = []
    
    print('Ticker, price')
    
    for line in file:
        
        #dont need the first line for our purposes
        if 'Symbol' in line:
            
            continue
        
        this_line = line
        
        ticker = this_line.rsplit('\t',1)[0]
        
        #gets a list of stock tickers
        our_list.append(this_line)    
    
    #print(our_list)
    for line in our_list:
        
        ticker = line.rsplit('\t',1)[0]     
        tickers = ticker.rsplit(',')
        tickers[0]= tickers[0][1:]
        tickers[1] = tickers[1][:-1]
        price = tickers[1]
        price = price.strip()
        price = price[1:-1]
        price = price[:-1]
        ticker = tickers[0]
        ticker = ticker[1:-1]
        
        val = options_screen(ticker)
        
        
        if val > -1 and float(price) < price_limit:
            penny_options.append(line)
            print(line)
       
        
        '''   
        if float(price) < price_limit:
            penny_options.append(line)
            print(line)
        '''
    
    file1 = open(r"Penny_Options.txt",'w')
    
    for line in penny_options:
        
        file1.write(str(line))   
    
    file1.close()
    file.close()
    
    
def main():

    full_screen(price_limit = 10)
    full_options(price_limit = 10)
                
    
    
print(full_options(price_limit = 10))
    

