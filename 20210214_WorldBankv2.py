#02/13/2021  - retrieve data from world bank based on indicator list 

# import libraries 
import pandas as pd 
import wbdata 
import os
import time
import datetime
import openpyxl

#only save upto prior year results since current year results will not be available to following year 
now = datetime.datetime.now()
# import pdb
#test an error
		
# import requested indicator list 
indReqDF = pd.read_csv("requestedIndicators.csv")

# df=wbdata.get_dataframe(indicators={"SP.DYN.TO65.FE.ZS":'Survival to age 65, female (% of cohort)'}, country='all',  keep_levels=False)
# print(df)

# import country code mappring from the UN M49  
unCntryCodeDF = pd.read_csv("UNSDCountryCodeMethodology.csv")
# ISO-alpha2 Code ,Region Name,  Country or Area
# dict_unCountries = unCntryCodeDF.set_index("Country or Area").to_dict()
# print(dict_unCountries)

# import country code mapping from nestle 
nestleCntryCodeDF = pd.read_csv("nestle_countryCode.csv" )
# nestleCntryCodeDF["NestleCodeFormat"] = "Yes"

# import indicator id look up table 
indCodeFormatDF = pd.read_csv("indicatorIDLookUptable.csv", names = ("Indmeta_text", "IndMetaID"))
dict_indCode = indCodeFormatDF.set_index("Indmeta_text")["IndMetaID"].to_dict()

# some codes are not in the nestle data 
# def check_CntryCodeLists(unCntryCodeDF, nestleCntryCodeDF):
#     uncode_list_to_add = list() 
#     nstl_unique_codes = nestleCntryCodeDF.["Country_Code"].unique()
#     criteria =lambda row: row["ISO-alpha2 Code"] not in nstl_unique_codes
#     not_in_nstl_df = unCntryCodeDF[unCntryCodeDF.apply(criteria, axis=1)]
    
#     return(not_in_nstl_df)

# add it to the nstl for country code formatting  

#some countries have differerent spelling in UN data 
# addToNstleCntryName = check_CntryCodeLists(unCntryCodeDF,nestleCntryCodeDF)
# nestleCntryCodeDF["Country_Code"] = nestleCntryCodeDF["Country_Code"].append(addToNstleCntryName["ISO-alpha2 Code"], ignore_index=True)
# nestleCntryCodeDF["World_Regions"] = nestleCntryCodeDF["World_Regions"].append(addToNstleCntryName["Region Name"], ignore_index=True)
# nestleCntryCodeDF["Countries"] = nestleCntryCodeDF["Countries"].append(addToNstleCntryName["Country or Area"], ignore_index=True)

#fill in variable about formatting Nestle data with NO to indicate UN
# nestleCntryCodeDF["NestleCodeFormat"].fillna("No")

def reqWorldBankData(reqDF): 
    # loop through each theme 
    uniqThemes = reqDF.Theme.unique()
    for theme in uniqThemes:
        print(theme)
        dfThemei = reqDF[(reqDF["Theme"]==theme) & (reqDF.HostingReference=="World Bank")].reset_index(drop=True)
        dfThememain =pd.DataFrame(columns=["FactID","Country", "Year", "Val", "Indmeta_text", "Download Date","Link","Reference","Theme_text","ThemeID" ])
        #   loop through each indicator list and  request
        for i in range(len(dfThemei.IndicatorCodeDS)):

            dlTime = datetime.datetime.now()  
            indDict = {dfThemei.IndicatorCodeDS[i]:dfThemei.IndicatorNameDS[i]}
            print(indDict)
            # retrieve data    
            df=wbdata.get_dataframe(indicators=indDict, country='all',  keep_levels=False)
            df.reset_index(level=df.index.names, inplace=True)
         
            # format data 
            if not df.empty:
                df.columns = ["Countries", "Year", "Val"]
                df["Indmeta_text"] = dfThemei.IndicatorName[i]
                df["Download Date"] = dlTime
                df["Link"] = dfThemei.Link[i]
                df["Reference"] = dfThemei.Reference[i]
                df["Theme_text"] = dfThemei.Theme[i]
                df["ThemeID"] = dfThemei.ThemeNumber[i]
                print(df.head(5)) 


                #Append each iteration to main df 
                dfThememain=dfThememain.append( df,ignore_index=True)

                dfThememain["World_Regions"] = dfThememain["Countries"].map(nestleCntryCodeDF.set_index("Countries")["World_Regions"].to_dict())
                dfThememain["Country_Code"] = dfThememain["Countries"].map(nestleCntryCodeDF.set_index("Countries")["Country_Code"].to_dict())
                dfThememain["IndMetaID"] = dfThememain["Indmeta_text"].map(dict_indCode)
                dfThememain["UNCountry_Code"] = dfThememain["Countries"].map(unCntryCodeDF.set_index("Country or Area")["ISO-alpha2 Code"].to_dict())
                dfThememain["UNRegion_Name"] = dfThememain["Countries"].map(unCntryCodeDF.set_index("Country or Area")["Region Name"].to_dict())

        # reorder columns 
        dfThememain = dfThememain.reindex(columns =["FactID", "Val","Year","Countries","Country_Code", "World_Regions", "IndmetaID","Indmeta_text","ThemeID","Theme_text","Link", "Reference", "Download Date", "UNCountry_Code", "UNRegion_Name"])

        #drop current year from results 
        dfThememain = dfThememain[dfThememain.Year!=str(now.year)]

        #remove where there's not a UN or Nestle Code 
        df_drop = dfThememain[dfThememain.Country_Code.isnull() & dfThememain.UNCountry_Code.isnull()]
        df_notNestle = dfThememain[dfThememain.Country_Code.isnull() & dfThememain.UNCountry_Code.notnull()]
        outputname3 = (os.getcwd()+'/WorldBankData/'+ 'QC_'+theme+'_discardedData.xlsx')            
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
        outputname2 = (os.getcwd()+'/WorldBankData/'+ str(dfThemei.ThemeNumber[0]) +' '+theme+'.csv')            
        outfile = open(outputname2, 'wb')
        dfThememain.to_csv(outfile,index = False, header=True)
        outfile.close()  
        return(dfThememain)


# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==3.2)])
# this is strange as 03/03/2020 - the following below will not owrk and breaks at  {'SP.DYN.TO65.FE.ZS': 'Survival to age 65, female (% of cohort)'}
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==1.1)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==3.1)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==3.5)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==4.6)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==5.3)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank")& (indReqDF.ThemeNumber==1.2)])



# import the demographics data that will not load and format
demographics= pd.read_csv("WorldBankData/1.1 Demographics.csv")
demographics["World_Regions"] = demographics["Countries"].map(nestleCntryCodeDF.set_index("Countries")["World_Regions"].to_dict())
demographics["Country_Code"] = demographics["Countries"].map(nestleCntryCodeDF.set_index("Countries")["Country_Code"].to_dict())
demographics["IndMetaID"] = demographics["Indmeta_text"].map(dict_indCode)
demographics["UNCountry_Code"] = demographics["Countries"].map(unCntryCodeDF.set_index("Country or Area")["ISO-alpha2 Code"].to_dict())
demographics["UNRegion_Name"] = demographics["Countries"].map(unCntryCodeDF.set_index("Country or Area")["Region Name"].to_dict())

# reorder columns 
demographics = demographics.reindex(columns =["FactID", "Val","Year","Countries","Country_Code", "World_Regions", "IndmetaID","Indmeta_text","ThemeID","Theme_text","Link", "Reference", "Download Date", "UNCountry_Code", "UNRegion_Name"])

#drop current year from results 
demographics = demographics[demographics.Year!=str(now.year)]

 #remove where there's not a UN or Nestle Code 
df_drop = demographics[demographics.Country_Code.isnull() & demographics.UNCountry_Code.isnull()]
df_notNestle = demographics[demographics.Country_Code.isnull() & demographics.UNCountry_Code.notnull()]
outputname3 = (os.getcwd()+'/WorldBankData/'+ 'QC_'+"demographics"+'_discardedData.xlsx')            
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
outputname2 = (os.getcwd()+'/WorldBankData/'+ '1.1 Demographics.csv')            
outfile = open(outputname2, 'wb')
demographics.to_csv(outfile,index = False, header=True)
outfile.close()  


# print(len(anmDF.Countries.unique()))
# print(len(anmDF.Country_Code.unique()))
# print(len(anmDF.Country_CodeUN.unique()))
# breakpoint()

# FactID	Country	Year	Val	Indmeta_text	Download Date	Link	Reference	Theme_text	ThemeID	Countries	World_Regions	Country_Code	IndMetaID	Country_CodeUN

# nstl_world_region_dict = nestleCntryCodeDF.set_index("Countries")["World_Regions"].to_dict()

# nstlCntryList = nstl_world_region_dict.keys()
# # print(nstlCntryList)

# anmCntryList = anmDF.Countries.unique()
# print(anmCntryList)

# for cntry in anmCntryList:
#     if cntry in nstlCntryList:
#         print(cntry)


# breakpoint
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==3.5)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==4.6)])
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==5.3)])

# for whatever reason I have to do this seperate 
# reqWorldBankData(indReqDF[(indReqDF.HostingReference=="World Bank") & (indReqDF.ThemeNumber==5.3)])


# df["IndmetaId"] = list()
# FactID	Val	Year	Countries	Coutry_code	World_Regions	Zones	IndmetaID	Indmeta_text	ThemeID	Theme_text	Link	Reference

# column_titles = ["Val","Year","Countries","Country_code", "World_Regions", "Zones","IndmetaID","Indmeta_text", "ThemeID", "Theme_text", "Link", "Reference", "Download Date"]
# dfThememain.reindex(columns=column_titles)


    


