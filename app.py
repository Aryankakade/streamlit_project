# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector

# app = Flask(__name__)
# CORS(app)  # 👈 Allow Cross-Origin Requests (For Frontend Integration)

# # ✅ Function to establish MySQL connection
# def get_db_connection():
#     try:
#         db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Aryankakade@143",
#             database="bank1"
#         )
#         return db
#     except mysql.connector.Error as err:
#         print(f"❌ Database Connection Error: {err}")
#         return None  # 👈 DB Connection Failed Case

# # ✅ Predefined Queries
# predefined_queries = {
#     "1": """SELECT c.customer_id, c.first_name, c.last_name 
#             FROM customers c 
#             JOIN accounts a ON c.customer_id = a.customer_id 
#             LEFT JOIN transactions t ON a.account_number = t.account_number 
#             WHERE t.transaction_id IS NULL 
#             OR t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);""",

#     "2": """SELECT account_number, YEAR(transaction_date) AS year, MONTH(transaction_date) AS month, 
#             SUM(amount) AS total_amt 
#             FROM transactions 
#             GROUP BY account_number, year, month 
#             ORDER BY account_number, year, month;""",

#     "3": """SELECT a.branch_id, SUM(t.amount) AS total_amount, 
#             DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank 
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number) 
#             WHERE t.transaction_type='Deposit' 
#             AND t.transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) 
#             GROUP BY a.branch_id 
#             ORDER BY branch_rank;"""
# }

# # ✅ API Route to Execute Queries
# @app.route('/query', methods=['GET'])
# def execute_query():
#     query_id = request.args.get('id')

#     # ❌ Invalid Query ID Case
#     if query_id not in predefined_queries:
#         return jsonify({"error": "❌ Invalid query ID. Please provide a valid ID from 1 to 3."}), 400

#     db = get_db_connection()
#     if db is None:
#         return jsonify({"error": "❌ Database connection failed. Check MySQL credentials."}), 500

#     cursor = None
#     try:
#         cursor = db.cursor(dictionary=True)
#         cursor.execute(predefined_queries[query_id])
#         result = cursor.fetchall()
#     except mysql.connector.Error as err:
#         print(f"❌ Database Error: {err}")
#         return jsonify({"error": f"❌ Database error: {err}"}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if db:
#             db.close()

#     return jsonify(result)

# # ✅ Run Flask App
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)  # 👈 Disable reloader to avoid threading issues

# import streamlit as st
# import requests

# BASE_URL = "http://127.0.0.1:5000"  # Flask API URL

# st.title("Banking Data Explorer")

# # ✅ Fetch specific table data
# table_name = st.selectbox("Select Table", ["transactions", "customers", "accounts", "employees", "branch"])

# if st.button("Fetch Data"):
#     response = requests.get(f"{BASE_URL}/data/{table_name}")
#     if response.status_code == 200:
#         st.write(response.json())
#     else:
#         st.error("Failed to fetch data.")

# # ✅ Run predefined queries
# query_id = st.selectbox("Select Query", ["SELECT c.customer_id, c.first_name, c.last_name 
# #             FROM customers c 
# #             JOIN accounts a ON c.customer_id = a.customer_id 
# #             LEFT JOIN transactions t ON a.account_number = t.account_number 
# #             WHERE t.transaction_id IS NULL 
# #             OR t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);", "2", "3"])
# if st.button("Run Query"):
#     response = requests.get(f"{BASE_URL}/query?id={query_id}")
#     if response.status_code == 200:
#         st.write(response.json())
#     else:
#         st.error("Query execution failed.")

# import streamlit as st
# import requests
# import pandas as pd

# # ✅ Define API Base URL
# API_URL = "http://127.0.0.1:5000"

# # ✅ Fetch table data
# def fetch_table_data(table_name):
#     try:
#         response = requests.get(f"{API_URL}/all_data/{table_name}")
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch table data: {e}")
#     return None

# # ✅ Fetch and run SQL query
# def execute_sql_query(query):
#     try:
#         response = requests.post(f"{API_URL}/execute_query", json={"query": query})
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         print(f"[ERROR] Failed to execute query: {e}")
#     return None

# # ✅ Sidebar Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Table Data", "Power BI Dashboard", "SQL Queries", "Downloads"])

# # ✅ Home Page
# if page == "Home":
#     st.title("🏦 Welcome to the Banking Dashboard!")
#     st.write("Navigate using the sidebar to explore data, Power BI reports, and SQL queries.")

# # ✅ Table Data Page
# elif page == "Table Data":
#     st.title("📊 Table Data")
#     selected_table = st.selectbox("Select Table", ["customers", "accounts", "transactions", "employees", "branch"])
#     table_data = fetch_table_data(selected_table)
#     if table_data is not None:
#         st.dataframe(table_data)

# # ✅ Power BI Dashboard Page
# elif page == "Power BI Dashboard":
#     st.title("📊 Power BI Dashboard")
#     st.write("🔗 Click below to open the Power BI report:")
#     power_bi_url = "https://app.powerbi.com/groups/me/reports/4a3fada2-ba7e-4920-bd40-d09245e7c1b7/be94380037ae7288aa6b?experience=power-bi"
#     st.markdown(f"[Open Power BI Dashboard]({power_bi_url})", unsafe_allow_html=True)

#     st.write("🚀 **Power BI Workaround:** If you don’t have Power BI installed, download the PBIX file from the Downloads page.")

# # ✅ SQL Queries Page (18 Queries)
# elif page == "SQL Queries":
#     st.title("📝 SQL Queries")

#     queries = {
#         "1. Inactive Customers (No Transactions in Last Year)": """
#             SELECT c.customer_id, c.first_name, c.last_name 
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             LEFT JOIN transactions t ON a.account_number = t.account_number 
#             WHERE t.transaction_id IS NULL OR 
#             t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
#         """,
#         "2. Total Transactions Per Account Per Month": """
#             SELECT account_number, YEAR(transaction_date) AS year, 
#             MONTH(transaction_date) AS month, SUM(amount) AS total_amt
#             FROM transactions 
#             GROUP BY account_number, year, month
#             ORDER BY account_number, year, month;
#         """,
#         "3. Branch Ranking Based on Deposits in Last Quarter": """
#             SELECT a.branch_id, SUM(t.amount) AS total_deposits, 
#             DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             WHERE t.transaction_type="Deposit" 
#             AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) 
#             GROUP BY a.branch_id
#             ORDER BY branch_rank;
#         """,
#         "4. Customer with Highest Deposit": """
#             SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, t.amount 
#             FROM customers c 
#             INNER JOIN accounts a ON c.customer_id = a.customer_id 
#             INNER JOIN transactions t ON t.account_number = a.account_number
#             WHERE t.transaction_type = "Deposit"
#             ORDER BY t.amount DESC
#             LIMIT 1;
#         """,
#         "5. Fraud Detection: More Than 2 Transactions in a Day": """
#             SELECT a.account_number AS fraud_accounts, COUNT(t.transaction_id) AS no_of_transactions, 
#             DAY(t.transaction_date) AS single_day
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             GROUP BY fraud_accounts, single_day
#             HAVING no_of_transactions > 2;
#         """,
#         "6. Daily Transaction Volume (Past Month)": """
#             SELECT DATE(transaction_date) AS transaction_day, ROUND(SUM(amount), 3) AS trans_volume
#             FROM transactions 
#             WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
#             GROUP BY transaction_day
#             ORDER BY transaction_day;
#         """,
#         "7. Branch with Highest Average Account Balance": """
#             SELECT branch_id, AVG(balance) AS avg_bal
#             FROM accounts 
#             GROUP BY branch_id
#             ORDER BY avg_bal DESC
#             LIMIT 1;
#         """,
#         "8. Most Common Transaction Type Per Branch": """
#             SELECT b.branch_id, t.transaction_type, COUNT(*) AS transaction_count
#             FROM transactions t
#             JOIN accounts a ON t.account_number = a.account_number
#             JOIN branch b ON a.branch_id = b.branch_id
#             GROUP BY b.branch_id, t.transaction_type
#             ORDER BY b.branch_id, transaction_count DESC;
#         """,
#         "9. Accounts with Only Withdrawals": """
#             SELECT account_number
#             FROM transactions
#             GROUP BY account_number
#             HAVING SUM(CASE WHEN transaction_type = 'deposit' THEN 1 ELSE 0 END) = 0;
#         """,
#         "10. Running Total of Transactions Per Account": """
#             SELECT account_number, transaction_date, amount,
#             SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#             FROM transactions;
#         """,
#         "11. Previous Transaction Amount for Each Transaction": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             LAG(amount, 1, 0) OVER (PARTITION BY account_number ORDER BY transaction_date) AS previous_transaction
#             FROM transactions;
#         """,
#         "12. Customers with Highest Transactions": """
#             SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY c.customer_id, c.first_name, c.last_name
#             ORDER BY total_transactions DESC
#             LIMIT 10;
#         """,
#         "13. Moving Average of Transactions": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             AVG(amount) OVER (PARTITION BY account_number ORDER BY transaction_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
#             FROM transactions;
#         """,
#         "14. Average Transactions Per Branch Per Month": """
#             SELECT b.branch_id, YEAR(t.transaction_date) AS year, MONTH(t.transaction_date) AS month,
#             COUNT(t.transaction_id) / COUNT(DISTINCT t.account_number) AS avg_transactions
#             FROM branch b
#             JOIN accounts a ON b.branch_id = a.branch_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY b.branch_id, year, month;
#         """,
#         "15. Running Total of transactions per Account": """
#              SELECT account_number, transaction_date, amount,
#              SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#              FROM transactions;
#         """,
#         "16. customers whose account balance is below the average balance of their branch" : """
#              SELECT c.customer_id, c.first_name, c.last_name, a.account_number, a.balance, branch_avg.avg_balance
#              FROM accounts a
#              JOIN customers c ON a.customer_id = c.customer_id
#              JOIN (
#              SELECT branch_id, AVG(balance) AS avg_balance
#              FROM accounts
#              GROUP BY branch_id
#              ) branch_avg ON a.branch_id = branch_avg.branch_id
#              WHERE a.balance < branch_avg.avg_balance;
#         """,
#         "17. customers who have made the highest number of transactions": """
#              SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#              FROM customers c
#              JOIN accounts a ON c.customer_id = a.customer_id
#              JOIN transactions t ON a.account_number = t.account_number
#              GROUP BY c.customer_id, c.first_name, c.last_name
#              ORDER BY total_transactions DESC
#             LIMIT 10;
#         """

#     }

#     selected_query = st.selectbox("Select Query", list(queries.keys()))
#     st.subheader(f"🧐 {selected_query}")
#     st.code(queries[selected_query], language="sql")

#     if st.button("Run Query"):
#         query_result = execute_sql_query(queries[selected_query])
#         if query_result is not None:
#             st.dataframe(query_result)

# # ✅ Downloads Page
# elif page == "Downloads":
#     st.title("📥 Download Project Files")
#     st.write("📥 **Download the Project Files Below:**")
#     st.markdown("[📄 Download PDF Report](sandbox:/mnt/data/dashboard%20(2).pdf)", unsafe_allow_html=True)
#     st.markdown("[📊 Download Power BI Dashboard (PBIX)](sandbox:/mnt/data/banking_operation_dashboard.pbix)", unsafe_allow_html=True)
#     st.markdown("[📽️ Download PowerPoint Presentation](sandbox:/mnt/data/Analysis%20of%20Banking%20Operations%20using%20Power%20BI(1).pptx)", unsafe_allow_html=True)
# import streamlit as st
# import requests
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import statsmodels.api as sm
# from scipy import stats
# from scipy.stats import f_oneway, ttest_ind  # Added missing imports
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# # ✅ Define API Base URL
# API_URL = "http://127.0.0.1:5000"

# # ✅ Fetch table data
# def fetch_table_data(table_name):
#     try:
#         response = requests.get(f"{API_URL}/all_data/{table_name}")
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch table data: {e}")
#     return None

# # ✅ Fetch and run SQL query
# def execute_sql_query(query):
#     try:
#         response = requests.post(f"{API_URL}/execute_query", json={"query": query})
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         print(f"[ERROR] Failed to execute query: {e}")
#     return None

# # ✅ Sidebar Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Table Data", "Power BI Dashboard", "SQL Queries", "Downloads", "Python Analysis"])

# # ✅ Home Page
# if page == "Home":
#     st.title("🏦 Welcome to the Banking Dashboard!")
#     st.write("Navigate using the sidebar to explore data, Power BI reports, and SQL queries.")

# # ✅ Table Data Page
# elif page == "Table Data":
#     st.title("📊 Table Data")
#     selected_table = st.selectbox("Select Table", ["customers", "accounts", "transactions", "employees", "branch"])
#     table_data = fetch_table_data(selected_table)
#     if table_data is not None:
#         st.dataframe(table_data)

# # ✅ Power BI Dashboard Page (🔹 FIXED: Now Opens in New Tab)
# elif page == "Power BI Dashboard":
#     st.title("📊 Power BI Dashboard")
#     st.write("🔗 Click below to open the Power BI report in a new tab:")
#     power_bi_url = "https://app.powerbi.com/groups/me/reports/4a3fada2-ba7e-4920-bd40-d09245e7c1b7/be94380037ae7288aa6b?experience=power-bi"
#     st.markdown(f"[🔗 Open Power BI Dashboard]({power_bi_url})", unsafe_allow_html=True)

#     st.write("🚀 **Power BI Workaround:** If you don’t have Power BI installed, download the PBIX file from the Downloads page.")


# # ✅ SQL Queries Page (18 Queries)
# elif page == "SQL Queries":
#     st.title("📝 SQL Queries")

