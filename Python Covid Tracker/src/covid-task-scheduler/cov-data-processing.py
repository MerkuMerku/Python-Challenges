import os
import shutil
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
from datetime import datetime

# disable pandas table copy warnings - these aren't relevant to what we're doing
pd.options.mode.chained_assignment = None

# webscrape from worldometers.info - our soup is a HTML table element
url = "https://www.worldometers.info/coronavirus/"
htmlContent = requests.get(url).text
soup = BeautifulSoup(htmlContent, 'html.parser')
covidTable = soup.find("table", attrs={"id": "main_table_countries_today"})

# here we simply extract the table headings from the soup, using the table head element (th)
head = covidTable.thead.find_all("tr")
headings = []
for th in head[0].find_all("th"):
    headings.append(th.text.replace("\n", "").strip())

# extract the rows of data from the table element, and append them to the data list.
body = covidTable.tbody.find_all("tr")
data = []
for r in range(1, len(body)):
    row = []
    for tr in body[r].find_all("td"):
        row.append(tr.text.replace("\n", "").strip())
    len(row)
    data.append(row)

# construct a dataframe using the data list, and the headings extracted from the HTML
df = pd.DataFrame(data, columns=headings)

######################################################################
#                         CLEAN DATA TABLE                           #
######################################################################

# define nan object for NAN data entries
NaN = np.nan

# recover appropriate columns - discard the rest
df = df.filter(['Continent', 'Country,Other', 'TotalCases',
                'TotalRecovered', 'Serious,Critical', 'ActiveCases', 'TotalDeaths'])

# strip artefacts from the data
df = df.replace(',', '', regex=True)
df = df.replace('\+', '', regex=True)
df = df.replace('', NaN, regex=True)

# convert appropriate columns from string to integer type
df[['TotalCases', 'TotalRecovered', 'Serious,Critical', 'ActiveCases', 'TotalDeaths']] = df[['TotalCases', 'TotalRecovered',
                                                                                             'Serious,Critical', 'ActiveCases', 'TotalDeaths']].apply(pd.to_numeric, downcast='float', errors='coerce')

# add date of processing to all rows
now = datetime.now()
dt_string = now.strftime("%d%m%Y")
df['DateProcessed'] = dt_string

# extract world data from the main dataframe
world_df = df.loc[df['Country,Other'] == "World"]

# select the appropriate data for the world data dataframe
world_df = world_df.filter(['TotalCases', 'TotalRecovered',
                            'Serious,Critical', 'ActiveCases', 'TotalDeaths', 'DateProcessed'])

# extract non-critical covid cases data
world_df = world_df.assign(NonCritical_Active=world_df['ActiveCases'].astype(
    float) - world_df['Serious,Critical'].astype(float))
# probably going to remove this
world_df.rename(columns={'NonCritical_Active': 'Non-Critical, Active',
                         'Serious,Critical': 'Critical, Active'}, inplace=True)

# add percentage columns from the data in the table
world_df = world_df.assign(TotalRecoveredPerc=(int(world_df['TotalRecovered'].astype(
    float)) / int(world_df['TotalCases'].astype(float))) * 100)
world_df = world_df.assign(CritPerc=(world_df['Critical, Active'].astype(
    float) / world_df['TotalCases'].astype(float)) * 100)
world_df = world_df.assign(DeathPerc=(world_df['TotalDeaths'].astype(
    float) / world_df['TotalCases'].astype(float)) * 100)
world_df = world_df.assign(NonCritPerc=(
    world_df['Non-Critical, Active'].astype(float) / world_df['TotalCases'].astype(float)) * 100)

# drop redundant cols, and re-assign column names for database transfer
world_df = world_df.drop(columns=['ActiveCases']).reset_index(drop=True)
world_df.rename(columns={'TotalCases': 'total_cases', 'TotalRecovered': 'total_recovered', 'Critical, Active': 'critical_active', 'TotalDeaths': 'total_deaths', 'DateProcessed': 'date_processed', 'Non-Critical, Active': 'non_critical_active',
                         'TotalRecoveredPerc': 'total_recovered_percentage', 'CritPerc': 'critical_active_percentage', 'DeathPerc': 'total_deaths_percentage', 'NonCritPerc': 'non_critical_active_percentage'}, inplace=True)

# extract continent data
continents_df = df.iloc[0:5]
continents_df.drop(columns=['Country,Other'], inplace=True)

# we don't have data for north america, so let's extract it from countries labeled under north america.
na = df.loc[df['Continent'] == "North America"]
del na["Continent"]
na = na.replace('', '0', regex=True)
row = []
row.append("North America")

# here we sum all country values for each column under the na dataframe to acquire the totals for north america
for column in na.columns[1:]:
    na[column] = pd.to_numeric(na[column], errors='coerce')
    row.append(round(na[column].sum()))
row = [row]

# add north america to the continents dataframe
continents_df = continents_df.append(pd.DataFrame(
    row, columns=continents_df.columns), ignore_index=True)
