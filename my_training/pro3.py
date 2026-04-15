import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib.ticker as ticker
#creating the indices
index=["Dec31"]
counting=True
while counting:
    for m in ["Jan", "Feb"]:
        for n in range(1, 32):
            daily = m + str(n)
            if daily in ["Feb29","Feb30","Feb31"]:
                counting=False
            else:
                index.append(daily)
#creating data-set
np.random.seed(21)
exp=pd.DataFrame(index=index)
exp["Date"]=pd.date_range(start="2025/12/31",end="2026/02/28",freq="D")
exp["Date"]=pd.to_datetime(exp["Date"]).dt.date
exp["Amount"]=None
exp["Payment_Method"]=np.random.choice(["Cash","Credit Card","Debit Card"],size=60)
exp["Category"]=np.random.choice(["Food","Transport","Entertainment","Bills","Health","Shopping"],size=60)
exp["Description"]=None
#other datasets
actions={
    "Food":["Groceries","Snacks","Cafeteria"],
    "Transport":["Uber","Metro","Taxi"],
    "Bills":["Taxes","College Tuitions","Internet"],
    "Health":["Flu Medications","Medical Visit","Dental Hygiene"],
    "Entertainment":["Movie ticket","Disney Land","Concert"],
    "Shopping":["Hair Products","Clothe","Tech Products"]
}

amounts={
    "Food":range(15,81),
    "Transport":range(5,41),
    "Entertainment":range(20,101),
    "Bills":range(50,301),
    "Health":range(40,151),
    "Shopping":range(30,201)
}
#fucntion to create the rest of the data set
def gen(action,amount,expense):
    dsc=[]
    price=[]
    for ex in expense:
        element=np.random.choice(action[ex])
        dsc.append(element)
        element=np.random.choice(amount[ex])
        price.append(element)
    return np.array(dsc),np.array(price)

