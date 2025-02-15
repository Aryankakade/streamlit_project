# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pymysql

# app = Flask(__name__)
# CORS(app)  # Enable CORS to allow Streamlit to fetch data

# # Home Route
# @app.route("/")
# def home():
#     return jsonify({"message": "Welcome to the Banking API!", "status": "running"})

# # Database connection function
# def get_db_connection():
#     return pymysql.connect(
#         host="localhost",
#         user="root",
#         password="Aryankakade@143",
#         database="bank1",
#         port=3306,
#         cursorclass=pymysql.cursors.DictCursor
#     )

# # API to fetch individual table data
# @app.route("/data/<table_name>", methods=["GET"])
# def get_table_data(table_name):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
#         data = cursor.fetchall()
#         conn.close()
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)})

# # API to fetch all tables data
# @app.route("/all_data", methods=["GET"])
# def get_all_tables_data():
#     tables = ["transactions", "customers", "accounts", "employees", "branch"]  # ✅ Correct tables
#     result = {}

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         for table in tables:
#             try:
#                 cursor.execute(f"SELECT * FROM {table} LIMIT 50")
#                 result[table] = cursor.fetchall()
#             except Exception as e:
#                 result[table] = {"error": str(e)}

#         conn.close()
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)})

# # ✅ Add API for executing SQL queries
# @app.route("/execute_query", methods=["POST"])
# def execute_query():
#     try:
#         data = request.get_json()
#         query = data.get("query")

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         conn.close()

#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)  # Run Flask on port 5000

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pymysql

# app = Flask(__name__)
# CORS(app)  # Enable CORS for Streamlit integration

# # ✅ Database connection function
# def get_db_connection():
#     try:
#         conn = pymysql.connect(
#             host="localhost",
#             user="root",
#             password="Aryankakade@143",
#             database="bank1",
#             port=3306,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return conn
#     except Exception as e:
#         print(f"[ERROR] Database connection failed: {e}")
#         return None

# # ✅ Home Route
# @app.route("/")
# def home():
#     return jsonify({"message": "Welcome to the Banking API!", "status": "running"})

# # ✅ Fetch individual table data (Fixed)
# @app.route("/all_data/<table_name>", methods=["GET"])
# def get_table_data(table_name):
#     try:
#         conn = get_db_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed!"}), 500
        
#         cursor = conn.cursor()
        
#         # Validate table name to prevent SQL injection
#         allowed_tables = {"transactions", "customers", "accounts", "employees", "branch"}
#         if table_name not in allowed_tables:
#             return jsonify({"error": "Invalid table name!"}), 400

#         print(f"[INFO] Fetching data from table: {table_name}")
#         cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
#         data = cursor.fetchall()
        
#         conn.close()
#         return jsonify(data)

#     except Exception as e:
#         print(f"[ERROR] Failed to fetch data: {e}")
#         return jsonify({"error": str(e)}), 500

# # ✅ Fetch all tables' data
# @app.route("/all_data", methods=["GET"])
# def get_all_tables_data():
#     tables = ["transactions", "customers", "accounts", "employees", "branch"]
#     result = {}

#     try:
#         conn = get_db_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed!"}), 500

#         cursor = conn.cursor()

#         for table in tables:
#             try:
#                 print(f"[INFO] Fetching data from: {table}")
#                 cursor.execute(f"SELECT * FROM {table} LIMIT 50")
#                 result[table] = cursor.fetchall()
#             except Exception as e:
#                 print(f"[ERROR] Failed to fetch {table}: {e}")
#                 result[table] = {"error": str(e)}

#         conn.close()
#         return jsonify(result)

#     except Exception as e:
#         print(f"[ERROR] Unexpected error: {e}")
#         return jsonify({"error": str(e)}), 500

# # ✅ Fetch KPIs (New)
# @app.route("/kpis", methods=["GET"])
# def get_kpis():
#     try:
#         conn = get_db_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed!"}), 500
        
#         cursor = conn.cursor()

#         query = """
#             SELECT 
#                 (SELECT COUNT(*) FROM customers) AS total_customers,
#                 (SELECT COUNT(*) FROM transactions) AS total_transactions,
#                 (SELECT SUM(amount) FROM transactions WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)) AS total_deposits,
#                 (SELECT COUNT(*) FROM accounts WHERE status = 'inactive') AS inactive_accounts
#         """
#         cursor.execute(query)
#         result = cursor.fetchone()