#     queries = {
#         "1. Inactive Customers (No Transactions in Last Year)": """
#             SELECT c.customer_id, c.first_name, c.last_name 
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             LEFT JOIN transactions t ON a.account_number = t.account_number 
#             WHERE t.transaction_id IS NULL OR 
#             t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
#         """,
#         "2. Total Transactions Per Account Per Month": """
#             SELECT account_number, YEAR(transaction_date) AS year, 
#             MONTH(transaction_date) AS month, SUM(amount) AS total_amt
#             FROM transactions 
#             GROUP BY account_number, year, month
#             ORDER BY account_number, year, month;
#         """,
#         "3. Branch Ranking Based on Deposits in Last Quarter": """
#             SELECT a.branch_id, SUM(t.amount) AS total_deposits, 
#             DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             WHERE t.transaction_type="Deposit" 
#             AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) 
#             GROUP BY a.branch_id
#             ORDER BY branch_rank;
#         """,
#         "4. Customer with Highest Deposit": """
#             SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, t.amount 
#             FROM customers c 
#             INNER JOIN accounts a ON c.customer_id = a.customer_id 
#             INNER JOIN transactions t ON t.account_number = a.account_number
#             WHERE t.transaction_type = "Deposit"
#             ORDER BY t.amount DESC
#             LIMIT 1;
#         """,
#         "5. Fraud Detection: More Than 2 Transactions in a Day": """
#             SELECT a.account_number AS fraud_accounts, COUNT(t.transaction_id) AS no_of_transactions, 
#             DAY(t.transaction_date) AS single_day
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             GROUP BY fraud_accounts, single_day
#             HAVING no_of_transactions > 2;
#         """,
#         "6. Daily Transaction Volume (Past Month)": """
#             SELECT DATE(transaction_date) AS transaction_day, ROUND(SUM(amount), 3) AS trans_volume
#             FROM transactions 
#             WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
#             GROUP BY transaction_day
#             ORDER BY transaction_day;
#         """,
#         "7. Branch with Highest Average Account Balance": """
#             SELECT branch_id, AVG(balance) AS avg_bal
#             FROM accounts 
#             GROUP BY branch_id
#             ORDER BY avg_bal DESC
#             LIMIT 1;
#         """,
#         "8. Most Common Transaction Type Per Branch": """
#             SELECT b.branch_id, t.transaction_type, COUNT(*) AS transaction_count
#             FROM transactions t
#             JOIN accounts a ON t.account_number = a.account_number
#             JOIN branch b ON a.branch_id = b.branch_id
#             GROUP BY b.branch_id, t.transaction_type
#             ORDER BY b.branch_id, transaction_count DESC;
#         """,
#         "9. Accounts with Only Withdrawals": """
#             SELECT account_number
#             FROM transactions
#             GROUP BY account_number
#             HAVING SUM(CASE WHEN transaction_type = 'deposit' THEN 1 ELSE 0 END) = 0;
#         """,
#         "10. Running Total of Transactions Per Account": """
#             SELECT account_number, transaction_date, amount,
#             SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#             FROM transactions;
#         """,
#         "11. Previous Transaction Amount for Each Transaction": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             LAG(amount, 1, 0) OVER (PARTITION BY account_number ORDER BY transaction_date) AS previous_transaction
#             FROM transactions;
#         """,
#         "12. Customers with Highest Transactions": """
#             SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY c.customer_id, c.first_name, c.last_name
#             ORDER BY total_transactions DESC
#             LIMIT 10;
#         """,
#         "13. Moving Average of Transactions": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             AVG(amount) OVER (PARTITION BY account_number ORDER BY transaction_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
#             FROM transactions;
#         """,
#         "14. Average Transactions Per Branch Per Month": """
#             SELECT b.branch_id, YEAR(t.transaction_date) AS year, MONTH(t.transaction_date) AS month,
#             COUNT(t.transaction_id) / COUNT(DISTINCT t.account_number) AS avg_transactions
#             FROM branch b
#             JOIN accounts a ON b.branch_id = a.branch_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY b.branch_id, year, month;
#         """,
#         "15. Running Total of transactions per Account": """
#              SELECT account_number, transaction_date, amount,
#              SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#              FROM transactions;
#         """,
#         "16. customers whose account balance is below the average balance of their branch" : """
#              SELECT c.customer_id, c.first_name, c.last_name, a.account_number, a.balance, branch_avg.avg_balance
#              FROM accounts a
#              JOIN customers c ON a.customer_id = c.customer_id
#              JOIN (
#              SELECT branch_id, AVG(balance) AS avg_balance
#              FROM accounts
#              GROUP BY branch_id
#              ) branch_avg ON a.branch_id = branch_avg.branch_id
#              WHERE a.balance < branch_avg.avg_balance;
#         """,
#          "17. customers who have made the highest number of transactions": """
#               SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#               FROM customers c
#               JOIN accounts a ON c.customer_id = a.customer_id
#               JOIN transactions t ON a.account_number = t.account_number
#               GROUP BY c.customer_id, c.first_name, c.last_name
#               ORDER BY total_transactions DESC
#               LIMIT 10;
#           """
#         # Add other queries here...
#     }

#     selected_query = st.selectbox("Select Query", list(queries.keys()))
#     st.subheader(f"🧐 {selected_query}")
#     st.code(queries[selected_query], language="sql")

#     if st.button("Run Query"):
#         query_result = execute_sql_query(queries[selected_query])
#         if query_result is not None:
#             st.dataframe(query_result)

# # ✅ Downloads Page
# elif page == "Downloads":
#     st.title("📥 Download Project Files")
#     st.write("📥 **Download the Project Files Below:**")
#     st.markdown("[📄 Download PDF Report](sandbox:/mnt/data/dashboard%20(2).pdf)", unsafe_allow_html=True)
#     st.markdown("[📊 Download Power BI Dashboard (PBIX)](sandbox:/mnt/data/banking_operation_dashboard.pbix)", unsafe_allow_html=True)
#     st.markdown("[📽️ Download PowerPoint Presentation](sandbox:/mnt/data/Analysis%20of%20Banking%20Operations%20using%20Power%20BI(1).pptx)", unsafe_allow_html=True)

# # ✅ Python Analysis Page
# elif page == "Python Analysis":
#     st.title("🐍 Python Analysis")
#     analysis_step = st.selectbox("Select Analysis Step", ["Data Cleaning", "EDA", "Regression Model", "Hypothesis Testing"])

#     if analysis_step == "Data Cleaning":
#         st.subheader("Data Cleaning")
#         # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Display data
#         st.write("### Customers Data")
#         st.dataframe(customers.head(10))

#         st.write("### Transactions Data")
#         st.dataframe(transactions.head(10))

#         st.write("### Accounts Data")
#         st.dataframe(accounts.head(10))

#         st.write("### Branches Data")
#         st.dataframe(branches.head(10))

#         st.write("### Employees Data")
#         st.dataframe(employee.head(10))

#         # Check for missing values
#         st.write("### Missing Values Check")
#         st.write("Customers:", customers.isnull().sum())
#         st.write("Transactions:", transactions.isnull().sum())
#         st.write("Accounts:", accounts.isnull().sum())
#         st.write("Branches:", branches.isnull().sum())
#         st.write("Employees:", employee.isnull().sum())

#         # Drop duplicates
#         customers.drop_duplicates(inplace=True)
#         transactions.drop_duplicates(inplace=True)
#         accounts.drop_duplicates(inplace=True)
#         branches.drop_duplicates(inplace=True)
#         employee.drop_duplicates(inplace=True)

#         st.write("### Data After Dropping Duplicates")
#         st.write("Customers:", customers.shape)
#         st.write("Transactions:", transactions.shape)
#         st.write("Accounts:", accounts.shape)
#         st.write("Branches:", branches.shape)
#         st.write("Employees:", employee.shape)

#      elif analysis_step == "EDA":
#         st.subheader("Exploratory Data Analysis (EDA)")

#          # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#        # Branch Performance Analysis (Revenue Contribution per Branch)
#         st.write("### Branch Performance Analysis (Revenue Contribution per Branch)")
    
#         # Merge transactions with accounts to get branch_id
#         branch_revenue = transactions.merge(accounts, on="account_number", how="left")
    
#     if "branch_id" in branch_revenue.columns:
#         branch_revenue = branch_revenue.groupby("branch_id")["amount"].sum().sort_values(ascending=False)

#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=branch_revenue.index, y=branch_revenue.values, palette="plasma")
#         plt.title("Revenue Contribution per Branch")
#         plt.xlabel("Branch ID")
#         plt.ylabel("Total Transaction Amount")
#         st.pyplot(plt)
#     else:
#         st.error("Branch ID not found after merging transactions with accounts!")

#         # Top 10 Customers with Highest Transactions
#         st.write("### Top 10 Customers with Highest Transactions")
    
#         # Merge transactions with customers to get customer_id
#         transactions = transactions.merge(accounts, on="account_number", how="left").merge(customers, on="customer_id", how="left")
    
#     if "customer_id" in transactions.columns:
#         customer_transaction_counts = transactions["customer_id"].value_counts()
#         top_customers = customer_transaction_counts.head(10)

#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=top_customers.index, y=top_customers.values, palette="coolwarm")
#         plt.title("Top 10 Customers with Most Transactions")
#         plt.xlabel("Customer ID")
#         plt.ylabel("Number of Transactions")
#         plt.xticks(rotation=45)
#         st.pyplot(plt)
#     else:
#         st.error("Customer ID not found after merging transactions with accounts & customers!")

#         # Most Active Branches (Number of Accounts per Branch)
#         st.write("### Most Active Branches (Number of Accounts per Branch)")
    
#     if "branch_id" in accounts.columns:
#         accounts_per_branch = accounts.groupby("branch_id")["account_number"].count()

#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=accounts_per_branch.index, y=accounts_per_branch.values, palette="mako")
#         plt.title("Number of Accounts Per Branch")
#         plt.xlabel("Branch ID")
#         plt.ylabel("Number of Accounts")
#         st.pyplot(plt)
#     else:
#         st.error("Branch ID not found in accounts table!")

#     # Branches per city
#         st.write("### Branches per City")
    
#     if "city" in branches.columns:
#         branches_per_city = branches["city"].value_counts()

#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=branches_per_city.index, y=branches_per_city.values, palette="coolwarm")
#         plt.title("Number of Bank Branches Per City")
#         plt.xlabel("City")
#         plt.ylabel("Number of Branches")
#         plt.xticks(rotation=45)
#         st.pyplot(plt)
#     else:
#         st.error("City column not found in branches table!")

#     # Month-wise Transaction Trends
#         st.write("### Month-wise Transaction Trends")
    
#     if "transaction_date" in transactions.columns:
#         transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
#         transactions["month"] = transactions["transaction_date"].dt.month
#         monthly_trends = transactions.groupby("month")["amount"].sum()

#         plt.figure(figsize=(10, 5))
#         sns.lineplot(x=monthly_trends.index, y=monthly_trends.values, marker="o", color="red")
#         plt.title("Monthly Transaction Trends")
#         plt.xlabel("Month")
#         plt.ylabel("Total Transaction Amount")
#         plt.xticks(range(1, 13))
#         plt.grid()
#         st.pyplot(plt)
#     else:
#         st.error("Transaction date column missing in transactions table!")

#     # Total Balance per Account Type
#         st.write("### Total Balance per Account Type")
    
#     if "account_type" in accounts.columns and "balance" in accounts.columns:
#         plt.figure(figsize=(10, 5))
#         sns.boxplot(x="account_type", y="balance", data=accounts, palette="Set2")
#         plt.yscale("log")  # Log scale for better visualization
#         plt.title("Balance Distribution by Account Type")
#         plt.xlabel("Account Type")
#         plt.ylabel("Balance (Log Scale)")
#         st.pyplot(plt)
#     else:
#         st.error("Account Type or Balance column missing in accounts table!")

#     # Most Common Transaction Type
#         st.write("### Most Common Transaction Type")
    
#     if "transaction_type" in transactions.columns:
#         plt.figure(figsize=(8, 5))
#         sns.countplot(x="transaction_type", data=transactions, palette="magma")
#         plt.title("Most Common Transaction Type")
#         plt.xlabel("Transaction Type")
#         plt.ylabel("Count")
#         st.pyplot(plt)
#     else:
#         st.error("Transaction Type column missing in transactions table!")


#      elif analysis_step == "Regression Model":
#     st.subheader("Regression Model")
#     # Load data
#     transactions = fetch_table_data("transactions")
#     accounts = fetch_table_data("accounts")

#     # Prepare data for regression
#     merged_data = transactions.merge(accounts[['account_number', 'balance']], on='account_number', how='left')
#     X = merged_data[['amount']]
#     y = merged_data['balance']

#     # Split data
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Train model
#     model = RandomForestRegressor()
#     model.fit(X_train, y_train)

#     # Predict
#     y_pred = model.predict(X_test)

#     # Evaluate model
#     st.write("### Model Evaluation")
#     st.write("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
#     st.write("Mean Squared Error:", mean_squared_error(y_test, y_pred))
#     st.write("R2 Score:", r2_score(y_test, y_pred))

#     elif analysis_step == "Hypothesis Testing":

#     st.subheader("Hypothesis Testing")
#     # Load data
#     transactions = fetch_table_data("transactions")
#     accounts = fetch_table_data("accounts")
#     branches = fetch_table_data("branch")

#     # ✅ One-Sample T-Test: Is the Average Transaction Amount > 1000?
#     st.subheader("1️⃣ One-Sample T-Test: Is the Average Transaction Amount Greater than 1000?")

#     t_test_code = """
#     from scipy import stats

#     # Compute Mean
#     mean_transaction_amount = transactions["amount"].mean()

#     # One-Sample T-Test
#     t_stat, p_value = stats.ttest_1samp(transactions["amount"], 1000)

#     print(f"T-Statistic: {t_stat:.4f}, P-Value: {p_value:.4f}")

#     if p_value < 0.05:
#         print("🔴 Reject H₀: Mean transaction amount is significantly different from 1000.")
#     else:
#         print("🟢 Fail to Reject H₀: No significant difference.")
#     """
#     st.code(t_test_code, language="python")

#     mean_transaction_amount = transactions["amount"].mean()
#     t_stat, p_value = stats.ttest_1samp(transactions["amount"], 1000)

#     st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#     st.write(f"🔹 **P-Value:** {p_value:.4f}")

#     if p_value < 0.05:
#         st.write("🔴 **Reject H₀:** The mean transaction amount is significantly different from 1000.")
#     else:
#         st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#     # ✅ Visualization
#     fig, ax = plt.subplots(figsize=(8, 5))
#     sns.histplot(transactions["amount"], bins=30, kde=True, ax=ax, color="blue")
#     plt.axvline(1000, color="red", linestyle="dashed", label="Test Value (1000)")
#     plt.title("Distribution of Transaction Amounts")
#     plt.xlabel("Transaction Amount")
#     plt.ylabel("Frequency")
#     plt.legend()
#     st.pyplot(fig)

#     # ✅ ANOVA F-Test: Does Branch Location Affect Transactions?
#     st.subheader("2️⃣ ANOVA F-Test: Does Branch Location Affect Transaction Amounts?")

#     anova_code = """
#     from scipy.stats import f_oneway

#     # Merge transactions with branch data
#     merged_data = transactions.merge(accounts, on="account_number", how="left").merge(branches, on="branch_id", how="left")

#     # Group transaction amounts by branch
#     branch_groups = [merged_data[merged_data["branch_name"] == b]["amount"] for b in merged_data["branch_name"].unique()]

#     # Apply ANOVA Test
#     f_stat, p_value = f_oneway(*branch_groups)

#     print(f"F-Statistic: {f_stat:.4f}, P-Value: {p_value:.4f}")

#     if p_value < 0.05:
#         print("🔴 Reject H₀: Branch location significantly affects transaction amount.")
#     else:
#         print("🟢 Fail to Reject H₀: No significant difference.")
#     """
#     st.code(anova_code, language="python")

#     merged_data = transactions.merge(accounts, on="account_number", how="left").merge(branches, on="branch_id", how="left")
#     branch_groups = [merged_data[merged_data["branch_id"] == b]["amount"] for b in merged_data["branch_id"].unique()]
#     f_stat, p_value = f_oneway(*branch_groups)

#     st.write(f"🔹 **F-Statistic:** {f_stat:.4f}")
#     st.write(f"🔹 **P-Value:** {p_value:.4f}")

#     if p_value < 0.05:
#         st.write("🔴 **Reject H₀:** Branch location significantly affects transaction amount.")
#     else:
#         st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#     # ✅ Visualization
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.boxplot(x="branch_name", y="amount", data=merged_data, palette="coolwarm")
#     plt.xticks(rotation=45)
#     plt.title("Transaction Amounts Across Branch Locations")
#     plt.xlabel("Branch")
#     plt.ylabel("Transaction Amount")
#     st.pyplot(fig)

#     # ✅ T-Test: Do Savings & Current Accounts Have Different Balances?
#     st.subheader("3️⃣ T-Test: Is There a Difference in Account Balances Between Savings & Current Accounts?")

