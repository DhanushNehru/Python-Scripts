import os
from twitter_bot_class import TwitterBot

if __name__ == "__main__":
    try:
        pj = TwitterBot(os.environ['EMAIL'], os.environ['PASSWORD'])
        pj.login()
        pj.search('100DaysOfCode')
        pj.like_tweets(10)
        pj.logout()
    except Exception as e:
        pj.logout()
        print(e)
