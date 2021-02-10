import pandas as pd
import requests
from bs4 import BeautifulSoup

import numpy as np


url = 'http://www.fullemployment.net/evi/3.0/SA2_profile_2016.php?SA2_code=124041467'

r = requests.get(url)
html = r.text

soup = BeautifulSoup(html)
table = soup.find('table', {"class": "table_list"})
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

result = pd.DataFrame(data)

from datetime import datetime, timedelta

#generated_dates = pd.date_range(datetime.today(), periods=5).tolist()

generated_dates = pd.date_range(start='10/2/2020', end = datetime.today() - timedelta(days=1)).tolist()

#generated_dates = pd.date_range(start='7/2/2020', end = datetime.today()).tolist()
dates = []
for date in generated_dates:
    new=date.strftime("%d-%B-%Y")
    if new[0] == '0':
        new = new[1:]
    dates.append(new)
    
print(dates)

dates[1]

generated_dates

m = dates[1]
m

url = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + m.strftime("%A-%d-%B")
url

url0 = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + dates0[dates.index(date)]
url = url0[:-5]

url

generated_dates = pd.date_range(start='11/7/2020', end = '11/8/2020').tolist()
dates = []
dates0 = []
for date in generated_dates:
    new=date.strftime("%d-%B-%Y")
    new0=date.strftime("%A-%d-%B-%Y")
    if new[0] == '0':
        new = new[1:]
    dates.append(new)
    dates0.append(new0)

for date in dates:
    n = 'https://www.dhhs.vic.gov.au/media-release-coronavirus-update-victoria-' + dates0[dates.index(date)]
    n = n.replace(n[-16], "", 1)

    print(n)

generated_dates = pd.date_range(start='11/2/2020', end = datetime.today()-timedelta(days=1)).tolist()
#generated_dates = pd.date_range(start='11/7/2020', end = '11/11/2020').tolist()
dates = []
dates0 = []
for date in generated_dates:
    new=date.strftime("%d-%B-%Y")
    new0=date.strftime("%A-%d-%B-%Y")
    if new[0] == '0':
        new = new[1:]
    dates.append(new)
    dates0.append(new0)

confirmed = pd.DataFrame()
active = pd.DataFrame()
first = True

for date in dates:
    print("Starting to retrieve data for " + date)
    try: 
        url = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + date

        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html)
        table = soup.find('table')

        rows = table.find_all('tr')
    except:
        try:
            url = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + str(0) + date 

            r = requests.get(url)
            html = r.text

            soup = BeautifulSoup(html)
            table = soup.find('table')

            rows = table.find_all('tr')
        except:
            try:
                url0 = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + date 
                url = url0[:-5]

                r = requests.get(url)
                html = r.text

                soup = BeautifulSoup(html)
                table = soup.find('table')

                rows = table.find_all('tr')
            except:
                try:
                    url0 = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + str(0) + date 
                    url = url0[:-5]

                    r = requests.get(url)
                    html = r.text

                    soup = BeautifulSoup(html)
                    table = soup.find('table')

                    rows = table.find_all('tr')
                except:
                    try:
                    
                        url = 'https://www.dhhs.vic.gov.au/coronavirus-update-for-victoria-' + dates0[dates.index(date)]
                        
                        r = requests.get(url)
                        html = r.text

                        soup = BeautifulSoup(html)
                        table = soup.find('table')

                        rows = table.find_all('tr')
                    except:
                        try:
                            url0 = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-' + dates0[dates.index(date)]
                            url = url0[:-5]
                            r = requests.get(url)
                            html = r.text

                            soup = BeautifulSoup(html)
                            table = soup.find('table')

                            rows = table.find_all('tr')
                        except:
                            try:
                                url = 'https://www.dhhs.vic.gov.au/coronavirus-update-for-victoria-' + date
                                r = requests.get(url)
                                html = r.text
                                soup = BeautifulSoup(html)
                                table = soup.find('table')
                                rows = table.find_all('tr')
                            except:
                                try:
                                    url0 = 'https://www.dhhs.vic.gov.au/media-release-coronavirus-update-victoria-' + dates0[dates.index(date)]
                                    url = url0.replace(url0[-16], "", 1)
                                    r = requests.get(url)
                                    html = r.text
                                    soup = BeautifulSoup(html)
                                    table = soup.find('table')
                                    rows = table.find_all('tr')
                                except:
                                    try:
                                        url = 'https://www.dhhs.vic.gov.au/media-release-coronavirus-update-victoria-' + date
                                        r = requests.get(url)
                                        html = r.text
                                        soup = BeautifulSoup(html)
                                        table = soup.find('table')
                                        rows = table.find_all('tr')
                                    except:
                                        url0 = 'https://www.dhhs.vic.gov.au/media-release-coronavirus-update-victoria-' + date
                                        url = url0[:-5]
                                        r = requests.get(url)
                                        html = r.text
                                        soup = BeautifulSoup(html)
                                        table = soup.find('table')
                                        rows = table.find_all('tr')
                                    
                        
        
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    result = pd.DataFrame(data)
    
    confirmed_cases = result.drop([2], axis=1).T.head()
    active_cases = result.drop([1], axis=1).T.head()
    
    confirmed_cases.columns = confirmed_cases.iloc[0]
    confirmed_cases.drop(confirmed_cases.index[0], inplace = True)
    confirmed_cases.columns = confirmed_cases.columns.str.upper()
    confirmed_cases.rename(index={1: date}, inplace=True)
    confirmed_cases = confirmed_cases[['HUME', 'MELBOURNE', 'MELTON', 'MORELAND', 'MOONEE VALLEY', 'WYNDHAM', 'MOORABOOL','MACEDON RANGES', 'HOBSONS BAY','YARRA','MARIBYRNONG','DAREBIN','BRIMBANK','TOTAL']]
 #   cols_to_sum = df.columns[ : df.shape[1]-1]

    #confirmed_cases['NWMPHN Total']= confirmed_cases[confirmed_cases.columns[:confirmed_cases.shape[1]-1]].sum(axis=1)
    #confirmed_cases.sort_index(axis=1, inplace = True)
    confirmed = confirmed.append(confirmed_cases)
    

    active_cases.columns = active_cases.iloc[0]
    active_cases.drop(active_cases.index[0], inplace = True)
    active_cases.columns = active_cases.columns.str.upper()
    active_cases.rename(index={2: date}, inplace=True)
    active_cases = active_cases[['HUME', 'MELBOURNE', 'MELTON', 'MORELAND', 'MOONEE VALLEY', 'WYNDHAM', 'MOORABOOL','MACEDON RANGES', 'HOBSONS BAY','YARRA','MARIBYRNONG','DAREBIN','BRIMBANK', 'TOTAL']]
    #active_cases['NWMPHN Total']= active_cases[active_cases].sum(axis=1)
    #active_cases.sort_index(axis=1, inplace = True)
    active = active.append(active_cases)
    #print(active_cases)

