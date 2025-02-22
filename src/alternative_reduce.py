import argparse
import json
from collections import defaultdict 
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', nargs='+')
parser.add_argument('--output', default='reduced_line_plot.png')
args = parser.parse_args()

hashtag_counter = defaultdict(lambda: defaultdict(int)) 
output_dir = "outputs"
output_files = os.listdir(output_dir)

for filename in output_files:
    filepath = os.path.join(output_dir, filename)
    if filename.endswith('.country'):
        date_part = filename.split("_")[1].split(".")[0]
        month_date = "-".join(date_part.split("-")[1:])
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for hashtag, country_counts in data.items():
                if hashtag in args.inputs:
                    if isinstance(country_counts, dict):
                        for country, count in country_counts.items():
                            hashtag_counter[hashtag][month_date] += count
                    else:
                        print(f" Warning: Unexpected format in {filename} for hashtag '{hashtag}'")

year = 2020
keys = [datetime.date(year, 1, 1) + datetime.timedelta(days=i) for i in range(365)]
date_strs = {d.strftime("%m-%d"): d for d in keys}

plt.rcParams['font.family'] = 'UnDotum' 

fig, ax = plt.subplots(figsize=(12, 6))
for hashtag, date_values in hashtag_counter.items():
    values = [date_values.get(d, 0) for d in date_strs]  # Get values, default 0
    ax.plot(keys, values, marker='o', linestyle='-', label=hashtag)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # 'Jan', 'Feb', etc.
ax.xaxis.set_major_locator(mdates.MonthLocator())  # Major ticks at months
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))  # Minor ticks weekly

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Labels and title
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Hashtag Trends Over the Year")
plt.grid(True)

# Add legend for hashtags
plt.legend(title="Hashtags")
plt.savefig(args.output)
plt.close()

print(f"Line plot written to {args.output}")

