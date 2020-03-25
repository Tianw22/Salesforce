# Import Salesforce Account from HubSpot Company.
# Data Clean and massage.

import pandas as pd
import re

df = pd.read_csv('all-companies.csv',encoding='utf-8-sig')#,encoding='utf8')
pd.DataFrame(df)
fnc = pd.read_excel('ComAccFieldNameChange.xlsx',encoding='utf8')
fnc = pd.DataFrame(fnc)
savecol = list(fnc['HS Field'])
df_dropped = df[savecol] # Only save the columns needed. 

# And rename them by the field name change table.
for i in range(0,len(fnc)):
    n1 = str(fnc['HS Field'][i])
    n2 = str(fnc['SF Field'][i])
    df_dropped = df_dropped.rename(columns={n1: n2})  
    
# Replace value in column
df_dropped["Account Protected Status"].replace({"No":"Open",
                                                "Yes - Top 35 Prospect Account":"Protected - Top Prospect"},
                                                 inplace=True)
df_dropped["Has Business in APAC"].replace({"Maybe":""},inplace=True)
for i in range(0,len(df_dropped)):
    if (df_dropped["Account Protected Status"][i] == "Yes - Opportunity Account"):
        if (df_dropped["Type"][i] == "Channel Partner") or (df_dropped["Lifecycle Stage"][i] == "Evangelist"): 
            df_dropped["Account Protected Status"][i] = "Protected - Active Opportunity Agent"
        else:
            df_dropped["Account Protected Status"][i] = "Protected - Active Opportunity Account"
for i in range(0,len(df_dropped)):
    if (df_dropped["Account Protected Status"][i] == "Yes - Customer Account"): 
        if (df_dropped["Type"][i] == "Channel Partner") or (df_dropped["Lifecycle Stage"][i] == "Evangelist"): 
            df_dropped["Account Protected Status"][i] = "Protected - Billing Agent"
        else:
            df_dropped["Account Protected Status"][i] = "Protected - Billing Customer"
for i in range(0,len(df_dropped)):
    if (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Action Needed") or (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Prospecting") or (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Pre-Qualify"): 
        if (df_dropped["Lifecycle Stage"][i] == "Subscriber"): 
            df_dropped["Lifecycle Stage"][i] = "Lead"
        elif (df_dropped["Lifecycle Stage"][i] == "Marketing Qualified Lead"):
            df_dropped["Lifecycle Stage"][i] = "Marketing Qualified Lead"
        elif (df_dropped["Lifecycle Stage"][i] == "Sales Qualified Lead"):
            df_dropped["Lifecycle Stage"][i] = "Sales Qualified Lead"                
for i in range(0,len(df_dropped)):
    if (df_dropped["Lifecycle Stage"][i] == "Opportunity"): 
        if (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Active Opportunity"): 
            df_dropped["Lifecycle Stage"][i] = "Active Opportunity"
        elif (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Lost Opportunity"):
            df_dropped["Lifecycle Stage"][i] = "Lost Opportunity"            
for i in range(0,len(df_dropped)):
    if (df_dropped["Lifecycle Stage"][i] == "Customer"): 
        if (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Billing Customer"): 
            df_dropped["Lifecycle Stage"][i] = "Billing Customer"
        elif (df_dropped["Company Status (Data Backup - HubSpot)"][i] == "Lost Customer"):
            df_dropped["Lifecycle Stage"][i] = "Lost Customer"
df_dropped["Lifecycle Stage"].replace({"Evangelist":"Billing Customer",
                                       "Other":"Disqualified"},inplace=True)            
df_dropped["Account Source"].replace({"Sales Discovery":"Online Research",
                                       "Channel Partner/Agent":"Channel Sub Agent"},inplace=True)            
for i in range(0,len(df_dropped)):
    if (df_dropped["Account Source"][i] == "Marketing Prospecting"): 
        if (df_dropped["Marketing Prospecting Breakdown"][i] == "Online Prospecting"): 
            df_dropped["Account Source"][i] = "Online Research"
        elif (df_dropped["Marketing Prospecting Breakdown"][i] == "Web Traffic"):
            df_dropped["Account Source"][i] = "Web - Direct Traffic"
        elif (df_dropped["Marketing Prospecting Breakdown"][i] == "Weekly Intelligence Research"):
            df_dropped["Account Source"][i] = "Online Research"
        elif (df_dropped["Marketing Prospecting Breakdown"][i] == "Outreach"):
            df_dropped["Account Source"][i] = "Online Research"
        elif (df_dropped["Marketing Prospecting Breakdown"][i] == "Campaign"):
            df_dropped["Account Source"][i] = "Email Campaign"     
        else:
            df_dropped["Account Source"][i] = "Online Research" 
for i in range(0,len(df_dropped)):
    if (df_dropped["Type"][i] == "Channel Partner"):
        if (df_dropped["Channel Partner Type"][i] == "Channel Master Agent"):
            df_dropped["Type"][i] = "Channel Master Agent"
        else:
            df_dropped["Type"][i] = "Channel Sub Agent"
    else:
        df_dropped["Type"][i] = "Direct Customer Account"            
df_dropped["Disqualify Reasons"].replace({"No China/APC Business":"Irrelevant",
                                          "No Longer Exist":"No Longer Existed",
                                          "Invalid Input":"Invalid Entry",
                                          "Other Reason":"Other Resons (To Be Specified)",
                                          "Not Interested in CTA":"Irrelevant"},
                                            inplace=True)            

# Drop the columns no longer needed.
df_new = df_dropped.drop(columns=["Channel Partner Type", "Marketing Prospecting Breakdown"])            
            
# Replace HubSpot username by Salesforce Id
user = pd.read_excel('User-updated.xlsx',encoding='utf-8-sig')
user = pd.DataFrame(user)
userid = user['Id']
username = user['HS User']
dfuser = df_new['Account Owner']
for i in range(0,len(user)):
    n1 = userid[i]
    n2 = username[i]
    df_new["Account Owner"].replace({n2:n1},inplace=True)
    
# Massage location data.
glob = pd.read_excel('ComAccGlobal.xlsx',encoding='utf-8-sig')
glob = pd.DataFrame(glob)
headq = pd.read_excel('ComAccHeadquater.xlsx',encoding='utf-8-sig')
headq = pd.DataFrame(headq)
df_new["Americas Headquarter"] = df_new["Global Headquarter"] # Generate a new column            
globold = glob['0 - Global Headquarter']
globnew1 = glob['Americas Headquarter']
globnew2 = glob['Global Headquarter']
for i in range(0,len(glob)):
    n1 = globold[i]
    n2 = globnew1[i]
    n3 = globnew2[i]
    df_new["Global Headquarter"].replace({n1:n3},inplace=True) # Replace value
    df_new["Americas Headquarter"].replace({n1:n2},inplace=True)    
headold = headq['1 - China Site Locations']
headnew = headq['China Site Locations (by City)TBD']
headfile = df_new['China Site Locations (by City)TBD']
head_dict = dict(zip(headold, headnew))
for i in range(0,len(df_new)):
    if type(df_new['China Site Locations (by City)TBD'][i])!=float:
        word = df_new['China Site Locations (by City)TBD'][i].split("; ")
        rep = [head_dict[x] if x in head_dict else x for x in word]
        listToStr = ';'.join([str(elem) for elem in rep])  
        df_new['China Site Locations (by City)TBD'][i] = listToStr
        
df_new.to_csv('SFimport.csv', index=False, encoding='utf-8-sig')
