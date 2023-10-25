import instaloader
from instaloader import Post
import requests
import sys

#Banner
print(''' 

------------------ Instagram Images and Post Downloader ------------------
                            [Coded By Muneeb]

''')

# #Function to check the internet connection
# #Got this from https://stackoverflow.com/a/24460981
def connection(url='http://www.google.com/', timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        print("You're connected to internet\n")
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def download_insta_post(loader, target_username, post_code):
    profile = instaloader.Profile.from_username(loader.context, target_username)
    post = Post.from_shortcode(loader.context, post_code)
    loader.download_post(post, target=target_username)

if connection() == True:
    # Create an instance of Instaloader
    L = instaloader.Instaloader()
    try:
        while True:
            a = "Press 'A' to download an instagram post from a private profile.\nPress 'B' to download an instagram post from a public profile.\nPress 'Q' to exit."
            print(a)
            select = str(input("\nInstaSave > ")).upper()
            try:
                if select == 'A':
                    username = input("Enter your IG username: ")
                    password = input("Enter your IG password: ")
                    L.login(username, password)
                    t_username = input("Enter the target insta username: ")
                    post_code = input("Enter the post code for the media (Please don't enter the URL - only code) : ")
                    download_insta_post(L, t_username, post_code)
                    print("Post downloaded successfully")
                if select == 'B':
                    t_username = input("Enter the target insta username: ") #sample input: quote_nietzsche
                    post_code = input("Enter the post code for the media (Please don't enter the URL - only code) : ") #sample input: Cyv0uoAOewp
                    download_insta_post(L, t_username, post_code)
                    print("Post downloaded successfully")
                if select == 'Q':
                    sys.exit()
                else:
                    sys.exit()
            except (KeyboardInterrupt):
                 print("Programme Interrupted")
    except(KeyboardInterrupt):
        print("\nProgramme Interrupted")
else:
    sys.exit()