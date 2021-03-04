import time
import datetime
import requests 
import pandas as pd
import pdb
import json 
import os


#only save upto prior year results since current year results will not be available to following year 
now = datetime.datetime.now()

#notes from Python group - for testing save the raw json data,  add a test to check that the s		

# import requested indicator list 
indReqDF = pd.read_csv("requestedIndicators.csv")


# import country code mappring from the UN M49  
unCntryCodeDF = pd.read_csv("UNSDCountryCodeMethodology.csv")

# import country code mapping from nestle 
nestleCntryCodeDF = pd.read_csv("nestle_countryCode.csv" )
# nestleCntryCodeDF["NestleCodeFormat"] = "Yes"

# import indicator id look up table 
indCodeFormatDF = pd.read_csv("indicatorIDLookUptable.csv", names = ("Indmeta_text", "IndMetaID"))
dict_indCode = indCodeFormatDF.set_index("Indmeta_text")["IndMetaID"].to_dict()

# download request 
dlTime = datetime.datetime.now()  
        
# retrieve all data with that code
def retr_json(ind):
    base_url = "https://ghoapi.azureedge.net/api/"
    ind_url = base_url+ind
    rind =  requests.get(ind_url) 
    whoIndData = rind.json()
    # with open("who")
    # json.dump(whoIndData)
# todo - save output with timestamp
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

        df =pd.DataFrame(zip(idData ,indCode, indName, spatialType ,spatialVal,timeType ,timeVal ,sexType, sexVal ,indVal ,indMean ,indlowCI ,indhiCI ,commentsData))
        df.columns = ["idData" ,"indCode", "indName", "spatialType" ,"spatialVal","timeType" ,"timeVal" ,"sexType", "sexVal" ,"indVal" ,"indMean" ,"indlowCI" ,"indhiCI" ,"commentsData"]
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
            print(df.head(5))

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

           #drop results not on country and year 
        # print("worrrrk")
        # print(dfThememain.head(5))
        dfThememain = dfThememain[(dfThememain.timeVal!=str(now.year -1)) & (dfThememain.timeType=="YEAR") & (dfThememain.spatialType=="COUNTRY")]
        # print(dfThememain.head(5))
    #    map the correct indicator text name to the results 
        indReqDF.rename(columns={'WHOSex': 'sexVal', 'IndicatorCodeDS': 'indCode'}, inplace=True)
        # print(indReqDF.columns)
        df2 = indReqDF[["sexVal","indCode","IndicatorName"]]
        # dfThememain["Indmeta_text"] = dfThememain[("sexVal","indCode") ].map(indReqDF.set_index("WHOSex","IndicatorCodeDS")["IndicatorName"].to_dict())
        dfThememain = dfThememain.merge(df2, on = ["sexVal","indCode"], how = "left")
        # print(dfThememain)
        #map to country code and region name 
        # dfThememain["Country_Code"] = dfThememain["spatialVal"].map(nestleCntryCodeDF.set_index("Countries")["Country_Code"].to_dict())
        dfThememain["Indmeta_text"] = dfThememain["IndicatorName"]
        dfThememain["IndMetaID"] = dfThememain["Indmeta_text"].map(indCodeFormatDF.set_index("Indmeta_text")["IndMetaID"].to_dict())
        dfThememain["Countries"] = dfThememain["spatialVal"].map(unCntryCodeDF.set_index("ISO-alpha3 Code")["Country or Area"].to_dict())
        dfThememain["Country_Code"] = dfThememain["spatialVal"].map(unCntryCodeDF.set_index("ISO-alpha3 Code")["ISO-alpha2 Code"].to_dict())
        dfThememain["World_Regions"] = dfThememain["Countries"].map(unCntryCodeDF.set_index("Country or Area")["Region Name"].to_dict())
        # print("worrrk")
        # print(dfThememain.head(5))

    #rename columns 
        dfThememain.rename(columns={'timeVal': 'Year', 'indVal': 'Val'}, inplace=True)
        # indCode, indName, spatialType ,spatialVal,timeType ,timeVal ,sexType, sexVal ,indVal ,indMean ,indlowCI ,indhiCI ,commentsData), 
      
     
        # reorder columns 
        dfThememain["FactID"] = ""
        print(dfThememain.columns )
        dfThememain = dfThememain[["FactID", "Val","Year","Countries","Country_Code", "World_Regions", "IndMetaID","Indmeta_text","ThemeID","Theme_text","Link", "Reference", "Download Date"]]

        #drop current year from results 
        df_output = dfThememain[(dfThememain.Year!=str(now.year -1))&(dfThememain.Country_Code.notnull())]
        print(now.year-1)
        print(dfThememain.head)
        #remove where there's not a UN or Nestle Code 
        df_drop = dfThememain[dfThememain.Country_Code.isnull() & dfThememain.Country_Code.isnull()]
        df_notNestle = dfThememain[dfThememain.Country_Code.isnull() & dfThememain.Country_Code.notnull()]
        outputname3 = (os.getcwd()+'/WHO Data/'+ 'QC_'+theme+'_discardedData.xlsx')            
        # df_drop.to_excel(outputname3, sheet_name = theme, index = False, header=True)
        df_dropsummary = df_drop.groupby("Countries").count()
        df_UNdropsummary =  df_notNestle.groupby("Countries").count()
        # df_dropsummary.to_excel(outputname3, sheet_name = theme+'summary', index = False, header=True)
        # outfile.close()  
        with pd.ExcelWriter(outputname3) as writer:  
            df_drop.to_excel(writer, sheet_name='AllDiscardedData')
            df_dropsummary.to_excel(writer, sheet_name='SummaryOfDiscard')
            df_notNestle.to_excel(writer, sheet_name ='AvailWithUNFormatOnly')
            df_UNdropsummary.to_excel(writer, sheet_name ='UNFormatOnlySummary')

        # export data 
        outputname2 = (os.getcwd()+'/WHO Data/'+ str(dfThemei.ThemeNumber[0]) +' '+theme+'.csv')            
        outfile = open(outputname2, 'wb')
        df_output.to_csv(outfile,index = False, header=True)
        outfile.close()  



 
    # export data 
    # outputname2 = ('WHO'+ str(dfThemei.ThemeNumber[0]) +' '+theme+'.csv')            
    # outfile = open(outputname2, 'wb')
    # dfThememain.to_csv(outfile,index = False, header=True)
    # outfile.close()   
   

# Call the function  individually for each set ... I think there's a time out issue if I try to run all of them at once  
# allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Chronic Disease Risk Factor")])

allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Overweight and Obesity")])
# allWHOData(indReqDF[(indReqDF.HostingReference=="WHO") & (indReqDF.Theme=="Life Style and Behaviour")])