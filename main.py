import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Streamlit setup
st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

category_file = "categories.json"
default_category = "Uncategorized"

# Different categories of transactions
# Initialize session state for categories if not already present
if "categories" not in st.session_state:
    st.session_state.categories = {
        default_category: [],
    }

# Load categories from JSON file if it exists
if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)

def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)

def categorize_transaction(df):
    df["Category"] = default_category  # Default category

    for category, keywords in st.session_state.categories.items():
        if category == default_category or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            details = row["Details"].lower().strip()
            if details in lowered_keywords:
                df.at[idx, "Category"] = category

    return df

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns] # Remove leading/trailing whitespace
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float) # Convert Amount to float after removing commas
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") # Convert Date to datetime format
        
        # st.write(df)
        return categorize_transaction(df)
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
                # Allow user to add the category
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()
                    else:
                        st.warning(f"Category '{new_category}' already exists.")


                st.write(debits_df)

            with tab2:
                st.write(credits_df)

        
main()