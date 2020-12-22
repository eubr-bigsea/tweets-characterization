#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Example of Mongo connection, Mongo query
to retrieve tweets and operations using the 
json package.
'''

''' IMPORT PACKAGES '''
import sys
# Mongo DB management
import pymongo
# Dealing with json
import json
# Dealing with date and time
import datetime
# from datetime import datetime 

import time
# Parsing command line parameters
import argparse
import re
# THIS CODE ENSURE THE CORRECT ENCODING (OPTIONAL)
reload(sys)
sys.setdefaultencoding('utf-8')

# THIS CODE IMPORT A .py file
from filters import *

from bson.json_util import dumps
from bson import Binary, Code


from pytz import timezone
import pytz

paths_selected = [
    "_id", "id", "text", "created_at", "geo", "place", "coordinates", "entities", 
    "_tmp_", "control", "lang", "source", "user.id", "user.screen_name", "user.location", "user.profile_image_url", 
    "user.profile_image_url_https", "user.friends_count", "user.followers_count", "user.description", "user.lang",
    "retweeted_status.id", "retweeted_status.text", "retweeted_status.created_at",
    "retweeted_status.user.id", "retweeted_status.user.screen_name",
    "retweeted_status.retweet_count", "retweeted_status.entities"
]

''' GETS THE COMMAND LINE PARAMETERS '''
def get_parameters():
    global args
    parser = argparse.ArgumentParser(description='This program retrieve from MongoDB and deal with json tweets.')
    parser.add_argument('-s','--server', help='Name of the MongoDB server', required=True)
    parser.add_argument('-p','--persistence', help='Name of the MongoDB persistence slave', required=False)
    parser.add_argument('-d','--database', help='Name of the MongoDB database', required=True)
    parser.add_argument('-c','--collection', help='Name of the MongoDB collection', required=True)
    parser.add_argument('-sd','--startDate', help='The date when a project or task is scheduled to begin/start. Ex: "AAAA-MM-DD HH:MM:SS" (ISO-8601)', required=True)
    parser.add_argument('-ed','--endDate', help='The date when a project or task is scheduled to finish/end. Ex: "AAAA-MM-DD HH:MM:SS" (ISO-8601)', required=True)
    parser.add_argument('-o','--output', help='Name of the output file', required=True)
    args = vars(parser.parse_args())



''' OPENS THE MONGO DB CONNECTION '''
def connect_db():
    global args, client
    ERROR = True #Controls if occurs connection error
    count_attempts = 0 #Number of attempts for connection
    while ERROR:
        try:
            count_attempts += 1
            # OPEN THE CONNECTION WITH THE MONGO DB
            if (args['persistence'] == None): client = pymongo.MongoClient(args['server'])
            else: client = pymongo.MongoClient([args['server'], args['persistence']])
            client.server_info()
            print 'MongoDB Connection opened after', str(count_attempts), 'attempts', str(datetime.datetime.now())
            ERROR = False
        except pymongo.errors.ServerSelectionTimeoutError:
            print 'MongoDB connection failed after', str(count_attempts), 'attempts. ', \
                  str(datetime.datetime.now()), '. A new attempt will be made in 60 seconds'
            ERROR = True
            time.sleep(60)
        if ( count_attempts > 20 ):
           print 'It was not possible to connect to MongoDB. Shutting down...'
           sys.exit()

'''Count the retrieved tweets and store each tweet to the dump'''
def operations_dates(records, paths, output_file):
    temp = 0
    # Save the results
    # Colocar a data do dump no arquivo
    # http://stackoverflow.com/questions/11280382/python-mongodb-pymongo-json-encoding-and-decoding
    arq = open(output_file, "w")
    for record in records:
        # print record['human_date']
        output_filter = dict_find(paths, record)

        # Variable to aux the human readable date
        auxDate = output_filter['created_at']
        # Create a new field
        output_filter['human_date'] =  str(auxDate)
        arq.write(dumps(output_filter)+'\n')
        temp+=1
    print 'Quantidade de registros:', temp

'''FUNCTION TO RETRIEVE THE TWEETS BETWEEN TWO SPECIFIC DATES'''
def retrieve_data_from_dates(collection, startDate,endDate):
    # run correct
    return collection.find({'created_at': {'$gte': startDate, '$lte': endDate }}, no_cursor_timeout=False)

'''MAIN FUNCTION'''
if ( __name__ == "__main__" ):
    get_parameters()
    connect_db()
    database = client[args['database']]
    collection = database[args['collection']]
    startDate = args['startDate']
    endDate = args['endDate']
    output_file = args['output']

    # Format the date
    fmt = '%Y-%m-%d %H:%M:%S'

    # UTC tzinfo=pytz.utc
    # -03:06 hours the timezone of Sao Paulo
    # gmz_tz = pytz.timezone('America/Sao_Paulo')
    gmt_tz = pytz.timezone('Etc/GMT+3')

    auxStartDate = datetime.datetime.strptime(startDate,fmt)
    auxStartDate = auxStartDate.replace(tzinfo=gmt_tz)

    auxEndDate = datetime.datetime.strptime(endDate,fmt)
    auxEndDate = auxEndDate.replace(tzinfo=gmt_tz)

    paths_selected = [
        "_id", "id", "text", "created_at", "geo", "place", "coordinates", "entities", 
        "_tmp_", "control", "lang", "source", "user.id", "user.screen_name", "user.location", "user.profile_image_url", 
        "user.profile_image_url_https", "user.friends_count", "user.followers_count", "user.description", "user.lang",
        "retweeted_status.id", "retweeted_status.text", "retweeted_status.created_at",
        "retweeted_status.user.id", "retweeted_status.user.screen_name",
        "retweeted_status.retweet_count", "retweeted_status.entities"
    ]

    print "=== Query Starting"
    startime = time.time()
    records = retrieve_data_from_dates(collection, auxStartDate, auxEndDate)
    stoptime = time.time()
    print "Time to retrievel data from collection: ", stoptime-startime
    print "=== Query Finished"
	
    # Create the outputfile name
    output_file = output_file+"_"+re.sub(" ","_",startDate)+"_"+re.sub(" ","_",endDate)+".json"


    startime = time.time()
    operations_dates (records,paths_selected,output_file)
    stoptime = time.time()
    print "Time to retrievel data from collection: ", stoptime-startime


	# startime = time.time()
 #    records = retrieve_data(collection)
 #    stoptime = time.time()
 #    print "Time to retrievel data from collection: ", stoptime-startime

 #    startime = time.time()
 #    operations(records)
 #    stoptime = time.time()
 #    print "Time to perfom operations on retrieve data: ", stoptime-startime
    
