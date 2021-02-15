#02/13/2021  - retrieve data from world bank based on indicator list 

# import libraries 
import pandas as pd 
import wbdata 
import os
import time
import datetime

#Data Format 
# FactID	Val	Year	Countries	Coutry_code	World_Regions	Zones	IndmetaID	Indmeta_text	ThemeID	Theme_text	Link	Reference

#Download Date  
dlTime = datetime.datetime.now()  

		
# import requested indicator list 
indReqDF = pd.read_csv("requestedIndicatorsManually.csv")
   
# def wbManual(indReqDF): 
    # for i in range(len(indReqDF.IndicatorCodeDS)):
i=0
# indDict = {indReqDF.IndicatorCodeDS[i]:indReqDF.IndicatorNameDS[i]}
# print(indDict)
# indDict = {"SH.STA.ACSN.UR":"People using safely managed sanitation services, urban (% of urban population)"}
# indDict = {"SH.STA.ACSN":"People using safely managed sanitation services (% of population)"}
# indDict= {"SH.STA.BRTW.ZS":"Low-birthweight babies (% of births)"}
df= wbdata.get_dataframe(indicators=indDict, keep_levels=False)
df.reset_index(level=df.index.names, inplace=True)
df.columns = ["Country", "Year", "Val"]
df["Indmeta_text"] = indReqDF.IndicatorName[i]
df["Download Date"] = dlTime
df["Link"] = indReqDF.Link[i]
df["Reference"] = indReqDF.Reference[i]
df["Theme_text"] = indReqDF.Theme[i]
df["ThemeID"] = indReqDF.ThemeNumber[i]

# export data 
outputname2 = (os.getcwd()+'/WorldBankData/'+ str(indReqDF.ThemeNumber[i]) +' '+indReqDF.IndicatorCodeDS[i]+'.csv')            
outfile = open(outputname2, 'wb')
df.to_csv(outfile,index = False, header=True)
outfile.close()   

# wbManual(indReqDF)
# Thse are a not in API 
# People using safely managed sanitation services, rural (% of rural population)		SH.STA.ACSN.RU 
# People using safely managed sanitation services (% of population)		SH.STA.ACSN 
# People using safely managed sanitation services, urban (% of urban population)		SH.STA.ACSN.UR 
# People using safely managed drinking water services (% of population)		SH.H2O.SAFE.ZS 
# People using safely managed drinking water services, rural (% of rural population)		SH.H2O.SAFE.RU.ZS
# People using safely managed drinking water services, urban (% of urban population)		SH.H2O.SAFE.UR.ZS
# is In API 
# Low-birthweight babies (% of births)		SH.STA.BRTW.ZS