continents_df = continents_df.assign(NonCritical_Active=continents_df['ActiveCases'].astype(
    float) - continents_df['Serious,Critical'].astype(float))
# probably going to remove this
continents_df.rename(columns={'NonCritical_Active': 'Non-Critical, Active',
                              'Serious,Critical': 'Critical, Active'}, inplace=True)

# add in percentage columns
continents_df = continents_df.assign(TotalRecoveredPerc=(
    continents_df['TotalRecovered'].astype(float) / continents_df['TotalCases'].astype(float)) * 100)
continents_df = continents_df.assign(CritPerc=(continents_df['Critical, Active'].astype(
    float) / continents_df['TotalCases'].astype(float)) * 100)
continents_df = continents_df.assign(DeathPerc=(continents_df['TotalDeaths'].astype(
    float) / continents_df['TotalCases'].astype(float)) * 100)
continents_df = continents_df.assign(NonCritPerc=(
    continents_df['Non-Critical, Active'].astype(float) / continents_df['TotalCases'].astype(float)) * 100)

continents_df = continents_df.sort_values(by=['TotalCases'], ascending=False)
continents_df.rename(columns={'TotalCases': 'total_cases', 'TotalRecovered': 'total_recovered', 'Serious, Critical': 'critical_active', 'TotalDeaths': 'total_deaths', 'DateProcessed': 'date_processed', 'Non-Critical, Active': 'non_critical_active',
                              'TotalRecoveredPerc': 'total_recovered_percentage', 'CritPerc': 'critical_active_percentage', 'DeathPerc': 'total_deaths_percentage', 'NonCritPerc': 'non_critical_active_percentage', 'Continent': 'continent'}, inplace=True)

# country
countries_df = df.loc[7:len(df)]
countries_df = countries_df.reset_index()
countries_df = countries_df.drop(columns='index')

countries_df = countries_df.assign(NonCritical_Active=countries_df['ActiveCases'].astype(
    float) - countries_df['Serious,Critical'].astype(float))
countries_df.rename(columns={'NonCritical_Active': 'Non-Critical, Active',
                             'Serious,Critical': 'Critical, Active'}, inplace=True)

# add in percentage columns
countries_df = countries_df.assign(TotalRecoveredPerc=(
    countries_df['TotalRecovered'].astype(float) / countries_df['TotalCases'].astype(float)) * 100)
countries_df = countries_df.assign(CritPerc=(countries_df['Critical, Active'].astype(
    float) / countries_df['TotalCases'].astype(float)) * 100)
countries_df = countries_df.assign(DeathPerc=(countries_df['TotalDeaths'].astype(
    float) / countries_df['TotalCases'].astype(float)) * 100)
countries_df = countries_df.assign(NonCritPerc=(
    countries_df['Non-Critical, Active'].astype(float) / countries_df['TotalCases'].astype(float)) * 100)

countries_df = countries_df.sort_values(by=['TotalCases'], ascending=False)
countries_df.rename(columns={'TotalCases': 'total_cases', 'Country,Other': 'country', 'TotalRecovered': 'total_recovered', 'Serious, Critical': 'critical_active', 'TotalDeaths': 'total_deaths', 'DateProcessed': 'date_processed', 'Non-Critical, Active':
                             'non_critical_active', 'TotalRecoveredPerc': 'total_recovered_percentage', 'CritPerc': 'critical_active_percentage', 'DeathPerc': 'total_deaths_percentage', 'NonCritPerc': 'non_critical_active_percentage', 'Continent': 'continent'}, inplace=True)

# create a folder for the csv data extracts if there isn't aready one using the os module
path = os.getcwd()
directory = 'csv_extracts'

if os.path.isdir(directory):
    print("Extracts directory found at '%s'" % (path+directory))
    path = os.path.join(path, directory)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        print("Removing old file '%s' at '%s'" % (filename, file_path))
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
else:
    print('Extracts directory not found, creating csv extracts directory and files...')
    path = os.path.join(path, directory)
    os.mkdir(path)
    try:
        if os.path.isdir(directory):
            print("Directory '% s' successfully created" % directory)
    except Exception as e:
        print("Could not create directory '% s'. Reason: %s" % (directory, e))

# create csv files from extracts

# world df
csv_name = path + "/world_csv_" + dt_string + ".csv"
print(csv_name)
world_df.to_csv(csv_name)

# continents df
csv_name = path + "/continent_csv_" + dt_string + ".csv"
print(csv_name)
continents_df.to_csv(csv_name)

# countries df
csv_name = path + "/country_csv_" + dt_string + ".csv"
print(csv_name)
countries_df.to_csv(csv_name)

engine = create_engine('sqlite:///../application/site.db', echo=True)
sqlite_connection = engine.connect()

world_df.to_sql("world", sqlite_connection, if_exists='replace')

continents_df.to_sql("continents", sqlite_connection, if_exists='replace')

countries_df.to_sql("countries", sqlite_connection, if_exists='replace')

sqlite_connection.close()
