import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from categorizer import categorize_expense
from predictor import predict_next_month
from analyzer import get_saving_tips

st.set_page_config(page_title="AI Finance Tracker", page_icon="💰", layout="wide")
st.title("💰 AI Finance Tracker")
st.markdown("*Upload your bank statement → Get instant AI-powered insights*")

st.sidebar.header("📂 Upload Statement")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
use_sample = st.sidebar.button("Try with Sample Data")

if use_sample:
    sample_path = os.path.join(BASE_DIR, "data", "sample_statement.csv")
    df = pd.read_csv(sample_path)
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = None

if df is not None:
    st.subheader("Your Transactions")
    st.dataframe(df, use_container_width=True)

    with st.spinner("AI is analyzing your expenses..."):
        df["Category"] = df["Description"].apply(categorize_expense)

    st.success("Categorization complete!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Spending by Category")
        category_totals = df.groupby("Category")["Amount"].sum().reset_index()
        fig = px.pie(category_totals, values="Amount", names="Category",
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Transaction Breakdown")
        fig2 = px.bar(category_totals, x="Category", y="Amount", color="Category",
                      color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Key Numbers")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Spent", f"${df['Amount'].sum():.2f}")
    m2.metric("Avg Transaction", f"${df['Amount'].mean():.2f}")
    m3.metric("Biggest Expense", f"${df['Amount'].max():.2f}")

    st.subheader("Next Month Prediction")
    prediction = predict_next_month(df["Amount"].tolist())
    st.info(f"Based on your spending, you will likely spend ${prediction} next month.")

    st.subheader("AI Saving Tips")
    with st.spinner("Generating personalized tips..."):
        tips = get_saving_tips(df)
    st.markdown(tips)

else:
    st.info("Upload your bank statement CSV from the sidebar, or click Try with Sample Data!")
