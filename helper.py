import os
import sys
import bs4 as bs
import pickle
import requests as req
import datetime as dt
import pandas as pd
import pandas_datareader.data as web


# hardcoded for testing purposes
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def save_index_tickers(url):
	# extract ticker symbol data from wikipedia website
	try:
		dat_ = req.get(url) # retrieve response from website
		tmp_ = bs.BeautifulSoup(dat_.text, 'lxml') # parse response data in text format using bs4 library
		tmp_table = tmp_.find('table', {'class':'wikitable sortable'}) # find table tag in response text
		tickers = []
		for row in tmp_table.findAll('tr')[1:]:
			# loop through all rows containing tr and td tag 
			# append ticker symbol to empty array tickers
			ticker = row.findAll('td')[0].text 
			tickers.append(ticker)

		with open('sp500tickers.pickle','wb') as file:
			# serialize data and store ticker data locally
			pickle.dump(tickers,file)

		return tickers

	except Exception as e:
		return ('Failed to execute due to error: ' + str(e))


# function to check if financial info for ticker exists
def get_ticker_symbols(start_datetime,end_datetime,site,ticker_list):
	for ticker in ticker_list:
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, site, start_datetime, end_datetime)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			# If file exists, check if up to date
			if df['Date'].diff():
				fname = ticker + '.csv'
				df.to_csv(fname, mode='a', header=False)
				print ('Ticker data updated')
			else:
				print ('{}.csv Currently exists and is upto date'.format(ticker))


def retrieve_ticker_financial_data(update_tickers=False):
	# Retrieve data from website, serialize and store on local

	if not os.path.exists('stock_dfs'): # check if folder exists
		os.makedirs('stock_dfs') # create folder
	
	if update_tickers:
		tickers = save_index_tickers() # get most up-to-date list of index
		start = dt.datetime.now() - timedelta(days=365)*10 # 10 years from now
		end = dt.datetime.now() 
		get_ticker_symbols(start,end,'yahoo',tickers)
	else:
		with open('sp500tickers.pickle','rb') as file:
			pickle.load(file)




def market_close_check():
	# Check if market is closed. If closed, update data.
	time_now = dt.datetime.now() # current time
	past_market_close = time_now.replace(hour=16,minute=5,second=0) # market close 
	if time_now < past_market_close: 
		return 'It is {}, market is still open.'.format(time_now) 
	else:
		print ('Market is now closed. Updating ticker data to latest close values')
		retrieve_ticker_financial_data(update_tickers=True)


