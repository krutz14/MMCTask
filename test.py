import pandas as pd
from scipy.stats import ttest_ind
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as matplotlibpy
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from scipy.stats import chi2_contingency

claims_data=pd.read_excel('Data - Case Study 1.xlsx',sheet_name='Data') #read data

# Check for missing values
claims_data['Claim Duration'] = str((claims_data['Closed Date'] - claims_data['Loss Date']).dt.days)
#claims_data.drop(columns=['Date of Birth','Report Date','Closed Date','Loss Date'],inplace=True)

# Convert categorical columns to categorical data type
cat_cols = ['Loss Type', 'Status_Updated', 'Cause Description', 'Occupation', 'Carrier', 'Sector/Industry']

status_mapping = {'Indemnity': 2, 'Medical Only': 1, 'Notice Only': 0}
# Map the non-ordinal string column to numerical values
claims_data['Status_encoded_Losstype'] = claims_data['Loss Type'].map(status_mapping)

status_mapping = {'Industrials': 1, 'Health Care': 2, 'Materials': 3,'Consumer Disc':4,'Consumer Staples':5}
# Map the non-ordinal string column to numerical values
claims_data['Sector/Industry_Encode'] = claims_data['Sector/Industry'].map(status_mapping)


status_mapping = {'Closed': 2, 'Open': 1}
# Map the non-ordinal string column to numerical values
claims_data['Status_Updated_encode'] = claims_data['Status_Updated'].map(status_mapping)


claims_data['hasStrain'] = claims_data['Cause Description'].str.contains(r'strain|Strain|STRAIN', regex=True)
claims_data['hasPain'] = claims_data['Cause Description'].str.contains(r'pain|Pain|PAIN', regex=True)
claims_data['hasShoulderInjury'] = claims_data['Cause Description'].str.contains(r'(shoulder|Shoulder|SHOULDER)&(injured|Injured|INJURED|Injury|injury|INJURY)', regex=True)
claims_data['hasKneeProblem'] = claims_data['Cause Description'].str.contains(r'knee|Knee|KNEE', regex=True)
claims_data['hasWristProblem'] = claims_data['Cause Description'].str.contains(r'wrist|Wrist|WRIST', regex=True)
claims_data['hasSprain'] = claims_data['Cause Description'].str.contains(r'sprain|Sprain|SPRAIN', regex=True)
claims_data['hasSlipped'] = claims_data['Cause Description'].str.contains(r'slipped|Slipped|SLIPPED|slip|Slip|SLIP', regex=True)


#for col in cat_cols:
 #   claims_data[col] = claims_data[col].astype('category')
claims_data=claims_data.drop(columns=['Date of Birth','Report Date','Closed Date','Loss Date','Accident State','Sector/Industry','Loss Type','Status_Updated','Cause Description','Occupation','Carrier'])
# Convert Litigation to binary numeric (1 for 'yes', 0 for 'no')
claims_data['Litigation'] = claims_data['Litigation'].map({'YES': 1, 'NO': 0})

# Handle missing values in Claim Cost 
claims_data['Claim Cost']=claims_data['Claim Cost'].fillna(claims_data['Claim Cost'].mean())
cat_cols=claims_data.columns
for col in cat_cols:
    claims_data[col]=pd.to_numeric(claims_data[col], errors='coerce')


# Cross-tabulate Litigation and High Cost
litigation_high_cost_crosstab = pd.crosstab(claims_data['Litigation'], claims_data['High Cost'])


# Perform Chi-square test
chi2, p, dof, expected = chi2_contingency(litigation_high_cost_crosstab)

print(f"Chi-square value: {chi2}")
print(f"P-value: {p}")
print(f"Degrees of freedom: {dof}")
print("Expected frequencies table:")
print(expected)

y_litigation = claims_data['Litigation']
claims_data= claims_data.drop(['Case Number', 'High Cost'], axis=1)
X=claims_data
y_litigation=y_litigation.fillna(0)



# Split data into training and testing sets
X_train, X_test, y_litigation_train, y_litigation_test = train_test_split(X, y_litigation, test_size=0.2, random_state=42)

# Initialize Decision Tree Classifier
dt_classifier = DecisionTreeClassifier(random_state=42)
print("Fit for x train",X_train.columns)

# Fit the model for predicting Litigation
dt_classifier.fit(X_train, y_litigation_train)


# Predict Litigation on test data
y_litigation_pred = dt_classifier.predict(X_test)

# Evaluate the model for Litigation prediction
print(classification_report(y_litigation_test, y_litigation_pred))
print(confusion_matrix(y_litigation_test, y_litigation_pred))
print("Accuracy", accuracy_score(y_litigation_test, y_litigation_pred))
matplotlibpy.figure(figsize=(12, 8))
plot_tree(dt_classifier, feature_names=X.columns, class_names=['No Litigation', 'Litigation'], filled=True)
matplotlibpy.show()


litigation_group = claims_data[claims_data['Litigation'] == 1]['Claim Cost']
non_litigation_group = claims_data[claims_data['Litigation'] == 0]['Claim Cost']

# Perform t-test to compare mean claim costs
t_stat, p_value = ttest_ind(litigation_group, non_litigation_group)
print("T-Statistic:", t_stat)
print("P-Value:", p_value)

#prediction mode;  
new_data = pd.DataFrame({
    'Accident State': [0],
    'Loss Type': [1],
    'Status_Updated': [0],
    'Cause Description': [2],
    'Occupation': [3],
    'Carrier': [1],
    'Sector/Industry': [2],
    'Claim Cost': [15000]
})