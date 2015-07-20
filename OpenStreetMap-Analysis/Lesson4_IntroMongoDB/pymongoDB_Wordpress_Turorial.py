#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import re
from pymongo import MongoClient

# Define source file and fields of interest
DATAFILE = 'Arachnid.csv'
ORIG_FIELDS = ['rdf-schema#label',
               'synonym',
               'phylum_label',
               'family_label',
               'rdf-schema#comment']
NEW_FIELDS = ['rdf-schema#label',
              'genus_label']

def process_file(filename, fields):
    # This function will turn our fields of interest from our source file into a list of dictionaries
    # data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # Skip first 3 rows bc they are metadata
        for i in range(3):
            l = reader.next()

        # Iterate through each spider...
        for line in reader:
            temp = {}
            # Iterate through each field of target spider
            for field, val in line.iteritems():
                if field not in fields:
                    continue
                # Only add required fields
                if field in fields:
                    temp[field] = val

            # Append spider to our data list
            data.append(temp)

def insert_data(data, db):
    # This function inserts list of dictionaries (in json format) into mongodb
    db.arachnid.insert(data)

def make_it_happen():
    # This function that leverages insert_data function and creates examples database and arachnid collection
    # Import pymongo and connect to running mongod instance
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    # Read 'dictionaries' into arachnid collection using insert_data function
    with open('arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)

def add_field(filename, fields):
    # This function will give us new field of interest
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # Skip first 3 rows bc they are metadata
        for i in range(3):
            l = reader.next()

        # Iterate through each spider...
        for line in reader:
            temp = {}
            # Iterate through each field of target spider
            for field, val in line.iteritems():
                if field not in fields:
                    continue
                if field in fields:
                    temp[field] = val

            data.append(temp)                    

def update_db(data, db):
    for el in data:
        # Loop through the spiders in the new fields data list, match the label with existing spiders in database
        spider = db.arachnid.find_one({'rdf-schema#label': el['rdf-schema#label']})
        # Then add new genus field to that spiders data
        spider['genus_label'] = el['genus_label']
        db.arachnid.save(spider)

if __name__ == "__main__":

    # CREATE SPIDERS LIST
    data = []
    process_file(DATAFILE, ORIG_FIELDS)
    print data[0]

    # CREATE SPIDERS JSON
    with open('arachnid.json', 'w') as outfile:
        json.dump(data, outfile)

    # CREATE DATABASE AND COLLECTION
    make_it_happen()

    # GRAB NEW FIELD FROM CSV
    data = []
    add_field(DATAFILE, NEW_FIELDS)

    # UPDATE DATABASE WITH GENUS
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples
    update_db(data, db)

