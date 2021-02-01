import json 
import requests 
import urllib.request as request
import pandas

# prevalence of anemia among children (% of children under 5)-
url = "http://api.worldbank.org/v2/country/all/indicator/SH.ANM.CHLD.ZS?format=json"
response = requests.get(url)
print(response.status_code)
# print(response.json())

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# jprint(response.json())

print(response.json()[1])

# data=json.loads(response)
# json.dumps(response, indent=4, sort_keys=True)

