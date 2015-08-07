#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET 
import re
import codecs
import json

'''
This file takes an osm files, parses it, and
writes each element into a JSON file. Using the audit.py 
file, potential errors that need correction to fit data 
model have been identified. The flow of functions ...

process_map uses --> shape_element uses --> everything else

These pieces of code can be used for element searching and Shaping

sample = "<node changeset="830792" id="335986968" lat="39.3419172" lon="-104.746838" timestamp="2009-01-24T17:35:23Z" uid="91266" user="HurricaneCoast" version="2">
    <tag k="addr:city" v="Franktown" />
    <tag k="created_by" v="Potlatch 0.10f" />
    <tag k="addr:street" v="Street G" />
    <tag k="addr:postcode" v="80116" />
</node>"
sample = ET.fromstring(sample)

for _, element in ET.iterparse(boulder_osm):
    for child in element:
        if child.tag == 'tag':
            if child.attrib['k'] == 'addr:street':
                if child.attrib['v'].rsplit(None, 1)[-1] == '106':
                #if child.attrib['v'].startswith('County Rd'):
                    for child in element:
                        print child.attrib
'''

small_boulder = 'boulder_sample.osm'
big_boulder = 'denver-boulder_colorado.osm'

## Helper lists & dictionaries #################################################

expected = ["Terrace", "Plaza",    "Locust",    "Bypass", "Mall",    "Mall", 
            "Street",  "Avenue",   "Boulevard", "Drive",  "Court",   "Place",
            "Square",  "Lane",     "Road",      "Trail",  "Parkway", "Commons",
            "Way",     "Broadway", "Circle",    "South",  "East",    "North",
            "Point",   "Row",      "West" ] # List of the street types we expect to see in the US

highways = ['2', '8', '40', '73', '74', '83', '85', '86', '119', '285', '287'] # Includes 'highway' and 'state highway' and 'us highway'

county_roads = ['7', '41', '45', '72', '126', '186', '314'] # Includes county roads

exceptions = ['19',        '#107',   '#169',     '#220',   '400',
              '1606',      '6001',   '6523',     '8765',   'A',
              'Highway',   'MUP',    'Boulder',  'Canyon', 'Centennial',
              'Center',    'Lamar',  'Lincoln',  'Mine',   'Newland',
              'Ramp',      'Run',    'Tennyson', 'Tilden', 'Ute',
              'Wadsworth', 'Walnut', 'Woodfern', 'G' ] # Exceptions that need manual checking

suites = ['1E',  '5B',   '106',  '110',  '120', 
          '154', '200',  '200b', '200c', '230',
          '300', '#300', '400',  '700',  '#850',
          '900', '2200', 'D',    'E1',    ] # Includes both 'Suite', 'Ste', and 'Unit'. Let them be.

addr_mapping = {"88th"         : "88th Street",
                "80208"        : "High Street",
                "80305"        : "South Lashley Lane",
                "Appia"        : "Via Appia Way",
                "Av"           : "Avenue",
                "Ave"          : "Avenue",
                "Ave."         : "Avenue",
                "Avenue)"      : "East Bromley Lane",
    			"ave."         : "Avenue",
    			"Arapahoe"     : "Arapahoe Avenue",
    			"Baselin"      : "Baseline Road",
                "Baseline"     : "Baseline Road",
    			"Blvd"         : "Boulevard",
                "Caria"        : "Caria Court",
                "Cherryvale"   : "Cherryvale Road",
    			"Cir"          : "Circle",
                "circle"       : "Circle",
    			"Colorado"     : 'West Alameda Parkway',
                "Colfax"       : "East Colfax Avenue",
                "Ct"           : "Court",
                "ct"           : "Court",
                "Dr"           : "Drive",
                "dr"           : "Drive",
                "Elm"          : "East Elm Street",
                "Etna"         : "Etna Court",
                "Grant"        : "Grant Place",
                "lane"         : "Lane",
                "Leetsdale"    : "Leetsdale Drive",
                "Ln"           : "Lane",
                "Main"         : "Main Street",
                "Mainstreet"   : "Main Street",
                "Osage"        : "Osage Drive",
                "Pennsylvania" : "Pennsylvania Avenue",
                "Pky"          : "Parkway",
                "Pkwy"         : "Parkway",
                "Pl"           : "Place",
                "Rd"           : "Road",
                "Rd."          : "Road",
                "rd"           : "Road",
                "Roadaddr"     : "Arapahoe Avenue",
                "S"            : "",
                "St"           : "Street",
                "St."          : "Street",
                "STreet"       : "Street",
                "Streer"       : "Street",
                "Strret"       : "Street",
                "st"           : "Street",
                "trail"        : "Trail",
                "Valmont"      : "Valmont Road",
                "Varra"        : "Varra Road"
                } # Map incorrect street types to desired

