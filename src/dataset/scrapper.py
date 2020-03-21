import json
import os
import requests
import traceback

from datetime import datetime

SUBREDDITS = ["jokes",
              "darkjokes",
              "dadjokes",
              "cleanjokes",
              "oneliners",
              "badjokes",
              "dirtyjokes",
              "DarkJokeCentral"]

URL = "https://api.pushshift.io/reddit/submission/search?limit=1000&sort=desc&&subreddit={}&before="

START_TIME = datetime.utcnow()

dirname = os.path.dirname(__file__)
subdir = os.path.join(dirname, 'scrapped')
if not os.path.exists(subdir):
    os.makedirs(subdir)


def download_from_url(filename, sub):
    print(f"Saving to {filename}")

    count = 0
    handle = open(filename, 'w')
    previous_epoch = int(START_TIME.timestamp())
    jokes = []
    while True:
        new_url = URL.format(sub) + str(previous_epoch)
        json_rq = requests.get(new_url, headers={'User-Agent': "Post downloader by /u/Watchful1 and waguramu@github"})
        json_data = json_rq.json()
        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break

        for object in objects:
            previous_epoch = object['created_utc'] - 1
            count += 1

            if object['is_self']:
                # if 'selftext' not in object:
                #     continue
                try:
                    jokes.append({"created": datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"),
                                  "score": str(object['score']),
                                  "title": object['title'],
                                  "body": object['selftext'] if 'selftext' in object else ""})
                except Exception as err:
                    print(f"Couldn't print post: {object['url']}")
                    print(traceback.format_exc())

        print(f"Saved {count} submissions through {datetime.fromtimestamp(previous_epoch).strftime('%Y-%m-%d')}")
    json.dump(jokes, handle, indent=1)
    print(f"Saved {count} submissions")
    handle.close()


for subreddit in SUBREDDITS:
    download_from_url(os.path.join(subdir, f"posts_{subreddit}.json"), subreddit)
