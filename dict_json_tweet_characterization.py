
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @ Author: Gustavo P. Avelar  (gpavelar)                      @
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

''' IMPORT PACKAGES '''
import sys
import io
# Dealing with json
import json
import simplejson
# Dealing with date and time
import datetime
import time
# Parsing command line parameters
import argparse
import re
import csv
from collections import OrderedDict

# THIS CODE ENSURE THE CORRECT ENCODING (OPTIONAL)
reload(sys)
sys.setdefaultencoding('utf-8')
# THE ID's OF SELECTED USERS OF THE 10 MOST POPULATED CITIES OF BRAZIL
top_cities = ["bh", "bsb", "ctba", "forz", "man", "poal", "rec", "rj", "sp", "ssa"]

''' GETS THE COMMAND LINE PARAMETERS '''
def get_parameters():
    global args
    parser = argparse.ArgumentParser(description='This program deal with json tweets and retrieve the information about selected users.')
    ''' Arquivo de entrada .json '''
    ''' Arquivo de saida das informacoes '''
    parser.add_argument('-i','--input', help='input filename in json format', required=True)
    parser.add_argument('-o','--output', help='file to store the informations', required=True)
    parser.add_argument('-c','--city', help='City to be evaluate \n[Belo horizonte - Use "bh", Brasilia - "bsb", Curitiba - "ctba", Fortaleza - "forz", Manaus - "man",  Porto Alegre - "poal",  Recife - "rec", Rio de Janeiro - "rj", Sao Paulo - "sp", Salvador - "ssa"] ', required=True)
    parser.add_argument('-u','--users_csv', help='file that store the informations about users and ids of twitter', required=False)
    parser.add_argument('-bd','--begindate', help='Begin date to be analyze', required=False)
    parser.add_argument('-ed','--enddate', help='End date to be analyze', required=False)
    args = vars(parser.parse_args())

   
''' Teste Tweet from the selected users with a dict '''
def operations_dict_tweets(database, output_information, city_name, dict_userid_count):
    print "#### Tweet of the selected users"

    # open tweets from json file
    tweets_file = open(database, "r")
    for line in tweets_file:
        try:
            #Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet:
                # get user id from each tweet
                user_id_comp = tweet['user']['id']
                # Check if the ID exist in the dictionary
                if dict_userid_count.has_key(str(user_id_comp)):
                    # increment the count of the selected ID
                    dict_userid_count[str(user_id_comp)] +=1
                    #print user_id_comp, dict_userid_count[str(user_id_comp)]
        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue
    tweets_file.close()

''' Count the mentions of the selected users '''
def operations_dict_mentions(database, output_information, city_name, dict_userid_mention):
    print "#### Mentions of the selected users"
    # open tweets from json file
    tweets_file = open(database, "r")
    for line in tweets_file:
        try:
            #Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet:
                    users_id_mention = [user_mention['id'] for user_mention in tweet['entities']['user_mentions']]
                    
                    for usersx_id in users_id_mention:
                        # Compare to user_id
                        if dict_userid_mention.has_key(str(usersx_id)):
                            dict_userid_mention[str(usersx_id)] +=1
        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue
    tweets_file.close()
    
''' Count retweet '''
def operations_dict_retweet(database, output_information, city_name, dict_userid_retweet):
    print "#### Retweet of the selected users"

    # open tweets from json file
    tweets_file = open(database, "r")
    for line in tweets_file:
        try:
            #Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'retweeted_status' in tweet:
                user_retweeted =  tweet['retweeted_status']['user']['id']
                if dict_userid_retweet.has_key(str(user_retweeted)):
                    dict_userid_retweet[str(user_retweeted)] +=1              
        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue
    tweets_file.close()
 
''' Teste Tweet from the selected users with a dict '''
def operations_dict_tweets_all(database, output_information, city_name, dict_userid_count,dict_userid_retweet, dict_userid_mention):
    print "#### All operations"

    # open tweets from json file
    tweets_file = open(database, "r")
    for line in tweets_file:
        try:
            #Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet:
                # get user id from each tweet
                user_id_comp = tweet['user']['id']
                # Check if the ID exist in the dictionary
                
                if dict_userid_count.has_key(str(user_id_comp)):
                    # increment the count of the selected ID
                    dict_userid_count[str(user_id_comp)] +=1
                    #print user_id_comp, dict_userid_count[str(user_id_comp)]

                # users mentioned
                users_id_mention = [user_mention['id'] for user_mention in tweet['entities']['user_mentions']]
                    
                for usersx_id in users_id_mention:
                        # increment the count of the selected ID
                        if dict_userid_mention.has_key(str(usersx_id)):
                           dict_userid_mention[str(usersx_id)] +=1    

                # Retweet status
                user_retweeted =  tweet['retweeted_status']['user']['id']
                if dict_userid_retweet.has_key(str(user_retweeted)):
                    dict_userid_retweet[str(user_retweeted)] +=1    
        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue
    tweets_file.close()

'''MAIN FUNCTION'''
# Call the python with args
# python automatic_tweets.py -i arquivo_tweets.json -o output_file -c city_name
# -u -bd -ed are not required

