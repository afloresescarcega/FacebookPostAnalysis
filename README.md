# FacebookPostAnalysis

A simple app that records information about the [UT LONGmemes for HORNSy teens](https://www.facebook.com/groups/1218486471522469) posters by scraping from the feed.

## Requirements
* Need a 'secret.txt' with app id in first line and app secret in second line. 
* Graph app needs access to [user_managed_groups](https://developers.facebook.com/docs/graph-api/reference/group/). Make sure your app has this permission. As of v2.10 of Graph API, will need app review.
* An empty 'posts.json' to store the post id, user and time information. Auto-generating an empty 'posts.json' is on the TODO list

## What does it do?
* Simply records who posted what at what time. That's it. ¯\\_(ツ)_/¯ 
* Print to console the url of a profile that is new to the json file, aka "the database". 
* Auto-generate post.json if inexistent. 


## TO-DO
* Retroactively and from then on, include the name of a user and a url to their profile picture for later retrival.
* Prune data when it gets really old to save on space and time reading and writing database
