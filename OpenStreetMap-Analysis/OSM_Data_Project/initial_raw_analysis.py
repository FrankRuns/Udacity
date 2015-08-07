#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET 
import re
from collections import defaultdict
import pprint
import codecs
import json

# Define Variables, Lists, and Dictionaries ##################################################

# Define file name
filename = 'boulder_sample.osm'

# Define regex expressions for various cleaning / identification functions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# postal_code_re = re.compile(r'\D(\d{5})\D", " "+s+" ')

# List of the street types we expect to see in the US
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "Broadway", "Circle", "East", "North", "Point", "Row", "West"]

# Map the 'incorrect' street abbrvs with the correct street names
mapping = { "Blvd" : "Boulevard",
            "Ave" : "Avenue",
            "ave." : "Avenue",
            "St" : "Street",
            "St.": "Street",
            "st" : "Street",
            "Rd" : "Road",
            "Rd." : "Road",
            "Cir" : "Circle",
            "Ct" : "Court",
            "Pky" : "Parkway",
            "Pl" : "Place",
            "lane" : "Lane"
            }

# High Level Analysis ##################################################

# High level analysis
# Identify number of tags in osm file
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if tags.has_key(elem.tag) == True:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags

# High level analysis
# Identify unique contributors in osm file
def unique_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'user' in element.attrib:
            users.update([element.attrib['user']])
    return users




# Identify Key Type Errors ##################################################

# Identify errors function
# Create dictionary that counts instances where 'k' attribute will need cleaning to be key in MongoDB
# Used by count_key_kinks()
def key_type(element, keys):
    if element.tag == "tag":
        print element.attrib['k']
        if lower.match(element.attrib['k']) != None:
            keys['lower'] += 1
        elif problemchars.match(element.attrib['k']) != None:
            keys['problemchars'] += 1
        elif lower_colon.match(element.attrib['k']) != None:
            keys['lower_colon'] += 1
        else:
            keys['other'] += 1
    return keys

