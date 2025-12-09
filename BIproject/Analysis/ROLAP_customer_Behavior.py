import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = 'C:/Users/mariem ben slama/BIproject/data/final data/customer_behavior.db'
connection = sqlite3.connect(db_path)

'''-----------------------------------------CUSTOMER BEHAVIOR ANALYSIS-----------------------------------------------'''
# Query 1: Subscription status and purchasing patterns
query_1 = '''
    SELECT 
        c.subscription_status,
        COUNT(f.customer_id) AS number_of_purchases,
        AVG(f.purchase_amount_usd) AS avg_purchase_amount
    FROM customer_dim AS c
    JOIN fact_table AS f ON c.customer_id = f.customer_id
    GROUP BY c.subscription_status
    ORDER BY avg_purchase_amount DESC;
'''
result_1 = pd.read_sql(query_1, connection)
print("\n\nSubscription Status and Purchasing Patterns:")
print(result_1)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 2: Average review rating by gender
query_2 = '''
    SELECT 
        c.gender,
        AVG(f.review_rating) AS avg_review_rating
    FROM customer_dim AS c
    JOIN fact_table AS f ON c.customer_id = f.customer_id
    GROUP BY c.gender
    ORDER BY  avg_review_rating DESC;
'''
result_2 = pd.read_sql(query_2, connection)
print("\n\nAverage Review Rating by Gender:")
print(result_2)
'''-----------------------------------------------------------------------------------------------------------------'''

# Query 3: Number of Purchases by Gender
query_3 = '''
    SELECT 
        c.gender, 
        COUNT(*) AS total_purchases
    FROM fact_table f
    JOIN customer_dim c ON f.customer_id = c.customer_id
    GROUP BY c.gender;
'''

result_3 = pd.read_sql(query_3, connection)
print("\n\nNumber of Purchases by Gender:")
print(result_3)

'''-----------------------------------------------------------------------------------------------------------------'''

# Query 15: Total Sales by Season and Gender
query_4 = '''
    SELECT 
        d.season, c.gender, 
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN date_dim d ON f.date_id = d.date_id
    JOIN customer_dim c ON f.customer_id = c.customer_id
    GROUP BY d.season, c.gender;
'''
result_4 = pd.read_sql(query_4, connection)
print("\n\nTotal Sales by Season and Gender:")
print(result_4)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 2: Average review rating by generation
query_5 = '''
    SELECT 
        c.generation,
        AVG(f.review_rating) AS avg_review_rating
    FROM customer_dim AS c
    JOIN fact_table AS f ON c.customer_id = f.customer_id
    GROUP BY c.generation
    ORDER BY  avg_review_rating DESC;
'''
result_5 = pd.read_sql(query_5, connection)
print("\n\nAverage Review Rating by Generation:")
print(result_5)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 6: Total Sales by generation
query_6 = '''
    SELECT 
        c.generation, 
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN customer_dim c ON f.customer_id = c.customer_id
    GROUP BY c.generation;
    '''
result_6 = pd.read_sql(query_6, connection)
print("\n\nTotal Sales by generation:")
print(result_6)
'''-----------------------------------------------------------------------------------------------------------------'''

# Query 7: Category Ranking  by Generation:
query_7 = '''
    SELECT 
        c.generation, p.category, COUNT(*) AS purchase_count
    FROM fact_table f
    JOIN customer_dim c ON f.customer_id = c.customer_id
    JOIN product_dim p ON f.product_id = p.product_id
    GROUP BY c.generation, p.category
    ORDER BY c.generation, purchase_count DESC;
'''
result_7 = pd.read_sql(query_7, connection)
print("\n\nCategory Ranking  by Generation:")
print(result_7)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 8: Top 10 Customers by Purchase Amount
query_8 = '''
    SELECT 
        c.customer_id,
        c.gender,
        c.subscription_status,
        SUM(f.purchase_amount_usd) AS total_purchase_amount
    FROM customer_dim AS c
    JOIN fact_table AS f ON c.customer_id = f.customer_id
    GROUP BY  c.customer_id
    ORDER BY total_purchase_amount DESC
    LIMIT 10;
    '''
