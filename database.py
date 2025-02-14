from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote

USERNAME = "root"
PASSWORD = quote("Aryankakade@143")  # Fix the @ issue
HOST = "localhost"
PORT = "3306"
DATABASE = "bank1"

engine = create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

def fetch_data(query):
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"⚠ Error Fetching Data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if error