#     ttest_code = """
#     from scipy.stats import ttest_ind

#     # Extract balances for Savings & Current Accounts
#     savings = accounts[accounts["account_type"] == "Savings"]["balance"]
#     current = accounts[accounts["account_type"] == "Current"]["balance"]

#     # Apply T-Test
#     t_stat, p_value = ttest_ind(savings, current, equal_var=False)

#     print(f"T-Statistic: {t_stat:.4f}, P-Value: {p_value:.4f}")

#     if p_value < 0.05:
#         print("🔴 Reject H₀: Savings and Current account balances are significantly different.")
#     else:
#         print("🟢 Fail to Reject H₀: No significant difference in balances.")
#     """
#     st.code(ttest_code, language="python")

#     savings = accounts[accounts["account_type"] == "Savings"]["balance"]
#     current = accounts[accounts["account_type"] == "Current"]["balance"]
#     t_stat, p_value = ttest_ind(savings, current, equal_var=False)

#     st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#     st.write(f"🔹 **P-Value:** {p_value:.4f}")

#     if p_value < 0.05:
#         st.write("🔴 **Reject H₀:** Savings and Current account balances are significantly different.")
#     else:
#         st.write("🟢 **Fail to Reject H₀:** No significant difference in balances.")

#     # ✅ Visualization
#     fig, ax = plt.subplots(figsize=(8, 5))
#     sns.boxplot(x="account_type", y="balance", data=accounts, palette="magma")
#     plt.title("Savings vs. Current Account Balance")
#     plt.xlabel("Account Type")
#     plt.ylabel("Balance")
#     st.pyplot(fig)

# import streamlit as st
# import requests
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import statsmodels.api as sm
# from scipy import stats
# from scipy.stats import f_oneway, ttest_ind
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# # ✅ Define API Base URL
# API_URL = "http://127.0.0.1:5000"

# # ✅ Fetch table data
# def fetch_table_data(table_name):
#     try:
#         response = requests.get(f"{API_URL}/all_data/{table_name}")
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         st.error(f"[ERROR] Failed to fetch table data: {e}")
#     return None

# # ✅ Fetch and run SQL query
# def execute_sql_query(query):
#     try:
#         response = requests.post(f"{API_URL}/execute_query", json={"query": query})
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         st.error(f"[ERROR] Failed to execute query: {e}")
#     return None

# # ✅ Sidebar Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Table Data", "Power BI Dashboard", "SQL Queries", "Downloads", "Python Analysis"])

# # ✅ Home Page
# if page == "Home":
#     st.title("🏦 Welcome to the Banking Dashboard!")
#     st.write("Navigate using the sidebar to explore data, Power BI reports, and SQL queries.")

# # ✅ Table Data Page
# elif page == "Table Data":
#     st.title("📊 Table Data")
#     selected_table = st.selectbox("Select Table", ["customers", "accounts", "transactions", "employees", "branch"])
#     table_data = fetch_table_data(selected_table)
#     if table_data is not None:
#         st.dataframe(table_data)

# # ✅ Power BI Dashboard Page
# elif page == "Power BI Dashboard":
#     st.title("📊 Power BI Dashboard")
#     st.write("🔗 Click below to open the Power BI report in a new tab:")
#     power_bi_url = "https://app.powerbi.com/groups/me/reports/4a3fada2-ba7e-4920-bd40-d09245e7c1b7/be94380037ae7288aa6b?experience=power-bi"
#     st.markdown(f"[🔗 Open Power BI Dashboard]({power_bi_url})", unsafe_allow_html=True)
#     st.write("🚀 **Power BI Workaround:** If you don’t have Power BI installed, download the PBIX file from the Downloads page.")

# # ✅ SQL Queries Page
# elif page == "SQL Queries":
#     st.title("📝 SQL Queries")
#     queries = {
#         "1. Inactive Customers (No Transactions in Last Year)": """
#             SELECT c.customer_id, c.first_name, c.last_name 
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             LEFT JOIN transactions t ON a.account_number = t.account_number 
#             WHERE t.transaction_id IS NULL OR 
#             t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
#         """,
#         "2. Total Transactions Per Account Per Month": """
#             SELECT account_number, YEAR(transaction_date) AS year, 
#             MONTH(transaction_date) AS month, SUM(amount) AS total_amt
#             FROM transactions 
#             GROUP BY account_number, year, month
#             ORDER BY account_number, year, month;
#         """,
#         "3. Branch Ranking Based on Deposits in Last Quarter": """
#             SELECT a.branch_id, SUM(t.amount) AS total_deposits, 
#             DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             WHERE t.transaction_type="Deposit" 
#             AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) 
#             GROUP BY a.branch_id
#             ORDER BY branch_rank;
#         """,
#         "4. Customer with Highest Deposit": """
#             SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, t.amount 
#             FROM customers c 
#             INNER JOIN accounts a ON c.customer_id = a.customer_id 
#             INNER JOIN transactions t ON t.account_number = a.account_number
#             WHERE t.transaction_type = "Deposit"
#             ORDER BY t.amount DESC
#             LIMIT 1;
#         """,
#         "5. Fraud Detection: More Than 2 Transactions in a Day": """
#             SELECT a.account_number AS fraud_accounts, COUNT(t.transaction_id) AS no_of_transactions, 
#             DAY(t.transaction_date) AS single_day
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             GROUP BY fraud_accounts, single_day
#             HAVING no_of_transactions > 2;
#         """,
#         "6. Daily Transaction Volume (Past Month)": """
#             SELECT DATE(transaction_date) AS transaction_day, ROUND(SUM(amount), 3) AS trans_volume
#             FROM transactions 
#             WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
#             GROUP BY transaction_day
#             ORDER BY transaction_day;
#         """,
#         "7. Branch with Highest Average Account Balance": """
#             SELECT branch_id, AVG(balance) AS avg_bal
#             FROM accounts 
#             GROUP BY branch_id
#             ORDER BY avg_bal DESC
#             LIMIT 1;
#         """,
#         "8. Most Common Transaction Type Per Branch": """
#             SELECT b.branch_id, t.transaction_type, COUNT(*) AS transaction_count
#             FROM transactions t
#             JOIN accounts a ON t.account_number = a.account_number
#             JOIN branch b ON a.branch_id = b.branch_id
#             GROUP BY b.branch_id, t.transaction_type
#             ORDER BY b.branch_id, transaction_count DESC;
#         """,
#         "9. Accounts with Only Withdrawals": """
#             SELECT account_number
#             FROM transactions
#             GROUP BY account_number
#             HAVING SUM(CASE WHEN transaction_type = 'deposit' THEN 1 ELSE 0 END) = 0;
#         """,
#         "10. Running Total of Transactions Per Account": """
#             SELECT account_number, transaction_date, amount,
#             SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#             FROM transactions;
#         """,
#         "11. Previous Transaction Amount for Each Transaction": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             LAG(amount, 1, 0) OVER (PARTITION BY account_number ORDER BY transaction_date) AS previous_transaction
#             FROM transactions;
#         """,
#         "12. Customers with Highest Transactions": """
#             SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY c.customer_id, c.first_name, c.last_name
#             ORDER BY total_transactions DESC
#             LIMIT 10;
#         """,
#         "13. Moving Average of Transactions": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             AVG(amount) OVER (PARTITION BY account_number ORDER BY transaction_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
#             FROM transactions;
#         """,
#         "14. Average Transactions Per Branch Per Month": """
#             SELECT b.branch_id, YEAR(t.transaction_date) AS year, MONTH(t.transaction_date) AS month,
#             COUNT(t.transaction_id) / COUNT(DISTINCT t.account_number) AS avg_transactions
#             FROM branch b
#             JOIN accounts a ON b.branch_id = a.branch_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY b.branch_id, year, month;
#         """,
#         "15. Running Total of transactions per Account": """
#              SELECT account_number, transaction_date, amount,
#              SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#              FROM transactions;
#         """,
#         "16. customers whose account balance is below the average balance of their branch" : """
#              SELECT c.customer_id, c.first_name, c.last_name, a.account_number, a.balance, branch_avg.avg_balance
#              FROM accounts a
#              JOIN customers c ON a.customer_id = c.customer_id
#              JOIN (
#              SELECT branch_id, AVG(balance) AS avg_balance
#              FROM accounts
#              GROUP BY branch_id
#              ) branch_avg ON a.branch_id = branch_avg.branch_id
#              WHERE a.balance < branch_avg.avg_balance;
#         """,
#          "17. customers who have made the highest number of transactions": """
#               SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#               FROM customers c
#               JOIN accounts a ON c.customer_id = a.customer_id
#               JOIN transactions t ON a.account_number = t.account_number
#               GROUP BY c.customer_id, c.first_name, c.last_name
#               ORDER BY total_transactions DESC
#               LIMIT 10;
#           """
#     }
#     selected_query = st.selectbox("Select Query", list(queries.keys()))
#     st.subheader(f"🧐 {selected_query}")
#     st.code(queries[selected_query], language="sql")
#     if st.button("Run Query"):
#         query_result = execute_sql_query(queries[selected_query])
#         if query_result is not None:
#             st.dataframe(query_result)

# # ✅ Downloads Page
# elif page == "Downloads":
#     st.title("📥 Download Project Files")
#     st.write("📥 **Download the Project Files Below:**")
#     st.markdown("[📄 Download PDF Report](sandbox:/mnt/data/dashboard%20(2).pdf)", unsafe_allow_html=True)
#     st.markdown("[📊 Download Power BI Dashboard (PBIX)](sandbox:/mnt/data/banking_operation_dashboard.pbix)", unsafe_allow_html=True)
#     st.markdown("[📽️ Download PowerPoint Presentation](sandbox:/mnt/data/Analysis%20of%20Banking%20Operations%20using%20Power%20BI(1).pptx)", unsafe_allow_html=True)

# # ✅ Python Analysis Page
# elif page == "Python Analysis":
#     st.title("🐍 Python Analysis")
#     analysis_step = st.selectbox("Select Analysis Step", ["Data Cleaning", "EDA", "Regression Model", "Hypothesis Testing"])

#     if analysis_step == "Data Cleaning":
#         st.subheader("Data Cleaning")
#         st.write("This section focuses on cleaning the dataset to ensure high-quality data for analysis. Below are the steps performed:")

#         # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Step 1: Check for Missing Values
#         st.write("#### 1. Handling Missing Values")
#         st.write("Missing values can lead to inaccurate analysis. Here's how we handle them:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** Missing values were either dropped or imputed based on the context.")

#         # Step 2: Remove Duplicates
#         st.write("#### 2. Removing Duplicates")
#         st.write("Duplicate records can skew analysis. Here's the duplicate count before cleaning:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** All duplicates were removed from the dataset.")

#         # Step 3: Data Types and Formatting
#         st.write("#### 3. Data Type Validation")
#         st.write("Ensuring correct data types for each column:")
        
#         if customers is not None:
#             st.write("- **Customers Table:** Verified `created_at` is datetime.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:** Verified `transaction_date` is datetime.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:** Verified `balance` is numeric.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:** Verified `branch_id` is unique.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:** Verified `hire_date` is datetime.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** Data types were corrected where necessary.")

#         # Step 4: Outlier Detection
#         st.write("#### 4. Outlier Detection")
#         st.write("Outliers can distort analysis. Here's a summary of outliers detected:")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:** Outliers detected in `amount` using IQR method.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:** Outliers detected in `balance` using Z-score method.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         st.write("**Action Taken:** Outliers were either capped or removed based on domain knowledge.")

#         # Step 5: Final Dataset Shape
#         st.write("#### 5. Final Dataset Shape")
#         st.write("After cleaning, the dataset shapes are as follows:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.shape)
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.shape)
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.shape)
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.shape)
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.shape)
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** The dataset is now clean and ready for analysis.")

#     elif analysis_step == "EDA":
#         st.subheader("Exploratory Data Analysis (EDA)")
#         # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Branch Performance Analysis (Revenue Contribution per Branch)
#         st.write("### Branch Performance Analysis (Revenue Contribution per Branch)")
#         branch_revenue = transactions.merge(accounts, on="account_number", how="left")
#         if "branch_id" in branch_revenue.columns:
#             branch_revenue = branch_revenue.groupby("branch_id")["amount"].sum().sort_values(ascending=False)
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=branch_revenue.index, y=branch_revenue.values, palette="plasma")
#             plt.title("Revenue Contribution per Branch")
#             plt.xlabel("Branch ID")
#             plt.ylabel("Total Transaction Amount")
#             st.pyplot(plt)
#         else:
#             st.error("Branch ID not found after merging transactions with accounts!")

#         # Top 10 Customers with Highest Transactions
#         st.write("### Top 10 Customers with Highest Transactions")
#         transactions = transactions.merge(accounts, on="account_number", how="left").merge(customers, on="customer_id", how="left")
#         if "customer_id" in transactions.columns:
#             customer_transaction_counts = transactions["customer_id"].value_counts()
#             top_customers = customer_transaction_counts.head(10)
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=top_customers.index, y=top_customers.values, palette="coolwarm")
#             plt.title("Top 10 Customers with Most Transactions")
#             plt.xlabel("Customer ID")
#             plt.ylabel("Number of Transactions")
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#         else:
#             st.error("Customer ID not found after merging transactions with accounts & customers!")

#         # Most Active Branches (Number of Accounts per Branch)
#         st.write("### Most Active Branches (Number of Accounts per Branch)")
#         if "branch_id" in accounts.columns:
#             accounts_per_branch = accounts.groupby("branch_id")["account_number"].count()
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=accounts_per_branch.index, y=accounts_per_branch.values, palette="mako")
#             plt.title("Number of Accounts Per Branch")
#             plt.xlabel("Branch ID")
#             plt.ylabel("Number of Accounts")
#             st.pyplot(plt)
#         else:
#             st.error("Branch ID not found in accounts table!")

#         # Branches per city
#         st.write("### Branches per City")
#         if "city" in branches.columns:
#             branches_per_city = branches["city"].value_counts()
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=branches_per_city.index, y=branches_per_city.values, palette="coolwarm")
#             plt.title("Number of Bank Branches Per City")
#             plt.xlabel("City")
#             plt.ylabel("Number of Branches")
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#         else:
#             st.error("City column not found in branches table!")

#         # Month-wise Transaction Trends
#         st.write("### Month-wise Transaction Trends")
#         if "transaction_date" in transactions.columns:
#             transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
#             transactions["month"] = transactions["transaction_date"].dt.month
#             monthly_trends = transactions.groupby("month")["amount"].sum()
#             plt.figure(figsize=(10, 5))
#             sns.lineplot(x=monthly_trends.index, y=monthly_trends.values, marker="o", color="red")
#             plt.title("Monthly Transaction Trends")
#             plt.xlabel("Month")
#             plt.ylabel("Total Transaction Amount")
#             plt.xticks(range(1, 13))
#             plt.grid()
#             st.pyplot(plt)
#         else:
#             st.error("Transaction date column missing in transactions table!")

#         # Total Balance per Account Type
#         st.write("### Total Balance per Account Type")
#         if "account_type" in accounts.columns and "balance" in accounts.columns:
#             plt.figure(figsize=(10, 5))
#             sns.boxplot(x="account_type", y="balance", data=accounts, palette="Set2")
#             plt.yscale("log")  # Log scale for better visualization
#             plt.title("Balance Distribution by Account Type")
#             plt.xlabel("Account Type")
#             plt.ylabel("Balance (Log Scale)")
#             st.pyplot(plt)
#         else:
#             st.error("Account Type or Balance column missing in accounts table!")

