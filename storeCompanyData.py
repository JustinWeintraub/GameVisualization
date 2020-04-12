import requests
import json
import time
import random
import os
from dotenv import load_dotenv

# goal of file is to find companies and their country of origin from the game data

load_dotenv()

for i in range(2, 10):
    # loads data in games{Year} files
    gameIds = []
    with open('./gameData/games/games'+str(2020-i)+'.json') as f:
        data = json.load(f)
        for line in data:
            gameIds.append(line['id'])

    # randomizes each year and splits them into 10 different parts
    # done so companies can be accounted for multiple times
    # and a multiquery can only consist of 10 requests
    random.shuffle(gameIds)
    rawData = ""
    for j in range(0, 10):
        # stringIds contains 50 games out of 500
        stringIds = str(gameIds[j*50:(j+1)*50])
        stringIds = "(" + stringIds[1:len(stringIds)-1] + ")"

        # multi query to get company countries
        rawData += '''
        query companies "''' + str(j) + '''" {
            fields name, country;
            where published = ''' + \
            str(stringIds) + '''
            & country >= 0; 
            limit 500; 
            sort popularity desc;
        };
        '''

    # requesting combined data
    response = requests.post(
        "https://api-v3.igdb.com/multiquery",
        headers={"user-key": os.environ.get('USERKEY')},
        data=str(rawData)
    )
    # stores data into one company file for every year
    # to be used in cleanCompanies
    with open('./gameData/companies/company'+str(2020-i)+'.json', 'w') as f:
        json.dump(response.json(), f)
