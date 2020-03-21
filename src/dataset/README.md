# Jokes Dataset Collector for Humorous Data 

This repository uses [pushshift.io](https://pushshift.io/) to collect data. Learn more about [the pushshift project](https://arxiv.org/abs/2001.08435)!  

This dataset contains 665 781 jokes from Reddit, wocka and stupidstuff. You can download it [here]().

## Collecting data
Install the necessary dependencies via pip:
 
```bash

pip install -r requirements.txt

```
To collect Reddit data, run the scrapper script:
```bash

python scrapper.py 

```
You can add our remove subreddits inside of the script.
Currently, it collects posts for the following ones:
```python

SUBREDDITS = ["jokes",
              "darkjokes",
              "dadjokes",
              "cleanjokes",
              "oneliners",
              "badjokes",
              "dirtyjokes",
              "DarkJokeCentral"]

```
## Assembling the dataset
To collate data into a dataset, run the collate script:
```bash

python collate.py

```
You can: 
* add or remove subreddits; 
* filter the jokes by offensive words;
* choose the length of the target size classes;
* choose tokens for the target content classes. 

We make no claim on ownership of these files and do not endorse any of the jokes. All data is provided as is for research purposes.

The following information and data were derived from the repository:

* [joke-dataset by taivop](https://github.com/taivop/joke-dataset)

## Files
Currently the dataset contains jokes from three sources, each in a different file.

```
----------------------------------------------------
posts_reddit_jokes.json |  195K jokes | 7.40M tokens
stupidstuff.json        | 3.77K jokes |  396K tokens
wocka.json              | 10.0K jokes | 1.11M tokens
----------------------------------------------------
TOTAL                   |  208K jokes | 8.91M tokens
----------------------------------------------------
```

## Format
Each file is a JSON document, containing a flat list of joke objects. Each joke object always has the `body` field with additional fields varying based on the dataset, described below.

Obviously they are not all funny; to find the best ones, sort on the relevant additional fields.

Note that the title is in part of the joke many cases.

### stupidstuff.json
Scraped from [stupidstuff.org](stupidstuff.org/jokes/).

Additional fields:

* `id` -- page ID on stupidstuff.org.
* `category` -- see available categories [here](http://stupidstuff.org/jokes/category.htm).
* `rating` -- mean user rating on a scale of 1 to 5.

```json
{
        "category": "Blonde Jokes",
        "body": "A blonde is walking down the street with her blouse open, exposing one of her breasts. A nearby policeman approaches her and remarks, \"Ma'am, are you aware that I could cite you for indecent exposure?\" \"Why, officer?\" asks the blonde. \"Because your blouse is open and your breast is exposed.\" \"Oh my goodness,\" exclaims the blonde, \"I must have left my baby on the bus!\"",
        "id": 14,
        "rating": 3.5
    }
```


### wocka.json
Scraped from [wocka.com](http://wocka.com/).

Additional fields:

* `id` -- page ID on wocka.com.
* `category` -- see available categories [here](http://www.wocka.com/).
* `title` -- title of the joke.

```json
{
        "title": "Infants vs Adults",
        "body": "Do infants enjoy infancy as much as adults enjoy adultery?",
        "category": "One Liners",
        "id": 17
    }
```

