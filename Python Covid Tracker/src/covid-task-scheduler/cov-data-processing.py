import os
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
from datetime import datetime

# turn off annoying warnigns
pd.options.mode.chained_assignment = None  # default='warn'

url = "https://www.worldometers.info/coronavirus/"
htmlContent = requests.get(url).text

soup = BeautifulSoup(htmlContent, 'html.parser')
covidTable = soup.find("table", attrs={"id": "main_table_countries_today"})