result_8 = pd.read_sql(query_8, connection)
print("\n\nTop 10 Customers by Purchase Amount:")
print(result_8)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 9: Seasonal purchase trends
query_9 ='''
    SELECT 
        d.season,
        COUNT(*) AS total_purchases,
        SUM(f.purchase_amount_usd) AS total_purchase_amount 
    FROM date_dim AS d
    JOIN fact_table AS f ON d.date_id = f.date_id
    GROUP BY d.season
    ORDER BY total_purchase_amount DESC; 
'''

result_9 = pd.read_sql(query_9, connection)
print("\n\nTotal Purchase Number And Amount per Season:")
print(result_9)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 10: Monthly Sales (Sales Based on Date)
query_10 = '''
    SELECT 
        d.month AS month, 
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN date_dim d ON f.date_id = d.date_id
    GROUP BY month
    ORDER BY month;
'''

result_10 = pd.read_sql(query_10, connection)
print("\n\nMonthly Sales (Sales Based on Date):")
print(result_10)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 11: Highest and Lowest Review Ratings by Category
query_11 = '''
    SELECT 
        p.category, 
        MAX(f.review_rating) AS max_rating, 
        MIN(f.review_rating) AS min_rating
    FROM fact_table f
    JOIN product_dim p ON f.product_id = p.product_id
    GROUP BY p.category;
'''
result_11 = pd.read_sql(query_11, connection)
print("\n\nHighest and Lowest Review Ratings by Category:")
print(result_11)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 12: Average Review Rating Per Item Purchased:
query_12 = '''
    SELECT 
        p.item_purchased, AVG(f.review_rating) AS avg_rating
    FROM fact_table f
    JOIN product_dim p ON f.product_id = p.product_id
    GROUP BY p.item_purchased
    ORDER BY avg_rating DESC;
'''

result_12 = pd.read_sql(query_12, connection)
print("\n\nAverage Review Rating Per Item Purchased:")
print(result_12)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 13: Top 10 items purchased based on total sales
query_13 = '''
    SELECT 
        p.item_purchased, 
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN product_dim p ON f.product_id = p.product_id
    GROUP BY p.item_purchased
    ORDER BY total_sales DESC
    LIMIT 10;
'''

result_13 = pd.read_sql(query_13, connection)
print("\n\nTop 10 items purchased based on total sales:")
print(result_13)
'''-----------------------------------------------------------------------------------------------------------------'''
#query 14: Number of Purchases and Sales Amount by Product Category
query_14 = '''
    SELECT 
        p.category,
        COUNT(f.product_id) AS total_purchases,
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN product_dim p ON f.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_sales DESC;
'''

result_10 = pd.read_sql(query_10, connection)
print("\n\nthe Most  Sold Product Category:")
print(result_10)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 15: Sales Based on Discount Applied
query_15 = '''
    SELECT 
        f.discount_applied, 
    SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    GROUP BY f.discount_applied;'''

result_15 = pd.read_sql(query_15, connection)
print("\n\nSales Based on Discount Applied:")
print(result_15)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 16: Percentage of Purchases with Discounts
query_16 = '''
    SELECT 
    	f.discount_applied,
    	COUNT() * 100.0 / (SELECT COUNT() FROM fact_table) AS percentage_of_purchases
    FROM fact_table f
    GROUP BY f.discount_applied;
'''
result_16 = pd.read_sql(query_16, connection)
print("\n\nPercentage of Purchases with Discounts:")
print(result_16)
'''-----------------------------------------------------------------------------------------------------------------'''
# Query 17: Sales Distribution Across Locations:
query_17 ='''
    SELECT 
        c.location, 
        SUM(f.purchase_amount_usd) AS total_sales
    FROM fact_table f
    JOIN customer_dim c ON f.customer_id = c.customer_id
    GROUP BY c.location
    ORDER BY total_sales DESC
    LIMIT 10;
'''

result_17 = pd.read_sql(query_17, connection)
print("\n\nSales Distribution Across Locations:")
print(result_17)

'''-----------------------------------------------------------------------------------------------------------------'''
# Query 18: Most Commonly Purchased Size by Category (relevant for stock management)
query_18 = '''
    SELECT 
        p.category, p.size, 
        COUNT(*) AS frequency
    FROM product_dim p
    JOIN fact_table f ON p.product_id = f.product_id
    GROUP BY p.category, p.size
    ORDER BY p.category, frequency DESC;
'''
result_18 = pd.read_sql(query_18, connection)
print("\nMost Commonly Purchased Size by Category:")
print(result_18)

# Close the database connection
connection.close()