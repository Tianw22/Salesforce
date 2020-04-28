import pandas as pd

dfall = pd.read_excel('System/All Call and Note with Contact.xlsx',encoding='utf-8-sig')#,encoding='utf8')
dfall = pd.DataFrame(dfall)
obj = "CALL"

dfall_rename = dfall.rename(columns={'Engagement ID': 'HubSpot Activity ID',
                                     'Activity type': 'TYPE',
                                     'Create date': 'ACTIVITYDATE',
                                     'Activity assigned to': 'CREATEDBYID',
                                     'HubSpot Team': 'HubSpot Team (Excel)',
                                     'Call notes': 'DESCRIPTION',
                                     'Contact ID': 'WHOID',
                                     'Call outcome': 'CALLOUTCOME'}) 
                                     
dfall_rename['COMPLETEDDATTIME'] = list(dfall_rename['ACTIVITYDATE'])
dfall_rename['CREATE DATE'] = list(dfall_rename['ACTIVITYDATE'])
dfall_rename['Owner Name (Excel)'] = list(dfall_rename['CREATEDBYID'])

dfall_drop = dfall_rename.drop(columns=["Activity created by","Activity date","Call status","First Name","Last Name","Email","Note body"])

dfcall = dfall_drop[dfall_drop["TYPE"] == "Call"]

dfcall["CALLOUTCOME"].replace({"Busy":"No Answer",
                               "Wrong number":"Invalid Number",
                               "Left live message":"Left Voicemail",
                               "No answer":"No Answer",
                               "Left voicemail":"Left Voicemail"},
                               inplace=True)
                               
dfcall['TASKSUBTYPE'] = ["Call"]*len(dfcall) 
dfcall['SUBJECT'] = ["Call"]*len(dfcall) 
dfcall['RECORDTYPEID'] = ["xxxxxxxxxxxxxxx"]*len(dfcall) #Find Id from data loader export

user = pd.read_excel('System/User.xlsx',encoding='utf-8-sig')
user = pd.DataFrame(user)
userid = user['Id']
username = user['HS User']
for i in range(0,len(user)):
    n1 = userid[i]
    n2 = username[i]
    dfcall["CREATEDBYID"].replace({n2:n1},inplace=True)
    
dfcall['OWNERID'] = list(dfcall['CREATEDBYID'])

dfcon = dfcall[dfcall['Salesforce target object'] == 'Contact']
dfcon.to_excel("OutPut/%sconraw.xlsx"%obj,index = False)
len(dfcon)

dfld = dfcall[dfcall['Salesforce target object'] == 'Lead']
dfld.to_excel("OutPut/%sldraw.xlsx"%obj,index = False)
len(dfld)
