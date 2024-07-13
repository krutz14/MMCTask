import pandas as pd
import matplotlib.pyplot as matplotlibpy
import seaborn as sb
import numpy as np

#claims_data = pd.read_csv('data.csv')
claims_data=pd.read_excel('Data - Case Study 1.xlsx',sheet_name='Data') #read data
claims_data_copy = claims_data.copy()
na_count = claims_data.isna().sum()
na_count = na_count[na_count > 0]
na_count.sort_values(inplace=True)
matplotlibpy.figure(figsize=(8, 6))
na_count.plot(kind='bar')
matplotlibpy.title('Count of Missing Values by Column')
matplotlibpy.xlabel('Columns')
matplotlibpy.ylabel('Number of Missing Values')
matplotlibpy.xticks(rotation=45)
matplotlibpy.show()



##can be made reusable later
claims_data=claims_data.convert_dtypes() #convert to best possible data type
claims_data['Claim Cost'] = claims_data['Claim Cost'].astype('str').str.replace(',', '').str.replace('-', '').astype(float)
claims_data['Claim Cost'].fillna(claims_data['Claim Cost'].mean()) #fillna

#claims_data['Status_Updated'] = claims_data['Status_Updated'].apply(lambda x:'Open' if str(x).strip()!= 'Open' or str(x).strip()!= 'Closed' else x.strip())
claims_data['Status_Updated'] = claims_data['Status_Updated'].apply(lambda x:'Open' if str(x).strip()=='0'  else x.strip())  #add only open or closed
claims_data['Litigation'] = claims_data['Litigation'].astype('category').apply(lambda x:str(x).upper()) #litigation value categorial and common case
#print(claims_data.info())
claims_data['Closed Date'].fillna(claims_data['Closed Date'].mean()) # add NA in dates where it's empty
#print(claims_data['Litigation'].unique())

sb.boxplot(x=claims_data['Sector/Industry'], y=claims_data['Claim Cost']) # the distribution of Claim Cost across different categories in the Sector/Industry



#-----------------------------------------------------------------------------------------
matplotlibpy.figure(figsize=(5, 3))
sb.countplot(x='Litigation', data=claims_data)
matplotlibpy.title('Count the claims by litigation status')  # count the claims by litigation status
matplotlibpy.xlabel('Litigation')
matplotlibpy.ylabel('Count')
matplotlibpy.show()
#-----------------------------------------------------------------------------------------#
# 

#-----------------------------------------------------------------------------------------
countdata=claims_data['Accident State'].value_counts().reset_index()
countdata.columns=['Accident State','count']
matplotlibpy.figure(figsize=(20, 18),dpi=80)
sb.barplot(y='Accident State',x='count', data=countdata)
matplotlibpy.title('Count the  Accident state max')  # count accident by status
matplotlibpy.xticks(rotation=45)
matplotlibpy.ylabel('Count')
matplotlibpy.show()
#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------
matplotlibpy.figure(figsize=(10, 6))
sb.scatterplot(x='Claim Cost', y='Litigation', data=claims_data)
matplotlibpy.title('Claim Cost vs. Litigation') #claim cost vs litigation
matplotlibpy.xlabel('Claim Cost')
matplotlibpy.ylabel('Litigation')
matplotlibpy.show()
#-----------------------------------------------------------------------------------------#