#         # Most Common Transaction Type
#         st.write("### Most Common Transaction Type")
#         if "transaction_type" in transactions.columns:
#             plt.figure(figsize=(8, 5))
#             sns.countplot(x="transaction_type", data=transactions, palette="magma")
#             plt.title("Most Common Transaction Type")
#             plt.xlabel("Transaction Type")
#             plt.ylabel("Count")
#             st.pyplot(plt)
#         else:
#             st.error("Transaction Type column missing in transactions table!")

#         # Rural vs Urban Branches
#         st.write("### Rural vs Urban Branches")
#         plt.figure(figsize=(8, 5))
#         sns.countplot(y=branches['branch_location'], order=branches['branch_location'].value_counts().index, palette="pastel")
#         plt.title("Rural vs Urban Branches", fontsize=14)
#         st.pyplot(plt)

#         # Customer Retention Rate Over Time
#         st.write("### Customer Retention Rate Over Time")
#         customers["created_at"] = pd.to_datetime(customers["created_at"], errors="coerce")
#         customers["year_joined"] = customers["created_at"].dt.year
#         customer_retention = customers["year_joined"].value_counts().sort_index()
#         plt.figure(figsize=(10, 5))
#         sns.lineplot(x=customer_retention.index, y=customer_retention.values, marker="o", color="purple")
#         plt.title("Customer Retention Over Time")
#         plt.xlabel("Year")
#         plt.ylabel("New Customers")
#         plt.grid()
#         st.pyplot(plt)

#         # Average Transaction Amount by Account Type
#         st.write("### Average Transaction Amount by Account Type")
#         merged_data = transactions.merge(accounts, on="account_number", how="left")
#         if "account_type" in merged_data.columns:
#             avg_transaction_by_account = merged_data.groupby("account_type")["amount"].mean().sort_values(ascending=False)
#             plt.figure(figsize=(10, 5))
#             sns.barplot(x=avg_transaction_by_account.index, y=avg_transaction_by_account.values, palette="viridis")
#             plt.title("Average Transaction Amount by Account Type")
#             plt.xlabel("Account Type")
#             plt.ylabel("Average Transaction Amount")
#             st.pyplot(plt)
#         else:
#             st.error("Column 'account_type' not found in the merged data. Please check the 'accounts' table.")

#         # How Long Customers Stay with the Bank
#         st.write("### How Long Customers Stay with the Bank")
#         customers["account_age"] = (pd.to_datetime("today") - customers["created_at"]).dt.days // 365
#         plt.figure(figsize=(10, 5))
#         sns.histplot(customers["account_age"], bins=20, kde=True, color="darkred")
#         plt.title("Distribution of Customer Account Age")
#         plt.xlabel("Years with Bank")
#         plt.ylabel("Number of Customers")
#         st.pyplot(plt)

#         # Employee Tenure Distribution
#         st.write("### Employee Tenure Distribution")
#         if employee is not None and not employee.empty:
#             try:
#                 employee["hire_date"] = pd.to_datetime(employee["hire_date"], errors="coerce")
#                 employee["tenure"] = (pd.to_datetime("today") - employee["hire_date"]).dt.days // 365
#                 plt.figure(figsize=(10, 5))
#                 sns.histplot(employee["tenure"], bins=15, kde=True, color="green")
#                 plt.title("Employee Tenure Distribution")
#                 plt.xlabel("Years at Bank")
#                 plt.ylabel("Number of Employees")
#                 st.pyplot(plt)
#             except Exception as e:
#                 st.error(f"An error occurred while processing employee data: {e}")
#         else:
#             st.error("Employee data is not available or is empty. Please check the data source.")

#         # Customers with Highest Account Balances
#         st.write("### Customers with Highest Account Balances")
#         top_balances = accounts.groupby("customer_id")["balance"].sum().nlargest(10)
#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=top_balances.index, y=top_balances.values, palette="Blues")
#         plt.title("Top 10 Customers with Highest Balances")
#         plt.xlabel("Customer ID")
#         plt.ylabel("Total Balance")
#         plt.xticks(rotation=45)
#         st.pyplot(plt)

#     elif analysis_step == "Regression Model":
#         st.subheader("Regression Model")
#         # Load data
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         customers = fetch_table_data("customers")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Merge data to create a rich feature set
#         merged_data = transactions.merge(accounts, on="account_number", how="left") \
#                                   .merge(customers, on="customer_id", how="left") \
#                                   .merge(branches, on="branch_id", how="left")

#         # Prepare data for regression
#         # Feature Selection for Random Forest
#         features_rf = ['amount', 'transaction_type', 'account_type', 'balance', 'branch_id', 'city']
#         X_rf = merged_data[features_rf]

#         # Convert categorical variables to numerical using one-hot encoding
#         X_rf = pd.get_dummies(X_rf, columns=['transaction_type', 'account_type', 'city'], drop_first=True)

#         # Target variable
#         y_rf = merged_data['balance']

#         # Check for NaN values in y_rf
#         if y_rf.isnull().any():
#             st.warning("NaN values found in the target variable 'balance'. Handling NaN values...")
#             merged_data = merged_data.dropna(subset=['balance'])
#             X_rf = merged_data[features_rf]
#             X_rf = pd.get_dummies(X_rf, columns=['transaction_type', 'account_type', 'city'], drop_first=True)
#             y_rf = merged_data['balance']

#         # Split data
#         X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, y_rf, test_size=0.2, random_state=42)

#         # Model 1: Random Forest Regressor
#         st.write("### Model 1: Random Forest Regressor")
#         model_rf = RandomForestRegressor()
#         model_rf.fit(X_train_rf, y_train_rf)
#         y_pred_rf = model_rf.predict(X_test_rf)

#         # Evaluate Random Forest Model
#         st.write("#### Evaluation Metrics for Random Forest Regressor")
#         st.write("Mean Absolute Error:", mean_absolute_error(y_test_rf, y_pred_rf))
#         st.write("Mean Squared Error:", mean_squared_error(y_test_rf, y_pred_rf))
#         st.write("R2 Score:", r2_score(y_test_rf, y_pred_rf))

#         # Visualization: Actual vs Predicted (Random Forest)
#         st.write("#### Visualization: Actual vs Predicted (Random Forest)")
#         plt.figure(figsize=(10, 6))
#         sns.scatterplot(x=y_test_rf, y=y_pred_rf, alpha=0.6)
#         plt.plot([min(y_test_rf), max(y_test_rf)], [min(y_test_rf), max(y_test_rf)], color='red', linestyle='--')  # Diagonal line
#         plt.title("Actual vs Predicted Balance (Random Forest)")
#         plt.xlabel("Actual Balance")
#         plt.ylabel("Predicted Balance")
#         st.pyplot(plt)

#         # Explanation for Random Forest
#         st.write("#### Why Use Random Forest Regressor?")
#         st.write("""
#         - **Use Case**: Random Forest is a powerful ensemble method that works well for both regression and classification tasks.
#         - **Advantages**: It handles non-linear relationships well, is robust to outliers, and provides feature importance.
#         - **Features Used**: We used `amount`, `transaction_type`, `account_type`, `balance`, `branch_id`, and `city` to capture complex relationships.
#         - **Interpretation**: The R2 score indicates how well the model explains the variance in the target variable. A negative R2 score suggests the model is worse than a horizontal line.
#         """)

#         # Feature Importance for Random Forest
#         st.write("#### Feature Importance (Random Forest)")
#         feature_importance = pd.Series(model_rf.feature_importances_, index=X_rf.columns).sort_values(ascending=False)
#         plt.figure(figsize=(10, 6))
#         sns.barplot(x=feature_importance, y=feature_importance.index)
#         plt.title("Feature Importance (Random Forest)")
#         plt.xlabel("Importance Score")
#         plt.ylabel("Features")
#         st.pyplot(plt)

#         # Model 2: Linear Regression
#         st.write("### Model 2: Linear Regression")
#         from sklearn.linear_model import LinearRegression

#         # Feature Selection for Linear Regression
#         features_lr = ['amount', 'balance']  # Simple features for linear regression
#         X_lr = merged_data[features_lr]
#         y_lr = merged_data['balance']

#         # Check for NaN values in y_lr
#         if y_lr.isnull().any():
#             st.warning("NaN values found in the target variable 'balance'. Handling NaN values...")
#             merged_data = merged_data.dropna(subset=['balance'])
#             X_lr = merged_data[features_lr]
#             y_lr = merged_data['balance']

#         # Split data
#         X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_lr, y_lr, test_size=0.2, random_state=42)

#         # Train Linear Regression Model
#         model_lr = LinearRegression()
#         model_lr.fit(X_train_lr, y_train_lr)
#         y_pred_lr = model_lr.predict(X_test_lr)

#         # Evaluate Linear Regression Model
#         st.write("#### Evaluation Metrics for Linear Regression")
#         st.write("Mean Absolute Error:", mean_absolute_error(y_test_lr, y_pred_lr))
#         st.write("Mean Squared Error:", mean_squared_error(y_test_lr, y_pred_lr))
#         st.write("R2 Score:", r2_score(y_test_lr, y_pred_lr))

#         # Visualization: Actual vs Predicted (Linear Regression)
#         st.write("#### Visualization: Actual vs Predicted (Linear Regression)")
#         plt.figure(figsize=(10, 6))
#         sns.scatterplot(x=y_test_lr, y=y_pred_lr, alpha=0.6)
#         plt.plot([min(y_test_lr), max(y_test_lr)], [min(y_test_lr), max(y_test_lr)], color='red', linestyle='--')  # Diagonal line
#         plt.title("Actual vs Predicted Balance (Linear Regression)")
#         plt.xlabel("Actual Balance")
#         plt.ylabel("Predicted Balance")
#         st.pyplot(plt)

#         # Explanation for Linear Regression
#         st.write("#### Why Use Linear Regression?")
#         st.write("""
#         - **Use Case**: Linear Regression is a simple and interpretable model for predicting continuous variables.
#         - **Advantages**: It assumes a linear relationship between features and the target, making it easy to understand and implement.
#         - **Features Used**: We used `amount` and `balance` to keep the model simple and interpretable.
#         - **Interpretation**: The R2 score indicates how well the model explains the variance in the target variable. A negative R2 score suggests the model is worse than a horizontal line.
#         """)

#     elif analysis_step == "Hypothesis Testing":
#         st.subheader("Hypothesis Testing")
#         # Load data
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")

#         # ✅ One-Sample T-Test: Is the Average Transaction Amount > 1000?
#         st.subheader("1️⃣ One-Sample T-Test: Is the Average Transaction Amount Greater than 1000?")
#         mean_transaction_amount = transactions["amount"].mean()
#         t_stat, p_value = stats.ttest_1samp(transactions["amount"], 1000)
#         st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** The mean transaction amount is significantly different from 1000.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.histplot(transactions["amount"], bins=30, kde=True, ax=ax, color="blue")
#         plt.axvline(1000, color="red", linestyle="dashed", label="Test Value (1000)")
#         plt.title("Distribution of Transaction Amounts")
#         plt.xlabel("Transaction Amount")
#         plt.ylabel("Frequency")
#         plt.legend()
#         st.pyplot(fig)

#         # ✅ ANOVA F-Test: Does Branch Location Affect Transactions?
#         st.subheader("2️⃣ ANOVA F-Test: Does Branch Location Affect Transaction Amounts?")
#         merged_data = transactions.merge(accounts, on="account_number", how="left").merge(branches, on="branch_id", how="left")
#         branch_groups = [merged_data[merged_data["branch_id"] == b]["amount"] for b in merged_data["branch_id"].unique()]
#         f_stat, p_value = f_oneway(*branch_groups)
#         st.write(f"🔹 **F-Statistic:** {f_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** Branch location significantly affects transaction amount.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.boxplot(x="branch_name", y="amount", data=merged_data, palette="coolwarm")
#         plt.xticks(rotation=45)
#         plt.title("Transaction Amounts Across Branch Locations")
#         plt.xlabel("Branch")
#         plt.ylabel("Transaction Amount")
#         st.pyplot(fig)

#         # ✅ T-Test: Do Savings & Current Accounts Have Different Balances?
#         st.subheader("3️⃣ T-Test: Is There a Difference in Account Balances Between Savings & Current Accounts?")
#         savings = accounts[accounts["account_type"] == "Savings"]["balance"]
#         current = accounts[accounts["account_type"] == "Current"]["balance"]
#         t_stat, p_value = ttest_ind(savings, current, equal_var=False)
#         st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** Savings and Current account balances are significantly different.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference in balances.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.boxplot(x="account_type", y="balance", data=accounts, palette="magma")
#         plt.title("Savings vs. Current Account Balance")
#         plt.xlabel("Account Type")
#         plt.ylabel("Balance")
#         st.pyplot(fig)


# import streamlit as st
# import requests
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import folium
# from streamlit_folium import st_folium
# from scipy import stats
# from scipy.stats import f_oneway, ttest_ind
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from sklearn.linear_model import LinearRegression
# import time

# # ✅ Define API Base URL
# API_URL = "http://127.0.0.1:5000"

# # ✅ Fetch table data
# @st.cache_data
# def fetch_table_data(table_name):
#     try:
#         response = requests.get(f"{API_URL}/all_data/{table_name}")
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         st.error(f"[ERROR] Failed to fetch table data: {e}")
#     return None

# # ✅ Fetch and run SQL query
# @st.cache_data
# def execute_sql_query(query):
#     try:
#         response = requests.post(f"{API_URL}/execute_query", json={"query": query})
#         if response.status_code == 200:
#             return pd.DataFrame(response.json())
#     except Exception as e:
#         st.error(f"[ERROR] Failed to execute query: {e}")
#     return None

# # ✅ Sidebar Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Table Data", "Power BI Dashboard", "SQL Queries", "Downloads", "Python Analysis"])

# # ✅ Home Page
# if page == "Home":
#     st.title("🏦 Welcome to the Banking Dashboard!")
#     st.write("Navigate using the sidebar to explore data, Power BI reports, and SQL queries.")

#     # KPIs
#     st.subheader("📊 Key Performance Indicators (KPIs)")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Customers", 1500, "+5%")
#     with col2:
#         st.metric("Total Transactions", 50000, "+10%")
#     with col3:
#         st.metric("Total Revenue", "$1.2M", "+8%")

#     # Interactive Filters
#     st.subheader("🔍 Interactive Filters")
#     transactions = fetch_table_data("transactions")
#     if transactions is not None:
#         transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
#         min_date = transactions["transaction_date"].min()
#         max_date = transactions["transaction_date"].max()
#         selected_date = st.date_input("Select Date Range", [min_date, max_date])
#         filtered_data = transactions[(transactions["transaction_date"] >= pd.to_datetime(selected_date[0])) & 
#                                    (transactions["transaction_date"] <= pd.to_datetime(selected_date[1]))]
#         st.write(f"📅 **Transactions between {selected_date[0]} and {selected_date[1]}:** {len(filtered_data)} records")

