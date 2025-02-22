import argparse
import json
from collections import defaultdict 
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', required=True)
parser.add_argument('--output', default='map_output.json')
args = parser.parse_args()

lang_counter = defaultdict(lambda: defaultdict(int))
country_counter = defaultdict(lambda: defaultdict(int))

hashtags = set()
with open("../hashtags", 'r') as f:
    for line in f:
        hashtags.add(line.strip().lower().lstrip('#'))

iteration = 0
with zipfile.ZipFile(args.filepath, 'r') as zip_ref:
    for name in zip_ref.namelist():
        with zip_ref.open(name, 'r') as file:
            for i, line in enumerate(file):
                line = line.decode('utf-8').strip()
                datum = json.loads(line)
                place = datum.get('place')
                if place:
                    country = place.get('country_code', 'unknown')
                lang = datum.get('lang', 'unknown')
                hashtags_in_tweet = {
                        tag['text'].lower() for tag in datum['entities']['hashtags']
                }
                matched_hashtags = hashtags_in_tweet.intersection(hashtags)
                if matched_hashtags:
                        print(f"✅ Matched Hashtags: {matched_hashtags} | Lang: {lang}")

                for hashtag in matched_hashtags:
                    lang_counter[hashtag][lang] += 1
                    country_counter[hashtag][country] += 1
            
        print(f"🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎 iteration = {iteration}, file = {name}")
        iteration += 1

with open(f"{args.output}.lang", 'w', encoding='utf-8') as fout:
    fout.write(json.dumps(lang_counter))
with open(f"{args.output}.country", 'w', encoding='utf-8') as fout:
    fout.write(json.dumps(country_counter))
