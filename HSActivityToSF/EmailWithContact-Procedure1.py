import pandas as pd

dfall = pd.read_excel('hubspot-crm-exports-all-emails-with-contact.xlsx',encoding='utf-8-sig')
dfall = pd.DataFrame(dfall)

dfall_rename = dfall.rename(columns={'Engagement ID': 'HubSpot Activity ID',
                                     'Activity type': 'TYPE',
                                     'Email subject': 'SUBJECT',
                                     'Create date': 'ACTIVITYDATE',
                                     'Activity assigned to': 'CREATEDBYID',
                                     'HubSpot Team': 'HubSpot Team (Excel)',
                                     'Email body': 'DESCRIPTION',
                                     'Contact ID': 'WHOID'}) 
                                     
dfall_rename['COMPLETEDDATTIME'] = list(dfall_rename['ACTIVITYDATE'])
dfall_rename['CREATE DATE'] = list(dfall_rename['ACTIVITYDATE'])
dfall_rename['Owner Name (Excel)'] = list(dfall_rename['CREATEDBYID'])

dfall_drop = dfall_rename.drop(columns=["Activity created by","Activity date","Email send status","First Name","Last Name","Email"])

dfall_drop["TYPE"].replace({"Email sent to contact":"Email",
                            "Email reply from contact":"Replied Email"},
                            inplace=True)
                        
dfall_drop['TASKSUBTYPE'] = ["Email"]*len(dfall_drop) 
dfall_drop['STATUS'] = ["Completed"]*len(dfall_drop) 
dfall_drop['RECORDTYPEID'] = ["xxxxxxxxxxxxxxx"]*len(dfall_drop) #Find it in Salesforce data loader export

user = pd.read_excel('User.xlsx',encoding='utf-8-sig')
user = pd.DataFrame(user)
userid = user['Id']
username = user['HS User']
for i in range(0,len(user)):
    n1 = userid[i]
    n2 = username[i]
    dfall_drop["CREATEDBYID"].replace({n2:n1},inplace=True)

dfall_drop['OWNERID'] = list(dfall_drop['CREATEDBYID'])

dfcon = dfall_drop[dfall_drop['Salesforce target object'] == 'Contact']
dfcon.to_excel("emailconraw.xlsx",index = False)
len(dfcon)

dfld = dfall_drop[dfall_drop['Salesforce target object'] == 'Lead']
dfld.to_excel("emailldraw.xlsx",index = False)
len(dfld)
