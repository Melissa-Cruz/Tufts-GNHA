# get  Prevalence of overweight, age-standardized from  WHO data https://apps.who.int/gho/data/node.main.A897A?lang=en 
# import library 
import requests 
import pandas as pd

#find the indicator code 
r = requests.get('https://ghoapi.azureedge.net/api/Indicator')
whoIndDict = r.json()

# print(whoIndDict) 
# print(len(whoIndDict))
# print(type(whoIndDict))
# print(whoIndDict["value"][1])

#dictionary is a colllection of dictionaries so you need to loop through and find indicator name and code
whoInd = list()
whoIndName = list() 

for elemDict in whoIndDict["value"]:
    whoInd.append(elemDict["IndicatorCode"])
    whoIndName.append(elemDict["IndicatorName"])
 
#create and export data frame of indicator code and indicator name to share 
whoGNHAIndDict = pd.DataFrame(zip(whoInd, whoIndName), columns=["IndicatorCode","IndicatorName"])
whoGNHAIndDict.to_csv (r'\WHOIndicatorDictionary.csv', header=True)


# IndexNum:849	Code:NCD_BMI_25A	Name:Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)
print(whoIndDict["value"][849])
# print(whoIndDict["value"][["IndicatorCode"]=="NCD_BMI_25A"]) #doesn't print what I expected

#retrieve all data with that code
base_url = "https://ghoapi.azureedge.net/api/"
ind_url = base_url+"NCD_BMI_25A"
rind =  requests.get(ind_url)
whoIndData = rind.json()

#  print an example of key value pair 
# print(whoIndData["value"][1])

#create a funciton to loop through key value pairs in dicitionary to save the information  #WhoID,Year, Age, Sex, Country, Value
def retrieveIndData(whoIndData, indicatorName):
    idData = list()
    indCode = list()
    indName =list()
    spatialType = list()
    spatialVal = list()
    timeType = list()
    timeVal = list()
    sexType = list()
    sexVal =list()
    indVal = list()
    indMean = list()
    indlowCI = list()
    indhiCI = list()
    commentsData =list()

    for elem in whoIndData["value"]:
        idData.append(elem["Id"])
        indCode.append(elem["IndicatorCode"])
        indName.append(indicatorName)
        spatialType.append(elem["SpatialDimType"])
        spatialVal.append(elem["SpatialDim"])
        timeType.append(elem["TimeDimType"])
        timeVal.append(elem["TimeDim"])
        sexType.append(elem["Dim1Type"])
        sexVal.append(elem["Dim1"])
        indVal.append(elem["Value"])
        indMean.append(elem["NumericValue"])
        indlowCI.append(elem["Low"])
        indhiCI.append(elem["High"])
        commentsData.append(elem["Comments"])
    
    df =pd.DataFrame(zip(idData ,indCode, indName, spatialType ,spatialVal,timeType ,timeVal ,sexType, sexVal ,indVal ,indMean ,indlowCI ,indhiCI ,commentsData), columns = ["id", "IndicatorCode","IndicatorName",  "SpatialType", "SpatialVal",
    "TimeType", "TimeValue", "SexType", "SexValue", "IndValue", "ValueMean", "ValueLowCI", "ValueHighCI","Comments"])

    return df

dfOW = retrieveIndData(whoIndData, indicatorName = "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)" )
dfOW.to_csv(r'WHO_OWdata.csv', index=False, header = True)
print(dfOW.head())



#Next stps is to make this more generalizeable i can make a function that creates a list from all the keys