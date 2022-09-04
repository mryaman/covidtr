# Suleyman Yaman
# TODO: Obtain population data from wikidata, maybe? 
# https://query.wikidata.org 

import requests
from bs4 import BeautifulSoup

# covid data
page = requests.get('https://covid19.saglik.gov.tr/')
soup = BeautifulSoup(page.text, 'xml')

table = soup.find('table', attrs = {'table table-striped'})
data = table.find_all('td')

data = [float(item.text.replace(',','.')) if index % 2  
        else item.text.strip() for index, item in enumerate(data)]

covid_data = dict(zip(*[iter(data)]*2)) # list to dict

# population
pop_page = requests.get('https://www.nufusu.com/')
soup = BeautifulSoup(pop_page.text, 'html.parser')
pop_table = soup.find('table', attrs = {'pure-table pure-table-bordered pure-table-striped'}) 

population = pop_table.find_all('strong')
population = [int(item.text.replace('.','')) for item in population]
city_names = pop_table.find_all('a')
city_names = [item['title'].replace(' Nüfusu', '') for item in city_names]

pop_data = dict(zip(city_names, population))
# covid_data has Afyon, not Afyonkarahisar
pop_data['Afyon'] = pop_data.pop('Afyonkarahisar')

# Weekly total case
weekly_cases = {key: value*pop_data[key]/100000 for key, value in covid_data.items()}
# Daily total case 
daily_cases = {key:  round(value/7, 3) for key, value in weekly_cases.items()}

print(daily_cases)

df_daily= pd.DataFrame([daily_cases])
df_daily = df_daily.T
df_daily = df_daily.astype(int)
df_daily.to_html()


df_weekly = pd.DataFrame([weekly_cases])
df_weekly = df_weekly.T
df_weekly = df_weekly.astype(int)
df_weekly.to_html()

