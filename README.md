# GameVisualization

Link to project: https://map-weintraub.herokuapp.com/map

This is a visualization based project for displaying data of percentage of 500 popular games coming from each country 
between the years 2011 and 2019. The visualization map includes hovering to read the data on each country and a slider
to choose the year. 

The data I got came from multiple push requests to the API of video games called IGBD. 
I had to get the 500 most popular games every year then find the companies that created them, as the companies had
data on country of origin. I then had to perform some data cleanup to turn country codes into percentages of a country being used. 
Some external services I used were Natural Earth for the geometry of the map
and Mldezoe's country dataset for converting ISO 3166 codes to country names.

Project's path to follow, with detailed comments in every file:
1. storeGameData.py
2. storeCompanyData.py
3. cleanCompanies.py
4. getPercents.py
5. map.py