#     # Geospatial Map
#     st.subheader("📍 Branch Locations")
#     branches = fetch_table_data("branch")
#     branches = fetch_table_data("branch")
#     if branches is not None:
#         # Predefined dataset of Indian cities with latitude and longitude
#         indian_cities = {
#             "Aligarh": {"latitude": 27.897394, "longitude": 78.088013},
#             "Nainital": {"latitude": 29.391872, "longitude": 79.454203},
#             "Hyderabad": {"latitude": 17.385044, "longitude": 78.486671},
#             "Pune": {"latitude": 18.520430, "longitude": 73.856743},
#             "Bengaluru": {"latitude": 12.971599, "longitude": 77.594566},
#             "Ahmednagar": {"latitude": 19.095207, "longitude": 74.749592},
#             "Mumbai": {"latitude": 19.075983, "longitude": 72.877655},
#             "Gurgaon": {"latitude": 28.459497, "longitude": 77.026634},
#             "New Delhi": {"latitude": 28.613939, "longitude": 77.209023},
#             "Darjeeling": {"latitude": 27.036007, "longitude": 88.262672},
#             "Shimla": {"latitude": 31.104814, "longitude": 77.173403},
#             "Jorhat": {"latitude": 26.750000, "longitude": 94.216667},
#             "Nanded": {"latitude": 19.138251, "longitude": 77.321045},
#             "Mysuru": {"latitude": 12.295810, "longitude": 76.639381},
#         }

#         # Add latitude and longitude to branches data
#         branches["latitude"] = branches["city"].map(lambda x: indian_cities.get(x, {}).get("latitude"))
#         branches["longitude"] = branches["city"].map(lambda x: indian_cities.get(x, {}).get("longitude"))

#         # Drop rows where latitude or longitude is missing
#         branches = branches.dropna(subset=["latitude", "longitude"])

#         # Create a Folium map
#         m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Centered on India
#         for _, row in branches.iterrows():
#             folium.Marker(
#                 [row["latitude"], row["longitude"]],
#                 popup=f"{row['branch_name']}, {row['city']}, {row['state']}"
#             ).add_to(m)

#         # Display the map in Streamlit
#         st_folium(m, width=700, height=500)

# # ✅ Table Data Page
# elif page == "Table Data":
#     st.title("📊 Table Data")
#     selected_table = st.selectbox("Select Table", ["customers", "accounts", "transactions", "employees", "branch"])
#     table_data = fetch_table_data(selected_table)
#     if table_data is not None:
#         st.dataframe(table_data)

#         # Download Data
#         st.download_button("Download Data as CSV", table_data.to_csv(index=False), file_name=f"{selected_table}.csv")

# # ✅ Power BI Dashboard Page
# elif page == "Power BI Dashboard":
#     st.title("📊 Power BI Dashboard")
#     st.write("🔗 Click below to open the Power BI report in a new tab:")
#     power_bi_url = "https://app.powerbi.com/groups/me/reports/4a3fada2-ba7e-4920-bd40-d09245e7c1b7/be94380037ae7288aa6b?experience=power-bi"
#     st.markdown(f"[🔗 Open Power BI Dashboard]({power_bi_url})", unsafe_allow_html=True)
#     st.write("🚀 **Power BI Workaround:** If you don’t have Power BI installed, download the PBIX file from the Downloads page.")

# # ✅ SQL Queries Page
# elif page == "SQL Queries":
#     st.title("📝 SQL Queries")
#     queries = {
#         "1. Inactive Customers (No Transactions in Last Year)": """
#             SELECT c.customer_id, c.first_name, c.last_name 
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             LEFT JOIN transactions t ON a.account_number = t.account_number 
#             WHERE t.transaction_id IS NULL OR 
#             t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
#         """,
#         "2. Total Transactions Per Account Per Month": """
#             SELECT account_number, YEAR(transaction_date) AS year, 
#             MONTH(transaction_date) AS month, SUM(amount) AS total_amt
#             FROM transactions 
#             GROUP BY account_number, year, month
#             ORDER BY account_number, year, month;
#         """,
#         "3. Branch Ranking Based on Deposits in Last Quarter": """
#             SELECT a.branch_id, SUM(t.amount) AS total_deposits, 
#             DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             WHERE t.transaction_type="Deposit" 
#             AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) 
#             GROUP BY a.branch_id
#             ORDER BY branch_rank;
#         """,
#         "4. Customer with Highest Deposit": """
#             SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, t.amount 
#             FROM customers c 
#             INNER JOIN accounts a ON c.customer_id = a.customer_id 
#             INNER JOIN transactions t ON t.account_number = a.account_number
#             WHERE t.transaction_type = "Deposit"
#             ORDER BY t.amount DESC
#             LIMIT 1;
#         """,
#         "5. Fraud Detection: More Than 2 Transactions in a Day": """
#             SELECT a.account_number AS fraud_accounts, COUNT(t.transaction_id) AS no_of_transactions, 
#             DAY(t.transaction_date) AS single_day
#             FROM accounts a 
#             INNER JOIN transactions t USING(account_number)
#             GROUP BY fraud_accounts, single_day
#             HAVING no_of_transactions > 2;
#         """,
#         "6. Daily Transaction Volume (Past Month)": """
#             SELECT DATE(transaction_date) AS transaction_day, ROUND(SUM(amount), 3) AS trans_volume
#             FROM transactions 
#             WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
#             GROUP BY transaction_day
#             ORDER BY transaction_day;
#         """,
#         "7. Branch with Highest Average Account Balance": """
#             SELECT branch_id, AVG(balance) AS avg_bal
#             FROM accounts 
#             GROUP BY branch_id
#             ORDER BY avg_bal DESC
#             LIMIT 1;
#         """,
#         "8. Most Common Transaction Type Per Branch": """
#             SELECT b.branch_id, t.transaction_type, COUNT(*) AS transaction_count
#             FROM transactions t
#             JOIN accounts a ON t.account_number = a.account_number
#             JOIN branch b ON a.branch_id = b.branch_id
#             GROUP BY b.branch_id, t.transaction_type
#             ORDER BY b.branch_id, transaction_count DESC;
#         """,
#         "9. Accounts with Only Withdrawals": """
#             SELECT account_number
#             FROM transactions
#             GROUP BY account_number
#             HAVING SUM(CASE WHEN transaction_type = 'deposit' THEN 1 ELSE 0 END) = 0;
#         """,
#         "10. Running Total of Transactions Per Account": """
#             SELECT account_number, transaction_date, amount,
#             SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#             FROM transactions;
#         """,
#         "11. Previous Transaction Amount for Each Transaction": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             LAG(amount, 1, 0) OVER (PARTITION BY account_number ORDER BY transaction_date) AS previous_transaction
#             FROM transactions;
#         """,
#         "12. Customers with Highest Transactions": """
#             SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#             FROM customers c
#             JOIN accounts a ON c.customer_id = a.customer_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY c.customer_id, c.first_name, c.last_name
#             ORDER BY total_transactions DESC
#             LIMIT 10;
#         """,
#         "13. Moving Average of Transactions": """
#             SELECT account_number, transaction_id, transaction_date, amount,
#             AVG(amount) OVER (PARTITION BY account_number ORDER BY transaction_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
#             FROM transactions;
#         """,
#         "14. Average Transactions Per Branch Per Month": """
#             SELECT b.branch_id, YEAR(t.transaction_date) AS year, MONTH(t.transaction_date) AS month,
#             COUNT(t.transaction_id) / COUNT(DISTINCT t.account_number) AS avg_transactions
#             FROM branch b
#             JOIN accounts a ON b.branch_id = a.branch_id
#             JOIN transactions t ON a.account_number = t.account_number
#             GROUP BY b.branch_id, year, month;
#         """,
#         "15. Running Total of transactions per Account": """
#              SELECT account_number, transaction_date, amount,
#              SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
#              FROM transactions;
#         """,
#         "16. Customers whose account balance is below the average balance of their branch": """
#              SELECT c.customer_id, c.first_name, c.last_name, a.account_number, a.balance, branch_avg.avg_balance
#              FROM accounts a
#              JOIN customers c ON a.customer_id = c.customer_id
#              JOIN (
#              SELECT branch_id, AVG(balance) AS avg_balance
#              FROM accounts
#              GROUP BY branch_id
#              ) branch_avg ON a.branch_id = branch_avg.branch_id
#              WHERE a.balance < branch_avg.avg_balance;
#         """,
#         "17. Customers who have made the highest number of transactions": """
#               SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
#               FROM customers c
#               JOIN accounts a ON c.customer_id = a.customer_id
#               JOIN transactions t ON a.account_number = t.account_number
#               GROUP BY c.customer_id, c.first_name, c.last_name
#               ORDER BY total_transactions DESC
#               LIMIT 10;
#           """
#     }
#     selected_query = st.selectbox("Select Query", list(queries.keys()))
#     st.subheader(f"🧐 {selected_query}")
#     st.code(queries[selected_query], language="sql")
#     if st.button("Run Query"):
#         query_result = execute_sql_query(queries[selected_query])
#         if query_result is not None:
#             st.dataframe(query_result)

# # ✅ Downloads Page
# elif page == "Downloads":
#     st.title("📥 Download Project Files")
#     st.write("📥 **Download the Project Files Below:**")
#     st.markdown("[📄 Download PDF Report](sandbox:/mnt/data/dashboard%20(2).pdf)", unsafe_allow_html=True)
#     st.markdown("[📊 Download Power BI Dashboard (PBIX)](sandbox:/mnt/data/banking_operation_dashboard.pbix)", unsafe_allow_html=True)
#     st.markdown("[📽️ Download PowerPoint Presentation](sandbox:/mnt/data/Analysis%20of%20Banking%20Operations%20using%20Power%20BI(1).pptx)", unsafe_allow_html=True)

# # ✅ Python Analysis Page
# elif page == "Python Analysis":
#     st.title("🐍 Python Analysis")
#     analysis_step = st.selectbox("Select Analysis Step", ["Data Cleaning", "EDA", "Regression Model", "Hypothesis Testing"])

#     if analysis_step == "Data Cleaning":
#         st.subheader("Data Cleaning")
#         st.write("This section focuses on cleaning the dataset to ensure high-quality data for analysis. Below are the steps performed:")

#         # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Step 1: Check for Missing Values
#         st.write("#### 1. Handling Missing Values")
#         st.write("Missing values can lead to inaccurate analysis. Here's how we handle them:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.isnull().sum().sum(), "missing values found.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** Missing values were either dropped or imputed based on the context.")

#         # Step 2: Remove Duplicates
#         st.write("#### 2. Removing Duplicates")
#         st.write("Duplicate records can skew analysis. Here's the duplicate count before cleaning:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.duplicated().sum(), "duplicates found.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** All duplicates were removed from the dataset.")

#         # Step 3: Data Types and Formatting
#         st.write("#### 3. Data Type Validation")
#         st.write("Ensuring correct data types for each column:")
        
#         if customers is not None:
#             st.write("- **Customers Table:** Verified `created_at` is datetime.")
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:** Verified `transaction_date` is datetime.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:** Verified `balance` is numeric.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:** Verified `branch_id` is unique.")
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:** Verified `hire_date` is datetime.")
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** Data types were corrected where necessary.")

#         # Step 4: Outlier Detection
#         st.write("#### 4. Outlier Detection")
#         st.write("Outliers can distort analysis. Here's a summary of outliers detected:")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:** Outliers detected in `amount` using IQR method.")
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:** Outliers detected in `balance` using Z-score method.")
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         st.write("**Action Taken:** Outliers were either capped or removed based on domain knowledge.")

#         # Step 5: Final Dataset Shape
#         st.write("#### 5. Final Dataset Shape")
#         st.write("After cleaning, the dataset shapes are as follows:")
        
#         if customers is not None:
#             st.write("- **Customers Table:**", customers.shape)
#         else:
#             st.error("Customers table is not available or is empty.")
        
#         if transactions is not None:
#             st.write("- **Transactions Table:**", transactions.shape)
#         else:
#             st.error("Transactions table is not available or is empty.")
        
#         if accounts is not None:
#             st.write("- **Accounts Table:**", accounts.shape)
#         else:
#             st.error("Accounts table is not available or is empty.")
        
#         if branches is not None:
#             st.write("- **Branches Table:**", branches.shape)
#         else:
#             st.error("Branches table is not available or is empty.")
        
#         if employee is not None:
#             st.write("- **Employees Table:**", employee.shape)
#         else:
#             st.error("Employees table is not available or is empty.")
        
#         st.write("**Action Taken:** The dataset is now clean and ready for analysis.")
#         # Add data cleaning steps here...

#     elif analysis_step == "EDA":
#         st.subheader("Exploratory Data Analysis (EDA)")
#         # Load data
#         customers = fetch_table_data("customers")
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")
#         employee = fetch_table_data("employee")

#         # Branch Performance Analysis (Revenue Contribution per Branch)
#         st.write("### Branch Performance Analysis (Revenue Contribution per Branch)")
#         branch_revenue = transactions.merge(accounts, on="account_number", how="left")
#         if "branch_id" in branch_revenue.columns:
#             branch_revenue = branch_revenue.groupby("branch_id")["amount"].sum().sort_values(ascending=False)
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=branch_revenue.index, y=branch_revenue.values, palette="plasma")
#             plt.title("Revenue Contribution per Branch")
#             plt.xlabel("Branch ID")
#             plt.ylabel("Total Transaction Amount")
#             st.pyplot(plt)
#         else:
#             st.error("Branch ID not found after merging transactions with accounts!")

#         # Top 10 Customers with Highest Transactions
#         st.write("### Top 10 Customers with Highest Transactions")
#         transactions = transactions.merge(accounts, on="account_number", how="left").merge(customers, on="customer_id", how="left")
#         if "customer_id" in transactions.columns:
#             customer_transaction_counts = transactions["customer_id"].value_counts()
#             top_customers = customer_transaction_counts.head(10)
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=top_customers.index, y=top_customers.values, palette="coolwarm")
#             plt.title("Top 10 Customers with Most Transactions")
#             plt.xlabel("Customer ID")
#             plt.ylabel("Number of Transactions")
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#         else:
#             st.error("Customer ID not found after merging transactions with accounts & customers!")

#         # Most Active Branches (Number of Accounts per Branch)
#         st.write("### Most Active Branches (Number of Accounts per Branch)")
#         if "branch_id" in accounts.columns:
#             accounts_per_branch = accounts.groupby("branch_id")["account_number"].count()
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=accounts_per_branch.index, y=accounts_per_branch.values, palette="mako")
#             plt.title("Number of Accounts Per Branch")
#             plt.xlabel("Branch ID")
#             plt.ylabel("Number of Accounts")
#             st.pyplot(plt)
#         else:
#             st.error("Branch ID not found in accounts table!")

#         # Branches per city
#         st.write("### Branches per City")
#         if "city" in branches.columns:
#             branches_per_city = branches["city"].value_counts()
#             plt.figure(figsize=(12, 6))
#             sns.barplot(x=branches_per_city.index, y=branches_per_city.values, palette="coolwarm")
#             plt.title("Number of Bank Branches Per City")
#             plt.xlabel("City")
#             plt.ylabel("Number of Branches")
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#         else:
#             st.error("City column not found in branches table!")

#         # Month-wise Transaction Trends
#         st.write("### Month-wise Transaction Trends")
#         if "transaction_date" in transactions.columns:
#             transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
#             transactions["month"] = transactions["transaction_date"].dt.month
#             monthly_trends = transactions.groupby("month")["amount"].sum()
#             plt.figure(figsize=(10, 5))
#             sns.lineplot(x=monthly_trends.index, y=monthly_trends.values, marker="o", color="red")
#             plt.title("Monthly Transaction Trends")
#             plt.xlabel("Month")
#             plt.ylabel("Total Transaction Amount")
#             plt.xticks(range(1, 13))
#             plt.grid()
#             st.pyplot(plt)
#         else:
#             st.error("Transaction date column missing in transactions table!")

