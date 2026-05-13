import pandas as pd
import numpy as np
#display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
#employee and products data bases
data_emp=np.array(["Alice", "Bob", "Charlie", "Diana", "Eve"])
data_product=np.array(["Laptop", "Phone", "Tablet", "Headphone", "Charger"])
#setting the seed
np.random.seed(1)
#the prices data structure
pro_prices={
    "Laptop":(800,1200),
    "Phone":(400,800),
    "Tablet":(300,600),
    "Headphone":(50,150),
    "Charger":(10,30),
}
#pricing products
def get_price(product):
    low , high = pro_prices[product]
    return np.random.randint(low, high + 1)
#creating the data base
sale_df=pd.DataFrame({"Employee":np.random.choice(data_emp, size=30),
                 "Product":np.random.choice(data_product, size=30),
                 },index=range(1,31))
sale_df["Price"]=sale_df["Product"].apply(get_price)
sale_df["Quantity"]=np.random.randint(low=1,high=6, size=30)
sale_df["Revenue"]=sale_df["Price"]*sale_df["Quantity"]
#creating sales column
conds=[sale_df["Revenue"]<200,(sale_df["Revenue"]>=200)&(sale_df["Revenue"]<=800),sale_df["Revenue"]>800]
chois=[1,2,6]
sale_df["Sale Category"]=np.select(conds,chois)
sale_df["Sale Category"]=sale_df["Sale Category"].replace({1:"Small",
                                                 2:"Medium",
                                                 6:"Large"})
sale_df["Date"]=pd.date_range(start="01-01-2026",end="30-01-2026",freq="D")
#day column
sale_df["Day"]=sale_df["Date"].dt.day_name()
#week column
week_data=[]
count=1
for d in sale_df["Day"]:
    week_data.append(f"Week {count}")
    if d == "Wednesday":
        count+=1
    else:
        pass
sale_df["Week"]=week_data
#1st 10 rows
i=input("press enter")
print(sale_df.head(10))
#DataFrame's shape
ii=input("")
r,c=sale_df.shape
print(f"Number of Rows={r}\nNumber of Columns={c}")
#column names and their dtypes
iii=input("")
columns=list(sale_df.columns)
for col in columns:
    d=sale_df[col].dtypes
    count=sale_df[col].count()
    print(f"Column {col}: count of {count} , data type of \"{d}\"")
#statistics
iv=input("")
stats=sale_df.describe()
index=stats.index
for cm in columns:
    if cm in ["Employee","Product","Date","Week","Day","Sale Category"]:
        continue
    print(f"Column \"{cm}\"")
    for i in index:
        if i == "count":
            continue
        print(f"has a {i} value of {stats.loc[i,cm]}")
#employees' data stats
v=input("press enter for evaluation of each employee")
groups0=sale_df.groupby("Employee")
em_i=list(data_emp)
TRevenue=groups0["Revenue"].sum()
AVRevenue=groups0["Revenue"].mean()
num_sells=groups0["Quantity"].sum()
for em in em_i:
    print(f"Employee {em} : {num_sells.loc[em]} sells, average revenue: {AVRevenue.loc[em]},total revenue: {TRevenue.loc[em]}")
#product stats
vi=input("press enter for product evaluation\n")
groups1=sale_df.groupby("Product")
TSold=groups1["Quantity"].sum()
TRevenue=groups1["Revenue"].sum()
AVRPrice=groups1["Price"].mean()
best=TSold.max()
highest=TRevenue.max()
best_pro=""
highest_pro=""
pro_i=list(data_product)
for pro in pro_i:
    print(f"Product {pro} : total quatity sold {TSold.loc[pro]}, average revenue: {AVRPrice.loc[pro]} , total revenue: {TRevenue.loc[pro]}")
    if TRevenue.loc[pro] == highest:
        highest_pro=pro
    if TSold.loc[pro] == best:
        best_pro=pro
print(f"{best_pro}s are the best selling product!\n{highest_pro}s are the highest revenue-generating product :D\n")
#data-cleaning function
def cleaned_df(ver):
    row,column=(0,0)
    cleaned=0
    if ver=="r":
        cleaned=sale_df[(sale_df["Revenue"] >= 1000)]
        print("this is the cleaned revenue version\n")
        print(cleaned.head(3))
        row,column=cleaned.shape
        print(f"\nrows={row},columns={column}\n")
    elif ver=="p":
        cleaned = sale_df[sale_df["Product"] == "Laptop"]
        print("this is the cleaned product version\n")
        print(cleaned.head(3))
        row,column = cleaned.shape
        print(f"\nrows={row} columns={column}\n")
    elif ver=="e":
        cleaned = sale_df[(sale_df["Employee"] == "Alice")]
        print(f"this is the cleaned employee version\n")
        print(cleaned.head(3))
        row, column = cleaned.shape
        print(f"\nrows={row} columns={column}\n")
    elif ver=="q":
        cleaned = sale_df[sale_df["Quantity"] >= 3]
        print(f"this is the cleaned quantity version\n")
        print(cleaned.head(3))
        row, column = cleaned.shape
        print(f"\nrows={row} columns={column}\n")
    else:
        print("Invalid Input!")
choosing=True
press=input("press enter to continue")
while choosing:
    q1 = input("choose the version you prefer\n"
               "\"R\":for cleaned revenue data frame\n"
               "\"P\":for cleaned product data frame\n"
               "\"E\":for cleaned employee data frame\n"
               "\"Q\":for cleaned quantity data frame\n").lower()
    cleaned_df(q1)
    q2=input("if you want to continue press \"Y\"\nif not then press \"N\"\n")
    if q2.lower()=="y":
        choosing=True
    else:
        choosing=False
#number of each category
s=0
m=0
l=0
for sale in sale_df["Sale Category"]:
    if sale=="Small":
        s+=1
    elif sale=="Medium":
        m+=1
    else:
        l+=1
vii=input("press enter for the numbers of each category\n")

print(f"the \"Sale Category\" column has {s} Smalls , {m} Mediums , {l} Larges\n"
      f"NOTE:\nthe smalls are revenue less than 200,\n"
      f"the mediums are revenue between 200 and 800\n"
      f"and the larges are revenue beyond 800\n")
#Top performers
performers=sale_df.groupby("Employee")["Revenue"].sum()
iix=input("those are the best three performers this month:\n")
print(f"{performers.sort_values(ascending=False).head(3)}\n")
#day to week analysis
processed=sale_df.drop(columns=["Employee","Date","Product","Revenue","Sale Category","Price"])
by_week=processed.groupby("Week")["Quantity"].max()
weekly_revenue=sale_df.groupby("Week")["Revenue"].sum()
#SalesByDay
ix=input("")
for m in by_week:
    p=processed.set_index("Week")
    for q,i,w in zip(p["Quantity"],p["Day"],p.index):
        if q==m:
            print(f"{i} has the highest sales of {q} in {w}\n ")
        else:
            continue
#each week total revenue
x=input("")
print(f"In this 30 days those are the total revenue of each week :\n")
print(weekly_revenue)
#employees' production matrix
xi=input("pivot table:")
prod_mat=pd.pivot_table(sale_df,
                        values="Revenue",
                        index="Employee",
                        columns="Product",
                        aggfunc="sum",
                        fill_value=0)
print(f"production matrix :\n{prod_mat}")