exp["Description"],exp["Amount"]=gen(actions,amounts,exp["Category"].values)
print(exp)
interaction=input("Press enter to see the rest of the information")
time.sleep(1)
#total expenses
print(f"Your total expenses in both months is {exp['Amount'].sum()} dollars")
time.sleep(1.2)
#average spent a day
print(f"with an average amount of {exp['Amount'].mean():1.1f} dollars a day")
#most expensive transaction
time.sleep(1.2)
i=exp['Amount'].idxmax()
print(f"the most expensive transaction you did was on {exp['Date'][i]}, you paid {exp['Amount'][i]} dollars for {exp['Description'][i]}")
time.sleep(1.2)
#Category with the highest the spending rate
highest_cat=exp.groupby("Category")["Amount"].sum()
print(f"The highest category you have spent your money on is {highest_cat.idxmax()}")
time.sleep(1.2)
#category with most number of transactions
categories=exp["Category"].value_counts()
print(f"the category with most number of transactions was {categories.idxmax()}")
time.sleep(1.2)
#the standard deviation of your expenses
print(f"the standard deviation of your whole expenses in those two months is {exp['Amount'].std():1.1f}")
#setting subplots
fig,axe=plt.subplots(3,3,figsize=(24, 18),layout="constrained")
fig.suptitle("Important Graphs For Those 60 Days", fontsize=16)
#bar chart of spending by Category
data=exp.groupby("Category")["Amount"].sum()
x1=data.index
y1=data.values
colors=["#4248f5","#dece52","#d48139","#37db91","#32a1b8","#964ddb"]
axe[0,0].bar(x1,y1,color=colors,edgecolor="Black",width=0.7)
axe[0,0].set_title("The Expenses in each Category",fontweight="bold",size=8,loc="center")
axe[0,0].set_xlabel("Categories",fontsize=7,fontweight="bold",color="#526cde")
axe[0,0].set_ylabel("Amount Spent",fontsize=7,fontweight="bold",color="#7051ad")
axe[0,0].tick_params(axis="both",labelsize=6)
#spending per day for the last 60 days line-chart
#first 30 days
x21=index[0:30]
y21=exp["Amount"].values[0:30]
axe[0,1].plot(x21,y21,color="#cc122e",marker='o',mfc="white",mec="#cc122e",ms=5,linewidth=4,linestyle="solid")
axe[0,1].set_title("Daily Expenses of the First 30 days",fontweight="bold",size=8,loc="center")
axe[0,1].set_xlabel("Date",fontsize=7,fontweight="bold",color="#1272cc")
axe[0,1].set_ylabel("Daily Expenses",fontsize=7,fontweight="bold",color="#08c271")
axe[0,1].tick_params(axis="both",labelsize=4,rotation=90)
#last 30 days
x22=index[31:60]
y22=exp["Amount"].values[31:60]
axe[0,2].plot(x22,y22,color="#1272cc",marker='o',mfc="white",mec="#1272cc",ms=5,linewidth=4,linestyle="solid")
axe[0,2].set_title("Daily Expenses of the last 30 days",fontweight="bold",size=8,loc="center")
axe[0,2].set_xlabel("Date",fontsize=7,fontweight="bold",color="#1272cc")
axe[0,2].set_ylabel("Daily Expenses",fontsize=7,fontweight="bold",color="#cc1242")
axe[0,2].tick_params(axis="both",labelsize=4,rotation=90)
#Pie chart
methods=exp["Payment_Method"].value_counts()
axe[1,0].pie(methods.values,labels=methods.index,autopct="%1.1f%%",colors=["#820f07","#3f0561","#051a61"],shadow=True,explode=[0.15,0,0],textprops={"fontsize":8, "fontweight":"bold"})
axe[1,0].set_title("Daily Payment Methods",fontweight="bold",size=8,loc="center")
#comparison between the first and the last 30 days
time.sleep(1.2)
tf=y21.sum()
tl=y22.sum()
print(f"total of spending that happened in the first and the last 30 days was:")
print(f"              the first 30 days    |    last 30 days")
print(f"                     {tf}          |        {tl}      ")
#comparison graph
width=0.35
x3=x1
x=np.arange(len(x3))
fy3=exp[0:30].groupby("Category")["Amount"].sum() #use reindex and groupby instead of this shit
ly3=exp[31:60].groupby("Category")["Amount"].sum()
fy3=fy3.reindex(x3,fill_value=0)
ly3=ly3.reindex(x3,fill_value=0)
axe[1,1].bar(x - width/2,fy3.values,color="#05ab7f",edgecolor="black",width=width)
axe[1,1].bar(x + width/2,ly3.values,color="#f08935",edgecolor="black",width=width)
axe[1,1].set_xlabel("Categories",fontsize=7,fontweight="bold",color="#0784eb")
axe[1,1].set_ylabel("Expenses",fontsize=7,fontweight="bold",color="#4a31d6")
axe[1,1].set_title("Side-By-Side Comparison",fontweight="bold",size=8,loc="center")
axe[1,1].legend(["First 30 days","Last 30 days"])
axe[1,1].set_xticks(x,x3)
axe[1,1].tick_params(axis="both",labelsize=4)
#Budget analysis
time.sleep(1.2)
spent=np.array([tf,tl])
conditioned=np.where(spent>2000,True,False)
counter=0
for i , x_val in enumerate(conditioned):
    if x_val and i==0:
        counter+=1
        print(f"the first month have overspent the whole budget with a total spent of :{tf}")
        time.sleep(1.2)
        print(f"Your expenses in {exp[0:30].groupby('Category')['Amount'].sum().idxmax()} caused the exceeding in the budget")
        break
    elif x_val and i==1:
        counter+=1
        print(f"the second month have overspent the whole budget with a total spent of :{tl}")
        time.sleep(1.2)
        print(f"Your expenses in {exp[31:60].groupby('Category')['Amount'].sum().idxmax()} caused the exceeding in the budget")
        break
if counter==0:
    print("the budget of 2000 hasn't been exceeded in both months")
