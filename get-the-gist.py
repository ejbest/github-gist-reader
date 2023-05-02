import requests
import datetime
import sys

def get_gists_since_time(user, time, headers):
    url = f"https://api.github.com/users/{user}/gists"
    if time:
        url += f"?since={time}"
    response = requests.request("GET", url, headers=headers)
    return response.json()

def display_gist(gist):
    
    response = requests.request("GET", gist['url'], headers=headers)
    response = response.json()['files']
    content = response[list(response.keys())[0]]['content']
    
    response = requests.request("GET",gist['comments_url'])
    response = (response.json())

    print(f"Gist ID: {gist['id']}")
    print(f"Description: {gist['description']}")
    print(f"Content: {content}")
    for i in response:
        print(f"Comments : {i['body'].strip()}")
    
    print(f"URL: {gist['html_url']}")
    print(f"Created at: {gist['created_at']}\n")

def display_gists(gists):
    if not gists:
        print("No new gists found since last run.")
    else:
        print(f"Found {len(gists)} new gist{'s' if len(gists) > 1 else ''} since last run:\n")
        
        for gist in gists:
            display_gist(gist)


filename = open("user_details.txt","r")

filename = filename.read().split("\n")

user = filename[0]
Authorization_key = filename[1]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": Authorization_key,
}

n = len(sys.argv)
fresh_start = None
if n >=2 :
	fresh_start = sys.argv[1] 

if fresh_start:
    with open("time.txt", "w") as f:
        f.write("")
    time = None
else:
    with open("time.txt", "r") as f:
        time = f.readline().strip()

if not time:
    print(f"Displaying all public gists for user {user}:\n")
    url = f"https://api.github.com/users/{user}/gists"
    response = requests.request("GET", url, headers=headers)
    gists = response.json()
    for gist in gists:
        display_gist(gist)
    time = datetime.datetime.utcnow().isoformat()

else:
    print(f"Checking for new gists since {time} for user {user}:\n")
    gists = get_gists_since_time(user, time, headers)
    display_gists(gists)
    time = datetime.datetime.utcnow().isoformat()

with open("time.txt", "w") as f:
    f.write(time)
