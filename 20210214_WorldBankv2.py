#02/13/2021  - retrieve data from world bank based on indicator list 

# import libraries 
import pandas as pd 
import wbdata 
import os
import time
import datetime
#test an error
		
# import requested indicator list 
indReqDF = pd.read_csv("requestedIndicators.csv")
# indReqDF.columns

def reqWorldBankData(reqDF): 
    # loop through each theme 
    uniqThemes = reqDF.Theme.unique()
    for theme in uniqThemes:
        
        dfThemei = reqDF[(reqDF["Theme"]==theme) & (reqDF.HostingReference=="World Bank")].reset_index(drop=True)
        dfThememain =pd.DataFrame(columns=["Country", "Year", "Val", "Indmeta_text", "Download Date","Link","Reference","Theme_text","ThemeID" ])
        print(theme)
           # indCode=list()
        # print(range(len(dfThemei.IndicatorCodeDS)))
    #   loop through each indicator list and  request
        for i in range(len(dfThemei.IndicatorCodeDS)):

            dlTime = datetime.datetime.now()  
            # print(i)
            # print(dfThemei.IndicatorCodeDS[0])
            # if dfThemei.HostingReference[i]=="World Bank":
            indDict = {dfThemei.IndicatorCodeDS[i]:dfThemei.IndicatorNameDS[i]}
            print(indDict)
            df=wbdata.get_dataframe(indicators=indDict, country='all',  keep_levels=False)
            df.reset_index(level=df.index.names, inplace=True)
            # print(df.head(5))

            # format data 
            if not df.empty:
                df.columns = ["Countries", "Year", "Val"]
                df["Indmeta_text"] = dfThemei.IndicatorName[i]
                df["Download Date"] = dlTime
                df["Link"] = dfThemei.Link[i]
                df["Reference"] = dfThemei.Reference[i]
                df["Theme_text"] = dfThemei.Theme[i]
                df["ThemeID"] = dfThemei.ThemeNumber[i]
                # print(df.head(5))

                #Append each iteration to main df 
                dfThememain=dfThememain.append( df,ignore_index=True)
                

 
                # outputname = (os.getcwd()+'/WorldBankData/'+str(dfThemei.ThemeNumber[i]) + ' '+dfThemei.IndicatorName[i]+'.csv')
        # export data 
        outputname2 = (os.getcwd()+'/WorldBankData/'+ str(dfThemei.ThemeNumber[0]) +' '+theme+'.csv')            
        outfile = open(outputname2, 'wb')
        dfThememain.to_csv(outfile,index = False, header=True)
        outfile.close()   



# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.HostingReference=="World Bank")])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==3.5)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==4.6)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==5.3)])

# for whatever reason I have to do this seperate 
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==5.3)])


# df["IndmetaId"] = list()
# FactID	Val	Year	Countries	Coutry_code	World_Regions	Zones	IndmetaID	Indmeta_text	ThemeID	Theme_text	Link	Reference

# column_titles = ["Val","Year","Countries","Country_code", "World_Regions", "Zones","IndmetaID","Indmeta_text", "ThemeID", "Theme_text", "Link", "Reference", "Download Date"]
# dfThememain.reindex(columns=column_titles)


    


