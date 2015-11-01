#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values. 

The following things should be done:
- DONE keys of the dictionary changed according to the mapping in FIELDS dictionary
- DONE trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- DONE if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- DONE if a value of a field is "NULL", convert it to None
- DONE if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
  * Note that the value associated with the classification key is a dictionary with
    taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'spiders.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

# PLACEHOLDER
filename = DATAFILE

def clean_label(label):
    return re.sub(r" .*","",label)

def clean_name(name):
    if bool(re.search(r'\d', el['name'])) == True or el['name'] == 'NULL':
        return el['label']

def parse_array(v):
    if v == 'NULL':
        return None
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]

def restructure(alist):
    for el in alist:
        el['classification'] = {
                    'family': el['family'],
                    'class': el['class'],
                    'phylum': el['phylum'],
                    'order': el['order'],
                    'kingdom': el['kingdom'],
                    'genus': el['genus']
                }
        del el['family']
        del el['class']
        del el['phylum']
        del el['order']
        del el['kingdom']
        del el['genus']
    return alist

    with open('Lighthouse.csv', "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            data.append(line)

def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            # now you are iterating across each observation
            # {name: frank, state: nj, honny: jess, etc.}
            temp = {}
            for field, val in line.iteritems():
                # now you are iterating through each element in a observation
                # field = name and val = frank
                if field not in process_fields:
                    # if name isn't in process fields, do nothing
                    continue
                if field in process_fields:
                    # if name is in process fields, add it to a temp list
                    temp[field] = val # key is 'order_label', val is 'correct'
                    # key should be FIELDS['order_label'] which is 'order'
                    # so switch it..
                    # but watch out because if the new name and the old name are the same... the whole thing will be deleted
                    if field != FIELDS[field]:
                        temp[FIELDS[field]] = temp[field]
                        del temp[field]
                # go back and loop through the next field in this observation
            # after you finish looking through that observation... add it to the data list
            data.append(temp)
            # now go back and loop through the next observation
        for el in data:
            # In this loop we'll clean up a few items first by parsing synonym string into list
            el['synonym'] = parse_array(el['synonym'])
            # Next by removing nonsense (aka '(sdfwef)') from labels 
            el['label'] = clean_label(el['label'])
            # 2nd if name is null or has special chars, replace it with the label
            if (bool(re.search(r'[^a-zA-Z\d\s:]', el['name'])) == True) or (el['name'] == 'NULL'):
                el['name'] = el['label']
            # Replace all NULL values as None
            for key in el:
                if el[key] == 'NULL':
                    el[key] = None
        # Restructure to create a classiffication feild within dict
        restructure(data)

    return data

# If you want to write data to json file...
# with open('spiders.json', 'w') as outfile:
#     json.dump(data, outfile)

def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None, 
        "name": "Argiope", 
        "classification": {
            "kingdom": "Animal", 
            "family": "Orb-weaver spider", 
            "order": "Spider", 
            "phylum": "Arthropod", 
            "genus": None, 
            "class": "Arachnid"
        }, 
        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
        "label": "Argiope", 
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()