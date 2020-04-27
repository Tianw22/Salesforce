import pandas as pd
from datetime import datetime
import time

dfcon = pd.read_excel('emailconraw.xlsx',encoding='utf-8-sig')#,encoding='utf8')
dfcon = pd.DataFrame(dfcon)

con = pd.read_csv('con-id-4-26-extract.csv')
con = pd.DataFrame(con)
con.columns

con = con.rename(columns={"HUBSPOT_CONTACT_ID_HUBSPOT_INTEGRATION__C":"WHOID"})
con.columns

con = con.dropna().reset_index(drop=True)

con["WHOID"] = con["WHOID"].astype(int)

conidmap = con.set_index("WHOID").ID
dfcon['CONTACTID'] = dfcon.WHOID.map(conidmap)

dfcon = dfcon.drop(columns=["WHOID","Salesforce target object"])
dfconnew = dfcon.rename(columns={"CONTACTID":"WHOID"})

actdatelist = list(dfconnew['ACTIVITYDATE'].astype(str))
for i in range(0,len(actdatelist)):
    inDate = actdatelist[i]
    d = datetime.strptime(inDate,"%Y-%m-%d %H:%M:%S")
    actdatelist[i] = d.strftime("%m/%d/%Y")
    
dfconnew['ACTIVITYDATE'] = actdatelist

dfconidmap = dfconnew[["HubSpot Activity ID","WHOID"]]
dfconidmap.to_excel("ContactIdActIdMap.xlsx",index = False)

dfcondrop = dfconnew.drop(columns=["WHOID"])

dfconnew2 = dfcondrop.drop_duplicates(subset=['HubSpot Activity ID'], keep=False).reset_index().drop(columns = ['index'])
final = dfconnew2[~dfconnew2.OWNERID.str.contains("(Deactivated)")].reset_index().drop(columns = ['index'])

final.to_csv("EMAIL-contact-NoConID-for-import.csv", index=False, encoding='utf-8-sig')
