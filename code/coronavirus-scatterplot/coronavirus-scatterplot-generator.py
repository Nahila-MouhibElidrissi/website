import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

IEXCloudToken = 'pk_dd4acf3b93b840f2878acef207ffd8cc'

countryETFs = {
              'United States': 'SPY',
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

populationData = pd.read_json('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')

finalData = pd.DataFrame(pd.np.empty((0, 5)))

#Drawdown Calculation
countryDrawdowns = {
              'United States': 0.00,
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
  pass

#Corona Cases
for country in list(countryETFs.keys()):
  pass

#Corona Deaths
for country in list(countryETFs.keys()):
  pass

#Population
for country in list(countryETFs.keys()):
  pass

#Creation of the DataFrame
for country in list(countryETFs.keys()):
    finalData = finalData.append(pd.Series[country,countryDrawdowns[country],CoronaCases[country],coronaDeaths[country],populationData[country]], ignore_index=True)
