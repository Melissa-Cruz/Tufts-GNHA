import requests
import json 

#make a call to the api on "Prevalence of wasting, weight for height (% of children under 5)"
response=requests.get("http://api.worldbank.org/v2/country/CO/indicators/SH.STA.WAST.ZS?format=json")





#check if the request was successfull - status code 200 
print(response.status_code) 

print(response.json())

#make a function to pring a formatted JSON object for easier readability
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# jprint(response.json())['date']

