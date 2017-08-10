#!/usr/bin/env python

import json
from facepy import GraphAPI
from facepy import utils
from datetime import date, datetime
import os.path

# file name constants
SECRET_FILE = "secret.txt"
POSTS_FILE = "posts.json"

def getInfo():
    """
    Retrieves app id and app secret from a file in the same directory as this script.
    First line must be app ID. The Facebook graph app must have user_managed_groups.
    Second line must be the app secret.
    
    Returns list with the app id and app secret in the order read in file
    """
    secret = open("secret.txt", 'r')
    return [line.strip() for line in secret]



# get app ID and app secret
idAndSecret = getInfo(); # tuple (ID, secret)

# get access token (token, expiration)
accessTokenInfo = utils.get_application_access_token(idAndSecret[0],idAndSecret[1])
graph = GraphAPI(accessTokenInfo[0]) # create graph object to GET, post or search

# skim the feed and see if there is a user post in a group
def fetchLatestFeed(user, group):
    """
    Skims the front-page of the recent activity section of the feed
    to see if there is a new post by given user.

    Parameters:
            user, a str for the ID of the user to search for
            group, a str for the ID of the group to be searching for
    Returns: 
            The permalink of the posts from user in group
    """
    fields = "/feed?fields=id,from,created_time,likes.limit(0).summary(true),comments.limit(0).summary(true),reactions.limit(0).summary(true)"
    return (graph.get(group + fields)['data'])

def updateReactionsAndComments(postsDict, indivPost):
    # add current timestamp and info on number of
    # reactions and comments
    numComments = indivPost['comments']  ['summary'] ['total_count'] 
    numReacts = indivPost["reactions"]  ['summary'] ['total_count'] 
    postsDict[indivPost['from']['id']]  [indivPost['id']]  [datetime.now().isoformat('-')] = [numReacts, numComments]
    return postsDict

group = '1218486471522469'
user = 'not yet implemented'


"""
-- Structure for posts dict --
"User id": {
    "posts":{
        "time stamp" : [amountOfReactions, amountOfComments]
        }
    }
"""

# check to see if file that stores posts exists in current directory as this script
if os.path.isfile(POSTS_FILE):
    # retrieve previously collected data
    with open(POSTS_FILE) as json_data:
            posts = json.load(json_data)
else:
    posts = {}

feedData = fetchLatestFeed(user, group)

# add post under userId if new
    # new posts should have the creation time as the first time stamp
    # with 0 reactions and 0 comments
# else update the values with the current time stamp
for post in feedData:
    # check to see if user is in posts
    userId = post['from'] ['id']
    if userId not in posts: 
        print("This person, https://www.facebook.com/" + userId, "is not in the DB")
        # create a new user ID and a new post dictionary with dictionary time created time stamp with values zero reactions and zero comments
        posts[userId] =  {post['id'] : {post["created_time"] : [0,0]}}
        # add current timestamp and info on number of reactions and comments
        posts = updateReactionsAndComments(posts, post)
    elif post['id'] not in posts[userId]: # user exists but a post is new
        posts[userId]  [post['id']] = {post['created_time'] : [0,0]}
        posts = updateReactionsAndComments(posts, post)
    else: # user exits and so does post, so update info on it
        posts = updateReactionsAndComments(posts, post)


# save collected data to 'posts.json' by overwriting it 
with open(POSTS_FILE, 'w') as outfile: 
        json.dump(posts, outfile)
