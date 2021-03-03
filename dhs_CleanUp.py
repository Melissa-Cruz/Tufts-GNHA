import time
import datetime
import requests 
import pandas as pd

		
# import requested dhs data downloaaded from website because API is still under development 
dhs = pd.read_csv("DHS//RawDHSData.csv")
dhs["id"] = dhs.index

# Print columns 
print(dhs.head())
# print(dhs.Year) 

#Convert survey into date, Please take the first year as the year variable(2017 in this example)
dhs["Year"] = " "
for i in range(len(dhs.Survey)):
    txt = str(dhs["Survey"][i]).split()[0]
    txt2 =txt.split("-",1)[0]
    # print(txt2 )
    dhs["Year"][i] = txt2
 


i
#Convert it into long format
dhs2 = dhs.melt(id_vars = ["Year", "Country", "Survey", "id"])  
print(dhs2)
# df = dhs2.unstack()
# print(df.head())
# print(dhs2.columns)
# for col in cols_list:
    # if col not in :



        


# dhst=pd.wide_to_long(dhs, i = ["id", "Year"], j = "Indicator")


#add country code  etc 

#add proper indicator name and other info from indrequeted


