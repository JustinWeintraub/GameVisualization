import json

# goal of file is to turn company data into usable country data, showing each time a country is used


# finds dictionary in list of dictionaries of country data
# where the country's ccn3 code is
def convertCountry(data, ccn3):
    if(ccn3 < 100):
        ccn3 = "0" + str(ccn3)
    for dict in data:
        if(str(dict['ccn3']) == str(ccn3)):
            return dict['cca3']


# opens key file, a list of every country's data
keyData = []
with open('./gameData/countries/key.json') as f:
    keyData = json.load(f)


# opens every year's companyData and store specific values in an array
companyData = []
for i in range(1, 10):
    year = str(2020-i)
    with open('./gameData/companies/company' + year + '.json') as f:
        data = json.load(f)
        for dictionary in data:
            for line in dictionary['result']:
                # push (convert(line['country]), year)
                companyData.append({'country': convertCountry(
                    keyData, line['country']), 'year': year})

# store result to be used in getPercents
with open('./gameData/countries/countries.json', 'w') as f:
    json.dump(companyData, f)
