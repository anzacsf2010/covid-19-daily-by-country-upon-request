#!/usr/bin/python3
#-------------------------------------------#
"""
###########################
Script: This is a simple tool that allows a user to enter any country that has been reported cases on COVID-19, and then show a data frame for the said county along with the visualization from Jan 22 to date. 

By: Andy St. Fort

Date: May 5, 2020
###########################
"""
import PySimpleGUI as sg      
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import requests
import io
from datetime import date, timedelta
plt.style.use('fivethirtyeight')


def main():
    """
    Main method. Will be passed in our conditional statement later.
    """
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],      
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
            ['Help', 'About...'], ] 
    sg.theme('Black') 
    layout = [  [sg.Text('Please enter a country name',size=(100,2),justification='center',auto_size_text=True)],
                [sg.In(size=(100,2), key='-countryName-',justification='center')],          
                [sg.Text('Correct country name will show here', size=(100,2), key='output',justification='center')],      
                [sg.Button('Get data',pad=((250, 5), 0),size=(7,0),bind_return_key=True),sg.Button('Clear',size=(7,0)),sg.Quit(size=(7,0))],
                [sg.Text('Country data output...', size=(100, 1),justification='center')],    
                [sg.Output(size=(100,42),key='-Print-')] ]      
    window = sg.Window('COVID-19 Country Data Analysis', layout, finalize=True)   
    
    
    def read_data_full():
        """
        Read online CSV file and save the data in csvFile variable
        """
        # Get CSV data from online (up to date CSV)
        url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
        csv = requests.get(url).content
        # Read CSV data
        csvFile = pd.read_csv(io.StringIO(csv.decode('unicode_escape')),error_bad_lines=False)
        csvFile = csvFile.set_index(['Date'])
        return csvFile


    def read_data_monthly(val): # setting Country as index
        """
        Setting 'Country' as the index in order to sort the values from the csvFile using country names
        """
        countryData = val.reindex(columns=['Country','Confirmed','Recovered','Deaths'])
        return countryData


    def generate_monthly_data(val): # Rearrangind per month
        """
        Rearranging the countryData from read_data_monthly() per month for better reporting on a monthly basis. The last month is reported via the last available data (Yesterday or 2 days back)
        """
        # January data for all countries
        janData = val.loc['2020-01-31']
        janDataCountriesTotal = janData.set_index(['Country'])
        # February data for all countries
        febData = val.loc['2020-02-29']
        febDataCountriesTotal = febData.set_index(['Country'])
        # March data for all countries
        marData = val.loc['2020-03-31']
        marDataCountriesTotal = marData.set_index(['Country'])
        # April data for all countries
        aprData = val.loc['2020-04-30']
        aprDataCountriesTotal = aprData.set_index(['Country'])
        # May data for all countries though last available day
        lastDay1 = str(date.today() - timedelta(days=1)) # Try for 1 day back
        lastDay2 = str(date.today() - timedelta(days=2)) # Try 2 days back if the 1 day back data has not been made available yet
        try:
            check = val.loc[lastDay1].count()
            if check == 0:
                mayData = val.loc[lastDay2]
            else: 
                mayData = val.loc[lastDay1]
        except:
            mayData = val.loc[lastDay2]
        mayDataCountriesTotal = mayData.set_index(['Country'])
        return janDataCountriesTotal,febDataCountriesTotal,marDataCountriesTotal,aprDataCountriesTotal,mayDataCountriesTotal


    def check_country_name(val1,val2):
        """
        Get a count check once country name is entered to make sure that the country name exist in the csvFile
        """
        return val1.loc[val2].count()


    def generate_daily_mean(val):
        """
        Generating daily mean via the last available data since the data is cumulative. Then, the total is divided by the total days of the outbreak (Jan 22, 2020 through last available data date)
        """
        numberOfDays = ((date.today() - timedelta(days=1))- date(2020, 1, 22)).days
        countryCasesDailyMean = np.round(val / numberOfDays)
        return countryCasesDailyMean

    
    def getPlotsforCountry(val):
        """
        Generate a plot for the country entered using the value from countryData
        """
        countryVal = countryData[countryData.Country == val]
        plt.rcParams['figure.figsize'] = (12,10)  
        countryVal.plot(grid=True)
        plt.show(block=False)
    

    # Invoking the necessary methods to get the data needed for the event loop.
    csvFile = read_data_full()
    countryData = read_data_monthly(csvFile)
    countryData_Jan,countryData_Feb,countryData_Mar,countryData_Apr,countryData_May = generate_monthly_data(countryData)


    # Event loop for Get data, quit and clear buttons
    while True:      
        event, values = window.read()      
        if event == 'Get data':  
            final_check = 0 # One more check to make sure if the country name is correct, to proceed with all the function invocations for this event
            try:        
                countryName = str(values['-countryName-'])
                if countryName in ['United States','USA','usa','United States of America','U.S.A','u.s.a','united states of america','u.s.a.','us','u.s.']:
                    countryName = 'US'
                    final_check = 1
                if countryName in ['Ivory Coast','ivory coast', 'Ivory coast']:
                    countryName = 'Cote d\'Ivoire'
                    final_check = 1
                if countryName in ['South Korea','south korea','Korea']:
                    countryName = 'Korea, South'
                    final_check = 1
                if countryName in ['England','Scotland','UK','U.K.','Northern Ireland','Wales','u.k.','uk','Great Britain']:
                    countryName = 'United Kingdom'
                    final_check = 1
                if countryName in ['Holland']:
                    countryName = 'Netherlands'
                    final_check = 1
                if countryName == 'Congo':
                    sg.popup_ok('Please type either [Congo (Brazzaville)] or [Congo (Kinshasa)] in your entry')
                check = check_country_name(countryData_Jan,countryName)
                if check == 0:
                    sg.popup_error('Country name not found! Please try again.')
                if check > 0:
                    final_check = 1
                if not countryName:
                    sg.popup_error('Invalid country name!')
            except:
                sg.popup_error('Invalid country name!')
                window['output'].update('') 
                window['-countryName-'].update('')
            window['output'].update(countryName)
            if final_check == 1:
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('Monthly Data')
                print(f'--------------January 2020 ({countryName})------------ \n')
                janSeries = countryData_Jan.loc[[countryName],['Confirmed','Recovered','Deaths']]
                print(janSeries)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(f'--------------February 2020 ({countryName})------------ \n')
                febSeries = countryData_Feb.loc[[countryName],['Confirmed','Recovered','Deaths']]
                print(febSeries)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(f'--------------March 2020 ({countryName})------------ \n')
                marSeries = countryData_Mar.loc[[countryName],['Confirmed','Recovered','Deaths']]
                print(marSeries)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(f'--------------April 2020 ({countryName})------------ \n')
                aprSeries = countryData_Apr.loc[[countryName],['Confirmed','Recovered','Deaths']]
                print(aprSeries)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(f'--------------May 2020 ({countryName})------------ \n')
                maySeries = countryData_May.loc[[countryName],['Confirmed','Recovered','Deaths']]
                print(maySeries)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('Daily Mean')
                print(f'--------------Daily Mean - To Date ({countryName})------------ \n')
                print(generate_daily_mean(maySeries))
                getPlotsforCountry(countryName)
        if event in ['Clear', None]:
            try:
                countryName = ''
            except:
                sg.popup_ok('An error has occurred.')
            window['-countryName-'].update('')
            window['output'].update('') 
            window['-Print-'].update('')
        if event == 'Quit':
            break


if __name__ == '__main__':
    main()
