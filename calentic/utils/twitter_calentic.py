from twitter import *
twitter = Twitter(auth=OAuth(
    "2354919097-bHmOkx36S9FK5Ozz3EQUTTtbmDOQ3evKvT9O2AN",
    "iWZAs2HpUPJQ9NbJzmbn5tAI4kJlpzvSlO73XmqHEKHOU",
    "NCQhM2FR5xr9AQtEttlj2w",
    "EPrEhdzCCjhfjOM9UGg7yHfPVKeW7XkzPQeOqDAE",
))
def publish_twitter(event, event_url):
    twitter.statuses.update(status='%s: %s' %(event, event_url))
