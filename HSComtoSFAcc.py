# Import Salesforce Account from HubSpot Company.
# Data Clean and massage.

import pandas as pd
import re

df = pd.read_csv('all-companies-3-26-3.csv',encoding='utf-8-sig')#,encoding='utf8')
pd.DataFrame(df)
fnc = pd.read_excel('ComAccFieldNameChange.xlsx',encoding='utf8')
fnc = pd.DataFrame(fnc)
savecol = list(fnc['HS Field'])
df_dropped = df[savecol]

for i in range(0,len(fnc)):
    n1 = str(fnc['HS Field'][i])
    n2 = str(fnc['SF Field'][i])
    df_dropped = df_dropped.rename(columns={n1: n2})    
    
df_dropped["Account Protected Status"].replace({"No":"Open",
                                                "Yes - Top 35 Prospect Account":"Protected - Top Prospect"},
                                                 inplace=True)

df_dropped["Has Business in APAC"].replace({"Maybe":"",
                                            "Unknown":""},inplace=True)
df_dropped["Has Business in China"].replace({"Maybe":"",
                                             "Unknown":""},inplace=True)
df_dropped["Has Business in LATAM"].replace({"Maybe":"",
                                             "Unknown":""},inplace=True)

df_dropped["Number of Sites in APAC"].replace({"Unknown":""},inplace=True)
df_dropped["Number of Sites in China"].replace({"Unkown":""},inplace=True)

LATAMloca = list(df_dropped["LATAM Site Locations (by Country)"])

for i in range(0,len(LATAMloca)):
    if (type(LATAMloca[i])!=float):    
        LATAMloca[i] = LATAMloca[i].replace("None;","")
        LATAMloca[i] = LATAMloca[i].replace("Unknown;","")
        LATAMloca[i] = LATAMloca[i].replace("Yes - Unspecified;","")
        LATAMloca[i] = LATAMloca[i].replace(";None","")
        LATAMloca[i] = LATAMloca[i].replace(";Unknown","")
        LATAMloca[i] = LATAMloca[i].replace(";Yes - Unspecified","")
        LATAMloca[i] = LATAMloca[i].replace("None","")
        LATAMloca[i] = LATAMloca[i].replace("Unknown","")
        LATAMloca[i] = LATAMloca[i].replace("Yes - Unspecified","")
        
df_dropped["LATAM Site Locations (by Country)"] = LATAMloca

AsLiTag = list(df_dropped["Association/List Tag"])

for i in range(0,len(AsLiTag)):
    if (type(AsLiTag[i])!=float):
        AsLiTag[i] = AsLiTag[i].replace("Nickname Update w/o Cleaning;","")
        AsLiTag[i] = AsLiTag[i].replace(";Nickname Update w/o Cleaning","")
        AsLiTag[i] = AsLiTag[i].replace("Nickname Update w/o Cleaning","")
        
        AsLiTag[i] = AsLiTag[i].replace("Nickname Update;","")
        AsLiTag[i] = AsLiTag[i].replace(";Nickname Update","")
        AsLiTag[i] = AsLiTag[i].replace("Nickname Update","")

        AsLiTag[i] = AsLiTag[i].replace("Potential Banned Company;","")
        AsLiTag[i] = AsLiTag[i].replace(";Potential Banned Company","")
        AsLiTag[i] = AsLiTag[i].replace("Potential Banned Company","")
        
        AsLiTag[i] = AsLiTag[i].replace("Uniworld All Data;","")
        AsLiTag[i] = AsLiTag[i].replace(";Uniworld All Data","")
        AsLiTag[i] = AsLiTag[i].replace("Uniworld All Data","")
        
df_dropped["Association/List Tag"] = AsLiTag

AccProSta = list(df_dropped["Account Protected Status"])
Lifecycle = list(df_dropped["Lifecycle Stage"])
Typelist = list(df_dropped["Type"])

for i in range(0,len(df_dropped)):
    if (AccProSta[i] == "Yes - Opportunity Account"):
        if (Typelist[i] == "Channel Partner") or (Lifecycle[i] == "Evangelist"): 
            AccProSta[i] = "Protected - Active Opportunity Agent"
        else:
            AccProSta[i] = "Protected - Active Opportunity Account"
for i in range(0,len(df_dropped)):
    if (AccProSta[i] == "Yes - Customer Account"): 
        if (Typelist[i] == "Channel Partner") or (Lifecycle[i] == "Evangelist"): 
            AccProSta[i] = "Protected - Billing Agent"
        else:
            AccProSta[i] = "Protected - Billing Customer"
            
df_dropped["Account Protected Status"] = AccProSta

ComStatus = list(df_dropped["Company Status (Data Backup - HubSpot)"])

for i in range(0,len(df_dropped)):
    if (ComStatus[i] == "Action Needed") or (ComStatus[i] == "Prospecting") or (ComStatus[i] == "Pre-Qualify"): 
        if (Lifecycle[i] == "Subscriber"): 
            Lifecycle[i] = "Lead"
        elif (Lifecycle[i] == "Marketing Qualified Lead"):
            Lifecycle[i] = "Marketing Qualified Lead"
        elif (Lifecycle[i] == "Sales Qualified Lead"):
            Lifecycle[i] = "Sales Qualified Lead"     
for i in range(0,len(df_dropped)):
    if (Lifecycle[i] == "Opportunity"): 
        if (ComStatus[i] == "Active Opportunity"): 
            Lifecycle[i] = "Active Opportunity"
        elif (ComStatus[i] == "Lost Opportunity"):
            Lifecycle[i] = "Lost Opportunity"