#         kpis = {
#             "Total Customers": result["total_customers"],
#             "Total Transactions": result["total_transactions"],
#             "Total Deposits (Last Month)": f"${result['total_deposits']:,.2f}" if result["total_deposits"] else "$0",
#             "Inactive Accounts": result["inactive_accounts"]
#         }

#         conn.close()
#         return jsonify(kpis)

#     except Exception as e:
#         print(f"[ERROR] Failed to fetch KPIs: {e}")
#         return jsonify({"error": str(e)}), 500

# # ✅ Execute SQL Query (Fixed)
# @app.route("/execute_query", methods=["POST"])
# def execute_query():
#     try:
#         data = request.get_json()
#         query = data.get("query")

#         if not query:
#             return jsonify({"error": "Query is required!"}), 400

#         conn = get_db_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed!"}), 500

#         cursor = conn.cursor()
#         print(f"[INFO] Executing query: {query}")
        
#         cursor.execute(query)
#         result = cursor.fetchall()
        
#         conn.close()
#         return jsonify(result)

#     except Exception as e:
#         print(f"[ERROR] Query execution failed: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     print("[INFO] Flask API is running on port 5000...")
#     app.run(debug=True, port=5000)



from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os  # ✅ Import os to use environment variables

app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit integration

# ✅ Secure Database connection function
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),  # ✅ Fetch from environment variable, default "localhost"
            user=os.getenv("DB_USER", "root"),  # ✅ Fetch user from env variable
            password=os.getenv("DB_PASSWORD", "Aryankakade@143"),  # ✅ Fetch password securely
            database=os.getenv("DB_NAME", "bank1"),  # ✅ Fetch DB name
            port=int(os.getenv("DB_PORT", 3306)),  # ✅ Default MySQL port 3306
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None

# ✅ Home Route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Banking API!", "status": "running"})

# ✅ Fetch individual table data (Fixed)
@app.route("/all_data/<table_name>", methods=["GET"])
def get_table_data(table_name):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed!"}), 500
        
        cursor = conn.cursor()
        
        # Validate table name to prevent SQL injection
        allowed_tables = {"transactions", "customers", "accounts", "employees", "branch"}
        if table_name not in allowed_tables:
            return jsonify({"error": "Invalid table name!"}), 400

        print(f"[INFO] Fetching data from table: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
        data = cursor.fetchall()
        
        conn.close()
        return jsonify(data)

    except Exception as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ Fetch all tables' data
@app.route("/all_data", methods=["GET"])
def get_all_tables_data():
    tables = ["transactions", "customers", "accounts", "employees", "branch"]
    result = {}

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed!"}), 500

        cursor = conn.cursor()

        for table in tables:
            try:
                print(f"[INFO] Fetching data from: {table}")
                cursor.execute(f"SELECT * FROM {table} LIMIT 50")
                result[table] = cursor.fetchall()
            except Exception as e:
                print(f"[ERROR] Failed to fetch {table}: {e}")
                result[table] = {"error": str(e)}

        conn.close()
        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ Fetch KPIs (New)
@app.route("/kpis", methods=["GET"])
def get_kpis():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed!"}), 500
        
        cursor = conn.cursor()

        query = """
            SELECT 
                (SELECT COUNT(*) FROM customers) AS total_customers,
                (SELECT COUNT(*) FROM transactions) AS total_transactions,
                (SELECT SUM(amount) FROM transactions WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)) AS total_deposits,
                (SELECT COUNT(*) FROM accounts WHERE status = 'inactive') AS inactive_accounts
        """
        cursor.execute(query)
        result = cursor.fetchone()

        kpis = {
            "Total Customers": result["total_customers"],
            "Total Transactions": result["total_transactions"],
            "Total Deposits (Last Month)": f"${result['total_deposits']:,.2f}" if result["total_deposits"] else "$0",
            "Inactive Accounts": result["inactive_accounts"]
        }

        conn.close()
        return jsonify(kpis)

    except Exception as e:
        print(f"[ERROR] Failed to fetch KPIs: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ Execute SQL Query (Fixed)
@app.route("/execute_query", methods=["POST"])
def execute_query():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "Query is required!"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed!"}), 500

        cursor = conn.cursor()
        print(f"[INFO] Executing query: {query}")
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        conn.close()
        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] Query execution failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("[INFO] Flask API is running on port 5000...")
    app.run(debug=False, host="0.0.0.0", port=5000)  # ✅ `debug=False` & `host="0.0.0.0"`
