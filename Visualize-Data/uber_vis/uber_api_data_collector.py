#http://www.latlong.net/convert-address-to-lat-long.html
# Cedar Grove
#40.865374
#-74.241216

#Newark
#40.689531
#-74.174462

#Penn Station
#40.7506
#-73.9939
#40.7506, -73.9939

#NYU
#40.7300, -73.9950

import requests
import json
import os
import os.path
import time

# libraries for datetime stuff
from dateutil.rrule import rrule,MINUTELY
import datetime
import bisect

# start time should be when the next hour starts. Run for 1 week (7 days)
times = list(rrule(MINUTELY,interval=5,dtstart=datetime.date.today(),count=
120))
start_time = times[bisect.bisect(times,datetime.datetime.now())]
end_time = start_time + datetime.timedelta(days=7)

# api call
call = "https://api.uber.com/v1/estimates/price?start_latitude=40.7506&start_longitude=-73.9939&end_latitude=40.7300&end_longitude=-73.9950&server_token=wx-F5ajgvEtiSJxZoDCqw5gqu1s1hrUEdsIfLwTy"

# write request to text file every 5 minutes

while (datetime.datetime.now() >= start_time and datetime.datetime.now() <= end_time):
	now = datetime.datetime.now()
	test = {}
	r = requests.get(call)
	tempdata = r.json()
	test[now] = tempdata
	if os.path.isfile('uberData.txt'):
		with open('uberData.txt', 'a') as f:
			f.write('\n')
			f.write(str(test))
			f.flush()
	else:
		with open('uberData.txt', 'a') as f:
			f.write(str(test))
			f.flush()
	time.sleep(60*5)

# below is 

# rfile = open('uberData.txt', 'r')
# data = rfile.read()
# data = data.split(',')

# parser.parse(strtime) to convert back string date

# unwinding the data
# dates = []
# for el in data:
# 	end = el.find(':')
# 	date = el[1:end]
# 	dates.append(date)

# import ast

# d = data[0]
# test = d[50+2:-1]
# ast.literal_eval(test)
