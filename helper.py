import os
import glob
import bs4 as bs
import pickle
import requests as req
import datetime as dt
import pandas as pd
import pandas_datareader.data as web


# hardcoded for testing purposes
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def save_index_tickers(url):
	# extract ticker symbol data from wikipedia website and return serialized data dump with .pickle extension
	# Note: this is currently setup to retrieve ticker symbols from wikipedia
	try:
		dat_ = req.get(url) # retrieve response from website
		tmp_ = bs.BeautifulSoup(dat_.text, 'lxml') # parse response data in text format using bs4 library
		tmp_table = tmp_.find('table', {'class':'wikitable sortable'}) # find table tag in response text
		filename = dat_.find('span', {'class':'mw-headline'}).text
		tickers = []
		for row in tmp_table.findAll('tr')[1:]:
			# loop through all rows containing tr and td tag 
			# append ticker symbol to empty array tickers
			ticker = row.findAll('td')[0].text.rstrip() 
			# find all symbols in td tag and strip \n from entry
			tickers.append(ticker)

		with open(filename +'.pickle','wb') as file:
			# serialize data and store ticker data locally
			pickle.dump(tickers,file)

		return tickers

	except Exception as e:
		return ('Failed to execute due to error: ' + str(e))


# function to check if financial info for ticker exists
def get_ticker_financial_data(start_datetime,end_datetime,site, update_tickers=False):
	# This function retrieves data for a given start and end datetime range
	# from a given site and list stored previously in save_index_tickers
	if not os.path.exists('stock_dfs'): 
	# check if folder exists
		os.makedirs('stock_dfs') 
		# create folder
	# if pickle data doesn't exist, run save_index_tickers
	# using glob can search for all files with pickle extension
	if len(glob.glob('./*.pickle')) == 0:
		pickle_files = save_index_tickers(url)
	else:
		pickle_files = glob.glob('./*.pickle')
		with open(pickle_files[0],'rb') as file:
			ticker_list = pickle.load(file)

	for ticker in ticker_list:

		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			try:
				df = web.DataReader(ticker, site, start_datetime, end_datetime)
				print ('Creating file: {}.csv'.format(ticker))
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
			except:
				# adding pass to ignore errors due to issue with some tickers having incorrectly formatted keys
				# The main errors being encountered are with a few tickers that are giving a KeyError: 'Date'
				# Adding this try/except will allow the loop to continue downloading data
				pass
		else:
			print ('{}.csv Currently exists and is upto date'.format(ticker))

			# # TO-DO find a way to check if there are any changes in file content 
			# # and update files by adding new rows of data to it.
			# If file exists, check if up to date
			# if df['Date'].diff():
				# start = dt.datetime.now() - timedelta(days=365)*10 
				# # 10 years from now
				# end = dt.datetime.now() 
			# 	fname = ticker + '.csv'
			# 	df.to_csv(fname, mode='a', header=False)
			# 	print ('Ticker data updated')
			# else:


def market_close_check():
	# Check if market is closed. If closed, update data.
	time_now = dt.datetime.now() # current time
	past_market_close = time_now.replace(hour=16,minute=5,second=0) # market close 
	if time_now < past_market_close: 
		print ('It is {}, market is still open.'.format(time_now) )
		retrieve_ticker_financial_data(update_tickers=False)
	else:
		print ('Market is now closed. Updating ticker data to latest close values')
		retrieve_ticker_financial_data(update_tickers=True)


def compile_data():
	pickle_list = glob.glob('./*.pickle')
	# find existing .pickle file
	with open(pickle_list[0],'rb') as f:
		tickers = pickle.load(f)

	# create empty dataframe
	main_df = pd.DataFrame()

	for count, ticker in enumerate(tickers):
		# using enumerate to loop through all the tickers
		# and keep track of the number of tickers 
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		# import csv into dataframe 
		df.set_index('Date',inplace=True)
		# set Date column as index column, 
		# inplace set to True so that its not redefined it everytime
		# is done in place.
		df.rename(columns = {'Adj Close', ticker}, inplace=True)
		# since the only values we need for analysis is the adjusted close value
		# we rename column name to ticker symbol
		df_adj_col_ticker = df.loc[:,[ticker]]
		if main_df.empty:
			main_df = df_adj_col
		else:
			main_df = main_df.join(df, how='outer')
		

