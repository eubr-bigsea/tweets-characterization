# Tweets statistics
# @ Author: Rodrigo Lemos Cardoso
# -----------------------------------------------------------------
# This script provides a profile, term and geolocation based statistics.
# The statistic is defined as follows:
# Given: Json file of tweets and list of target profiles using this format:
# <USERNAME> <CITY>, for every line, we do:
# As for the target profile statistics
# - Extract every tweet coming from target profiles
# - Extract every tweet that mentions a target profile
# - Extract every tweet that retweets a target profile
# As for the terms statistics
# - Extract tweets that were collected by hashtag
# - Extract tweets that were collected by keyword
# - Extract tweets that were collected by hashtags or keyword
# - Extract tweets that were collected by hashtags and keyword
# -----------------------------------------------------------------

import argparse
import os
from subprocess import call
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
Necessary in order to read the json file correctly
'''
false = False
true = True
null = None

''' GETS THE COMMAND LINE PARAMETERS '''
def get_parameters():
    global args
    parser = argparse.ArgumentParser(description='Compute basic statistics on tweet data')
    parser.add_argument('-i','--input', help='input filename in json format', required=True)
    parser.add_argument('-p','--profiles', help='file that store the informations about users of twitter. Format should be <USERNAME> <CITY> on each line', required=True)
    args = vars(parser.parse_args())


class Stats:
    '''
    Class that handle the statistics
        The list of profiles will be a dictionary of usernames mapped to
        a dictionary of two fields: city (from where the profiles are from)
        and a dictionary of stats (count of tweets, mentions and retweets)
    '''
    def __init__(self, list_of_profiles_file):
        self.list_of_profiles = {}
        profiles = []
        # Reads every profile and its city while prepares the statistic for tweets, retweets and mentions
        with open(list_of_profiles_file, 'r') as f:
            profiles = f.read().split('\n')
        for line in profiles:
            profile = line.split()[0]
            city = ''.join(line.split()[1:])
            self.list_of_profiles[profile] = {}
            self.list_of_profiles[profile]['city'] = city
            self.list_of_profiles[profile]['stats'] = {}
            self.list_of_profiles[profile]['stats']['tweets'] = 0
            self.list_of_profiles[profile]['stats']['retweets'] = 0
            self.list_of_profiles[profile]['stats']['mentions'] = 0
        self.hashtag_stats = {}
        self.keywords_stats = {}

    '''
    Test if the tweet belongs to a target profile
    '''
    def test_if_belongs_to_target_profile(self, tweet):
        username = tweet['user']['screen_name']
        if username in self.list_of_profiles.keys():
            return True
        else:
            return False

    '''
    Test if the tweet retweets a target profile
    '''
    def test_if_retweets_target_profile(self, tweet):
        if 'retweeted_status' in tweet.keys():
            if 'quoted_status' in tweet['retweeted_status'].keys():
                if tweet['retweeted_status']['quoted_status']['user']['screen_name'] in self.list_of_profiles.keys():
                    return True
        return False

    '''
    Test if the tweet mentions a target profile
    '''
    def test_if_mentions_target_profile(self, tweet):
        mentions = []
        for mention in tweet['entities']['user_mentions']:
            if mention['screen_name'] in self.list_of_profiles.keys():
                mentions.append(mention['screen_name'])
        return set(mentions)

    '''
    Test if the tweet was collected by hashtag
    '''
    def test_if_has_hashtags(self, field):
        if field['id'] == 354:
            return True
        else:
            return False

    '''
    Test if the tweet was collected by keyword
    '''
    def test_if_has_keywords(self, field):
        if field['id'] == 355:
            return True
        else:
            return False

    '''
    Test if the tweet is geolocated
    '''
    def test_if_is_geolocated(self, tweet):
        if 'geo' in tweet.keys():
            if tweet['geo'] != null:
                return True
        return False

    '''
    Get the top 10 profiles with the most tweets + retweets + mentions
    '''
    def get_most_popular_profiles(self):
        return sorted(self.list_of_profiles.iteritems(), key=lambda (k,v): (v['stats']['tweets'] + v['stats']['mentions'] + v['stats']['retweets'],k))[-10:]
    
    '''
    Compute the statistic
    '''
    def compute_stats(self, file_of_tweets):

        tweets_from_target_profiles = 0
        tweets_using_terms = 0
        tweets_using_hashtags = 0
        tweets_using_keywords = 0
        tweets_using_hashtags_and_keywords = 0
        geolocated_tweets = 0

        tweets_from_target_profiles_and_using_terms = 0
        tweets_from_target_profiles_and_geolocated = 0
        tweets_using_terms_and_geolocated = 0

        tweets_from_target_profiles_using_terms_and_geolocated = 0

        # For every tweet
        with open(file_of_tweets, 'r') as f:
            for line in f:
                # Removes the last character of the json line (It is a linebreak)
                tweet = eval(line[:-1])
                # Get the author
                username = tweet['user']['screen_name']
                # Get the type of collect
                coleta = tweet['control']['coletas']

                # Check profile informations
                is_from_profile = self.test_if_belongs_to_target_profile(tweet)
                is_retweeting_profile = self.test_if_retweets_target_profile(tweet)
                is_mentioning_profile = self.test_if_mentions_target_profile(tweet)

                if is_from_profile:
                    self.list_of_profiles[username]['stats']['tweets'] += 1
                    tweets_from_target_profiles += 1

                if is_retweeting_profile:
                    self.list_of_profiles[profile]['stats']['retweets'] += 1

                for profile in is_mentioning_profile:
                    self.list_of_profiles[profile]['stats']['mentions'] += 1

                collected_by_hashtag = False
                collected_by_keyword = False

                # Check terms informations
                for k in coleta:

                    # If it was not collected by term, we skip it
                    if 'terms' not in k.keys():
                        continue

                    has_hashtag = self.test_if_has_hashtags(k)
                    has_keyword = self.test_if_has_keywords(k)

                    for term in k['terms']:
                        if has_hashtag:
                            if term not in self.keywords_stats.keys():
                                self.keywords_stats[term] = 0
                            self.keywords_stats[term] += 1
                            collected_by_hashtag = True

                        if has_keyword:
                            if term not in self.hashtag_stats.keys():
                                self.hashtag_stats[term] = 0
                            self.hashtag_stats[term] += 1
                            collected_by_keyword = True

                # Test if it is geolocated
                is_geolocated = self.test_if_is_geolocated(tweet)

                if is_geolocated:
                    geolocated_tweets += 1

                if collected_by_hashtag == True:
                    tweets_using_hashtags += 1

                if collected_by_keyword == True:
                    tweets_using_keywords += 1

                if collected_by_hashtag == True and collected_by_keyword == True:
                    tweets_using_hashtags_and_keywords += 1

                if collected_by_hashtag == True or collected_by_keyword == True:
                    tweets_using_terms += 1

                if is_from_profile == True and (collected_by_hashtag == True or collected_by_keyword == True):
                    tweets_from_target_profiles_and_using_terms += 1

                if is_from_profile == True and is_geolocated == True:
                    tweets_from_target_profiles_and_geolocated += 1

                if (collected_by_hashtag == True or collected_by_keyword == True) and is_geolocated == True:
                    tweets_using_terms_and_geolocated += 1

                if is_from_profile == True and (collected_by_hashtag == True or collected_by_keyword == True) and is_geolocated == True:
                    tweets_from_target_profiles_using_terms_and_geolocated += 1


        self.hashtag_stats = sorted(self.hashtag_stats.items(), key=lambda x:x[1])
        self.keywords_stats = sorted(self.keywords_stats.items(), key=lambda x:x[1])

        print "------------------------------------------------"
        print "-Intersections:---------------------------------"
        print "------------------------------------------------"
        print "- Profiles                                      " + str(tweets_from_target_profiles)
        print "- Terms                                         " + str(tweets_using_terms)
        print "    --> Hashtags                                " + str(tweets_using_hashtags)
        print "    --> Keywords                                " + str(tweets_using_keywords)
        print "    --> Hashtags and Keywords                   " + str(tweets_using_hashtags_and_keywords)
        print "- Geolocated                                    " + str(geolocated_tweets)
        print "- Profiles and Terms                            " + str(tweets_from_target_profiles_and_using_terms)
        print "- Profiles and Geolocated                       " + str(tweets_from_target_profiles_and_geolocated)
        print "- Terms and Geolocated                          " + str(tweets_using_terms_and_geolocated)
        print "- Profiles and Terms and Geolocated             " + str(tweets_from_target_profiles_using_terms_and_geolocated)
        print "------------------------------------------------"
        print "-Top 10 Target Profiles-------------------------"
        print "------------------------------------------------"
        for profile, stats in self.get_most_popular_profiles():
            print profile, stats['stats']['tweets'], stats['stats']['mentions'], stats['stats']['retweets']
        print "------------------------------------------------"
        print "-Top 10 Hashtags -------------------------------"
        print "------------------------------------------------"
        for hashtag,amount in self.hashtag_stats[-10:]:
            print hashtag,amount
        print "------------------------------------------------"
        print "-Top 10 Keywords -------------------------------"
        print "------------------------------------------------"
        for keyword,amount in self.keywords_stats[-10:]:
            print keyword,amount
        print "------------------------------------------------"

if ( __name__ == "__main__" ):
    get_parameters()
    S = Stats(args['profiles'])
    S.compute_stats(str(args['input']))

