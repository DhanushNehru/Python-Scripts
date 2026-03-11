import requests

url = input("ENTER REPO URL:- ")

# convert normal github url -> api url
parts = url.strip().split("/")
owner = parts[-2]
repo = parts[-1].replace(".git","")

api_url = f"https://api.github.com/repos/{owner}/{repo}"

response = requests.get(api_url)

if response.status_code != 200:
    print("Repository not found")
    exit()

data = response.json()

print("\nRepository Information\n")

print(f"Name: {data['name']}")
print(f"Owner: {data['owner']['login']}")
print(f"Description: {data['description']}")
print(f"Language: {data['language']}")
print(f"Stars: {data['stargazers_count']}")
print(f"Forks: {data['forks_count']}")
print(f"Open Issues: {data['open_issues_count']}")
print(f"Visibility: {data['visibility']}")
print(f"Size: {data['size']} KB")
print(f"Created At: {data['created_at']}")
print(f"Clone URL: {data['clone_url']}")

# contributors info-------
contributors = requests.get(f"{api_url}/contributors").json()
print(f"\nTotal Contributors: {len(contributors)}")

# Languages used----------
lang_data = requests.get(f"{api_url}/languages").json()

total = sum(lang_data.values())

print("\nLanguages Used:")

for lang in lang_data:
    percent = (lang_data[lang] / total) * 100
    print(f"{lang} : {percent:.2f}%")
