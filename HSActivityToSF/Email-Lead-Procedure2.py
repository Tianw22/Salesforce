import pandas as pd

dfld = pd.read_excel('emailldraw.xlsx',encoding='utf-8-sig')#,encoding='utf8')
dfld = pd.DataFrame(dfld)

ld = pd.read_csv('lead-id-extract.csv')
ld = pd.DataFrame(ld)

ld = ld.rename(columns={"HUBSPOT_CONTACT_ID_HUBSPOT_INTEGRATION__C":"WHOID"})
ld = ld.dropna().reset_index(drop=True)
ld["WHOID"] = ld["WHOID"].astype(int)

ldidmap = ld.set_index("WHOID").ID
dfld['LEADID'] = dfld.WHOID.map(ldidmap) ### REPLACE HUBSPOT ID WITH SALESFORCE ID

dfld = dfld.drop(columns=["WHOID","Salesforce target object"])
dfldnew = dfld.rename(columns={"LEADID":"WHOID"})

actdatelist = list(dfldnew['ACTIVITYDATE'].astype(str))
from datetime import datetime
import time
for i in range(0,len(actdatelist)):
    inDate = actdatelist[i]
    d = datetime.strptime(inDate,"%Y-%m-%d %H:%M:%S")
    actdatelist[i] = d.strftime("%m/%d/%Y")
    
dfldnew['ACTIVITYDATE'] = actdatelist

dfldnew.to_csv("EMAIL-lead-for-import.csv", index=False, encoding='utf-8-sig')
