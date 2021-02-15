import time
import datetime
import requests 
import pandas as pd

		
# import requested indicator list 
indReqDF = pd.read_csv("requestedIndicators.csv")

# download request 
dlTime = datetime.datetime.now()  
        
# retrieve all data with that code
def retr_json(ind):
    base_url = "https://ghoapi.azureedge.net/api/"
    ind_url = base_url+ind
    rind =  requests.get(ind_url)
    whoIndData = rind.json()
    return whoIndData

#create a funciton to loop through key value pairs in dicitionary to save the information  #WhoID,Year, Age, Sex, Country, Value
#whoIndData is the JSON data and indicatorName is the name of the indicator in the data
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
# loop through each  json bit to append all the values for each country and year to form one data set 
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

def allWHOData(reqDF):
    uniqThemes = reqDF.Theme.unique()
    for theme in uniqThemes:
        
        dfThemei = reqDF[(reqDF["Theme"]==theme) & (reqDF.HostingReference=="WHO")].drop_duplicates(subset="IndicatorCodeDS").reset_index(drop=True)
        dfThememain =pd.DataFrame()
        # whoCode = dfThemei.IndicatorCodeDS.unique()
        # whoIndNme =dfThemei.WHOIndName.unique()
        print(theme)
        #   loop through each indicator list and  request
        for i in range(len(dfThemei.IndicatorCodeDS)):
            print(i)
            json_data = retr_json(dfThemei.IndicatorCodeDS[i])
            df = retrieveIndData(json_data,dfThemei.WHOIndName[i])
            if not df.empty:
                # df["Indmeta_text"] = dfThemei.IndicatorName[i]
                df["Download Date"] = dlTime
                df["Link"] = dfThemei.Link[i]
                df["Reference"] = dfThemei.Reference[i]
                df["Theme_text"] = dfThemei.Theme[i]
                df["ThemeID"] = dfThemei.ThemeNumber[i]
                # print(df.head(5))

                #Append each iteration to main df 
                dfThememain=dfThememain.append( df,ignore_index=True)
            print(df.head(5))

 
    # export data 
    outputname2 = ('WHO'+ str(dfThemei.ThemeNumber[0]) +' '+theme+'.csv')            
    outfile = open(outputname2, 'wb')
    dfThememain.to_csv(outfile,index = False, header=True)
    outfile.close()   
   

# Call the function  individually for each set ... I think there's a time out issue if I try to run all of them at once  
# allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Chronic Disease Risk Factor")])

allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Overweight and Obesity")])
allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Life Style and Behaviour")])