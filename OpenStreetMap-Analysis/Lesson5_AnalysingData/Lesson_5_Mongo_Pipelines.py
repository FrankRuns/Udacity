'''Use an aggregation query to answer the following question. 

What is the most common city name in our cities collection?

Your first attempt probably identified None as the most frequently occurring city name. 
What that actually means is that there are a number of cities without a name field at all. 
It's strange that such documents would exist in this collection and, depending on your situation, 
might actually warrant further cleaning. 

To solve this problem the right way, we should really ignore cities that don't have a name specified. 
As a hint ask yourself what pipeline operator allows us to simply filter input? 
How do we test for the existence of a field?
'''

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [ { "$match" : { "name" : { "$exists" : True } } },
                 { "$group" : { "_id" : "$name",
                                "count" : { "$sum" : 1 } } },
                 { "$sort" : { "count" : -1 } },
                 { "$limit" : 1 } ]

    return pipeline

'''Use an aggregation query to answer the following question. 

Which Region in India has the largest number of cities with longitude between 75 and 80?
'''

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [ { "$match" : { "country" : "India" } },
                 { "$match" : { "lon" : { "$gt" : 75, "$lt" : 80 } } },
                 { "$unwind" : "$isPartOf" },
                 { "$group" : { "_id" : "$isPartOf",
                                "count" : { "$sum" : 1 } } },
                 { "$sort" : { "count" : -1 } },
                 { "$limit" : 1 } ]
    return pipeline

'''Use an aggregation query to answer the following question. 

Extrapolating from an earlier exercise in this lesson, find the average regional city population 
for all countries in the cities collection. What we are asking here is that you first calculate the 
average city population for each region in a country and then calculate the average of all the 
regional averages for a country. As a hint, _id fields in group stages need not be single values. 
They can also be compound keys (documents composed of multiple fields). You will use the same 
aggregation operator in more than one stage in writing this aggregation query. I encourage you to 
write it one stage at a time and test after writing each stage.
'''

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [ { "$unwind" : "$isPartOf" },
                 { "$group" : { "_id" : { "country" : "$country", "region" : "$isPartOf" },
                                "region_avg" : { "$avg" : "$population" } } },
                 { "$group" : { "_id" : "$_id.country",
                                "avgRegionalPopulation" : { "$avg" : "$region_avg" } } } ] 

    return pipeline