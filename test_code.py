from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np
from sklearn.cluster import KMeans


nRowsRead = None # specify 'None' if want to read whole file
df1 = pd.read_csv('C:/Users/Administrator/Desktop/2017_1.csv', delimiter=',', nrows = nRowsRead)

df1['DateTime'] = pd.to_datetime(df1['Transaction_Date'])

#Add month column
df1['Month'] = df1['DateTime'].dt.month




#step 3
step_3_dataset = df1.sort_values(['Transaction_Amount'], ascending=[0])
step_3_dataset=step_3_dataset.loc[step_3_dataset['Transaction_Amount']<10000]
step_3_dataset=step_3_dataset.loc[step_3_dataset['Transaction_Amount']>9000]


#step 4 
test_set=df1

a=df1.groupby(['Cardholder_Name','Month'])[['Transaction_Amount']].sum().reset_index()
step_4_dataset=a.loc[a['Transaction_Amount']>20000]

#step 1

c=df1.groupby(['Cardholder_Name'])[['Transaction_Amount']].count()
step_1_dataset=c.loc[c['Transaction_Amount']>300]

#step 2
d=df1.groupby(['Merchant_Name'])[['Transaction_Amount']].count()
step_2_dataset=d.loc[d['Transaction_Amount']>5000]





#Customer Level file
Customer_level_table=df1
#['Cardholder_Name'] #48763 lines

Customer_level_table.sort_values('Cardholder_Name', inplace = True) 
Customer_level_table=Customer_level_table.drop_duplicates(subset='Cardholder_Name', keep='first', inplace=False)
#1032 lines/customers

#Customer_level_table=Customer_level_table['Cardholder_Name']

#Mark customers as per step 1
step_1_dataset=step_1_dataset.drop(['Transaction_Amount'], axis=1)
step_1_dataset['Marker1']=1
left = pd.merge(Customer_level_table, step_1_dataset, on='Cardholder_Name',how='left')


#Mark customers as per step 2
step_2_dataset=step_2_dataset.drop(['Transaction_Amount'], axis=1)
step_2_dataset['Marker2']=1
left = pd.merge(left, step_2_dataset, on='Merchant_Name',how='left')

 
#Mark customers as per step 3
step_3_dataset=step_3_dataset.drop(['DateTime','Month','Phone','Transaction_Date','Transaction_Amount','Merchant_Category_Code Description','Merchant_Name','Merchant_State_Province','Department','Department_Contact'], axis=1)
step_3_dataset['Marker3']=1
left = pd.merge(left, step_3_dataset, on='Cardholder_Name',how='left')

#Mark customers as per step 4
#step_4_dataset=step_4_dataset.drop(['Month','Transaction_Amount'], axis=1)

step_4_dataset=step_4_dataset['Cardholder_Name']
step_4_dataset= step_4_dataset.values
step_4_dataset = pd.DataFrame(step_4_dataset)
step_4_dataset.columns=['Cardholder_Name']
step_4_dataset['Marker4']=1
left = pd.merge(left, step_4_dataset, on='Cardholder_Name',how='left')
left.fillna(0, inplace=True)

left['Total_marker']=left['Marker1']+left['Marker2']+left['Marker3']+left['Marker4']





left['Description']= np.where(left['Total_marker']==1, 'Potentially suspect account', '_')
left['Reason_for_flag']= np.where(left['Marker1']==1, 'Algorithm Step 1', '_')
left['Reason_for_flag']= np.where(left['Marker2']==1, 'Algorithm Step 2', left['Reason_for_flag'])
left['Reason_for_flag']= np.where(left['Marker3']==1, 'Algorithm Step 3', left['Reason_for_flag'])
left['Reason_for_flag']= np.where(left['Marker4']==1, 'Algorithm Step 4', left['Reason_for_flag'])


full_dataset=left
just_flagged_accounts=left.loc[left['Total_marker']==1]

#show datasets
pd.set_option('display.max_columns', 30);full_dataset;
pd.set_option('display.max_columns', 30);just_flagged_accounts;

