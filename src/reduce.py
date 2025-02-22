import argparse
import json
from collections import defaultdict 

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', nargs='+')
parser.add_argument('--output_lang', default='reduced_output.lang.json')
parser.add_argument('--output_country', default='reduced_output.country.json')
args = parser.parse_args()

lang_counter = defaultdict(lambda: defaultdict(int)) 
country_counter = defaultdict(lambda: defaultdict(int))

for filename in args.inputs:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if filename.endswith('.lang'):
            for hashtag, lang_counts in data.items():
                if isinstance(lang_counts, dict):
                    for lang, count in lang_counts.items():
                        lang_counter[hashtag][lang] += count
                else:
                    print(f" Warning: Unexpected format in {filename} for hashtag '{hashtag}'")
                    print(f"   Expected dictionary but found: {lang_counts} (type: {type(lang_counts)})")

        elif filename.endswith('.country'):
            for hashtag, country_counts in data.items():
                if isinstance(country_counts, dict):
                    for country, count in country_counts.items():
                        country_counter[hashtag][country] += count
                else:
                    print(f" Warning: Unexpected format in {filename} for hashtag '{hashtag}'")
                    print(f"   Expected dictionary but found: {country_counts} (type: {type(country_counts)})")
with open(args.output_lang, 'w') as f:
    json.dump(lang_counter, f, indent=2)
with open(args.output_country, 'w') as f:
    json.dump(country_counter, f, indent=2)

print(f"Reduced counts written to {args.output_lang} and {args.output_country}")
