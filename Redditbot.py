import spaw
import json
import configparser
import praw

# Initializes a praw instance.
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('all')

# config.ini is a file with the streamable account info.
# .gitignore is used to remove it from the repo for security purposes.
config = configparser.ConfigParser()
config.read("config.ini")
email = config.get('streamable_info', 'email')
password = config.get('streamable_info', 'password')

# Initializes a SPAW instance, and does authorization. 
spaw = spaw.SPAW()
spaw.auth(email, password)

# Only check the top 5 posts in the 'rising' sorting.
for submission in subreddit.rising(limit=5):
    # Gets the url for the submission.
    url = submission.url

    # Checks if the submission is a video from facebook.
    if 'facebook' in url and 'video' in url:
        # If the url is indeed a video from facebook, imports it to streamable using SPAW. Then retrieves the json response.
        response = spaw.videoImport(url)

        # First check if the importing proceeded successfully.
        if (response['status']) != '200':
            # Generates a url link, using the streamable shortcode from the response json.
            link = 'https://streamable.com/' + str(response['shortcode'])

            # Random cat gif from fun :3
            cat_link = 'http://thecatapi.com/api/images/get?format=src&type=gif'
            
            # Posts a comment with the mirror link.
            submission.reply('''Streamable Mirror: [Link](%s)  \n*******  \n Hi, I am a bot. I take Facebook video links and return Streamable Mirrors, why? cause Facebook sucks  \nFeel free to pm me about any errors, my master check occasionally.  \nPsst, here is a [random cat gif](%s), why? cause cats don't suck unlike Facebook. ''' % (link, cat_link))
        else:
            # If the importing fails for some reason, ignore the post.
            pass
    else:
        # If the video is not from facebook, ignore the post.
        pass