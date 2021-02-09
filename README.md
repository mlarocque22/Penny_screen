# Penny_screen
Screens New York Stock Exchange or NASDAQ to find stocks under a set dollar threshold that have options

I have attached two text files that the code created. One is for all stocks under $5 that support options. The other is for all stocks under $10 that support options

This code is for use in a future project that involves then finding undervalued and highly volatile stocks under $5 and $10 in order to trade options on. 

In order to keep this repository from getting cluttered, besides the example text files, all the text files I am generating using this are in github.com/mlarocque22/stock_text_files

Robinhood does not support trading on many of the smaller NASDAQ stocks that will show up on the screen. 

USAGE GUIDE

First run full_screen(). Set Exchange_Path to which ever exchange you want to use, Either NASDAQ or NYSE. NYSE is the default. Set your price limit, default is $10
This will output a text file with a list of all the stocks under that set price limit. 
Then run full_options(). Price limit is again 10 by default. This will output a text file with a list of all stocks that support options and are under that price threshold

IE code

full_screen(Exchange_Path = 'NASDAQ', price_limit = 5)
full_option(price_limit = 5)

full_screen only needs to be ran once and from then on you can just use full_options for any stocks below that price threshold. 
