#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

'''
This file contains the analysis of open street map data
using both the Python MongoDB driver and MongoDB Shell.
'''

# MongoDB Query and Data Analysis ##################################################

# Initiate Mongo client
client = MongoClient("mongodb://localhost:27017")
db = client.osm

# Using mongo shell look at particular street names for unknown street type in order to clean
db.osmb_807.find({ "address.street" : '6001'})
# Go to http://www.openstreetmap.org/way/223312254 to see that this node is on South Newport Street
# Change the record in the database
db.osmb_807.update({"address.street" : "6001"},
                   { $set: { "address.street" : "South Newport Street"} } )
# Here are the first three changes we make with this method
'6001' = 'South Newport Street'
'1601' = 'Central Campus Mall'
'6001' = 'South Newport Street'

# Using python driver find # of occurances for cities
result = db.osmb_807.aggregate([{ "$match" : { "address.city" : { "$exists" : 1 } } },
                                { "$group" : { "_id" : "$address.city",
                                               "count" : { "$sum" : 1 } } },
                                { "$sort" : { "count" : -1 } } ] )

# Using mac terminal look at file sizes
ls -lh denver-boulder_colorado.osm
ls -lh denver-boulder_colorado.osm.json

# Using mongo shell, how many documents?
db.osmb_807.find().count()

# Using python driver how many nodes and ways?
result = db.osmb_807.aggregate([{ "$group" : { "_id" : "$type",
                                               "count" : { "$sum" : 1 } } },
                                { "$sort" : { "count" : -1 } } ] ) 

# Using python driver, who is the top contributor by # of contributions?
result = db.osmb_807.aggregate([{ "$group" : { "_id" : "$created.user",
                                               "count" : { "$sum" : 1 } } },
                                { "$sort" : { "count" : -1 } },
                                { "$limit" : 1 } ] )

# Using mongo shell and python driver, what percent of contributors made only a single contribution?
db.osmb_807.distinct("created.user").length
result = db.osmb_807.aggregate( [ { "$group" : { "_id" : "$created.user",
                                                 "count" : { "$sum" : 1 } } },
                                  { "$group" : { "_id" : "$count",
                                                 "num_users" : { "$sum" : 1 } } },
                                  { "$sort" : { "_id" : 1 } },
                                  { "$limit" : 1 } ] )

# To get counts for every user so we can create a histogram
result = db.osmb_807.aggregate( [ { "$group" : { "_id" : "$created.user",
												            "count" : { "$sum" : 1 } } } ] )
data = []
for el in result:
	data.append(el['count'])
import matplotlib.pyplot as plt
data.sort()
plt.hist(data, bins=50)
plt.ylabel('people with that # of contributions')
plt.xlabel('# contributions')
plt.show()

# Using python, how many footways (runnin trails) are there in this map?
result = db.osmb_807.aggregate( [ { "$match" : { "highway" : "footway" } },
                                  { "$group" : { "_id" : "footway",
                                                 "count" : { "$sum" : 1 } } } ] )

# Using python, look at the first footway element to see how its structured
result = db.osmb_807.aggregate( [ { "$match" : { "highway" : "footway" } },
                                  { "$limit" : 5 } ] )

# The trail goes to a peak, what's the highest peak in our dataset?
result = db.osmb_807.aggregate( [ { "$match" : { "natural" : "peak" } },
                                  { "$project" : { "_id" : 0,
                                                   "Peak" : "$name",
                                                   "Elevation" : "$ele",
                                                   "User" : "$created.user"} },
                                  { "$sort" : { "Elevation" : -1 } } ] )

# Using mongo shell, how many peaks are there in the dataset?
 db.osmb_807.find({"natural" : "peak"}).count()

# Other fun queries

# To get top amenities
result = db.osmb_807.aggregate( [ { "$match" : { "amenity" : { "$exists" : 1 } } },
                                  { "$group" : { "_id" : "$amenity",
                                                 "count" : { "$sum" : 1 } } },
                                  { "$sort" : { "count" : -1} },
                                  { "$limit" : 10 } ] )

# Tagged as natural
result = db.osmb_807.aggregate( [ { "$match" : { "natural" : { "$exists" : 1 } } },
                                  { "$group" : { "_id" : "$natural",
                                                 "count" : { "$sum" : 1 } } },
                                  { "$sort" : { "count" : -1 } } ] )

# This is popular religion
result = db.osmb_807.aggregate( [ { "$match" : { "amenity" : { "$exists" : 1 },
                                                 "amenity" : "place_of_worship" } },
                                  { "$group" : { "_id" : "$religion",
                                                 "count" : { "$sum" : 1 } } },
                                  { "$sort" : { "count" : -1} },
                                  { "$limit" : 5 } ] )

# This is popular cuisine.
result = db.osmb_807.aggregate( [ { "$match" : { "amenity" : { "$exists" : 1 }, "amenity":"restaurant"} },
                                  { "$group" : { "_id" : "$cuisine",
                                                 "count" : { "$sum" : 1 } } },
                                  { "$sort" : { "count" : -1} },
                                  { "$limit" : 10 } ] )