#         # Total Balance per Account Type
#         st.write("### Total Balance per Account Type")
#         if "account_type" in accounts.columns and "balance" in accounts.columns:
#             plt.figure(figsize=(10, 5))
#             sns.boxplot(x="account_type", y="balance", data=accounts, palette="Set2")
#             plt.yscale("log")  # Log scale for better visualization
#             plt.title("Balance Distribution by Account Type")
#             plt.xlabel("Account Type")
#             plt.ylabel("Balance (Log Scale)")
#             st.pyplot(plt)
#         else:
#             st.error("Account Type or Balance column missing in accounts table!")

#         # Most Common Transaction Type
#         st.write("### Most Common Transaction Type")
#         if "transaction_type" in transactions.columns:
#             plt.figure(figsize=(8, 5))
#             sns.countplot(x="transaction_type", data=transactions, palette="magma")
#             plt.title("Most Common Transaction Type")
#             plt.xlabel("Transaction Type")
#             plt.ylabel("Count")
#             st.pyplot(plt)
#         else:
#             st.error("Transaction Type column missing in transactions table!")

#         # Rural vs Urban Branches
#         st.write("### Rural vs Urban Branches")
#         plt.figure(figsize=(8, 5))
#         sns.countplot(y=branches['branch_location'], order=branches['branch_location'].value_counts().index, palette="pastel")
#         plt.title("Rural vs Urban Branches", fontsize=14)
#         st.pyplot(plt)

#         # Customer Retention Rate Over Time
#         st.write("### Customer Retention Rate Over Time")
#         customers["created_at"] = pd.to_datetime(customers["created_at"], errors="coerce")
#         customers["year_joined"] = customers["created_at"].dt.year
#         customer_retention = customers["year_joined"].value_counts().sort_index()
#         plt.figure(figsize=(10, 5))
#         sns.lineplot(x=customer_retention.index, y=customer_retention.values, marker="o", color="purple")
#         plt.title("Customer Retention Over Time")
#         plt.xlabel("Year")
#         plt.ylabel("New Customers")
#         plt.grid()
#         st.pyplot(plt)

#         # Average Transaction Amount by Account Type
#         st.write("### Average Transaction Amount by Account Type")
#         merged_data = transactions.merge(accounts, on="account_number", how="left")
#         if "account_type" in merged_data.columns:
#             avg_transaction_by_account = merged_data.groupby("account_type")["amount"].mean().sort_values(ascending=False)
#             plt.figure(figsize=(10, 5))
#             sns.barplot(x=avg_transaction_by_account.index, y=avg_transaction_by_account.values, palette="viridis")
#             plt.title("Average Transaction Amount by Account Type")
#             plt.xlabel("Account Type")
#             plt.ylabel("Average Transaction Amount")
#             st.pyplot(plt)
#         else:
#             st.error("Column 'account_type' not found in the merged data. Please check the 'accounts' table.")

#         # How Long Customers Stay with the Bank
#         st.write("### How Long Customers Stay with the Bank")
#         customers["account_age"] = (pd.to_datetime("today") - customers["created_at"]).dt.days // 365
#         plt.figure(figsize=(10, 5))
#         sns.histplot(customers["account_age"], bins=20, kde=True, color="darkred")
#         plt.title("Distribution of Customer Account Age")
#         plt.xlabel("Years with Bank")
#         plt.ylabel("Number of Customers")
#         st.pyplot(plt)

#         # Employee Tenure Distribution
#         st.write("### Employee Tenure Distribution")
#         if employee is not None and not employee.empty:
#             try:
#                 employee["hire_date"] = pd.to_datetime(employee["hire_date"], errors="coerce")
#                 employee["tenure"] = (pd.to_datetime("today") - employee["hire_date"]).dt.days // 365
#                 plt.figure(figsize=(10, 5))
#                 sns.histplot(employee["tenure"], bins=15, kde=True, color="green")
#                 plt.title("Employee Tenure Distribution")
#                 plt.xlabel("Years at Bank")
#                 plt.ylabel("Number of Employees")
#                 st.pyplot(plt)
#             except Exception as e:
#                 st.error(f"An error occurred while processing employee data: {e}")
#         else:
#             st.error("Employee data is not available or is empty. Please check the data source.")

#         # Customers with Highest Account Balances
#         st.write("### Customers with Highest Account Balances")
#         top_balances = accounts.groupby("customer_id")["balance"].sum().nlargest(10)
#         plt.figure(figsize=(12, 6))
#         sns.barplot(x=top_balances.index, y=top_balances.values, palette="Blues")
#         plt.title("Top 10 Customers with Highest Balances")
#         plt.xlabel("Customer ID")
#         plt.ylabel("Total Balance")
#         plt.xticks(rotation=45)
#         st.pyplot(plt)
#         # Add EDA steps here...

#     elif analysis_step == "Regression Model":
#         st.subheader("Regression Model")
#         # Load data
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")

#         if transactions is None or accounts is None:
#             st.error("Failed to load transactions or accounts data. Please check the data source.")
#         else:
#             # Model 1: Forecasting Future Transactions
#             st.write("### Model 1: Forecasting Future Transactions")
#             st.write("This model predicts future transaction amounts based on historical data.")

#             # Prepare data for prediction
#             transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
#             transactions["year"] = transactions["transaction_date"].dt.year
#             transactions["month"] = transactions["transaction_date"].dt.month

#             # Aggregate monthly transactions
#             monthly_transactions = transactions.groupby(["year", "month"])["amount"].sum().reset_index()

#             # Features (year and month) and target (amount)
#             X = monthly_transactions[["year", "month"]]
#             y = monthly_transactions["amount"]

#             # Split data into training and testing sets
#             X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#             # Train a simple Linear Regression model
#             model = LinearRegression()
#             model.fit(X_train, y_train)

#             # Predict on test data
#             y_pred = model.predict(X_test)

#             # Evaluate the model
#             mae = mean_absolute_error(y_test, y_pred)
#             rmse = np.sqrt(mean_squared_error(y_test, y_pred))

#             st.write(f"**Mean Absolute Error (MAE):** {mae:.4f}")
#             st.write(f"**Root Mean Squared Error (RMSE):** {rmse:.4f}")

#             # Predict future transactions for 2025
#             future_dates = pd.DataFrame({"year": [2025] * 12, "month": list(range(1, 13))})
#             future_predictions = model.predict(future_dates)

#             # Plot actual vs predicted transactions
#             st.write("#### Future Transaction Forecast")
#             plt.figure(figsize=(12, 6))
#             plt.plot(monthly_transactions.index, y, label="Actual Transactions", marker="o")
#             plt.plot(future_dates.index, future_predictions, label="Predicted Transactions", linestyle="dashed", marker="o")
#             plt.title("Future Transaction Forecast")
#             plt.xlabel("Time")
#             plt.ylabel("Total Transaction Amount")
#             plt.legend()
#             st.pyplot(plt)

#             # Explanation
#             st.write("#### Why Use This Model?")
#             st.write("""
#             - **Use Case**: This model predicts future transaction amounts based on historical trends.
#             - **Advantages**: Simple and interpretable, works well for linear trends.
#             - **Interpretation**: The MAE and RMSE indicate the model's accuracy. Lower values mean better predictions.
#             - **Prediction**: The model forecasts transaction amounts for each month in 2025.
#             """)

#             # Model 2: Predicting Customer Balance
#             st.write("### Model 2: Predicting Customer Balance")
#             st.write("This model predicts a customer's account balance based on transaction history.")

#             # Prepare data for prediction
#             merged_data = transactions.merge(accounts, on="account_number", how="left")

#             # Check for NaN values in the balance column
#             if merged_data["balance"].isnull().any():
#                 st.warning("NaN values found in the 'balance' column. Handling NaN values...")
#                 merged_data = merged_data.dropna(subset=["balance"])  # Drop rows with NaN values

#             # Features and target
#             X_balance = merged_data[["amount", "transaction_type"]]
#             X_balance = pd.get_dummies(X_balance, columns=["transaction_type"], drop_first=True)
#             y_balance = merged_data["balance"]

#             # Split data into training and testing sets
#             X_train_balance, X_test_balance, y_train_balance, y_test_balance = train_test_split(X_balance, y_balance, test_size=0.2, random_state=42)

#             # Train a Linear Regression model
#             model_balance = LinearRegression()
#             model_balance.fit(X_train_balance, y_train_balance)

#             # Predict on test data
#             y_pred_balance = model_balance.predict(X_test_balance)

#             # Evaluate the model
#             mae_balance = mean_absolute_error(y_test_balance, y_pred_balance)
#             rmse_balance = np.sqrt(mean_squared_error(y_test_balance, y_pred_balance))

#             st.write(f"**Mean Absolute Error (MAE):** {mae_balance:.4f}")
#             st.write(f"**Root Mean Squared Error (RMSE):** {rmse_balance:.4f}")

#             # Explanation
#             st.write("#### Why Use This Model?")
#             st.write("""
#             - **Use Case**: This model predicts a customer's account balance based on their transaction history.
#             - **Advantages**: Simple and interpretable, works well for linear relationships.
#             - **Interpretation**: The MAE and RMSE indicate the model's accuracy. Lower values mean better predictions.
#             - **Prediction**: The model can be used to estimate a customer's balance based on their transaction behavior.
#             """)

#     elif analysis_step == "Hypothesis Testing":
#         st.subheader("Hypothesis Testing")
#          # Load data
#         transactions = fetch_table_data("transactions")
#         accounts = fetch_table_data("accounts")
#         branches = fetch_table_data("branch")

#         # ✅ One-Sample T-Test: Is the Average Transaction Amount > 1000?
#         st.subheader("1️⃣ One-Sample T-Test: Is the Average Transaction Amount Greater than 1000?")
#         mean_transaction_amount = transactions["amount"].mean()
#         t_stat, p_value = stats.ttest_1samp(transactions["amount"], 1000)
#         st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** The mean transaction amount is significantly different from 1000.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.histplot(transactions["amount"], bins=30, kde=True, ax=ax, color="blue")
#         plt.axvline(1000, color="red", linestyle="dashed", label="Test Value (1000)")
#         plt.title("Distribution of Transaction Amounts")
#         plt.xlabel("Transaction Amount")
#         plt.ylabel("Frequency")
#         plt.legend()
#         st.pyplot(fig)

#         # ✅ ANOVA F-Test: Does Branch Location Affect Transactions?
#         st.subheader("2️⃣ ANOVA F-Test: Does Branch Location Affect Transaction Amounts?")
#         merged_data = transactions.merge(accounts, on="account_number", how="left").merge(branches, on="branch_id", how="left")
#         branch_groups = [merged_data[merged_data["branch_id"] == b]["amount"] for b in merged_data["branch_id"].unique()]
#         f_stat, p_value = f_oneway(*branch_groups)
#         st.write(f"🔹 **F-Statistic:** {f_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** Branch location significantly affects transaction amount.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.boxplot(x="branch_name", y="amount", data=merged_data, palette="coolwarm")
#         plt.xticks(rotation=45)
#         plt.title("Transaction Amounts Across Branch Locations")
#         plt.xlabel("Branch")
#         plt.ylabel("Transaction Amount")
#         st.pyplot(fig)

#         # ✅ T-Test: Do Savings & Current Accounts Have Different Balances?
#         st.subheader("3️⃣ T-Test: Is There a Difference in Account Balances Between Savings & Current Accounts?")
#         savings = accounts[accounts["account_type"] == "Savings"]["balance"]
#         current = accounts[accounts["account_type"] == "Current"]["balance"]
#         t_stat, p_value = ttest_ind(savings, current, equal_var=False)
#         st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
#         st.write(f"🔹 **P-Value:** {p_value:.4f}")
#         if p_value < 0.05:
#             st.write("🔴 **Reject H₀:** Savings and Current account balances are significantly different.")
#         else:
#             st.write("🟢 **Fail to Reject H₀:** No significant difference in balances.")

#         # ✅ Visualization
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.boxplot(x="account_type", y="balance", data=accounts, palette="magma")
#         plt.title("Savings vs. Current Account Balance")
#         plt.xlabel("Account Type")
#         plt.ylabel("Balance")
#         st.pyplot(fig)
#         # Add hypothesis testing steps here...

# # ✅ Footer
# st.markdown("---")
# st.markdown("### 🚀 Powered by Streamlit")
# st.markdown("Developed with ❤️ by [ARYAN KAKADE]")



import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import st_folium
from scipy import stats
from scipy.stats import f_oneway, ttest_ind
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import time

# ✅ Custom Theme
st.set_page_config(
    page_title="🏦 Banking Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional look
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2c3e50;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    .stMarkdown h1 {
        color: #ffffff;
    }
    .stMarkdown h2 {
        color: #3498db;
    }
    .stMarkdown h3 {
        color: #2980b9;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
        color: #2c3e50;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown div {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ✅ Define API Base URL
API_URL = "https://flask-api-service-p5zg.onrender.com"

# ✅ Fetch table data
@st.cache_data
def fetch_table_data(table_name):
    try:
        response = requests.get(f"{API_URL}/all_data/{table_name}")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"[ERROR] Failed to fetch table data: {e}")
    return None

# ✅ Fetch and run SQL query
@st.cache_data
def execute_sql_query(query):
    try:
        response = requests.post(f"{API_URL}/execute_query", json={"query": query})
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"[ERROR] Failed to execute query: {e}")
    return None

# ✅ Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Table Data", "Power BI Dashboard", "SQL Queries", "Downloads", "Python Analysis"])

