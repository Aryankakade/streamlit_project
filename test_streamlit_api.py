import streamlit as st 
import requests 
 
st.title("Streamlit API Test") 
 
url = "http://127.0.0.1:5000/data/transactions" 
response = requests.get(url) 
 
if response.status_code == 200: 
    data = response.json() 
    st.write("? API Response:") 
    st.json(data) 
else: 
    st.error(f"? API Request Failed: {response.status_code}") 
