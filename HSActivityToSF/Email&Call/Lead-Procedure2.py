import pandas as pd
from datetime import datetime
import time

obj = input().upper() #email or call

dfld = pd.read_excel('OutPut/%sldraw.xlsx'%obj,encoding='utf-8-sig')#,encoding='utf8')
dfld = pd.DataFrame(dfld)

ld = pd.read_csv('System/lead-id-extract.csv')
ld = pd.DataFrame(ld)

ld = ld.rename(columns={"HUBSPOT_CONTACT_ID_HUBSPOT_INTEGRATION__C":"WHOID"})

ld = ld.dropna().reset_index(drop=True)

ld["WHOID"] = ld["WHOID"].astype(int)

ldidmap = ld.set_index("WHOID").ID
dfld['LEADID'] = dfld.WHOID.map(ldidmap)

dfld = dfld.drop(columns=["WHOID","Salesforce target object"])
dfldnew = dfld.rename(columns={"LEADID":"WHOID"})
dfldnew = dfldnew.dropna(subset=['WHOID']).reset_index().drop(columns = ['index'])

actdatelist = list(dfldnew['ACTIVITYDATE'].astype(str))
for i in range(0,len(actdatelist)):
    inDate = actdatelist[i]
    d = datetime.strptime(inDate,"%Y-%m-%d %H:%M:%S")
    actdatelist[i] = d.strftime("%m/%d/%Y")
    
dfldnew['ACTIVITYDATE'] = actdatelist

final = dfldnew[~dfldnew.OWNERID.str.contains("(Deactivated)")].reset_index().drop(columns = ['index'])

final.to_csv("OutPut/%s-lead-for-import.csv"%obj, index=False, encoding='utf-8-sig')
