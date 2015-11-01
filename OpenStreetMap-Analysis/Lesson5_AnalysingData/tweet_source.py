#!/usr/bin/env python
"""
The tweets in our twitter collection have a field called "source". This field describes the application
that was used to create the tweet. Following the examples for using the $group operator, your task is 
to modify the 'make-pipeline' function to identify most used applications for creating tweets. 
As a check on your query, 'web' is listed as the most frequently used application.
'Ubertwitter' is the second most used. 

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation pipeline
that can be passed to the MongoDB aggregate function. As in our examples in this lesson, the aggregation 
pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. 
If you want to run this code locally on your machine, you have to install MongoDB, 
download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the twitter dataset 
used in examples in this lesson. 
If you attempt some of the same queries that we looked at in the lesson examples,
your results will be different.
"""

"""
{"text":"eu preciso de terminar de fazer a minha tabela, est\u00e1 muito foda **","in_reply_to_status_id":null,"retweet_count":null,"contributors":null,"created_at":"Thu Sep 02 18:11:23 +0000 2010","geo":null,"source":"web","coordinates":null,"in_reply_to_screen_name":null,"truncated":false,"entities":{"user_mentions":[],"urls":[],"hashtags":[]},"retweeted":false,"place":null,"user":{"friends_count":73,"profile_sidebar_fill_color":"768575","location":"","verified":false,"follow_request_sent":null,"favourites_count":1,"profile_sidebar_border_color":"1c9dbd","profile_image_url":"http://a2.twimg.com/profile_images/1036412454/OgAAADXK9q6kaxrvfwQTINH66RVLAH9YHb-veRTA4FaWb9KtbGGV_yKTGzmvzTfJidqAb5gK_mpspIE-MIvAASGH2CwAm1T1UIPQk0-HS8x_TV5kdnW30nch7ODk-1_normal.jpg","geo_enabled":false,"created_at":"Fri Jul 03 21:44:05 +0000 2009","description":"s\u00f3 os loucos sabem (:","time_zone":"Brasilia","url":"http://http://www.orkut.com.br/Main#Profile?uid=1433295880233078770","screen_name":"Bia_cunha1","notifications":null,"profile_background_color":"081114","listed_count":0,"lang":"en","profile_background_image_url":"http://a1.twimg.com/profile_background_images/133178546/biatwitter.jpg","statuses_count":3504,"following":null,"profile_text_color":"25b8c2","protected":false,"show_all_inline_media":false,"profile_background_tile":true,"name":"Beatriz Helena Cunha","contributors_enabled":false,"profile_link_color":"eb55b6","followers_count":102,"id":53507833,"profile_use_background_image":true,"utc_offset":-10800},"favorited":false,"in_reply_to_user_id":null,"id":22819396900}
{"text":"Study Implicates Immune System in Parkinson's Disease Pathogenesis http://bit.ly/duhe4P","in_reply_to_status_id":null,"retweet_count":null,"contributors":null,"created_at":"Thu Sep 02 18:11:23 +0000 2010","geo":null,"source":"<a href=\"http://twitterfeed.com\" rel=\"nofollow\">twitterfeed</a>","coordinates":null,"in_reply_to_screen_name":null,"truncated":false,"entities":{"user_mentions":[],"urls":[{"indices":[67,87],"url":"http://bit.ly/duhe4P","expanded_url":null}],"hashtags":[]},"retweeted":false,"place":null,"user":{"friends_count":780,"profile_sidebar_fill_color":"DDEEF6","location":"","verified":false,"follow_request_sent":null,"favourites_count":0,"profile_sidebar_border_color":"C0DEED","profile_image_url":"http://a0.twimg.com/profile_images/642263456/Medscape_Pathology_normal.gif","geo_enabled":false,"created_at":"Fri Jan 08 17:40:11 +0000 2010","description":"Latest medical news, articles, and features from Medscape Pathology.","time_zone":"Eastern Time (US & Canada)","url":"http://www.medscape.com/pathology","screen_name":"MedscapePath","notifications":null,"profile_background_color":"06649a","listed_count":26,"lang":"en","profile_background_image_url":"http://a1.twimg.com/profile_background_images/68099960/TwitterWrapper_Pathology.jpg","statuses_count":475,"following":null,"profile_text_color":"333333","protected":false,"show_all_inline_media":false,"profile_background_tile":false,"name":"Medscape Pathology","contributors_enabled":false,"profile_link_color":"0084B4","followers_count":309,"id":103041614,"profile_use_background_image":true,"utc_offset":-18000},"favorited":false,"in_reply_to_user_id":null,"id":22819397000}
"""

from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.examples

# Create twitter collection in examples database
def  make_twitter_collection():
    jsonstr = open('twitter.json').read()
    jsonarr = jsonstr.split( '\n' )

    tweets = []
    for jsonstr in jsonarr:
        tweets.append(json.loads(jsonstr))

    db.twitter.insert(tweets)

# Define the desired aggregation
def make_pipeline():
    pipeline = [{ "$group" : { "_id" : "$source",
                               "count" : { "$sum" : 1 } } }, 
                { "$sort" : { "count" : -1 } }]
    return pipeline

# 
def tweet_sources(db, pipeline):
    result = db.twitter.aggregate(pipeline)
    return result

if __name__ == '__main__':
    pipeline = make_pipeline()
    result = tweet_sources(db, pipeline)
    import pprint
    pprint.pprint(result)
    assert result["result"][0] == {u'count': 868, u'_id': u'web'}
