import json
import os
import re
import html

from typing import Dict, List, Optional

SUBREDDITS = ["jokes",
              "darkjokes",
              "dadjokes",
              "cleanjokes",
              "oneliners",
              "badjokes",
              "dirtyjokes",
              "DarkJokeCentral",
              "reddit_jokes"]

# Sanity check for the jokes length
THRESHOLD_LOW = 20
THRESHOLD_HIGH = 1000

# Target number of characters for class size labels
SHORT_MAX = 200
MEDIUM_MAX = 400
LONG_MAX = 800

# Filter tokens for offensive language
FILTERS = [('pedo',),
           ('dead bab',),
           (' rape', ' rapist', 'raping'),
           ('killer',),
           ('zoophil', 'necrophil'),
           ('nazi', 'hitler')]


dirname = os.path.dirname(__file__)
subdir = os.path.join(dirname, 'data')
if not os.path.exists(subdir):
    os.makedirs(subdir)

# File handlers
FILTERED = open(os.path.join(subdir, "filtered.txt"), 'a+')
REMOVED = open(os.path.join(subdir,"removed.txt"), 'a+')
TRASH = open(os.path.join(subdir, "trash.txt"), 'a+')


# Tokens for content classes
CLASSES = {
    "chicken": ["chicken"],
    "trump": ["trump"],
    "religion": ["catholic", "jesus", "god", "buddh", "islam",
                 "muslim", "relig"],
    "bar": ["bar", "barmen", "bartender"],
    "queer": ["gay", "lesb", "bisex", "transsex", "homos", "queer", "lgbt"],
    "blind": ["blind"],
    "pet": ["cat", "dog", "pet"],
    "army": ["army", "military"],
    "police": ["cop", "police"],
    "clown" : ["clown", "circus"],
    "german": ["german"],
    "french": ["french"],
    "italian": ["italian"],
    "british": ["engl", "brit", "brexit"],
    "boss": ["boss"],
    "doctor": ["doctor", " dr."],
    "date": ["date", "dating", "girlfriend", "boyfriend"],
    "friend": ["friend"],
    "family" : ["mom", "mum", "momma", "mother", "brother",
                "sister", "father", "grandfather", "grandpa",
                "grandmother", "grandma", "granny", "parent",
                "family"],
    "cookie" : ["cookie", "shortbread", "biscuit"],
}


def unescape(s: str) -> str:
    s = html.unescape(s).replace(u'\u201c', '"').replace(u'\u201d', '"')
    return s


def is_censored(s: str, filters) -> bool:
    s = s.lower()
    for f in filters:
        for sub in f:
            if s.find(sub) != -1:
                return True

    return False


def annotate_length(s: str) -> str:
    length = len(s)
    if length <= SHORT_MAX:
        return f"<|short|> {s}"
    elif length <= MEDIUM_MAX:
        return f"<|medium|> {s}"
    elif length <= LONG_MAX:
         return f"<|long|> {s}"
    else:
        return f"<|story|> {s}"


def is_removed(s: str) -> bool:
    s = s.lower()
    if s.find('deleted') != -1 or s.find('removed') != -1:
        return True
    return False


def sanitise(s: str) -> str:
    s = re.sub('[^-A-Za-z0-9.,;?!\'\"]+', ' ', s)
    s = ' '.join(s.split())
    s = re.sub(r'([-.,;?!"])\1+', r'\1', s)
    s = s.split("x200B;")
    s = ''.join(s)
    return s


def class_frequency_picker(s: str, classes: Dict[str, List]) -> Optional[str]:
    class_frequencies = {}
    for class_key, tokens in classes.items():
        class_frequencies.update({class_key: sum([s.count(x) for x in tokens])})
    if sum(list(class_frequencies.values())) > 0:
        class_key = max(class_frequencies, key=class_frequencies.get)
        return class_key
    else:
        return None


def determine_type(s: str, sub: str) -> str:
    _s = s.lower()
    _sl = re.sub('[^A-Za-z0-9]+', ' ', _s).split(' ')

    if "yo momma" in _s or \
            "yo mama" in _s or \
            "yo momma" in _s:
        return f"<|momma|>{s}"

    if "i like my" in _s:
        return f"<|likemy|>{s}"

    if "dadjokes" in sub:
        return f"<|dadjokes|>{s}"

    content_type = class_frequency_picker(_s, CLASSES)
    if content_type is not None:
        return f"<|{content_type}|>{s}"

    return f"<|other|>{s}"


def preprocess_string(s: str, sub: str, remove=True, censor=True) -> str:
    s = sanitise(s)

    if remove and is_removed(s):
        REMOVED.write(f"<|REMOVED|> {s}\n")
        return ""
    elif len(s) < THRESHOLD_LOW:
        TRASH.write(f"<|TRASH|> {s}\n")
        return ""
    elif len(s) > THRESHOLD_HIGH:
        TRASH.write(f"<|TRASH|> {s}\n")
        return ""
    elif censor and is_censored(s, FILTERS):
        FILTERED.write(f"<|FILTERED|> {s}\n")
        return ""
    else:
        s = determine_type(s, sub)
        s = annotate_length(s)
        if s is None:
            return ""
        s = f"{s}<|endoftext|>\n"
        return s


with open(os.path.join(subdir, 'dataset_clean.txt'), 'a+') as dataset:
    for subreddit in SUBREDDITS:
        with open(f'scrapped/posts_{subreddit}.json') as json_file:
            data = json.load(json_file)
            for d in data:
                if int(d['score']) > 1:
                    title = unescape(d['title'])
                    body = unescape(d['body'])

                    if len(body) + len(title) > 0:
                        joke = ''
                        if body.lower().startswith(title.lower()):
                            joke = body
                        else:
                            joke = f"{title}{'' if title.endswith(('!', '?', ';', '-', ',', '.')) else '.'} {body}"

                        joke = preprocess_string(joke, sub=subreddit, remove=True, censor=True)

                        if joke != "":
                            s = sanitise(body).lower().replace(' ', '')
                            if s != 'deleted' and s != 'removed':
                                if joke.lower().find('kinkink') == -1 \
                                        and joke.lower().find('hhhhhhh') == -1 \
                                        and joke.lower().find('imgur') == -1 \
                                        and joke.lower().find('reddit') == -1 \
                                        and joke.lower().find('edit') == -1 \
                                        and joke.lower().find('http') == -1:
                                    dataset.write(joke)
                            else:
                                REMOVED.write(f"<|REMOVED|> {joke}\n")

    with open('wocka.json') as json_file:
        data = json.load(json_file)
        for d in data:
            body = unescape(d['body'])
            if len(body) > 0:  # and len(d['body']) < 350 and
                joke = preprocess_string(body, sub=subreddit, remove=True, censor=True)
                if joke != "":
                    dataset.write(joke)

    with open('stupidstuff.json') as json_file:
        data = json.load(json_file)
        for d in data:
            body = unescape(d['body'])
            if len(body) > 0:  # and len(d['body']) < 350 and
                joke = preprocess_string(body, sub=subreddit, remove=True, censor=True)
                if joke != "":
                    dataset.write(joke)

FILTERED.close()
REMOVED.close()
TRASH.close()
print("Done!")
