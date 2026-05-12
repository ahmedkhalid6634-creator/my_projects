import pandas as pd
import matplotlib.pyplot as plt
#setting font
plt.rcParams['font.family']=['Consolas','Segoe UI Emoji']
#setting display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#importing the file
df = pd.read_csv(r'C:\Users\amrk3\Downloads\employee_records_raw.csv')
#standerizing formats
df['Full Name'] = df['Full Name'].str.lower()
df['Phone Number']=df['Phone Number'].str.replace(r'(\d{3})(\d{3})(\d{4})',r'\1-\2-\3',regex=True)
df['Employment Status']=df['Employment Status'].str.upper()
##filling the NANs
df['Department']=df['Department'].fillna('Unassigned')
df['Employment Status']=df['Employment Status'].fillna('UNKNOWN')
##standerizing departments
df['Department']=df['Department'].str.lower()
dept={
    'eng':"Engineering",
    'research':"Research",
    'unassigned':"Unassigned",
    'marketing':"Marketing",
    'hr':"HR",
    'sales':"Sales",
    'it':"IT",
    'engineering':"Engineering",
    'operations':"Operations"
}
df['Department']=df['Department'].map(dept)
##formating and sorting dates
df["Hire Date"]=pd.to_datetime(df["Hire Date"],format='mixed')
df=df.sort_values(by=['Hire Date'])
df['Hire Date'] = df['Hire Date'].dt.strftime('%d/%m/%Y')
##formating salary
df['Salary']=df['Salary'].str.replace(r'[$,]','',regex=True)
df['Salary']=df['Salary'].str.replace(r'[k]','000',regex=True)
df['Salary']=pd.to_numeric(df['Salary'],errors='coerce').astype('int64')
#cleaning data-set
cleaned=df.drop_duplicates(subset=["Full Name",'Email'],keep='last')
#visual report for the data-set

##intializing the canvas

plt.style.use('bmh')

fig=plt.figure(figsize=(16,10))

##bar chart

bar=plt.subplot2grid((2,3),(0,0),rowspan=1,colspan=1)

emp_status=cleaned['Employment Status'].value_counts(ascending=True)

axe=bar.bar(emp_status.index,emp_status.values,color='#f5c542',edgecolor='black')

bar.set_title('Employees\' Status',fontweight='bold',fontsize=14)

bar.set_xlabel('Employment Status',fontweight='bold',fontsize=10)

bar.set_ylabel('No_Employees',fontweight='bold',fontsize=10)

plt.ylim(0,60)

plt.bar_label(axe,fontsize=10)

##pie chart

group=cleaned.groupby('Department')['Salary'].sum().sort_values(ascending=False)

pie=plt.subplot2grid((2,3),(0,1),rowspan=1,colspan=2)

pie.pie(group.values,colors=['#2E86AB','#A23B72','#F18F01','#C73E1D','#6A994E','#BC4B51','#8B6F47','#5E548E'],shadow=True,explode=[0.3,0,0,0,0,0,0,0],autopct='%1.1f%%',

textprops={

'fontsize':10,

'fontweight':'bold',

},wedgeprops={

'linewidth':1,

'edgecolor':'black',

})

pie.legend(group.index,loc='upper right',frameon=True,edgecolor='black',fontsize=10,bbox_to_anchor=(1.7,0.6))

pie.set_title("Total Salary/Department",fontweight='bold')

##histogram

hist=plt.subplot2grid((2,3),(1,0),rowspan=1,colspan=1)

my_bins=[40000,60000,80000,100000,120000,140000,160000]

n,bins,axe2=hist.hist(cleaned["Salary"].values,bins=my_bins,color='#0e5796',alpha=0.7,edgecolor='black')

hist.set_xticks(my_bins)

hist.set_title('Salary Distribution',fontweight='bold',fontsize=14)

hist.set_xlabel('Salary Ranges',fontweight='bold',fontsize=10)

hist.set_ylabel('NO_Employees',fontweight='bold',fontsize=10)

plt.bar_label(axe2,fontsize=10,fontweight='bold')

plt.ylim(0,25)

##bar chart2

bar2=plt.subplot2grid((2,3),(1,1),rowspan=1,colspan=2)

title_count=cleaned['Job Title'].value_counts(ascending=True)

axe3=bar2.bar(title_count.index,title_count.values,color="#50168a",edgecolor='black')

plt.bar_label(axe3,fontsize=10,fontweight='bold')

bar2.set_title('Specialization Distribution',fontweight='bold',fontsize=14)

bar2.set_xlabel('Job Title',fontweight='bold',fontsize=12)
bar2.set_ylabel('NO_Employees',fontweight='bold',fontsize=12)
bar2.set_ylim(0,25)
plt.tight_layout()
plt.subplots_adjust(hspace=0.5, wspace=0.6)
#plt.show()
#plt.savefig('employee_records_visuals.png',dpi=300,bbox_inches='tight',transparent=False)
#cleaned.to_csv('employee_records_cleaned.csv',index=False)