cols = ['HUME', 'MELBOURNE', 'MELTON', 'MORELAND', 'MOONEE VALLEY', 'WYNDHAM', 'MOORABOOL','MACEDON RANGES', 'HOBSONS BAY','YARRA','MARIBYRNONG','DAREBIN','BRIMBANK']
confirmed[cols] = confirmed[cols].apply(pd.to_numeric, errors='coerce', axis=1)
confirmed['NWMPHN region']= confirmed[confirmed.columns[:confirmed.shape[1]-1]].sum(axis=1)
confirmed.rename(columns={'TOTAL':'VIC'}, inplace=True)

active[cols] = active[cols].apply(pd.to_numeric, errors='coerce', axis=1)
active['NWMPHN region']=active[active.columns[:active.shape[1]-1]].sum(axis=1)
active.rename(columns={'TOTAL': 'VIC'}, inplace=True)
confirmed
active

    

confirmed

confirmed



from pandas import ExcelWriter

writer = ExcelWriter('test.xlsx')
all.to_excel(writer)
writer.save()



zones=pd.read_csv("zones.txt",delimiter="\t", header = None)

zones

url = "http://www.fullemployment.net/evi/3.0/evi_3.0.php?SUA_Name_2016=Morisset+-+Cooranbong&order=1"
    
r = requests.get(url)
html = r.text

soup = BeautifulSoup(html)
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

result = pd.DataFrame(data) #table on the websitea

result = result[[0,2]]
result.columns=['SA2', 'EVI score']

result

df = pd.DataFrame()
for line in zones[0]:
    start = line.find(">",0,len(line))
    line = line[start+1:]
    #print(line)
    line = line.replace("-","+-+",1)
    #print(line)
    
    url = "http://www.fullemployment.net/evi/3.0/evi_3.0.php?SUA_Name_2016=" + line + "&order=1"
    
    r = requests.get(url)
    html = r.text

    soup = BeautifulSoup(html)
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    final = pd.DataFrame(data) #table on the websitea
    
    df = df.append(final)
df

df = df[[0,2]]
df.columns=['SA2', 'EVI score']

df

All_EVI = pd.merge(df, details, on='SA2', how='inner')

L_evi = pd.merge(df, details, on = 'SA2', how='left')
L_evi

R_evi = pd.merge(df, details, on='SA2', how = 'right')
R_evi

df[df.SA2 == 'Victor Harbor']

R_evi['EVI score_x'].isnull().sum()

R_evi.isnull().sum()

All_EVI[All_EVI.SA2 == 'Victor Harbor']

writer = ExcelWriter('EVI.xlsx')
R_evi.to_excel(writer)
writer.save()