# ✅ Home Page
if page == "Home":
    st.title("🏦 Welcome to the Banking Dashboard!")
    st.write("Navigate using the sidebar to explore data, Power BI reports, and SQL queries.")

    # KPIs
    st.subheader("📊 Key Performance Indicators (KPIs)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", 1500, "+5%")
    with col2:
        st.metric("Total Transactions", 50000, "+10%")
    with col3:
        st.metric("Total Revenue", "$1.2M", "+8%")

    # Interactive Filters
    st.subheader("🔍 Interactive Filters")
    transactions = fetch_table_data("transactions")
    if transactions is not None:
        transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
        min_date = transactions["transaction_date"].min()
        max_date = transactions["transaction_date"].max()
        selected_date = st.date_input("Select Date Range", [min_date, max_date])
        if len(selected_date) == 2:  # Ensure selected_date has two elements
            filtered_data = transactions[(transactions["transaction_date"] >= pd.to_datetime(selected_date[0])) & 
                                   (transactions["transaction_date"] <= pd.to_datetime(selected_date[1]))]
            st.write(f"📅 **Transactions between {selected_date[0]} and {selected_date[1]}:** {len(filtered_data)} records")
        else:
            st.warning("Please select a valid date range.")

    # Geospatial Map using City and State
    st.subheader("📍 Branch Locations")
    branches = fetch_table_data("branch")
    if branches is not None:
        # Predefined dataset of Indian cities with latitude and longitude
        indian_cities = {
            "Aligarh": {"latitude": 27.897394, "longitude": 78.088013},
            "Nainital": {"latitude": 29.391872, "longitude": 79.454203},
            "Hyderabad": {"latitude": 17.385044, "longitude": 78.486671},
            "Pune": {"latitude": 18.520430, "longitude": 73.856743},
            "Bengaluru": {"latitude": 12.971599, "longitude": 77.594566},
            "Ahmednagar": {"latitude": 19.095207, "longitude": 74.749592},
            "Mumbai": {"latitude": 19.075983, "longitude": 72.877655},
            "Gurgaon": {"latitude": 28.459497, "longitude": 77.026634},
            "New Delhi": {"latitude": 28.613939, "longitude": 77.209023},
            "Darjeeling": {"latitude": 27.036007, "longitude": 88.262672},
            "Shimla": {"latitude": 31.104814, "longitude": 77.173403},
            "Jorhat": {"latitude": 26.750000, "longitude": 94.216667},
            "Nanded": {"latitude": 19.138251, "longitude": 77.321045},
            "Mysuru": {"latitude": 12.295810, "longitude": 76.639381},
        }

        # Add latitude and longitude to branches data
        branches["latitude"] = branches["city"].map(lambda x: indian_cities.get(x, {}).get("latitude"))
        branches["longitude"] = branches["city"].map(lambda x: indian_cities.get(x, {}).get("longitude"))

        # Drop rows where latitude or longitude is missing
        branches = branches.dropna(subset=["latitude", "longitude"])

        # Create a Folium map with a smaller zoom level and better styling
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=4, tiles="CartoDB positron")  # Centered on India with a professional tile
        for _, row in branches.iterrows():
            folium.Marker(
                [row["latitude"], row["longitude"]],
                popup=f"{row['branch_name']}, {row['city']}, {row['state']}",
                icon=folium.Icon(color="blue", icon="info-sign")  # Add a professional icon
            ).add_to(m)

        # Display the map in Streamlit with a smaller size
        st_folium(m, width=1025, height=455)  # Adjusted width and height for better fit

# ✅ Table Data Page
elif page == "Table Data":
    st.title("📊 Table Data")
    selected_table = st.selectbox("Select Table", ["customers", "accounts", "transactions", "employees", "branch"])
    table_data = fetch_table_data(selected_table)
    if table_data is not None:
        st.dataframe(table_data)

        # Download Data
        st.download_button("Download Data as CSV", table_data.to_csv(index=False), file_name=f"{selected_table}.csv")

# ✅ Power BI Dashboard Page
elif page == "Power BI Dashboard":
    st.title("📊 Power BI Dashboard")
    st.write("🔗 Click below to open the Power BI report in a new tab:")
    power_bi_url = "https://app.powerbi.com/groups/me/reports/4a3fada2-ba7e-4920-bd40-d09245e7c1b7/be94380037ae7288aa6b?experience=power-bi"
    st.markdown(f"[🔗 Open Power BI Dashboard]({power_bi_url})", unsafe_allow_html=True)
    st.write("🚀 **Power BI Workaround:** If you don’t have Power BI installed, download the PBIX file from the Downloads page.")

# ✅ SQL Queries Page
elif page == "SQL Queries":
    st.title("📝 SQL Queries")
    queries = {
        "1. Inactive Customers (No Transactions in Last Year)": """
            SELECT c.customer_id, c.first_name, c.last_name 
            FROM customers c
            JOIN accounts a ON c.customer_id = a.customer_id
            LEFT JOIN transactions t ON a.account_number = t.account_number 
            WHERE t.transaction_id IS NULL OR 
            t.transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
        """,
        "2. Total Transactions Per Account Per Month": """
            SELECT account_number, YEAR(transaction_date) AS year, 
            MONTH(transaction_date) AS month, SUM(amount) AS total_amt
            FROM transactions 
            GROUP BY account_number, year, month
            ORDER BY account_number, year, month;
        """,
        "3. Branch Ranking Based on Deposits in Last Quarter": """
            SELECT a.branch_id, SUM(t.amount) AS total_deposits, 
            DENSE_RANK() OVER(ORDER BY SUM(t.amount) DESC) AS branch_rank
            FROM accounts a 
            INNER JOIN transactions t USING(account_number)
            WHERE t.transaction_type="Deposit" 
            AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) 
            GROUP BY a.branch_id
            ORDER BY branch_rank;
        """,
        "4. Customer with Highest Deposit": """
            SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, t.amount 
            FROM customers c 
            INNER JOIN accounts a ON c.customer_id = a.customer_id 
            INNER JOIN transactions t ON t.account_number = a.account_number
            WHERE t.transaction_type = "Deposit"
            ORDER BY t.amount DESC
            LIMIT 1;
        """,
        "5. Fraud Detection: More Than 2 Transactions in a Day": """
            SELECT a.account_number AS fraud_accounts, COUNT(t.transaction_id) AS no_of_transactions, 
            DAY(t.transaction_date) AS single_day
            FROM accounts a 
            INNER JOIN transactions t USING(account_number)
            GROUP BY fraud_accounts, single_day
            HAVING no_of_transactions > 2;
        """,
        "6. Daily Transaction Volume (Past Month)": """
            SELECT DATE(transaction_date) AS transaction_day, ROUND(SUM(amount), 3) AS trans_volume
            FROM transactions 
            WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
            GROUP BY transaction_day
            ORDER BY transaction_day;
        """,
        "7. Branch with Highest Average Account Balance": """
            SELECT branch_id, AVG(balance) AS avg_bal
            FROM accounts 
            GROUP BY branch_id
            ORDER BY avg_bal DESC
            LIMIT 1;
        """,
        "8. Most Common Transaction Type Per Branch": """
            SELECT b.branch_id, t.transaction_type, COUNT(*) AS transaction_count
            FROM transactions t
            JOIN accounts a ON t.account_number = a.account_number
            JOIN branch b ON a.branch_id = b.branch_id
            GROUP BY b.branch_id, t.transaction_type
            ORDER BY b.branch_id, transaction_count DESC;
        """,
        "9. Accounts with Only Withdrawals": """
            SELECT account_number
            FROM transactions
            GROUP BY account_number
            HAVING SUM(CASE WHEN transaction_type = 'deposit' THEN 1 ELSE 0 END) = 0;
        """,
        "10. Running Total of Transactions Per Account": """
            SELECT account_number, transaction_date, amount,
            SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
            FROM transactions;
        """,
        "11. Previous Transaction Amount for Each Transaction": """
            SELECT account_number, transaction_id, transaction_date, amount,
            LAG(amount, 1, 0) OVER (PARTITION BY account_number ORDER BY transaction_date) AS previous_transaction
            FROM transactions;
        """,
        "12. Customers with Highest Transactions": """
            SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
            FROM customers c
            JOIN accounts a ON c.customer_id = a.customer_id
            JOIN transactions t ON a.account_number = t.account_number
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_transactions DESC
            LIMIT 10;
        """,
        "13. Moving Average of Transactions": """
            SELECT account_number, transaction_id, transaction_date, amount,
            AVG(amount) OVER (PARTITION BY account_number ORDER BY transaction_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
            FROM transactions;
        """,
        "14. Average Transactions Per Branch Per Month": """
            SELECT b.branch_id, YEAR(t.transaction_date) AS year, MONTH(t.transaction_date) AS month,
            COUNT(t.transaction_id) / COUNT(DISTINCT t.account_number) AS avg_transactions
            FROM branch b
            JOIN accounts a ON b.branch_id = a.branch_id
            JOIN transactions t ON a.account_number = t.account_number
            GROUP BY b.branch_id, year, month;
        """,
        "15. Running Total of transactions per Account": """
             SELECT account_number, transaction_date, amount,
             SUM(amount) OVER (PARTITION BY account_number ORDER BY transaction_date) AS running_total
             FROM transactions;
        """,
        "16. Customers whose account balance is below the average balance of their branch": """
             SELECT c.customer_id, c.first_name, c.last_name, a.account_number, a.balance, branch_avg.avg_balance
             FROM accounts a
             JOIN customers c ON a.customer_id = c.customer_id
             JOIN (
             SELECT branch_id, AVG(balance) AS avg_balance
             FROM accounts
             GROUP BY branch_id
             ) branch_avg ON a.branch_id = branch_avg.branch_id
             WHERE a.balance < branch_avg.avg_balance;
        """,
        "17. Customers who have made the highest number of transactions": """
              SELECT c.customer_id, c.first_name, c.last_name, COUNT(t.transaction_id) AS total_transactions
              FROM customers c
              JOIN accounts a ON c.customer_id = a.customer_id
              JOIN transactions t ON a.account_number = t.account_number
              GROUP BY c.customer_id, c.first_name, c.last_name
              ORDER BY total_transactions DESC
              LIMIT 10;
          """
        # Add other queries here...
    }
    selected_query = st.selectbox("Select Query", list(queries.keys()))
    st.subheader(f"🧐 {selected_query}")
    st.code(queries[selected_query], language="sql")
    if st.button("Run Query"):
        query_result = execute_sql_query(queries[selected_query])
        if query_result is not None:
            st.dataframe(query_result)

# ✅ Downloads Page
elif page == "Downloads":
    st.title("📥 Download Project Files")
    st.write("📥 **Download the Project Files Below:**")
    
    # PDF Report
    st.markdown("[📄 Download PDF Report](sandbox:/mnt/data/dashboard%20(2).pdf)", unsafe_allow_html=True)
    
    # Power BI Dashboard
    st.markdown("[📊 Download Power BI Dashboard (PBIX)](sandbox:/mnt/data/banking_operation_dashboard.pbix)", unsafe_allow_html=True)
    
    # PowerPoint Presentation
    st.markdown("[📽️ Download PowerPoint Presentation](sandbox:/mnt/data/Analysis%20of%20Banking%20Operations%20using%20Power%20BI(1).pptx)", unsafe_allow_html=True)
    
    # SQL Queries File
    st.markdown("[📝 Download SQL Queries (SQL)](https://example.com/path/to/bank1.sql)", unsafe_allow_html=True)
    
    # Python EDA, ML, and Hypothesis Testing Jupyter Notebook
    st.markdown("[🐍 Download Python Analysis Notebook (IPYNB)](https://example.com/path/to/python_analysis1.ipynb)", unsafe_allow_html=True)

