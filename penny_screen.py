import requests
from requests.exceptions import Timeout


#function for getting the most recent price for a stock
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
        
    #finds the price at open if available
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
    
    #if open price isnt working on yahoo finance, it uses previous close to get the price data
    if 'N/A' in price:
        
        find = str_x.find('Previous Close')
        
        subx = str_x[find:find+8000]
    
        #looks for a unique identifyer in the code
        val = subx.find('data-test="PREV_CLOSE-value')
    
        #makes a much smaller substring
        sub = subx[val+50:val+150]
    
        #finds the indexes for the value we are looking for
        begin = sub.find('>')
    
        begin+=1
    
        end = sub.find('<')
    
        str_price = sub[begin:end]
    
        price = str_price.replace(',','')
        
        
    
    return(price)


#code to go through a text file of every stock on a given exchange and screen it based on price
#by default it uses the NYSE but can be set for the NASDAQ
def full_screen(Exchange_Path = 'NYSE', price_limit = 10):
    
    #exception list for the NASDAQ as weird problems can happen with yahoo finance if the stock is also on the NYSE
    NASDAQ_EXCEPTION_LIST = ['AAXN', 'ACAM', 'ACAMW', 'GHIVW', 'LPRO', 'OEPWU', 'OTEX']
    
    if Exchange_Path == 'NYSE':
        
        list_path = r"NYSE.txt"
    
    if Exchange_Path == 'NASDAQ':
        
        list_path = r"NASDAQ.txt"
    
    file = open(list_path,'r')
    
    our_list = []
    
    penny_stocks = []
    
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
        
        if tick in NASDAQ_EXCEPTION_LIST and Exchange_Path == 'NASDAQ':
            
            continue
        
        try:
            
            price = p_screen(tick)
            
        except:
            
            print("Exception Raised: ", tick)
        
        
        try:
            
            if float(price) < price_limit:
                
                #print(tick,price)
                penny_stocks.append((tick, price))
                
                print(tick,price)
        
        except:
            
            print(tick, 'fuck it')
            #NASDAQ_EXCEPTION_LIST.append(tick)
    
    #NASDAQ has some weird problems using Yahoo Finance and tickers for the NASDAQ might not show up if its on the NYSE
    #i used this to get the exception list above
    #print(NASDAQ_EXCEPTION_LIST)        
    file1 = open(r"Penny_Stocks.txt",'w')
    
    for line in penny_stocks:
        
        file1.write(str(line)+'\n')   
    
    file1.close()
    
    file.close()
          
    
    
#code for screening an individual stock for whether it has options   
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



#change the path to the generated text file from full_screen(). can be used on the full NYSE or NASDAQ list as well but will take significantly
#more time
def full_options(price_limit = 10):
    
    file = open(r"Penny_Stocks.txt",'r')
    
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
    
    
    for line in our_list:
        
        #lazy way of fixing text file problems
        
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
    

