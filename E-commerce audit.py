import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.pyplot import tight_layout
plt.rcParams['font.family'] = ['Trebuchet MS','Segoe UI Emoji']
#setting displaying options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#importing the file
path=os.path.abspath('tech_store_sales_raw.csv')
df=pd.read_csv(path)
#cleaning the data
#clean duplicates
df.drop_duplicates('order_id',inplace=True,ignore_index=True)
#handeling missing emails
df['customer_email']=df['customer_email'].replace(np.nan,"Not Provided")
#handeling typos in payment_status
df["payment_status"]=df["payment_status"].replace('payed','paid')
#handeling quantities less than 0
df["quantity"]=df["quantity"].abs()
#removing rows with quantities equal to zero
remove=df[df["quantity"]==0]
df=df.drop(remove.index).reset_index(drop=True)
#handeling typos
df['product_name']=df['product_name'].replace({
    "Laptp":"Laptop",
    "Headphnes":"Headphones",
    "i Phone":"iPhone"
})
#handeling zero prices
prices = {'Laptop': 899, 'iPhone': 799, 'iPad': 499, 'Headphones': 199,
          'Keyboard': 79, 'Mouse': 29, 'Monitor': 299, 'Webcam': 89,
          'USB Cable': 15, 'Charger': 25}
df['price'] = df['product_name'].map(prices)
#standerizing date formats
df['date']=df['date'].apply(pd.to_datetime)
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
#analysis
##total revenue
df["revenue"]=df['price']*df['quantity']
##top products
products=df.groupby("product_name")['revenue'].sum().sort_values(ascending=False)
##by category revenue
by_categories=df.groupby('category')['revenue'].sum().sort_values(ascending=False)
##monthly trends
trends=df.groupby(df['date'].dt.to_period('M'))['revenue']
#Visualizations
plt.style.use('bmh')
fig= plt.figure(figsize=(10,8))
#bar
axe1=plt.subplot2grid((2,2),(0,0),rowspan=1,colspan=2)
axe1.bar(products.index,products.values,color='#4287f5',edgecolor='black',width=0.7)
axe1.set_title('Revenue💰/Products💻')
axe1.set_ylabel('Revenue($)')
axe1.set_xlabel('Products')
#plot
axe2=plt.subplot2grid((2,2),(1,0),rowspan=1,colspan=1)
axe2.plot(["January","February","March","April","May","June"],trends.sum().values,linestyle='--',marker='o',color='#5142f5',mec='#5142f5',mfc='#EEEEEE')
axe2.fill_between(["January","February","March","April","May","June"],trends.sum().values,0,color='#5142f5',alpha=0.2)
axe2.set_title("Revenue Of The Last 6 Months📉💸")
axe2.set_ylabel('Revenue($)')
axe2.set_xlabel('Months')
#pie
axe3=plt.subplot2grid((2,2),(1,1),rowspan=1,colspan=1)
wedges,text,per=axe3.pie(x=by_categories.values,explode=[0.2,0,0,0],shadow=True,autopct='%1.1f%%',radius=0.9,textprops={
    'fontsize':11},wedgeprops={
    'width':0.7,
    'edgecolor':'black',
    'linewidth':1
})
axe3.legend(wedges,by_categories.index,loc='upper right',frameon=True,edgecolor='black',fontsize=10,bbox_to_anchor=(1.5,1))
axe3.set_title('Sales by Category🍩')
tight_layout()
#plt.show()
#plt.savefig('E-commerce Visuals.png',dpi=300,bbox_inches='tight',transparent=False)
#df.to_csv('tech_store_sales_cleaned.csv',index=False)
print(df["revenue"].sum())