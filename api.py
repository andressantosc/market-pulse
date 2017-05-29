import requests
from flask import json

api_username = '0312015bd643bbf9ce1035f78e70ea1d'
api_password = '6c0c47ad7ab24e16ed1be09f7cc7b61f'
base_url = "https://api.intrinio.com"

call_type_list = {
	
	#Returns the most recent data point for a selected identifier (ticker symbol, stock market index symbol, CIK ID, etc.) for a selected tag. Income statement, cash flow statement, and ratios are returned as trailing twelve months values. All other data points are returned as their most recent value, either as of the last release financial statement or the most recent reported value.
	'data_point' :'/data_point?',
	#Returns the historical data for for a selected identifier (ticker symbol or index symbol) for a selected tag. Income statement, cash flow statement, and ratios are returned as trailing twelve months values by default, but can be changed with the type parameter. All other historical data points are returned as their value on a certain day based on filings reported as of that date.
	'history' : '/historical_data?',
	#Returns security list and information all securities that match the given conditions. The API call credits required for each call is equal to the number of conditions specified.
	'screener' : '/securities/search?',
	#Returns professional-grade historical stock prices for a security or stock market index. New EOD prices are available at 5p.m. EST and intraday prices are updated every minute during the trading day from IEX. Historical prices are available back to 1996 or the IPO date, with some companies with data back to the 1970s. Stock market index historical price data is available back to the 1950s at the earliest. Data from Quandl, QuoteMedia and the Federal Reserve Economic Data.
	'prices' : '/prices?',
	#Returns company list and information for all companies covered by Intrinio.
	'companies' : '/companies?',
	#Returns indices list and information for all indices covered by Intrinio.
	'indices' : '/indices?',
	#Returns owners list and information for all insider and institutional owners of securities covered by Intrinio.
	'owners' : '/owners?',
	#Returns the complete list of SEC filings for a company.
	'company_filings' : '/companies/filings?',
	#Returns the most recent news stories for a company.
	'company_news' : '/news?',
	#Returns a list of available standardized fundamentals (fiscal year and fiscal period) for a given ticker and statement.
	'available_fundamentals' : '/fundamentals/standardized?',
	#Returns the standardized tags and labels for a given ticker, statement, and date or fiscal year/fiscal quarter.
	'standardized_tags' : '/tags/standardized?',
	#Returns professional-grade historical financial data. This data is standardized, cleansed and verified to ensure the highest quality data sourced directly from the XBRL financial statements. The primary purpose of standardized financials are to facilitate comparability across a single company’s fundamentals and across all companies fundamentals. For example, it is possible to compare total revenues between two companies as of a certain point in time, or within a single company across multiple time periods. This is not possible using the as reported financial statements because of the inherent complexity of reporting standards.
	'standardized_financials' : '/financials/standardized?',
	#Returns the As Reported Financials directly from the financial statements of the XBRL filings from the company.
	'reported_financials' : '/financials/reported?'
}


def geturl(type, par):

	url = base_url + call_type_list[type]

	response = requests.get(url, params=par, auth=(api_username, api_password))

	if response.status_code == 401: 
		print("Unauthorized! Check your username and password.")
		return {}

	data = response.json()
	return data

def str_financials(dataset):
	rev_data = dataset
	new_data = dict()
	for data in rev_data:
		new_data[data['date']] = '{:,}'.format(data['value'])

	new_data = json.dumps(new_data)
	
	return new_data