for i in range(0,len(df_dropped)):
    if (Lifecycle[i] == "Customer"): 
        if (ComStatus[i] == "Billing Customer"): 
            Lifecycle[i] = "Billing Customer"
        elif (ComStatus[i] == "Lost Customer"):
            Lifecycle[i] = "Lost Customer"
            
df_dropped["Lifecycle Stage"] = Lifecycle
df_dropped["Lifecycle Stage"].replace({"Evangelist":"Billing Customer",
                                       "Other":"Disqualified"},inplace=True)

AccSource = list(df_dropped["Account Source"])
MarProBre = list(df_dropped["Marketing Prospecting Breakdown"])

for i in range(0,len(df_dropped)):
    if (AccSource[i] == "Marketing Prospecting"): 
        if (MarProBre[i] == "Online Prospecting"): 
            AccSource[i] = "Online Research"
        elif (MarProBre[i] == "Web Traffic"):
            AccSource[i] = "Web - Direct Traffic"
        elif (MarProBre[i] == "Weekly Intelligence Research"):
            AccSource[i] = "Online Research"
        elif (MarProBre[i] == "Outreach"):
            AccSource[i] = "Online Research"
        elif (MarProBre[i] == "Campaign"):
            AccSource[i] = "Email Campaign"     
        else:
            AccSource[i] = "Online Research" 
            
df_dropped["Account Source"] = AccSource
df_dropped["Account Source"].replace({"Sales Discovery":"Online Research",
                                       "Channel Partner/Agent":"Channel Sub Agent"},inplace=True)

ChanParType = list(df_dropped["Channel Partner Type"])

for i in range(0,len(df_dropped)):
    if (Typelist[i] == "Channel Partner") and (ChanParType[i] == "Channel Master Agent"):
        Typelist[i] = "Channel Master Agent"
    elif (Typelist[i] == "Channel Partner") and (ChanParType[i] != "Channel Master Agent"):
        Typelist[i] = "Channel Sub Agent"
    elif (Typelist[i] != "Channel Master Agent") and (Typelist[i] != "Channel Sub Agent"):
        Typelist[i] = "Direct Customer Account"
        
df_dropped["Type"] = Typelist

df_dropped["Disqualify Reasons"].replace({"No China/APC Business":"Irrelevant",
                                          "No Longer Exist":"No Longer Existed",
                                          "Invalid Input":"Invalid Entry",
                                          "Other Reason":"Other Resons (To Be Specified)",
                                          "Not Interested in CTA":"Irrelevant"},
                                            inplace=True)

df_new = df_dropped.drop(columns=["Channel Partner Type", "Marketing Prospecting Breakdown"])

user = pd.read_excel('User-updated.xlsx',encoding='utf-8-sig')
user = pd.DataFrame(user)
userid = user['Id']
username = user['HS User']
dfuser = df_new['Account Owner']
for i in range(0,len(user)):
    n1 = userid[i]
    n2 = username[i]
    df_new["Account Owner"].replace({n2:n1},inplace=True)
    
samplelist = df_new['China Site Locations (by Province)']
fulllist = []
for i in range(0,len(samplelist)):
    if type(samplelist[i])!=float: 
        word = samplelist[i].split("; ")
        fulllist = fulllist + word
finalcity = list(set(fulllist))
pd.DataFrame(finalcity).to_excel("allcity-in-HS.xlsx")

glob = pd.read_excel('ComAccGlobal.xlsx',encoding='utf-8-sig')
glob = pd.DataFrame(glob)

globold = glob['0 - Global Headquarter']
globnew1 = glob['Americas Headquarter']
globnew2 = glob['Global Headquarter']
localist = list(df_new["Global Headquarter"])       
df_new["Americas Headquarter"] = df_new["Global Headquarter"]

for i in range(0,len(glob)):
    n1 = globold[i]
    n2 = globnew1[i]
    n3 = globnew2[i]
    df_new["Global Headquarter"].replace({n1:n3},inplace=True)
    df_new["Americas Headquarter"].replace({n1:n2},inplace=True)
    
headq = pd.read_excel('ComAccChinaProvince.xlsx',encoding='utf-8-sig')
headq = pd.DataFrame(headq)

headold = headq['1 - China Site Locations']
headnew = headq['China Site Locations (by Province)']
headfile = list(df_new['China Site Locations (by Province)'])
head_dict = dict(zip(headold, headnew))

for i in range(0,len(df_new)):
    if type(headfile[i])!=float:   
        wordstr = headfile[i].split("; ")
        for key in head_dict:
            for j in range(0,len(wordstr)):
                if (len(key)==len(wordstr[j])):
                    wordstr[j] = wordstr[j].replace(key, head_dict[key])
        rep = list(set(wordstr))
        listToStr = ';'.join([str(elem) for elem in rep])
        headfile[i] = listToStr
        
for i in range(0,len(headfile)):
    if (type(headfile[i])!=float):        
        headfile[i] = headfile[i].replace("Wrong Value;","")
        headfile[i] = headfile[i].replace(";Wrong Value","")
        headfile[i] = headfile[i].replace("Wrong Value","")
        
df_new['China Site Locations (by Province)'] = headfile

df_provice = df_new[['China Site Locations (by Province)','HubSpot Company ID (HS Integration)']]
pd.DataFrame(df_provice).to_excel("provice-update-to-HS.xlsx")

df_new.to_csv('accfinish-final-version.csv', index=False, encoding='utf-8-sig')
