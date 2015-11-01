#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import requests
from bs4 import BeautifulSoup
import urllib2
import random
import time

#################################################################################
# TURNSTILE DATA ################################################################
#################################################################################

# Define the weeks of data we want (this is the easiest way for our purposes)
# http://web.mta.info/developers/turnstile.html
urls = ['http://web.mta.info/developers/data/nyct/turnstile/turnstile_150711.txt',
		'http://web.mta.info/developers/data/nyct/turnstile/turnstile_150718.txt',
		'http://web.mta.info/developers/data/nyct/turnstile/turnstile_150725.txt',
	    'http://web.mta.info/developers/data/nyct/turnstile/turnstile_150801.txt',
	    'http://web.mta.info/developers/data/nyct/turnstile/turnstile_150808.txt'
	    ]

# Create home for filenames
filenames = []

# Grab turnstile data in specified urls and write to csv
def get_turnstile_data(list_of_urls):
	for link in list_of_urls:
		url = link
		name = url[-10:-4]
		response = urllib2.urlopen(url)

		with open(name+'.csv', 'wb') as outfile:
			wr = csv.writer(outfile)
			for line in response:
				wr.writerow(str(line).split(','))

		filenames.append(name+'.csv')

get_turnstile_data(urls)

# Read each csv and combine into larger dataframe
f0 = pd.read_csv(filenames[0])
f1 = pd.read_csv(filenames[1])
f2 = pd.read_csv(filenames[2])
f3 = pd.read_csv(filenames[3])
f4 = pd.read_csv(filenames[4])
alldata = pd.concat([f0,f1,f2,f3,f4])

# Make a unique turnstile identifier
alldata['UUNIT'] = alldata['C/A'] + '_' + alldata['UNIT'] + '_' + alldata['SCP']
# Sort the data by unique identifie, date, time that will help with finding hourly entries
alldata = alldata.sort(['UUNIT', 'DATE', 'TIME'], ascending=[1, 1, 1])
# Since the entries data is cumulative, find the change in entries every four hour period
alldata['HOURLY'] = alldata['HOURLY'] = (alldata['ENTRIES'] - alldata['ENTRIES'].shift(1)) 
# Everytime a row contains the next unique turnstile... the hourly change is incorrect. Remove those.
alldata = alldata[(alldata['DATE'] != '07/04/2015') & (alldata['TIME'] != '00:00:00')]
# Removing data that is representative of a system glitch or counter problem (descending cum entries?, > 1 entry per second over 4 hours?)
alldata = alldata[alldata['HOURLY'] > -1]
alldata = alldata[alldata['HOURLY'] < 7501]

#################################################################################
# LOCATION DATA #################################################################
#################################################################################

# Read the goe locations data (I've downloaded locally)
# https://github.com/chriswhong/nycturnstiles/blob/master/geocoded.csv
station_file = 'entry_locations.csv'

# Read it to a dataframe, rename columns we need, and join with entries data on C/A 
stations = pd.read_csv(station_file, header=None)
stations.rename(columns={1:'C/A',5:'LAT',6:'LON'}, inplace=True)
alldata = alldata.merge(stations, on='C/A',how='left')

# Scale back our dataset to only our columns of interest
interest = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'HOURLY', 'UUNIT', 'LAT', 'LON']
alldata = alldata.ix[:,interest]

# Lastly, to make this a bit easier (and it's a total temporary cheat) drop rows with NA values
alldata = alldata.dropna()

#################################################################################
# WEATHER DATA ##################################################################
#################################################################################

# http://api.wunderground.com/api

# Define the staple stuff for the api call...
base_api = "http://api.wunderground.com/api/"
api = "###PUTAPIKEYHERE###/"
querytype = "geolookup/history_"

# You have 31 days... 374 locations... that's 11,594 api calls. Your limit is 5,000 per day or 10 per minute.
# So instead do sample of data

# Remember to set a seed!!!
random.seed(1234)
rows = random.sample(alldata.index, 20)
data_20 = alldata.ix[rows]

# Loop through 20 observations and get your weather data
for i in range(len(data_20)):
	# Define date and time
	day = data_20.iloc[i]['DATE'].replace('/','') 
	day = day[-4:] + day[:4]
	timeofday = int(data_20.iloc[i]['TIME'][:2])
	# Define geo coords
	lat = str(data_20.iloc[i]['LAT'])
	lon = str(data_20.iloc[i]['LON'])
	# Define the index
	dex = data_20.iloc[i].name
	# Define call based on parameters above
	call = base_api+api+querytype+day+'/q/'+lat+','+lon+'.json'
	# Make the call and parse with bs4
	r = requests.get(call)
	soup = BeautifulSoup(r.content)
	tempdata = r.json()
	# Parse the json output and add weather data to our dataframe
	data_20.loc[dex,'TEMP'] = tempdata['history']['observations'][timeofday][u'tempi']
	data_20.loc[dex,'PRECIP'] = tempdata['history']['observations'][timeofday][u'precipi']
	data_20.loc[dex,'RAIN'] = tempdata['history']['observations'][timeofday][u'rain']
	# Don't exceed API limit... 10 per minute so 6 second delay will be plenty
	time.sleep(6)
