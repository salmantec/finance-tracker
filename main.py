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
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


# File uploading & loading w/ pandas
def main():
    st.title("Simple Finance Dashboard")
    
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        
main()