if ( __name__ == "__main__" ):
    get_parameters()
    # json file to be used to calculate the following informations: number of tweets, retweets and mentions.
    database = args['input']
    # file to store the information of tweets, mentions and retweets
    output_information = args['output']
    # name the city used to be verify
    city_name = args['city']
    # file with the information about selected users 
    users_file_csv = args['users_csv'] 
    ## @@ not being used yet
    # date that starts the dump
    date_start = args['begindate']
   	# date that finish the dump
    date_end = args['enddate']

    # Create dictionaries
    dict_userid_name = {}
    dict_userid_count = {}
    dict_userid_retweet = {}
    dict_userid_mention = {}
        
    
    # verificar se o parametro city pertence a lista de top_cities
    #top_cities = ["bh", "bsb", "ctba", "forz", "man", "poal", "rec", "rj", "sp", "ssa"]
    if(city_name in top_cities):
        # Load a dictionary of the selected city
        # arq = open(output_information+"_"+city_name+'.txt', 'a+')
        users_file_csv = "cities_csv/"+city_name+".csv"
        # csv reader from userid/username file
        reader = csv.reader(open(users_file_csv, 'r'))
        
        for row in reader:
            users_id, users_name = row
            dict_userid_name[users_id] = users_name
            dict_userid_count[users_id] = 0
            dict_userid_retweet[users_id] = 0
            dict_userid_mention[users_id] = 0

        
        startime = time.time()
        operations_dict_tweets(database, output_information, city_name, dict_userid_count)
        stoptime = time.time()
        print "Time to retrievel characterization # tweets: ", stoptime-startime
        
        startime = time.time()
        operations_dict_mentions(database, output_information, city_name, dict_userid_mention)
        stoptime = time.time()
        print "Time to retrievel characterization # mentions: ", stoptime-startime
        
        startime = time.time()
        operations_dict_retweet(database, output_information, city_name, dict_userid_retweet)
        stoptime = time.time()
        print "Time to retrievel characterization # retweets: ", stoptime-startime
        
        # Save the results
        json_output = []
        # dict_test = {}
        # Open file to stored the characterization
        with open(output_information+"_"+city_name+".json", 'w') as fp:
            for rows in dict_userid_name:
            	# dict_test.OrderedDict()
            	dict_output = {"name_": dict_userid_name[rows], "num_tweets": dict_userid_count[rows], "num_mentions": dict_userid_mention[rows], "num_retweets": dict_userid_retweet[rows]} 
                json_output.append(dict_output)
            # print json_output
            json.dump(json_output,fp)
        # OUTPUT in TXT
        # arq = open(output_information+"_"+city_name+".txt", "a+")
        # arq.write("User ID/NAME \t # Tweets \t # Mentions \t # Retweets \n")
        # for rows in dict_userid_name:
        #     arq.write("@"+dict_userid_name[rows]+ "\t"+ str(dict_userid_count[rows]) + "\t"+ str(dict_userid_mention[rows]) +"\t"+ str(dict_userid_retweet[rows])+ "\n")
        #     #print "@"+dict_userid_name[rows], dict_userid_count[rows],  dict_userid_mention[rows], dict_userid_retweet[rows]
        # arq.close()
       
    elif (city_name == "all"):
        # Open csv file
        users_file_csv = "cities_csv/users_id_name.csv"
        # csv reader from userid/username file
        reader = csv.reader(open(users_file_csv, 'r'))

        # For to fill up the dictionary
        for row in reader:
            users_id, users_name = row
            dict_userid_name[users_id] = users_name
            dict_userid_count[users_id] = 0
            dict_userid_retweet[users_id] = 0
            dict_userid_mention[users_id] = 0


        startime = time.time()
        operations_dict_tweets_all(database,output_information, city_name, dict_userid_count, dict_userid_retweet, dict_userid_mention)
        stoptime = time.time()
        print "Time to retrievel characterization # tweets: ", stoptime-startime

        json_output = []
        # dict_test = {}
        # Open file to stored the characterization
        with open(output_information+'.json', 'w') as fp:
            for rows in dict_userid_name:
            	# dict_test.OrderedDict()
            	dict_output = {"name_": dict_userid_name[rows], "num_tweets": dict_userid_count[rows], "num_mentions": dict_userid_mention[rows], "num_retweets": dict_userid_retweet[rows]} 
                json_output.append(dict_output)
            # print json_output
            json.dump(json_output,fp)

        # OUTPUT in TXT
        # arq = open(output_information+"all.txt", "a+")
        # arq.write("User ID/NAME \t # Tweets \t # Mentions \t # Retweets \n")
        # for rows in dict_userid_name:
            # arq.write("@"+dict_userid_name[rows]+ "\t"+ str(dict_userid_count[rows]) + "\t"+ str(dict_userid_mention[rows]) +"\t"+ str(dict_userid_retweet[rows])+ "\n")
            #print "@"+dict_userid_name[rows], dict_userid_count[rows],  dict_userid_mention[rows], dict_userid_retweet[rows]
        # arq.close()
    else:
        print "@@@ choose a existent option for the city (-c) parameter"
