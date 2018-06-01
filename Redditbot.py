import requests
import json
import configparser
import praw

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('')

for submission in subreddit.new(limit=2):
    url = submission.url
    score = submission.score

    if 'facebook' in url and 'video' in url and score > 20:
        config = configparser.ConfigParser()
        config.read("config.ini")
        email = config.get('streamable_info', 'email')
        password = config.get('streamable_info', 'password')

        try:
            response = requests.get('https://api.streamable.com/import?url='+url, auth=(email, password)).json()
            link = 'https://streamable.com/' + str(response['shortcode'])
            cat_link = 'http://thecatapi.com/api/images/get?format=src&type=gif'
            
            submission.reply('''Streamable Mirror: [Link](%s)  \n*******  \n Hi, I am a bot. I take Facebook video links and return Streamable Mirrors, why? cause Facebook sucks  \nFeel free to pm me about any errors, my master check occasionally. I think ಠ_ಠ  \nPsst, here is a [random cat gif](%s), why? cause cats don't suck unlike Faceboo. ''' % (link, cat_link))
        except requests.exceptions.RequestException:
            pass
    else:
        pass
