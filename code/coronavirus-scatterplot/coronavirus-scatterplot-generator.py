import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import datetime
from datetime import date
from matplotlib.ticker import PercentFormatter

finalData = pd.DataFrame(pd.np.empty((0, 5)))

#############################################################################################
#Find function to be used later
#############################################################################################

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

#############################################################################################
#Drawdown calculation
#############################################################################################
countryETFs = {
              'US': 'SPY',
              'China': 'MCHI', 
              'Japan': 'EWJ',
              'Germany': 'EWG',
              'India': 'INDA', 
              'United Kingdom': 'EWU',
              'France': 'EWQ',
              'Italy': 'EWI',
              'Brazil': 'EWZ',
              'Canada': 'EWC'
              }

countryDrawdowns = {
              'US': 0.00,
              'China': 0.00,
              'Japan': 0.00,
              'Germany': 0.00,
              'India': 0.00,
              'United Kingdom': 0.00,
              'France': 0.00,
              'Italy': 0.00,
              'Brazil': 0.00,
              'Canada': 0.00,
              }

for country in list(countryETFs.keys()):
  b = countryETFs[country]
  tgt_website = r'https://sg.finance.yahoo.com/quote/'+b+'/key-statistics?p='+b
  stock_company = f"https://finance.yahoo.com/quote/{b}"
  soup = BeautifulSoup(requests.get(stock_company).text, "html.parser")
  ticker_data_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{b}?symbol={b}&period1=1546300800&period2=9999999999&interval=1d"
  ticker_data = json.loads(requests.get(ticker_data_url).text)
  closingPrices = pd.Series(ticker_data['chart']['result'][0]['indicators']['quote'][0]['close'])

  dollarDrawdown = (closingPrices - closingPrices.cummax()).min()
  maxPrice = -list(closingPrices.cummax())[-1]
  maxDrawdown = dollarDrawdown/maxPrice
  
  countryDrawdowns[country] = maxDrawdown
  
#############################################################################################
#Coronavirus cases
#############################################################################################
coronavirusCases = {
              'US': 0.00,
              'China': 0.00,
              'Japan': 0.00,
              'Germany': 0.00,
              'India': 0.00,
              'United Kingdom': 0.00,
              'France': 0.00,
              'Italy': 0.00,
              'Brazil': 0.00,
              'Canada': 0.00,
              }

coronavirusData = pd.read_json('https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json')
updateDate = datetime.datetime.today().strftime('%Y-%m-%d')
updateDateNoZeros = datetime.datetime.today().strftime('%Y-%-m-%-d')
yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%-m-%-d')

for country in list(coronavirusCases.keys()):
    try:
        i = find(coronavirusData[country],'date',updateDate)
        coronavirusCases[country] = coronavirusData[country][i]['confirmed']
    except:
        i = find(coronavirusData[country],'date',yesterday)
        coronavirusCases[country] = coronavirusData[country][i]['confirmed']

#############################################################################################
#Coronavirus Deaths
#############################################################################################
coronavirusDeaths = {
              'US': 0.00,
              'China': 0.00,
              'Japan': 0.00,
              'Germany': 0.00,
              'India': 0.00,
              'United Kingdom': 0.00,
              'France': 0.00,
              'Italy': 0.00,
              'Brazil': 0.00,
              'Canada': 0.00,
              }

for country in list(coronavirusDeaths.keys()):
    try:
        i = find(coronavirusData[country],'date',updateDate)
        coronavirusDeaths[country] = coronavirusData[country][i]['deaths']
    except:
        i = find(coronavirusData[country],'date',yesterday)
        coronavirusDeaths[country] = coronavirusData[country][i]['deaths']

#############################################################################################
#Country populations
#############################################################################################
countryPopulations = {
              'US': 0.00,
              'China': 0.00,
              'Japan': 0.00,
              'Germany': 0.00,
              'India': 0.00,
              'United Kingdom': 0.00,
              'France': 0.00,
              'Italy': 0.00,
              'Brazil': 0.00,
              'Canada': 0.00,
              }

populationDict = pd.read_json('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json').set_index('country').to_dict()['population']

for country in list(countryPopulations.keys()):
    if(country == 'US'):
        countryPopulations[country] = populationDict['United States']
    else:
        countryPopulations[country] = populationDict[country]

#############################################################################################
#Creation of the finalized DataFrame
#############################################################################################
for country in list(countryETFs.keys()):
    finalData = finalData.append(pd.Series([
                                            country,
                                            countryDrawdowns[country],
                                            coronavirusCases[country],
                                            coronavirusDeaths[country],
                                            countryPopulations[country]]), 
                                                                            ignore_index=True)

finalData.columns=['Country','Drawdown','Coronavirus Cases','Coronavirus Deaths','Population']

finalData.set_index('Country', inplace = True)

finalData['Cases per Capita'] = finalData['Coronavirus Cases']/finalData['Population']
finalData['Deaths per Capita'] = finalData['Coronavirus Deaths']/finalData['Population']

#############################################################################################
#Define axis variables for plotting
#############################################################################################
y = finalData['Drawdown']
x1 = finalData['Cases per Capita']*10000
x2 = finalData['Deaths per Capita']
z = finalData.index

#############################################################################################
#Plot (CASES)
#############################################################################################
plt.clf()
plt.figure(figsize=(14,6))
plt.scatter(x1, y)
ax = plt.gca()
ax.yaxis.set_major_formatter(PercentFormatter(1))
for x,y,z in zip(x1,y,z):

    label = z
    if(z=='Canada' or z=='France'):
        plt.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    else:
        plt.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='left') # horizontal alignment can be left, right or center
    
plt.title('Stock market reactions to coronavirus cases')
plt.ylabel('Stock market drawdown')
plt.xlabel('Coronavirus cases per 10000')

plt.savefig('Cases.png')

#############################################################################################
#Plot (DEATHS)
#############################################################################################
plt.clf()
plt.figure(figsize=(14,6))
plt.scatter(x2, y)
ax = plt.gca()
ax.yaxis.set_major_formatter(PercentFormatter(1))
for x,y,z in zip(x2,y,z):

    label = z
    if(z=='Canada' or z=='France'):
        plt.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    else:
        plt.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='left') # horizontal alignment can be left, right or center
    
plt.title('Stock market reactions to coronavirus deaths')
plt.ylabel('Stock market drawdown')
plt.xlabel('Coronavirus deaths per 10000')

plt.savefig('Deaths.png')
