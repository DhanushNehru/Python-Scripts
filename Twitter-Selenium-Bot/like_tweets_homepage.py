import os
from twitter_bot_class import TwitterBot

# writing this sample comment on my github codespace beta access

if __name__ == "__main__":
    try:
        pj = TwitterBot(os.environ['EMAIL'], os.environ['PASSWORD'])
        pj.login()
        pj.like_tweets(10)
        pj.logout()
    except Exception as e:
        pj.logout()
        print(e)