# Identify errors function
# Count instances where 'k' attribute will need cleaning to be key in MongoDB
# Uses key_type
def count_key_kinks(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys




# Audit Data / Identify Errors ##################################################

# Add street types to street_type dictionary. Form example { 'St.' : ['Wilson St.', 'North St.']}
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Add error postal codes to postcodes. Form example ['adcbe', '564324', '123lf']
def audit_postal_code(postal_codes, this_postal_code):
    if this_postal_code.isdigit() == False:
        postal_codes.append(this_postal_code)
    if len(this_postal_code) != 5:
        postal_codes.append(this_postal_code)

# Add error house numbers to house_num list. For example, ['here', 'Denver']
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

def audit_house_num(house_nums, this_house_num):
    if contains_digits(this_house_num) == False:
        house_nums.append(this_house_num)

# Add error house numbers to house_num list. For example, ['Denver, CO']
def audit_city_name(city_names, this_city_name):
    if re.match('^[\w-]+$', this_city_name) is None:
        city_names.append(this_city_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def is_house_num(elem):
    return (elem.attrib['k'] == "addr:housenumber")

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib["v"])
    return street_types
    # Fix: Conform to street mapping if possible

def audit_post(osmfile):
    osm_file = open(osmfile, "r")
    postal_codes = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(postal_codes, tag.attrib["v"]) 
    return postal_codes
    # Fix: Take first five digits

def audit_house(osmfile):
    osm_file = open(osmfile, "r")
    house_nums = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:city':
                    print tag.attrib['v']
                if is_house_num(tag):
                    audit_house_num(house_nums, tag.attrib["v"]) 
    return house_nums
    # Only one is '?'. Only thing I can think of is to replace with '00'

def audit_city(osmfile):
    osm_file = open(osmfile, "r")
    city_names = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_name(city_names, tag.attrib["v"]) 
    return city_names
    # Only one is '?'. Only thing I can think of is to replace with '00'



# Fix Errors ##################################################

# Function to 
def update_street_name(name, mapping):
    kind = name.rsplit(None, 1)[-1]
    if kind in mapping.values():
        return name
    else:
        return name.replace(str(kind), mapping[kind])

def update_postal_code(this_postal_code):
    if len(this_postal_code) != 5:
        return this_postal_code[:5]
    else:
        return this_postal_code




# Helper to test individual node
testel = '''    
<node changeset="784670" visible="true" id="358913212" lat="40.0230413" lon="-105.2799903" timestamp="2009-03-11T11:45:25Z" uid="4732" user="iandees" version="1">
        <tag k="ele" v="1640" />
        <tag k="name" v="Casey Middle School" />
        <tag k="amenity" v="school" />
        <tag k="gnis:created" v="08/31/1992" />
        <tag k="gnis:state_id" v="08" />
        <tag k="gnis:county_id" v="013" />
        <tag k="gnis:feature_id" v="178666" />
</node>
'''

testel = '''
    <way changeset="28902281" id="328630439" timestamp="2015-02-17T07:42:42Z" uid="2237750" user="chachafish" version="2">
        <nd ref="3354436286" />
        <nd ref="3354436287" />
        <nd ref="3354436288" />
        <nd ref="3354436289" />
        <nd ref="3354436286" />
        <tag k="building" v="house" />
        <tag k="addr:city" v="Denver" />
        <tag k="addr:street" v="Glenarm Pl" />
        <tag k="addr:postcode" v="802055" />
        <tag k="addr:housenumber" v="2941" />
    </way>
'''

testel = ET.fromstring(testel)




# Shape Individ Element Prep ##################################################

{
  "created": {
    "uid": "117055", 
    "changeset": "7551724", 
    "version": "6", 
    "user": "GPS_dr", 
    "timestamp": "2011-03-14T04:12:27Z"
  }, 
  "type": "node", 
  "id": "25676629", 
  "pos": [
    39.9822661, 
    -105.2638756
  ]
}

# Shaping the element to be pushed to JSON
def shape_element(element):
    # Declare dict for new reshaped element
    node = {}
    # Declare dict for metadata of this node
    created = {}
    # Define the metadata fields we want to pull from this element
    created_fields = ['changeset', 'version', 'timestamp', 'user', 'uid']
    # Define other high level items of interest (example = 'id', 'type', 'pos')
    high_level_items = ['id', 'visible', 'type']
    # Define other elements of interest
    elems_of_int = ['name', 'amenity', 'landuse', 'wheelchair', 'peak', 'website', 'phone', 'historic', 'religion', 'cuisine', 'microbrewery', 'fee', 'opening_hours']
    # If this element is node or way, do stuff below
    if element.tag == "node" or element.tag == "way" :
        # Store the element keys (for instance 'uid', 'changeset', 'timestamp', etc.)
        keys = element.attrib.keys()
        # First we add the created metadata of interest, high_level_keys, position and their values
        for item in keys:
            if item in created_fields:
                created[item] = element.attrib[item]
            if item in high_level_items:
                node[item] = element.attrib[item]
            if 'lat' in keys:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        # Store created fields and values as element within the node
        node['created'] = created
        # Declare address key and all other attributes of interest
        for child in element:
            if child.tag == 'tag':
                if child.attrib['k'].startswith('addr:') == 1 and child.attrib['k'].count(':') < 2:
                    node['address'] = {}
                if child.attrib['k'] in elems_of_int:
                    node[child.attrib['k']] = child.attrib['v']

        # Process and add the address values
        for child in element:
            if child.tag == 'tag':
                if child.attrib['k'].startswith('addr:') == 1:
                    if child.attrib['k'].count(':') < 2:
                        field = child.attrib['k'][5:]
                        if field == 'street':
                            value = update_street_name(child.attrib['v'], mapping)
                        elif field == 'postcode':
                            value = update_postal_code(child.attrib['v'])
                        else:
                            value = child.attrib['v']
                        node['address'].update({field : value})
        # Process the way nds
        if element.tag == "way":
            nds = []
            for child in element:
                if child.tag == 'nd':
                    nds.append(child.attrib['ref'])
            node['node_refs'] = nds
        return node
    else:
        return None




# Create JSON ##################################################

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

# importing json file into mongo
# start a mongod instance using ./mongod
# open new terminal window and cd to mongo bin folder
# move records from json to mongo like this..
# ./mongoimport --db exampls --collection osmb_728 --type json --file /Users/frankCorrigan/Udacity/OpenStreetMap-Analysis/OSM_Data_Project/boulder_sample.osm.json

# Now we need to start running queries to find our trouble spots in the data
# Number of records
# Number of unique users
# Number of nodes and ways
# Number of chosen type of nodes (points, cafes, shops, etc.)




# MongoDB Query and Data Analysis ##################################################

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.osm
pipeline = [ { "$group" : { "_id" : "$user",
                            "count" : { "$sum" : 1 } } },
             { "$sort" : { "count" : -1 } },
             { "$limit" : 5 } ]
result = db.osmb_728.aggregate(pipeline)
# Here are the top 10 contributors
result = db.osmb_728.aggregate([ { "$group" : { "_id" : "$created.user",
                            "count" : { "$sum" : 1 } } },
             { "$sort" : { "count" : -1 } },
             { "$limit" : 10 } ])
# Here are the types of nodes we have
result = db.osmb_728.aggregate({ "$group" : { "_id" : "$type",
                            "count" : { "$sum" : 1 } } },
             { "$sort" : { "count" : -1 } })

# We can check to ensure state is CO and City is either Denver of Boulder...
# We need to add tags to records --- name, amenity, landuse, leisure, wheelchair, peak, website, phone, historic, religion, cuisine, microbrewery, fee, opening_hours
