import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def uniq(list):
	vals = []
	# Iterate through original list
	for el in list:
		# If element not in new list, add it to new list
		if not el in vals:
			vals.append(el)
	# Return new list
	return vals

def isfloat(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def isint(x):
	try:
		int(x)
		return True
	except ValueError:
		return False

def get_type(val):
	if isint(val) == True:
		return int
	elif isfloat(val) == True:
		return float
	elif val == 'NULL':
		return type(None)
	elif val.startswith('{'):
		return list
	else:
		return str



def audit_file(CITIES, FIELDS):
    fieldtypes = {}

    for el in FIELDS:

	    with open(CITIES, 'r') as f:
	    	dreader = csv.DictReader(f)

	    	for i in range(3):
	    		next(dreader)

	    	types = []

	    	for i in dreader:
	    		val = i[el]
	    		types.append(get_type(val))

	    	types = set(types)
	    	#types = uniq(types)

	    	fieldtypes[el] = types