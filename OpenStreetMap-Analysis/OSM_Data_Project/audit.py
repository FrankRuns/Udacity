#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

'''
This file contains a group of functions to audit
an open street map xml file. Included are functions
to check street type, postal code, and city name.
'''

small_boulder = 'boulder_sample.osm'
big_boulder = 'denver-boulder_colorado.osm'

# Audit Street Type ######################################################

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # Define regex expressions for grabing street type

expected = ["Mall", "Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "Broadway", "Circle", "Mall", "South", "East", "North", "Point", "Row", "West"] # List of the street types we expect to see in the US

def audit_street_type(street_types, street_name):
    # Parse street type from name and if not in expected move to dictionary
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    # Identify element tag as street name
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    # Parse osm file for inconsistent street types
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib["v"])
    return street_types

# Audit Postal Code ######################################################

def audit_postal_code(error_codes, postal_codes, this_postal_code):
    # Append incorrect zip codes to list
    if this_postal_code.isdigit() == False:
        error_codes.append(this_postal_code)
    elif len(this_postal_code) != 5:
        error_codes.append(this_postal_code)
    else:
        postal_codes.update([this_postal_code])

def is_postal_code(elem):
    # Identify element tag as postal code
    return (elem.attrib['k'] == "addr:postcode")

def audit_post(osmfile):
    # Parse osm file for incorrect postal codes
    osm_file = open(osmfile, "r")
    error_codes = []
    postal_codes = set([])
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(error_codes, postal_codes, tag.attrib["v"]) 
    return error_codes, postal_codes

bad_list, good_list = audit_post(small_boulder)

# Identify zip codes in our data outside of Boulder County
boulder_county_zips = [ '80514', '80516', '80241', '80439', '80534', 
                        '80540', '80020', '80544', '80455', '80023', 
                        '80026', '80025', '80027', '80466', '80465', 
                        '80038', '80301', '80471', '80303', '80214',
                        '80474', '80302', '80305', '80304', '80309',
                        '80481', '80314', '80310', '80226', '80401',
                        '80502', '80501', '80403', '80504', '80503',
                        '80510', '80422', '80513', '80512' ]

# Count zip codes that occur outside Boulder County
count = 0
for el in good_list:
    if el not in boulder_county_zips:
        count += 1

# Audit City Name ######################################################

def audit_city_name(bad_cities, good_cities, this_city_name):
    # Append non-conforming cities to bad and conforming ones to good
    this_city = this_city_name.lower()
    if this_city.find(',') > -1:
        bad_cities.update([this_city])
    elif re.search('\sco', this_city) != None:
        bad_cities.update([this_city])
    else:
        good_cities.update([this_city])

def is_city_name(elem):
    # Identify element tag as city name
    return (elem.attrib['k'] == "addr:city")

def audit_city(osmfile):
    # Parse osm file for 'bad' and 'good' city names
    osm_file = open(osmfile, "r")
    bad_cities = set([])
    good_cities = set([])
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_name(bad_cities, good_cities, tag.attrib["v"]) 
    return bad_cities, good_cities

bad_cities, good_cities = audit_city(small_boulder)

# Identify city names in our data outside of Boulder County
boulder_county_cities = [ 'boulder', 'lafayette', 'longmont', 'louisville',
           'erie', 'jamestown', 'lyons', 'nederland',
           'superior', 'town of ward', 'allenspark', 'coal creek',
           'eldora', 'eldorado springs', 'gold hill', 'gunbarrel',
           'niwot', 'valmont', 'caribou', 'hygiene' ]

# Count city names that occur outside Boulder County
count = 0
for el in good_cities:
    if el not in boulder_county_cities:
        count += 1

# Audit House Number ######################################################

_digits = re.compile('\d') # check if digit

def contains_digits(d):
    # Function to check if digit
    return bool(_digits.search(d))

def audit_house_num(house_nums, this_house_num):
    # Function pulling out non-digit house numbers
    if contains_digits(this_house_num) == False:
        house_nums.append(this_house_num)

def is_house_num(elem):
    # Identify element tag as house number
    return (elem.attrib['k'] == "addr:housenumber")

def audit_house(osmfile):
    # Parse osm file for 'bad' house numbers (not digits)
    osm_file = open(osmfile, "r")
    house_nums = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:housenumber':
                    print tag.attrib['v']
                if is_house_num(tag):
                    audit_house_num(house_nums, tag.attrib["v"]) 
    return house_nums