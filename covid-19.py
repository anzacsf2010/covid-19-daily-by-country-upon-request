#!/usr/bin/python3
#-------------------------------------------#
import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt
import requests
import io
from datetime import date, timedelta

print('################################# \n')
print('COVID-19 Data Analysis')
print('################################# \n')

def main():
    # Get CSV data from online (up to date CSV)
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    csv = requests.get(url).content
    print('+++++++++++++++++++++++++++++++')
    # Read CSV data
    csvFile = pd.read_csv(io.StringIO(csv.decode('utf-8')),error_bad_lines=False)
    csvFile = csvFile.set_index(['Date'])
    #print('+++++++++++++++++++++++++++++++')
    # January data for all countries
    janData = csvFile.loc['2020-01-31']
    janDataCountriesTotal = janData.set_index(['Country'])
    #print('Total Confirmed, Recovered, and Death Cases by Country in January:')
    #print(janDataCountriesTotal)
    #print('+++++++++++++++++++++++++++++++')
    # February data for all countries
    febData = csvFile.loc['2020-02-29']
    febDataCountriesTotal = febData.set_index(['Country'])
    #print('Total Confirmed, Recovered, and Death Cases by Country in February:')
    #print(febDataCountriesTotal)
    #print('+++++++++++++++++++++++++++++++')
    # March data for all countries
    marData = csvFile.loc['2020-03-31']
    marDataCountriesTotal = marData.set_index(['Country'])
    #print('Total Confirmed, Recovered, and Death Cases by Country in March:')
    #print(marDataCountriesTotal)
    #print('+++++++++++++++++++++++++++++++')
    # April data for all countries
    aprData = csvFile.loc['2020-04-30']
    aprDataCountriesTotal = aprData.set_index(['Country'])
    #print('Total Confirmed, Recovered, and Death Cases by Country in April:')
    #print(aprDataCountriesTotal)
    #print('+++++++++++++++++++++++++++++++')
    # May data for all countries though last available day
    lastDate = str(date.today() - timedelta(days=1))
    mayData = csvFile.loc[lastDate]
    mayDataCountriesTotal = mayData.set_index(['Country'])
    #print('Total Confirmed, Recovered, and Death Cases by Country in May:')
    #print(mayDataCountriesTotal)
    # Take user input and process input value
    def getCountryName():
        while True:
            try:
                s = input('Country name: ')
            except:
                print(f'{s} is not a country name')
                continue
            if not (janDataCountriesTotal.loc[s].count() > 0):
                print(f'{s} is not a country name. Please check spelling.')
                continue
            if not s:
                print('Country name cannot be empty')
                continue
            else:
                print('Country name: ')
                countryName = s
                break
            return countryName
            countryName = countryName
        return countryName
    countryName = getCountryName()
    # Use input value to return data
    def getDataforCountry(val):
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'--------------January 2020 ({countryName})------------ \n')
        print('Total Confirmed, Recovered, and Death Cases: \n')
        janSeries = janDataCountriesTotal.loc[[val],['Confirmed','Recovered','Deaths']]
        print(janSeries)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'--------------February 2020 ({countryName})------------ \n')
        print('Total Confirmed, Recovered, and Death Cases: \n')
        febSeries = febDataCountriesTotal.loc[[val],['Confirmed','Recovered','Deaths']]
        print(febSeries)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'--------------March 2020 ({countryName})------------ \n')
        print('Total Confirmed, Recovered, and Death Cases: \n')
        marSeries = marDataCountriesTotal.loc[[val],['Confirmed','Recovered','Deaths']]
        print(marSeries)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'--------------April 2020 ({countryName})------------ \n')
        print('Total Confirmed, Recovered, and Death Cases: \n')
        aprSeries = aprDataCountriesTotal.loc[[val],['Confirmed','Recovered','Deaths']]
        print(aprSeries)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'--------------May 2020 ({countryName})------------ \n')
        print('Total Confirmed, Recovered, and Death Cases: \n')
        maySeries = mayDataCountriesTotal.loc[[val],['Confirmed','Recovered','Deaths']]
        print(maySeries)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # Graph results for given country
    def getPlotsforCountry(val):
        return "We are working on this"
    # Run for given country
    print(f'Here is the data for {countryName}:')
    getDataforCountry(countryName)
    # Decide to run it for another country
    while True:
        try:
            nextStep = input('Do you want to see another country? Y/N: ')
        except ValueError:
            print('Please enter Y or N: ')
            continue
        if nextStep not in ['Y','N']:
            print('Please enter Y or N: ')
            continue
        if nextStep == 'Y':
            countryName = getCountryName()
            print(f'Here is the data for {countryName}:')
            getDataforCountry(countryName)
            continue
        else:
            print('Thank you for using this tool.')
            break


if __name__ == '__main__':
    main()