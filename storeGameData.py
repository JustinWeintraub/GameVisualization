import os
import requests
import json
import time
from dotenv import load_dotenv

# goal of file is to get game data, specifically the companies that created them
# as the companies have data of country of origin

load_dotenv()

pattern = '%d.%m.%Y %H:%M:%S'

for i in range(1, 10):
    # gets start and end times of every year
    original = '01.01.'+str(2020-i) + ' 00:00:00'
    end = '01.01.'+str(2020-i+1) + ' 00:00:00'
    original = int(time.mktime(time.strptime(original, pattern)))
    end = int(time.mktime(time.strptime(end, pattern)))

    # finds companies of top 500 games released in a year, calling api
    raw_data = "fields involved_companies; where involved_companies >=1 & first_release_date > " + \
        str(original) + " & first_release_date < " + str(end) + \
        "; limit 500; sort popularity desc;"
    response = requests.post(
        "https://api-v3.igdb.com/games/",
        headers={"user-key": os.environ.get('USERKEY')}, data=raw_data)

    # stores gameData to be used in storeCompanyData
    with open(('./gameData/games/games'+str(2020-i)+'.json'), 'w') as f:
        json.dump(response.json(), f)
