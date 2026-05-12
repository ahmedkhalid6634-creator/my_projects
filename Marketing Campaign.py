import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#font
plt.rcParams['font.family'] = 'Trebuchet MS'
#display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#importing files
ml_df=pd.read_csv('mailchimp_q1_export.txt',sep='\t')
gg_df=pd.read_csv('google_ads_q1_raw.csv')
fb_df=pd.read_excel('facebook_marketing_q1_final.xlsx')
#renaming and matching columns
##facebook columns
fb_df=fb_df.rename(columns={
    "reporting_start":'Date',
    "ad_set_name":"Campaign Name",
    "spend_usd":"Costs",
    "link_clicks":"Clicks",
    "revenue_generated":"Revenue",
    "reach":"Views",# reach is counted by individual account
    'leads_captured':'Leads'
})
##google columns
gg_df=gg_df.rename(columns={
    "Campaign":"Campaign Name",
    "Impressions":"Views",
    "Total_Cost":"Costs"
})
##email columns
ml_df=ml_df.rename(columns={
    "Campaign_ID":"Campaign Name",
    "Opens":"Views", #impressions and opens is counted by the single open of the ad
    "Unique_Clicks":"Clicks",
    "Dispatch_Date":"Date",
})
#editing data
##email campaign
ml_df['Clicks']=ml_df['Clicks']*3
ml_df["Costs"]=np.array([49.4,50.6,50.1,49.9,49.6,50.4]) #100$ cost per subscription per month
##google campaign
gg_df["Revenue"]=gg_df['Conversions']*150 #150$ per conversion
##poping unmatched data
gg_conversions=gg_df.pop("Conversions")
fb_leads=fb_df.pop("Leads")
mail_SentEmails=ml_df.pop("Emails_Sent")
##adding platform column
gg_df["Platform"]=["Google"]*gg_df.shape[0]
fb_df["Platform"]=["FaceBook"]*fb_df.shape[0]
ml_df["Platform"]=["Email"]*ml_df.shape[0]
#analysis cost per lead
##facebook leads
fb_df["CPL"]=(fb_df["Costs"]/fb_leads).round(2) #cost per lead
##google conversions
gg_df["CPL"]=(gg_df["Costs"]/gg_conversions).round(2) #cost per conversion
##merging data
df_sum=pd.concat([gg_df,fb_df,ml_df],ignore_index=True,axis=0)
##standerizing dates
df_sum["Date"]=pd.to_datetime(df_sum["Date"],format='mixed')
##order
df_sum=df_sum.sort_values(by=['Date'],ascending=True,ignore_index=True)
#filling gaps
df_sum["CPL"]=df_sum["CPL"].fillna("N/A")
#analytic rows
##ROI
df_sum["ROI(%)"]=(((df_sum["Revenue"]-df_sum["Costs"])/df_sum["Costs"])*100).round(2) #return on investment
##CPC
df_sum["CPC"]=(df_sum["Costs"]/df_sum["Clicks"]).round(2) #cost per click
##RPC
df_sum["RPC"]=(df_sum["Revenue"]/df_sum["Clicks"]).round(2) #revenue per click
#reordering columns
df_sum=df_sum[["Date","Platform","Campaign Name","Views","Clicks","Costs","Revenue","ROI(%)","CPC","RPC","CPL"]]
#analysis
##avg ROI
###google
gg_roi=df_sum[df_sum["Platform"]=="Google"]["ROI(%)"].mean().round(2) #average ROI(%) for google
###emails
ml_roi=df_sum[df_sum["Platform"]=="Email"]["ROI(%)"].mean().round(2) #average ROI(%) for emails
###facebook
fb_roi=df_sum[df_sum["Platform"]=="FaceBook"]["ROI(%)"].mean().round(2) #average ROI(%) for facebook
##avg CPL for google and facebook
gg_cpl=df_sum[(df_sum["Platform"]=="Google")& (df_sum["CPL"] != np.inf)]["CPL"].mean().round(2) #average CPL for google
fb_cpl=df_sum[df_sum["Platform"]=="FaceBook"]["CPL"].mean().round(2) #average CPL for facebook
##total revenue and costs in each platform
###google
gg_rev=df_sum[df_sum["Platform"]=="Google"]["Revenue"].sum() #total revenue for google
gg_costs=df_sum[df_sum["Platform"]=="Google"]["Costs"].sum() #total costs for google
###facebook
fb_rev=df_sum[df_sum["Platform"]=="FaceBook"]["Revenue"].sum() #total revenue for facebook
fb_costs=df_sum[df_sum["Platform"]=="FaceBook"]["Costs"].sum() #total costs for facebook
###email
ml_rev=df_sum[df_sum["Platform"]=="Email"]["Revenue"].sum() #total revenue for emails
ml_costs=df_sum[df_sum["Platform"]=="Email"]["Costs"].sum() #total costs for emails
##average CPC and RPC for each platform
###google
gg_cpc=df_sum[df_sum["Platform"]=="Google"]["CPC"].mean().round(2) #average cpc for google
gg_rpc=df_sum[df_sum["Platform"]=="Google"]["RPC"].mean().round(2) #average rpc for google
###facebook
fb_cpc=df_sum[df_sum["Platform"]=="FaceBook"]["CPC"].mean().round(2) #average cpc for facebook
fb_rpc=df_sum[df_sum["Platform"]=="FaceBook"]["RPC"].mean().round(2) #average rpc for facebook
###email
ml_cpc=df_sum[df_sum["Platform"]=="Email"]["CPC"].mean().round(2) #average cpc for emails
ml_rpc=df_sum[df_sum["Platform"]=="Email"]["RPC"].mean().round(2) #average rpc for emails
#visualization
plt.style.use("bmh")
fig=plt.figure(figsize=(10,8))
##grouped-bars
datum1=df_sum.groupby("Platform")[["Costs","Revenue"]].sum()
x=np.arange(len(datum1.index))
width=0.35
axe1=plt.subplot2grid((3,3),(0,0),rowspan=1,colspan=3)
a=axe1.bar(x-width/2,datum1["Costs"],width=0.2,edgecolor="black",color="#1aa0d9")
b=axe1.bar(x+width/2,datum1["Revenue"],width=0.2,edgecolor="black",color="#e62542")
axe1.set_title("Budget&Revenue\nComparison",fontsize=14,fontweight="bold")
axe1.legend(["Budget","Revenue"], frameon=True,loc='best')
axe1.set_xticks(x)
axe1.set_xticklabels(datum1.index)
axe1.set_xlabel("Platforms",fontsize=12,fontweight="bold")
axe1.set_ylabel("Revenue/Budget",fontsize=12,fontweight="bold")
axe1.bar_label(a,fontsize=9)
axe1.bar_label(b,fontsize=9)
axe1.set_ylim(0,300000)
##views comparison
datum2=df_sum.groupby("Platform")["Views"].sum()
axe2 = plt.subplot2grid((3,3),(2,0),rowspan=1,colspan=1)
v=axe2.bar(datum2.index,datum2.values,edgecolor="black",color="#ed0e2c",width=0.7)
axe2.set_title("Views Comparison",fontsize=14,fontweight="bold")
axe2.set_xlabel("Platforms",fontsize=12,fontweight="bold")
axe2.set_ylabel("Views",fontsize=12,fontweight="bold")
axe2.bar_label(v,fontsize=9)
axe2.set_ylim(0,1000000)
##hirozontal CPL comparison
axe3=plt.subplot2grid((3,3),(2,1),rowspan=1,colspan=1)
z=axe3.barh(["FaceBook","Google"],np.array([fb_cpl,gg_cpl]),edgecolor="black",color="#06c267",height=0.4)
axe3.set_title("CPL Comparison",fontsize=14,fontweight="bold")
axe3.set_xlabel("CPL",fontsize=12,fontweight="bold")
axe3.set_ylabel("Platforms",fontsize=12,fontweight="bold")
axe3.bar_label(z,fontsize=9,rotation=270)
axe3.set_xlim(0,45)
##ROI Chart
axe4=plt.subplot2grid((3,3),(2,2),rowspan=1,colspan=1)
r=axe4.bar(["Emails","Facebook","Google"],np.array([ml_roi,fb_roi,gg_roi]),edgecolor="black",color="#e66419",width=0.4)
axe4.bar_label(r,fontsize=9)
axe4.set_title("ROI(%) Across Platforms",fontsize=14,fontweight="bold")
axe4.set_xlabel("Platforms",fontsize=12,fontweight="bold")
axe4.set_ylabel("ROI(%)",fontsize=12,fontweight="bold")
axe4.set_ylim(0,30000)
##monthly trend
datum3=df_sum.groupby("Date")[["Revenue","Costs"]].sum()
axe5=plt.subplot2grid((3,3),(1,0),rowspan=1,colspan=3)
axe5.plot(datum3.index,datum3["Revenue"],linestyle='-',color="#02c4cf",linewidth=2,marker='o',mec="#02c4cf",mfc="#EEEEEE",label="Revenue")
axe5.plot(datum3.index,datum3["Costs"],linestyle='-',color="#8626ed",linewidth=2,marker='o',mec="#8626ed",mfc="#EEEEEE",label="Costs")
axe5.legend(loc='best',frameon=True)
axe5.set_title("Last 3 Months Trend",fontsize=14,fontweight="bold")
axe5.set_xlabel("Date",fontsize=12,fontweight="bold")
axe5.set_ylabel("Revenue/Costs",fontsize=12,fontweight="bold")
axe5.fill_between(datum3.index, datum3["Revenue"], color="#8626ed", alpha=0.2)
axe5.fill_between(datum3.index,datum3["Costs"],datum3["Revenue"],color="#02c4cf",alpha=0.2)
plt.tight_layout()
#plt.show()
df_sum.to_excel("Marketing_Campaigns_cleaned.xlsx",index=False)
plt.savefig("Marketing Campaign Visuals.png",dpi=300,bbox_inches='tight',transparent=False)