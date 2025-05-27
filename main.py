import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Streamlit setup
st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns] # Remove leading/trailing whitespace
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float) # Convert Amount to float after removing commas
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") # Convert Date to datetime format
        
        # st.write(df)
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# File uploading & loading w/ pandas
def main():
    # Page title
    st.title("Simple Finance Dashboard")
    
    # Upload file component
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            # Create a summary of debits and credits
            tab1, tab2 = st.tabs(["Expenses (Debit)", "Incomes (Credits)"])
            with tab1:
                st.write(debits_df)

            with tab2:
                st.write(credits_df)

        
main()