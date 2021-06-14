from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
import numpy as np
import pandas as pd

def dataCollection():
    url = "https://www.worldometers.info/coronavirus/"
    htmlContent = requests.get(url).text

    soup = BeautifulSoup(htmlContent, 'html.parser')
    covidTable = soup.find("table",attrs={"id": "main_table_countries_today"})

def dataSort():
    # extract the table headings from the soup
    head = covidTable.thead.find_all("tr")
    headings = []

    for th in head[0].find_all("th"):
        headings.append(th.text.replace("\n", "").strip())

    # extract actual data from the soup
    body = covidTable.tbody.find_all("tr")
    data = []

    # iterate through every row in the html
    for r in range(1,len(body)):
        row = []
        # find all column entries in that particular row
        for tr in body[r].find_all("td"):
            row.append(tr.text.replace("\n","").strip())
        data.append(row)
    df = pd.DataFrame(data,columns = headings)
    df.head(20)

def dataSplit():



def createCSV():

