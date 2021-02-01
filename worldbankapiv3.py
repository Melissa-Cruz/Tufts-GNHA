import pandas as pd 
from pandas.io.json import json_normalize

url = "http://api.worldbank.org/v2/country/all/indicator/SH.ANM.CHLD.ZS?format=json"
my_dataset = requests.get(url, headers=header, params=param).json()

data = json_normalize(my_dataset)