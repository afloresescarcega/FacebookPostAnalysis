import json
from facepy import GraphAPI
from facepy import utils
from datetime import date, datetime

def getInfo():
    secret = open("secret.txt", 'r')
    return [line.strip() for line in secret]



# get app ID and app secret
idAndSecret = getInfo(); # tuple (ID, secret)
print idAndSecret

# get access token (token, expiration)
accessTokenInfo = utils.get_application_access_token(idAndSecret[0],idAndSecret[1])
graph = GraphAPI(accessTokenInfo[0]) # create graph object to GET, post or search

# skim the feed and see if there is a user post in a group
"""
Skims the front-page of the recent activity section of the feed
to see if there is a new post by given user.

Parameters:
        user, a str for the ID of the user to search for
        group, a str for the ID of the group to be searching for
Returns: 
        The permalink of the posts from user in group
"""
def fetchLatestFeed(user, group):
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
# retrieve previously collected data
with open('posts.json') as json_data:
        posts = json.load(json_data)

feedData = fetchLatestFeed(user, group)

# add post under userId if new
    # new posts should have the creation time as the first time stamp
    # with 0 reactions and 0 comments
# else update the values with the current time stamp
for post in feedData:
    # check to see if user is in posts
    userId = post['from'] ['id']
    if userId not in posts: 
        print "This person,", userId, "is not in the DB" 
        # create a new user ID and a new post dictionary with dictionary time created time stamp with values zero reactions and zero comments
        posts[userId] =  {post['id'] : {post["created_time"] : [0,0]}}
        # add current timestamp and info on number of reactions and comments
        posts = updateReactionsAndComments(posts, post)
    elif post['id'] not in posts[userId]: # user exists but a post is new
        posts[userId]  [post['id']] = {post['created_time'] : [0,0]}
        posts = updateReactionsAndComments(posts, post)
    else: # user exits and so does post, so update info on it
        posts = updateReactionsAndComments(posts, post)


# save collected data to 'posts.json'
with open('posts.json', 'w') as outfile:
        json.dump(posts, outfile)