#graph comparison 2
p=np.arange(2)
axe[1,2].barh(p-0.20/2,spent,color="#a442f5",edgecolor="black",height=0.20,label="Expenses")
axe[1,2].barh(p+0.20/2,np.array([2000,2000]),color="#d10f32",edgecolor="black",height=0.20,label="Budget")
axe[1,2].set_yticks(p,["First month","Second month"])
axe[1,2].set_title("Budget/Expenses",fontsize=8,fontweight="bold")
axe[1,2].set_xlabel("Expenses",fontsize=7,fontweight="bold")
axe[1,2].set_ylabel("Month",fontsize=7,fontweight="bold")
axe[1,2].tick_params(axis="both",labelsize=4)
axe[1,2].legend()
#highesst expensive transactions
time.sleep(1.2)
sorts=exp.sort_values(by=["Amount"],ascending=[False]).head(5)
print("the highest 5 transactions that happened in those 60 days")
time.sleep(1.2)
print(sorts)
xlabel=[]
for d,v in zip(sorts.index,sorts["Description"]):
    xlabel.append(f"{d} #{v}")
axe[2,0].bar(range(5),sorts["Amount"],edgecolor="black",width=width,color="#fcb603")
axe[2,0].set_xticks(range(5),xlabel)
axe[2,0].set_title("Top 5 Transactions",fontweight="bold",size=8)
axe[2,0].set_xlabel("Transactions",fontsize=7,fontweight="bold",color="#2cde59")
axe[2,0].set_ylabel("Amounts",fontsize=7,fontweight="bold",color="#47de2c")
axe[2,0].tick_params(axis="both",labelsize=4)
#histogram
my_bins=sorted([0,15,80,5,40,20,100,50,300,40,150,30,200])
median=exp["Amount"].median()
n,bini,patches=axe[2,1].hist(exp["Amount"],bins=my_bins,edgecolor="black")
axe[2,1].axvline(median,color="red",label=f"Median:{median:1.1f}", linewidth=1.5,linestyle='--')
for i,patch in enumerate(patches):
    if my_bins[i]<median:
        patch.set_facecolor("orange")
    else:
        patch.set_facecolor("#47de2c")

axe[2,1].set_title("Transactions Distribution",fontweight="bold",size=8,loc="center")
axe[2,1].set_xlabel("Amounts",fontsize=7,fontweight="bold",color="#2cde59")
axe[2,1].set_ylabel("Frequency",fontsize=7,fontweight="bold",color="#47de2c")
axe[2,1].tick_params(axis="both",labelsize=4)
legend_elements = [
    Patch(facecolor='orange', label=f'Small (<${median:1.1f})'),
    Patch(facecolor='#47de2c', label=f'Large (≥${median:1.1f})'),
    plt.Line2D([0], [0], color='red', linestyle='--', label='Median')]
axe[2, 1].add_line(legend_elements[2])
axe[2,1].legend(handles=legend_elements, loc='upper right', fontsize=5)
#scatter plots
x4=exp.index
y4=exp["Amount"]
conditions=[exp["Category"]=="Bills",exp["Category"]=="Shopping",exp["Category"]=="Entertainment",exp["Category"]=="Transport",exp["Category"]=="Health",exp["Category"]=="Food"]
choices=["#42f5e6","#4293f5","#7723de","#a9de23","#d97e0f","#db217e"]
colors_category=np.select(conditions,choices,default="none")
sizes=exp["Amount"]/2
axe[2,2].scatter(x4,y4,color=colors_category,s=sizes,edgecolor="black",linewidth=1)
axe[2,2].set_title("Scatter Plot Analysis",fontweight="bold",size=8)
axe[2,2].set_xlabel("Date",fontsize=7,fontweight="bold",color="black")
axe[2,2].set_ylabel("Amount",fontsize=7,fontweight="bold",color="black")
axe[2,2].tick_params(axis="x",rotation=90)
axe[2,2].xaxis.set_major_locator(ticker.MultipleLocator(5))
legend_elements2 = [
    Patch(facecolor="#db217e", label="Food"),
    Patch(facecolor="#d97e0f", label="Health"),
    Patch(facecolor="#a9de23", label="Transport"),
    Patch(facecolor="#7723de", label="Entertainment"),
    Patch(facecolor="#4293f5", label="Shopping"),
    Patch(facecolor="#42f5e6", label="Bills")]
axe[2,2].legend(handles=legend_elements2)
#showing the graphs
plt.show()