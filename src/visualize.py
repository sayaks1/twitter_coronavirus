#!/usr/bin/env python3

# command line args
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output', default='bar_graph.png')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path, 'r', encoding='utf-8') as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

top10_desc = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=True)[:10]
top10 = sorted(top10_desc, key=lambda item: item[1])
keys = [k for k, v in top10]
values = [v for k, v in top10]

plt.rcParams['font.family'] = 'UnDotum'  

plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='navy')
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title(f'Top 10 Keys for hashtag: {args.key} (Sorted Low to High)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig(args.output)
plt.close()

print(f"Bar graph saved as {args.output}")


# print the count values
# items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
# for k,v in items:
 #   print(k,':',v)
