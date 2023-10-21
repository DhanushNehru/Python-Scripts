import tweepy
import time 

apic= ""# add api_code 
apisc="" # add api_secret_code

acc= ""#add account_code
acsc= ""# add acount_secret_code             

cnt=open(r"bot.txt","r+")
counts=cnt.read()
count=int(counts)
auth = tweepy.OAuthHandler(apic,apisc)
auth.set_access_token(acc,acsc)
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
user=api.me()
print(user.screen_name)
search=input("Enter the keyword to be searched") # akss for the keyword here 
nrtweets=500
count=0
for tweet in tweepy.Cursor(api.search,search).items(nrtweets):
    try:
        print("tweet-number",count,"retweeted")
        count=count+1
        tweet.retweet()
        time.sleep(30)
        ctr=str(count)
        cnt.truncate() 
        cnt.write(ctr)
        print("RETWEETED:",count)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
ctr=str(count)
cnt.truncate() 
cnt.write(ctr)