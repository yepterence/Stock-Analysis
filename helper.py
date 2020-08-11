import os, sys
import bs4 as bs
import pickle
import requests as req

# hardcoded for testing purposes
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def save_index_tickers(url):
	try:
		dat_ = req.get(url)
		tmp_ = bs.BeautifulSoup(resp.txt, 'lxml')
		tmp_table = tmp_.find('table', {'class':'wikitable sortable'})
		tickers = []
		for row in tmp_table.findAll('tr')[1:]:
			# look for tr tag 
			ticker = row.findAll('td')[0].text
			# 
			tickers.append(ticker)

		with open('sp500tickers.pickle','wb') as file:
			pickle.dump(tickers,file)

		return tickers

	except Exception as e:
		return ('URL for index does not exist due to' + str(e))


def save_index_tickers(url):
	# extract ticker symbol data from wikipedia website
	try:
		dat_ = req.get(url)
		tmp_ = bs.BeautifulSoup(resp.txt, 'lxml')
		tmp_table = tmp_.find('table', {'class':'wikitable sortable'})
		tickers = []
		for row in table.findAll('tr')[1:]:
			ticker = row.findAll('td')[0].text
			tickers.append(ticker)

		with open('sp500tickers.pickle','wb') as file:
			pickle.dump(tickers,file)

		return tickers

	except Exception as e:
		return ('URL for index does not exist due to' + str(e))


# function to check if financial info for ticker exists
def get_data_from_site(start_date,end_date):
	for ticker in tickers:
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'yahoo', start, end)
			df.to_csv
		else:
			# If file exists, check if up to date
			if df['Date'].diff():
				fname = ticker + '.csv'
				df.to_csv(fname, mode='a', header=False)
				print ('Ticker data updated')
			else:
				print ('{}.csv Currently exists and is upto date'.format(ticker))

def retrieve_and_update():
	# Retrieve data from website, serialize and store on local
	if reload_sp500:
		tickers = save_index_tickers()
	else:
		with open('sp500tickers.pickle','rb') as file:
			pickle.dump(tickers,file)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')



def market_close_check():
	# Check if market is closed. If closed, update data.
	time_now = datetime.datetime.now() # current time
	past_market_close = time_now.replace(hour=16,minute=5,second=0) # market close 
	if time_now < past_market_close: 
		return 'It is {} market is still open.'.format(time_now) 
	else:
		retrieve_and_update()