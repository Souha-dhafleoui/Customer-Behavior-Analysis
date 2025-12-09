import pandas as pd
from script.extract import extract_csv, extract_json, extract_excel

#EXTRACTION OF DATASETS:
purchases = extract_csv('../data/raw data/purchase_records.csv')
customerRelation = extract_json('../data/raw data/customer_relation.json')
customerInfo = extract_excel('../data/raw data/customer_info.xlsx')

#checking datasets
print(purchases)
print(customerRelation)
print(customerInfo) 

#CLEANING OF DATA:
#checking for missing values: (No missing values were found)
print(purchases.isna().sum())
print(customerRelation.isna().sum())
print(customerInfo.isna().sum())

#Checking for duplicate rows: (1 Duplicate is found in customer_info)
print("Duplicate rows in purchase_records:", purchases.duplicated().sum())
print("Duplicate rows in customer_relation:", customerRelation.duplicated().sum())
print("Duplicate rows in customer_info:", customerInfo.duplicated().sum())
    #view duplicate
duplicates = customerInfo[customerInfo.duplicated()]
print(duplicates)
    #drop duplicate:
customerInfo.drop_duplicates(inplace=True)

#check initial column names:
print(purchases.columns)
print(customerRelation.columns)
print(customerInfo.columns)

#Drop unnecessary columns: promo code used, shipping type and payment method:
purchases = purchases.drop(['Shipping Type', 'Promo Code Used', 'Payment Method'], axis=1)

# Replace spaces with underscores in column names for all three datasets
purchases.columns = purchases.columns.str.strip().str.lower().str.replace(" ", "_")
customerRelation.columns = customerRelation.columns.str.strip().str.lower().str.replace(" ", "_")
customerInfo.columns = customerInfo.columns.str.strip().str.lower().str.replace(" ", "_")

# Verify the changes by printing the column names
print("Purchase Records Columns:", purchases.columns)
print("Customer Relation Columns:", customerRelation.columns)
print("Customer Info Columns:", customerInfo.columns)


#check data types:
print("purchase_records info:", purchases.info())
print("customer_relation info:",customerRelation.info())
print("customer_info info:",customerInfo.info())

#Change date datatype (from object-->datetime64[ns])
purchases['date']=pd.to_datetime(purchases['date'])

#Adding generation column to customer info:
def assign_generation(age):
    if 6 <= age <= 24:  # Gen Z: 1997–2013
        return 'Gen Z'
    elif 25 <= age <= 40:  # Millennials: 1981–1996
        return 'Millennials'
    elif 41 <= age <= 56:  # Gen X: 1965–1980
        return 'Gen X'
    elif 57 <= age <= 75:  # Baby Boomers: 1946–1964
        return 'Baby Boomers'
    elif age >= 76:  # Silent Generation: 1928–1945
        return 'Silent'
    else:
        return 'Unknown'

customerInfo['generation'] = customerInfo['age'].apply(assign_generation)

#Addition of ID columns:
purchases['product_id'] = range(10,len(purchases)+10)
purchases['date_id'] = range(100,len(purchases)+100)

#renaming purchase_amount to avoid problems later while working with SQLlite
purchases.rename(columns={'purchase_amount_(usd)': 'purchase_amount_usd'}, inplace=True)


#INTEGRATION OF DATA:

#merging the datasets:
merge_customer = pd.merge(customerInfo, customerRelation, on='customer_id', how='inner')

# Merge the result with purchase_records on 'Customer ID'
cleaned_data = pd.merge(merge_customer, purchases, on='customer_id', how='inner')

#Reorder columns
desired_order = [
    'customer_id', 'gender', 'age', 'generation', 'location', 'subscription_status', 'previous_purchases', 'frequency_of_purchases', 'product_id',
    'item_purchased', 'category', 'size', 'color', 'review_rating', 'purchase_amount_usd', 'discount_applied', 'date_id',
    'date', 'season'
]
cleaned_data = cleaned_data[desired_order]

# Show the final dataframe with the columns ordered as specified
print(cleaned_data.head())

#Create fact table
fact_table= cleaned_data[['customer_id', 'product_id', 'date_id', 'purchase_amount_usd',
                          'discount_applied', 'review_rating']].drop_duplicates()

#Create product dimension
product_dim= cleaned_data[['product_id', 'item_purchased', 'category',
                                  'size', 'color']].drop_duplicates()

#Create customer dimension
customer_dim= cleaned_data[['customer_id', 'age', 'gender', 'location',
                                   'subscription_status', 'generation', 'previous_purchases', 'frequency_of_purchases']].drop_duplicates()

# Create Time Dimension
date_dim= cleaned_data[['date_id', 'date']].drop_duplicates()
date_dim['quarter'] = date_dim['date'].dt.quarter  # Extract quarter
date_dim['month'] = date_dim['date'].dt.month      # Extract month
date_dim['day'] = date_dim['date'].dt.day          # Extract day
date_dim= pd.merge(date_dim, cleaned_data[['date_id', 'season']].drop_duplicates(), on='date_id', how='left')

#check tables
print(fact_table.head())
print(customer_dim.head())
print(product_dim.head())
print(date_dim.head())

#save datasets to final data folder
cleaned_data.to_csv('../data/final data/cleaned_data.csv', index=False)
fact_table.to_csv('../data/final data/fact_table.csv', index=False)
customer_dim.to_csv('../data/final data/customer_dim.csv', index=False)
product_dim.to_csv('../data/final data/product_dim.csv', index=False)
date_dim.to_csv('../data/final data/date_dim.csv', index=False)