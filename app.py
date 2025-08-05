import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Sales Data Dashboard')

# Upload file
uploaded_file = st.file_uploader("Upload your sales_data.xlsx file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")
    st.write(df.head())

    # Data Cleaning
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
    df['Product_ID'] = df['Product_ID'].astype(int)
    df['Sales_Amount'] = df['Sales_Amount'].astype(float)
    df['Quantity_Sold'] = df['Quantity_Sold'].astype(int)
    df['Unit_Cost'] = df['Unit_Cost'].astype(float)
    df['Unit_Price'] = df['Unit_Price'].astype(float)
    df['Discount'] = df['Discount'].astype(float)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    text_columns = ['Sales_Rep', 'Region', 'Product_Category',
                    'Customer_Type', 'Payment_Method', 'Sales_Channel', 'Region_and_Sales_Rep']
    for col in text_columns:
        df[col] = df[col].str.lower().str.strip()

    st.subheader("Cleaned Data Overview")
    st.write(df.info())

    # Visualization 1: Revenue by Region
    st.subheader("Revenue by Region")
    region_sales = df.groupby('Region')['Sales_Amount'].sum().sort_values(ascending=False)
    st.bar_chart(region_sales)

    # Visualization 2: Top 5 Products by Revenue
    st.subheader("Top 5 Products by Revenue")
    top_products = df.groupby('Product_ID')['Sales_Amount'].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_products)

    # Visualization 3: Revenue per Salesperson
    st.subheader("Revenue by Sales Representative")
    sales_rep_revenue = df.groupby('Sales_Rep')['Sales_Amount'].sum().sort_values(ascending=False)
    st.bar_chart(sales_rep_revenue)

    # Visualization 4: Customer Type Distribution
    st.subheader("Customer Type Distribution")
    customer_type_counts = df['Customer_Type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(customer_type_counts, labels=customer_type_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
    st.pyplot(fig)

    # Visualization 5: Sales Amount vs Discount
    st.subheader("Sales Amount vs Discount")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df['Discount'], df['Sales_Amount'], alpha=0.5, color='purple')
    ax2.set_xlabel('Discount')
    ax2.set_ylabel('Sales Amount')
    ax2.set_title('Sales Amount vs Discount')
    st.pyplot(fig2)
else:
    st.info('Please upload an Excel file to proceed.')