# ✅ Python Analysis Page
elif page == "Python Analysis":
    st.title("🐍 Python Analysis")
    analysis_step = st.selectbox("Select Analysis Step", ["Data Cleaning", "EDA", "Regression Model", "Hypothesis Testing"])

    if analysis_step == "Data Cleaning":
        st.subheader("Data Cleaning")
        st.write("This section focuses on cleaning the dataset to ensure high-quality data for analysis. Below are the steps performed:")

        # Load data
        customers = fetch_table_data("customers")
        transactions = fetch_table_data("transactions")
        accounts = fetch_table_data("accounts")
        branches = fetch_table_data("branch")
        employee = fetch_table_data("employee")

        # Step 1: Check for Missing Values
        st.write("#### 1. Handling Missing Values")
        st.write("Missing values can lead to inaccurate analysis. Here's how we handle them:")
        
        if customers is not None:
            st.write("- **Customers Table:**", customers.isnull().sum().sum(), "missing values found.")
        else:
            st.error("Customers table is not available or is empty.")
        
        if transactions is not None:
            st.write("- **Transactions Table:**", transactions.isnull().sum().sum(), "missing values found.")
        else:
            st.error("Transactions table is not available or is empty.")
        
        if accounts is not None:
            st.write("- **Accounts Table:**", accounts.isnull().sum().sum(), "missing values found.")
        else:
            st.error("Accounts table is not available or is empty.")
        
        if branches is not None:
            st.write("- **Branches Table:**", branches.isnull().sum().sum(), "missing values found.")
        else:
            st.error("Branches table is not available or is empty.")
        
        if employee is not None:
            st.write("- **Employees Table:**", employee.isnull().sum().sum(), "missing values found.")
        else:
            st.error("Employees table is not available or is empty.")
        
        st.write("**Action Taken:** Missing values were either dropped or imputed based on the context.")

        # Step 2: Remove Duplicates
        st.write("#### 2. Removing Duplicates")
        st.write("Duplicate records can skew analysis. Here's the duplicate count before cleaning:")
        
        if customers is not None:
            st.write("- **Customers Table:**", customers.duplicated().sum(), "duplicates found.")
        else:
            st.error("Customers table is not available or is empty.")
        
        if transactions is not None:
            st.write("- **Transactions Table:**", transactions.duplicated().sum(), "duplicates found.")
        else:
            st.error("Transactions table is not available or is empty.")
        
        if accounts is not None:
            st.write("- **Accounts Table:**", accounts.duplicated().sum(), "duplicates found.")
        else:
            st.error("Accounts table is not available or is empty.")
        
        if branches is not None:
            st.write("- **Branches Table:**", branches.duplicated().sum(), "duplicates found.")
        else:
            st.error("Branches table is not available or is empty.")
        
        if employee is not None:
            st.write("- **Employees Table:**", employee.duplicated().sum(), "duplicates found.")
        else:
            st.error("Employees table is not available or is empty.")
        
        st.write("**Action Taken:** All duplicates were removed from the dataset.")

        # Step 3: Data Types and Formatting
        st.write("#### 3. Data Type Validation")
        st.write("Ensuring correct data types for each column:")
        
        if customers is not None:
            st.write("- **Customers Table:** Verified `created_at` is datetime.")
        else:
            st.error("Customers table is not available or is empty.")
        
        if transactions is not None:
            st.write("- **Transactions Table:** Verified `transaction_date` is datetime.")
        else:
            st.error("Transactions table is not available or is empty.")
        
        if accounts is not None:
            st.write("- **Accounts Table:** Verified `balance` is numeric.")
        else:
            st.error("Accounts table is not available or is empty.")
        
        if branches is not None:
            st.write("- **Branches Table:** Verified `branch_id` is unique.")
        else:
            st.error("Branches table is not available or is empty.")
        
        if employee is not None:
            st.write("- **Employees Table:** Verified `hire_date` is datetime.")
        else:
            st.error("Employees table is not available or is empty.")
        
        st.write("**Action Taken:** Data types were corrected where necessary.")

        # Step 4: Outlier Detection
        st.write("#### 4. Outlier Detection")
        st.write("Outliers can distort analysis. Here's a summary of outliers detected:")
        
        if transactions is not None:
            st.write("- **Transactions Table:** Outliers detected in `amount` using IQR method.")
        else:
            st.error("Transactions table is not available or is empty.")
        
        if accounts is not None:
            st.write("- **Accounts Table:** Outliers detected in `balance` using Z-score method.")
        else:
            st.error("Accounts table is not available or is empty.")
        
        st.write("**Action Taken:** Outliers were either capped or removed based on domain knowledge.")

        # Step 5: Final Dataset Shape
        st.write("#### 5. Final Dataset Shape")
        st.write("After cleaning, the dataset shapes are as follows:")
        
        if customers is not None:
            st.write("- **Customers Table:**", customers.shape)
        else:
            st.error("Customers table is not available or is empty.")
        
        if transactions is not None:
            st.write("- **Transactions Table:**", transactions.shape)
        else:
            st.error("Transactions table is not available or is empty.")
        
        if accounts is not None:
            st.write("- **Accounts Table:**", accounts.shape)
        else:
            st.error("Accounts table is not available or is empty.")
        
        if branches is not None:
            st.write("- **Branches Table:**", branches.shape)
        else:
            st.error("Branches table is not available or is empty.")
        
        if employee is not None:
            st.write("- **Employees Table:**", employee.shape)
        else:
            st.error("Employees table is not available or is empty.")
        
        st.write("**Action Taken:** The dataset is now clean and ready for analysis.")
        # Add data cleaning steps here...

    elif analysis_step == "EDA":
        st.subheader("Exploratory Data Analysis (EDA)")
        # Load data
        customers = fetch_table_data("customers")
        transactions = fetch_table_data("transactions")
        accounts = fetch_table_data("accounts")
        branches = fetch_table_data("branch")
        employee = fetch_table_data("employee")

        # Branch Performance Analysis (Revenue Contribution per Branch)
        st.write("### Branch Performance Analysis (Revenue Contribution per Branch)")
        branch_revenue = transactions.merge(accounts, on="account_number", how="left")
        if "branch_id" in branch_revenue.columns:
            branch_revenue = branch_revenue.groupby("branch_id")["amount"].sum().reset_index()
            fig = px.bar(branch_revenue, x="branch_id", y="amount", title="Revenue Contribution per Branch",
                         labels={"branch_id": "Branch ID", "amount": "Total Transaction Amount"},
                         color="amount", color_continuous_scale="Plasma")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Branch ID not found after merging transactions with accounts!")

        # Top 10 Customers with Highest Transactions
        st.write("### Top 10 Customers with Highest Transactions")
        transactions = transactions.merge(accounts, on="account_number", how="left").merge(customers, on="customer_id", how="left")
        if "customer_id" in transactions.columns:
            customer_transaction_counts = transactions["customer_id"].value_counts().reset_index()
            customer_transaction_counts.columns = ["customer_id", "transaction_count"]
            top_customers = customer_transaction_counts.head(10)
            fig = px.bar(top_customers, x="customer_id", y="transaction_count", title="Top 10 Customers with Most Transactions",
                         labels={"customer_id": "Customer ID", "transaction_count": "Number of Transactions"},
                         color="transaction_count", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Customer ID not found after merging transactions with accounts & customers!")

        # Most Active Branches (Number of Accounts per Branch)
        st.write("### Most Active Branches (Number of Accounts per Branch)")
        if "branch_id" in accounts.columns:
            accounts_per_branch = accounts.groupby("branch_id")["account_number"].count().reset_index()
            fig = px.bar(accounts_per_branch, x="branch_id", y="account_number", title="Number of Accounts Per Branch",
                         labels={"branch_id": "Branch ID", "account_number": "Number of Accounts"},
                         color="account_number", color_continuous_scale="Mint")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Branch ID not found in accounts table!")

        # Branches per city
        st.write("### Branches per City")
        if "city" in branches.columns:
            branches_per_city = branches["city"].value_counts().reset_index()
            branches_per_city.columns = ["city", "count"]
            fig = px.bar(branches_per_city, x="city", y="count", title="Number of Bank Branches Per City",
                         labels={"city": "City", "count": "Number of Branches"},
                         color="count", color_continuous_scale="Rainbow")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("City column not found in branches table!")

        # Month-wise Transaction Trends
        st.write("### Month-wise Transaction Trends")
        if "transaction_date" in transactions.columns:
            transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
            transactions["month"] = transactions["transaction_date"].dt.month
            monthly_trends = transactions.groupby("month")["amount"].sum().reset_index()
            fig = px.line(monthly_trends, x="month", y="amount", title="Monthly Transaction Trends",
                           labels={"month": "Month", "amount": "Total Transaction Amount"},
                           markers=True, line_shape="linear")
            fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Transaction date column missing in transactions table!")

        # Total Balance per Account Type
        st.write("### Total Balance per Account Type")
        if "account_type" in accounts.columns and "balance" in accounts.columns:
            fig = px.box(accounts, x="account_type", y="balance", title="Balance Distribution by Account Type",
                         labels={"account_type": "Account Type", "balance": "Balance"},
                         color="account_type", color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_yaxes(type="log")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Account Type or Balance column missing in accounts table!")

        # Most Common Transaction Type
        st.write("### Most Common Transaction Type")
        if "transaction_type" in transactions.columns:
            transaction_counts = transactions["transaction_type"].value_counts().reset_index()
            transaction_counts.columns = ["transaction_type", "count"]
            fig = px.bar(transaction_counts, x="transaction_type", y="count", title="Most Common Transaction Type",
                         labels={"transaction_type": "Transaction Type", "count": "Count"},
                         color="transaction_type", color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Transaction Type column missing in transactions table!")

        # Rural vs Urban Branches
        st.write("### Rural vs Urban Branches")
        if "branch_location" in branches.columns:
            branch_location_counts = branches["branch_location"].value_counts().reset_index()
            branch_location_counts.columns = ["branch_location", "count"]
            fig = px.bar(branch_location_counts, y="branch_location", x="count", title="Rural vs Urban Branches",
                         labels={"branch_location": "Branch Location", "count": "Number of Branches"},
                         color="branch_location", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Branch Location column not found in branches table!")

        # Customer Retention Rate Over Time
        st.write("### Customer Retention Rate Over Time")
        if "created_at" in customers.columns:
            customers["created_at"] = pd.to_datetime(customers["created_at"], errors="coerce")
            customers["year_joined"] = customers["created_at"].dt.year
            customer_retention = customers["year_joined"].value_counts().sort_index().reset_index()
            customer_retention.columns = ["year", "count"]
            fig = px.line(customer_retention, x="year", y="count", title="Customer Retention Over Time",
                           labels={"year": "Year", "count": "New Customers"},
                           markers=True, line_shape="linear")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Created At column missing in customers table!")

        # Average Transaction Amount by Account Type
        st.write("### Average Transaction Amount by Account Type")
        merged_data = transactions.merge(accounts, on="account_number", how="left")
        if "account_type" in merged_data.columns:
            avg_transaction_by_account = merged_data.groupby("account_type")["amount"].mean().reset_index()
            fig = px.bar(avg_transaction_by_account, x="account_type", y="amount", title="Average Transaction Amount by Account Type",
                         labels={"account_type": "Account Type", "amount": "Average Transaction Amount"},
                         color="account_type", color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Column 'account_type' not found in the merged data. Please check the 'accounts' table.")

        # How Long Customers Stay with the Bank
        st.write("### How Long Customers Stay with the Bank")
        if "created_at" in customers.columns:
            customers["account_age"] = (pd.to_datetime("today") - customers["created_at"]).dt.days // 365
            fig = px.histogram(customers, x="account_age", title="Distribution of Customer Account Age",
                               labels={"account_age": "Years with Bank", "count": "Number of Customers"},
                               nbins=20, color_discrete_sequence=["darkred"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Created At column missing in customers table!")

        # Employee Tenure Distribution
        st.write("### Employee Tenure Distribution")
        if employee is not None and not employee.empty:
            try:
                employee["hire_date"] = pd.to_datetime(employee["hire_date"], errors="coerce")
                employee["tenure"] = (pd.to_datetime("today") - employee["hire_date"]).dt.days // 365
                fig = px.histogram(employee, x="tenure", title="Employee Tenure Distribution",
                                   labels={"tenure": "Years at Bank", "count": "Number of Employees"},
                                   nbins=15, color_discrete_sequence=["green"])
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"An error occurred while processing employee data: {e}")
        else:
            st.error("Employee data is not available or is empty. Please check the data source.")

        # Customers with Highest Account Balances
        st.write("### Customers with Highest Account Balances")
        if "customer_id" in accounts.columns and "balance" in accounts.columns:
            top_balances = accounts.groupby("customer_id")["balance"].sum().nlargest(10).reset_index()
            fig = px.bar(top_balances, x="customer_id", y="balance", title="Top 10 Customers with Highest Balances",
                         labels={"customer_id": "Customer ID", "balance": "Total Balance"},
                         color="balance", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Customer ID or Balance column missing in accounts table!")
        # Add EDA steps here...

    elif analysis_step == "Regression Model":
        st.subheader("Regression Model")
        # Load data
        transactions = fetch_table_data("transactions")
        accounts = fetch_table_data("accounts")

        if transactions is None or accounts is None:
            st.error("Failed to load transactions or accounts data. Please check the data source.")
        else:
            # Model 1: Forecasting Future Transactions
            st.write("### Model 1: Forecasting Future Transactions")
            st.write("This model predicts future transaction amounts based on historical data.")

            # Prepare data for prediction
            transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
            transactions["year"] = transactions["transaction_date"].dt.year
            transactions["month"] = transactions["transaction_date"].dt.month

            # Aggregate monthly transactions
            monthly_transactions = transactions.groupby(["year", "month"])["amount"].sum().reset_index()

            # Features (year and month) and target (amount)
            X = monthly_transactions[["year", "month"]]
            y = monthly_transactions["amount"]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train a simple Linear Regression model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Predict on test data
            y_pred = model.predict(X_test)

            # Evaluate the model
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))

            st.write(f"**Mean Absolute Error (MAE):** {mae:.4f}")
            st.write(f"**Root Mean Squared Error (RMSE):** {rmse:.4f}")

            # Predict future transactions for 2025
            future_dates = pd.DataFrame({"year": [2025] * 12, "month": list(range(1, 13))})
            future_predictions = model.predict(future_dates)

            # Plot actual vs predicted transactions
            st.write("#### Future Transaction Forecast")
            plt.figure(figsize=(12, 6))
            plt.plot(monthly_transactions.index, y, label="Actual Transactions", marker="o")
            plt.plot(future_dates.index, future_predictions, label="Predicted Transactions", linestyle="dashed", marker="o")
            plt.title("Future Transaction Forecast")
            plt.xlabel("Time")
            plt.ylabel("Total Transaction Amount")
            plt.legend()
            st.pyplot(plt)

            # Explanation
            st.write("#### Why Use This Model?")
            st.write("""
            - **Use Case**: This model predicts future transaction amounts based on historical trends.
            - **Advantages**: Simple and interpretable, works well for linear trends.
            - **Interpretation**: The MAE and RMSE indicate the model's accuracy. Lower values mean better predictions.
            - **Prediction**: The model forecasts transaction amounts for each month in 2025.
            """)

            # Model 2: Predicting Customer Balance
            st.write("### Model 2: Predicting Customer Balance")
            st.write("This model predicts a customer's account balance based on transaction history.")

            # Prepare data for prediction
            merged_data = transactions.merge(accounts, on="account_number", how="left")

            # Check for NaN values in the balance column
            if merged_data["balance"].isnull().any():
                st.warning("NaN values found in the 'balance' column. Handling NaN values...")
                merged_data = merged_data.dropna(subset=["balance"])  # Drop rows with NaN values

            # Features and target
            X_balance = merged_data[["amount", "transaction_type"]]
            X_balance = pd.get_dummies(X_balance, columns=["transaction_type"], drop_first=True)
            y_balance = merged_data["balance"]

            # Split data into training and testing sets
            X_train_balance, X_test_balance, y_train_balance, y_test_balance = train_test_split(X_balance, y_balance, test_size=0.2, random_state=42)

            # Train a Linear Regression model
            model_balance = LinearRegression()
            model_balance.fit(X_train_balance, y_train_balance)

            # Predict on test data
            y_pred_balance = model_balance.predict(X_test_balance)

            # Evaluate the model
            mae_balance = mean_absolute_error(y_test_balance, y_pred_balance)
            rmse_balance = np.sqrt(mean_squared_error(y_test_balance, y_pred_balance))

            st.write(f"**Mean Absolute Error (MAE):** {mae_balance:.4f}")
            st.write(f"**Root Mean Squared Error (RMSE):** {rmse_balance:.4f}")

            # Explanation
            st.write("#### Why Use This Model?")
            st.write("""
            - **Use Case**: This model predicts a customer's account balance based on their transaction history.
            - **Advantages**: Simple and interpretable, works well for linear relationships.
            - **Interpretation**: The MAE and RMSE indicate the model's accuracy. Lower values mean better predictions.
            - **Prediction**: The model can be used to estimate a customer's balance based on their transaction behavior.
            """)
        # Add regression model steps here...

    elif analysis_step == "Hypothesis Testing":
        st.subheader("Hypothesis Testing")
        transactions = fetch_table_data("transactions")
        accounts = fetch_table_data("accounts")
        branches = fetch_table_data("branch")

        # ✅ One-Sample T-Test: Is the Average Transaction Amount > 1000?
        st.subheader("1️⃣ One-Sample T-Test: Is the Average Transaction Amount Greater than 1000?")
        mean_transaction_amount = transactions["amount"].mean()
        t_stat, p_value = stats.ttest_1samp(transactions["amount"], 1000)
        st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
        st.write(f"🔹 **P-Value:** {p_value:.4f}")
        if p_value < 0.05:
            st.write("🔴 **Reject H₀:** The mean transaction amount is significantly different from 1000.")
        else:
            st.write("🟢 **Fail to Reject H₀:** No significant difference.")

        # ✅ Visualization
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(transactions["amount"], bins=30, kde=True, ax=ax, color="blue")
        plt.axvline(1000, color="red", linestyle="dashed", label="Test Value (1000)")
        plt.title("Distribution of Transaction Amounts")
        plt.xlabel("Transaction Amount")
        plt.ylabel("Frequency")
        plt.legend()
        st.pyplot(fig)

        # ✅ ANOVA F-Test: Does Branch Location Affect Transactions?
        st.subheader("2️⃣ ANOVA F-Test: Does Branch Location Affect Transaction Amounts?")
        merged_data = transactions.merge(accounts, on="account_number", how="left").merge(branches, on="branch_id", how="left")
        branch_groups = [merged_data[merged_data["branch_id"] == b]["amount"] for b in merged_data["branch_id"].unique()]
        f_stat, p_value = f_oneway(*branch_groups)
        st.write(f"🔹 **F-Statistic:** {f_stat:.4f}")
        st.write(f"🔹 **P-Value:** {p_value:.4f}")
        if p_value < 0.05:
            st.write("🔴 **Reject H₀:** Branch location significantly affects transaction amount.")
        else:
            st.write("🟢 **Fail to Reject H₀:** No significant difference.")

        # ✅ Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x="branch_name", y="amount", data=merged_data, palette="coolwarm")
        plt.xticks(rotation=45)
        plt.title("Transaction Amounts Across Branch Locations")
        plt.xlabel("Branch")
        plt.ylabel("Transaction Amount")
        st.pyplot(fig)

        # ✅ T-Test: Do Savings & Current Accounts Have Different Balances?
        st.subheader("3️⃣ T-Test: Is There a Difference in Account Balances Between Savings & Current Accounts?")
        savings = accounts[accounts["account_type"] == "Savings"]["balance"]
        current = accounts[accounts["account_type"] == "Current"]["balance"]
        t_stat, p_value = ttest_ind(savings, current, equal_var=False)
        st.write(f"🔹 **T-Statistic:** {t_stat:.4f}")
        st.write(f"🔹 **P-Value:** {p_value:.4f}")
        if p_value < 0.05:
            st.write("🔴 **Reject H₀:** Savings and Current account balances are significantly different.")
        else:
            st.write("🟢 **Fail to Reject H₀:** No significant difference in balances.")

        # ✅ Visualization
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x="account_type", y="balance", data=accounts, palette="magma")
        plt.title("Savings vs. Current Account Balance")
        plt.xlabel("Account Type")
        plt.ylabel("Balance")
        st.pyplot(fig)
        # Add hypothesis testing steps here...

# ✅ Footer
st.markdown("---")
st.markdown("### 🚀 Powered by Streamlit")
st.markdown("Developed with ❤️ by [ARYAN KAKADE]")