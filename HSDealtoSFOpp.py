import pandas as pd

df = pd.read_csv('hs-sf-export.csv',encoding='utf-8-sig')
df = pd.DataFrame(df)
fnc = pd.read_excel('DealOppFieldNameChange.xlsx',encoding='utf-8-sig')
fnc = pd.DataFrame(fnc)

savecol = list(fnc['HS Field'])
df_dropped = df[savecol]
for i in range(0,len(fnc)):
    n1 = str(fnc['HS Field'][i])
    n2 = str(fnc['SF Field'][i])
    df_dropped = df_dropped.rename(columns={n1: n2})  
    
lostr = list(df_dropped["Closed Lost Reason"])
wonr = list(df_dropped["Closed Won Reason"])
lostd = list(df_dropped["Lost Reason Dropdown"])
wond = list(df_dropped["Won Reason Dropdown"])
for i in range(0,len(df_dropped)):
    if (type(lostr[i])==float):
        lostr[i] = ""
    if (type(lostd[i])==float):
        lostd[i] = ""
    if (type(wonr[i])==float):
        wonr[i] = ""
    if (type(wond[i])==float):
        wond[i] = ""
        
reason = [i + j for i, j in zip(lostr, wonr)] 
dropdown = [i + j for i, j in zip(lostd, wond)] 

df_dropped["Closed Reason Detail"] = reason
df_dropped["Closed Reason Dropdown"] = dropdown

df_new = df_dropped.drop(columns=["Closed Lost Reason", "Closed Won Reason","Lost Reason Dropdown","Won Reason Dropdown"])

pmreview = list(df_new["PM Reviewed (System)"])
for i in range(0,len(pmreview)):
    if (type(pmreview[i]) != float) and (pmreview[i] == "PM Reviewed - Yes"):
        pmreview[i] = "True"
    elif (type(pmreview[i]) == float):
        pmreview[i] = "False"

df_new["PM Reviewed (System)"] = pmreview

df_new["Closing Team"].replace({"Strategic Account - CN":"Strategic Account Team",
                                "Strategic Account - US Enterprise":"Strategic Account Team"},
                                inplace=True)
                                
df_new["Stage"].replace({"20%- Discovery": "Discovery", 
                             "40%- Requirement Understood/Proposal Generated": "Proposal Sent to Customer/Negotiation", 
                             "50%- Budget Approved/Solution Agreed On/Time Frame<90 days": "Budget Approved/Proposal Agreed",
                             "70%- Commercial Term and Vehicle(MSA/SOF) Agreed": "Commercial Term and Vehicle (MSA/SOF) Agreed",
                             "80%- Order Form Sent/Waiting for Signature": "Order Form Generated/Sent to Customer",
                             "Closed Won - Order Form Signed":"Closed Won",
                             "Closed Lost/Cancelled":"Closed Lost"},
                             inplace=True)
                             
df_new["Closed Reason Dropdown"].replace({"Pricing Uncompetitive":"Price",
                                              "Internal Turnover too Slow":"Turnover",
                                              "Lack of Resource/Product":"Resouce/Product/Solution",
                                              "Customer Budget Issue":"Customer Cancelled",
                                              "Demand Change/Cancelled":"Customer Cancelled",
                                              "Customer/Partner No Response":"Customer Cancelled",
                                              "Bad Timing":"Timing",
                                              "Other (Please indicate)":"Other (Please specify)",
                                              "Authority":"Reputation",
                                              "Competition":"Resouce/Product/Solution",
                                              "Contract":"Resouce/Product/Solution",
                                              "Need":"Resouce/Product/Solution",
                                              "Network":"Resouce/Product/Solution",
                                              "Pricing":"Price",
                                              "Product":"Resouce/Product/Solution",
                                              "Promotion":"Price",
                                              "Referral":"Relationship",
                                              "Service":"Resouce/Product/Solution",
                                              "Other":"Other (Please specify)"},
                                              inplace=True)
                                              
df_new["Opportunity Source Detail"].replace({"Direct Sales":"Cold Call/Email",
                                             "Email Marketing":"SDR Outreach",
                                             "Market Intelligence":"Other"},
                                             inplace=True)
                                             
df_new["China Centric Channel Opportunity (Y/N)"].replace({"China Centric":"Yes",
                                                               "Non-China Region":"No"},
                                                               inplace=True)
                                                               
df_new["CTG统谈分签协同销售"].replace({"FALSE":""},inplace=True)

user = pd.read_excel('User-updated.xlsx',encoding='utf-8-sig')
user = pd.DataFrame(user)
userid = user['Id']
username = user['HS User']

for i in range(0,len(user)):
    n1 = userid[i]
    n2 = username[i]
    df_new["Opportunity Owner"].replace({n2:n1},inplace=True)
    df_new["Channel Manager"].replace({n2:n1},inplace=True)
    df_new["Closing Manager"].replace({n2:n1},inplace=True)
    
account = pd.read_csv('acc-hsid-sfid-extract.csv',encoding= 'unicode_escape')
account = pd.DataFrame(account)

accid = account['ID']
accname = account['NAME']
acchsid = account['HUBSPOT_COMPANY_ID__C']
for i in range(0,len(account)):
    n1 = accid[i]
    n2 = accname[i]
    df_new["Master Agent"].replace({n2:n1},inplace=True)
    df_new["Sub Agent"].replace({n2:n1},inplace=True)
    
df_new["Master Agent"].replace({"None":""},inplace=True)

hsidlist = list(df_new["HubSpot Company ID (HS Integration)"])
hsiddict = dict(zip(acchsid, accid))
for i in range(0,len(df_new)):
    if type(hsidlist[i])!=float:   
        for key in hsiddict:
            hsidlist[i] = hsidlist[i].replace(str(key), hsiddict[key])
            
df_new["Account Name"] = hsidlist

df_final = df_new.drop(columns=["HubSpot Company ID (HS Integration)"]) 
df_final.to_csv('dealtoopp.csv',encoding='utf-8-sig', index=False)
