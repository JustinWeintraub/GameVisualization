import json
from collections import defaultdict
from itertools import chain

# goal of file is to turn the counts gotten by cleanCompanies of each country
# into percent of times found in a year
countryData = []
with open('./gameData/countries/countries.json') as f:
    countryData = json.load(f)

# get count of repeat instances of year/country and store all instances in list
c = defaultdict(int)
for d in countryData:
    c[frozenset(d.items())] += 1
counterList = [dict(chain(k, (('count', count),))) for k, count in c.items()]

# get the total amount of country data every year
years = {}
for dictionary in counterList:
    year = dictionary['year']
    count = dictionary['count']
    try:
        years[year] += count
    except:
        years[year] = count

# convert count to percentages
percentageData = counterList
for dictionary in percentageData:
    dictionary['count'] = float(dictionary['count']) / \
        years[dictionary['year']] * 100

# stores data to be used in map.py
with open('./mapData/countries.json', 'w') as f:
    json.dump(percentageData, f)