city_mapping = { "auroraa"      : "aurora",
                 "centenn"      : "centennial",
                 "demver"       : "denver",
                 "dener"        : "denver",
                 "edgwater"     : "edgewater",
                 "hemderson"    : "henderson",
                 "thorton"      : "thornton",
                 "westminister" : "westminster"
                } # Map incorrect city names to desired

## Update Functions #################################################

def update_street_name(name, expected = expected, exceptions = exceptions, highways = highways, county_roads = county_roads, mapping = addr_mapping):
    # Define streety type and correct if necessary
    kind = name.rsplit(None, 1)[-1]
    if kind in expected or kind in suites:
        name = name
    elif kind in exceptions:
        name = name
    elif kind in highways:
    	name = 'Highway ' + kind
    elif kind in county_roads:
    	name = 'County Road ' + kind
    else:
        name = name.replace(str(kind), addr_mapping[kind])
    return name

def update_postal_code(this_postal_code):
    # Take first 5-digits if postal code > 5 digits
    if len(this_postal_code) != 5:
        return this_postal_code[:5]
    else:
        return this_postal_code

def update_city(this_city):
    # Change city string to lower and correct if necessary
    lcity = this_city.lower()
    if lcity.find(',') != -1:
        return lcity[:lcity.find(',')]
    elif re.search('\sco', this_city) != None:
        return lcity[:lcity.find(' ')]
    elif lcity in city_mapping.keys():
        lcity = lcity.replace(lcity, city_mapping[lcity])
    else:
        return lcity
    return lcity

## Element Shaping and Writing to JSON #################################################

def shape_element(element):
    # Shaping the element to be pushed to JSON
    # Declare dict for new reshaped element
    node = {}
    # Declare dict for metadata of this node
    created = {}
    # Define the metadata fields we want to pull from this element
    created_fields = ['changeset', 'version', 'timestamp', 'user', 'uid']
    # Define other high level items of interest (example = 'id', 'type', 'pos')
    high_level_items = ['id', 'visible', 'type']
    # Define other elements of interest
    elems_of_int = ['highway', 'foot', 'bicycle', 'name', 'natural', 'ele', 'amenity', 'landuse', 'wheelchair', 'peak', 'website', 'phone', 'historic', 'religion', 'cuisine', 'microbrewery', 'fee', 'opening_hours']
    # If this element is node or way, do stuff below
    if element.tag == "node" or element.tag == "way" :
    	# First field we add to node is the type of node
    	node['type'] = element.tag
        # Store the element keys (for instance 'uid', 'changeset', 'timestamp', etc.)
        keys = element.attrib.keys()
        # Second we add the created metadata of interest, high_level_keys, position and their values
        for item in keys:
            if item in created_fields:
                created[item] = element.attrib[item]
            if item in high_level_items:
                node[item] = element.attrib[item]
            if 'lat' in keys:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        # Store created fields and values as element within the node
        node['created'] = created
        # If node contains address data, add address field
        for child in element:
        	if child.tag == 'tag':
        		if child.attrib['k'].startswith('addr:'):
        			node['address'] = {}
        # Populate address key (if present) and all other attributes of interest
        for child in element:
            if child.tag == 'tag':
                if child.attrib['k'].startswith('addr:') == 1 and child.attrib['k'].count(':') < 2:
                    field = child.attrib['k'][5:]
                    if field == 'street':
                        value = update_street_name(child.attrib['v'])
                    elif field == 'city':
                        value = update_city(child.attrib['v'])
                    elif field == 'postcode':
                        value = update_postal_code(child.attrib['v'])
                    else:
                        value = child.attrib['v']
                    node['address'].update({field : value})
                if child.attrib['k'] in elems_of_int:
                    node[child.attrib['k']] = child.attrib['v']
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

def process_map(file_in, pretty = False):
    # Process to JSON. Used start, end objects to improve performance
    # Depending upon file size... this may take a few minutes
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        context = ET.iterparse(file_in,events=('start','end'))
        context = iter(context)
        event, root = context.next()
        for event, element in context:
            if event == 'end':
                el = shape_element(element)
                if el:
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
            root.clear()
    return data

## Mongo Import Instructions (after JSON created) ###################################

# Start a mongod instance using ./mongod
# Open new terminal window and cd to mongo bin folder
# Move records from json to mongo with this command using mongo import
# ./mongoimport --db osm --collection osmb_807 --type json --file /Users/frankCorrigan/Udacity/OpenStreetMap-Analysis/OSM_Data_Project/denver-boulder_colorado.osm.json

