import bs4 as bs
from collections import Counter
import datetime as dt
import glob
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests as req
import sklearn 

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
			except Exception as e:
				# adding pass to ignore errors due to issue with some tickers having incorrectly formatted keys
				# The main errors being encountered are with a few tickers that are giving a KeyError: 'Date'
				# Adding this try/except will allow the loop to continue downloading data
				print ('Failed to retrieve data for {} due to'.format(ticker) + str(e))
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

def update_ticker_data():
	# should be used in conjunction with market close check
	data_loc = os.path.relpath('./stock_dfs')
	file_list = os.listdir(data_loc)
	for file in file_list:
		time_last_updated = os.path.getmtime('./{}'.format(file))
		if time_last_updated == dt.datetime.now()

def compile_index_data(data_filepath,index_name):
	"""
	 Input filepath of financial data csv dump
	 compile all the information into one dataframe
	 return dataframe containing Adjusted price values of each 
	 security listed in directory 
	"""
	# find existing .pickle file
	filename = [_ for _ in glob.glob('*.pickle') if index_name in _ ][0].split('.')[0] + '_adj_close.csv'

	# with open(pickle_list[0],'rb') as f:
	# 	tickers = pickle.load(f)

	tickers = os.listdir(data_filepath)
	os.chdir(data_filepath)
	# retrieve list of csv files in given filepath
	main_df = pd.DataFrame()
	# create empty dataframe
	if filename in tickers:
		print ('{} already exists'.format(filename))
	else:
		for count, ticker in enumerate(tickers):
			try:
				# using enumerate to loop through all the tickers
				# and keep track of the number of tickers 
				df = pd.read_csv(ticker)
				# import csv into dataframe 
				df.set_index('Date',inplace=True)
				# set Date column as index column, 
				# inplace set to True so that its not redefined it everytime
				# is done in place.
				t_name = ticker.split('.')[0]
				df.rename(columns = {'Adj Close': t_name}, inplace=True)
				# since the only values we need for analysis is the adjusted close value
				# we rename column name to ticker symbol
				# df_adj_col_ticker = df[ticker].to_frame()
				if main_df.empty:
					main_df = df[t_name].to_frame()
					# convert series into dataframe
				else:
					main_df = main_df.join(df[t_name].to_frame(), how='outer')
				# Track progress of compiling
				if count % 10 == 0:
					print ('Percent complete: {}'.format(round(count/500*100)))
			except Exception as e:
				print ('Failed to compile {} due to: '.format(t_name) + str(e))
				pass

		# convert dataframe to csv
		print ('Compiling data into {}'.format(filename))
		main_df.to_csv(filename)
	return filename 

time_period = 7
# time frame in the future to see if stock will profit/loss
# will probably make this a variable at some point.

def process_data_for_labels(df, ticker, time_period):
	"""
	pricing data converted into percentage change to normalize data
	percentage change will be considered as features
	labels will be either buy, sell or hold.
	if each week, the company's increasing by 2% = buy
	if decreasing by 2% = sell, if neither, hold.
	Each model is made on a per-company basis, but each company is 
	going take into account all the other prices in the index
	"""
	data_ = df.fillna(0)
	# ensuring NaN values are replaced by 0 incase data doesn't exist. 
	# Avoiding inplace as it does not convert NaNs as expected, and will return None
	tickers = df.columns.values.tolist()
	# grab all adj close values of security
	for i in range(1,time_period+1):
		# loop through 7 days of adj close values
		data_['{}_{}d'.format(ticker, i)] = (data_[ticker].shift(-i)-data_[ticker])/data_[ticker]
		# create each column with percentage change in adj close values with increasing time. The shift
		# function allows us to grab the previous adjusted close entry. 
	data_.fillna(0)
	# To ensure there are no NaN values in dataset
	return tickers, data_
	# returns list of tickers and dataframe

def action_label(*args):
	# returns numerical value that can be used to label tickers as 
	# buy, sell or hold 
	columns = [x for x in args]
	req = 0.02
	for col in columns:
		if col > req:
			return 1
		elif col < -req:
			return -1
	return 0

def extract_featuresets(df, ticker_list,ticker):
	# ticker_list, df = process_data_for_labels(df, ticker, time_period)
	df['{}_target'.format(ticker)] = list(map(action_label, *[data_['{}_{}d'.format(ticker, i)] for i in range (1, time_period)]))
	# creates new column ticker_target (feature sets), that generates a buy, sell or hold label for each ticker
	vals = df['{}_target'.format(ticker)].values.tolist()
	# list price values of ticker 
	str_vals = [str(i) for i in vals]
	# convert all to string for usage in Counter
	print ('Data spread: ', Counter(str_vals))
	df.fillna(0)
	df = df.replace([np.inf,-np.inf],np.nan)
	df.dropna(inplace=True)

	df_vals = df[[ticker for ticker in ticker_list]].pct_change()
	df_vals = df_vals.replace([np.inf,-np.inf], 0)
	df_vals.fillna(0, inplace=True)

	# Labels
	X = df_vals.values
	y = df['{}_target'.format(ticker)].values

	return X, y, df