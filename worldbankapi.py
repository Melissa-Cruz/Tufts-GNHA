import json 
import requests 
import urllib.request as request

# prevalence of anemia among children (% of children under 5)-Afghanistan
url = "http://api.worldbank.org/v2/country/all/indicator/SH.ANM.CHLD.ZS?format=json"
with request.urlopen(url) as response:
    if response.getcode()==200:
        source = response.read()
        data = json.loads(source)
        json1_data = json.loads(source)[0]
        type(json1_data)
        print(json1_data.keys())
        # print(data.keys())
        # datapoints = json1_data['datapoints']
        # print(datapoints)
    else:
        print(response.getcode())

type(json1_data)
print(json1_data['total'])


# for (var key in obj.d) {
#     console.log("Key: " + key);
#     console.log("Value: " + obj.d[key]);
# }

