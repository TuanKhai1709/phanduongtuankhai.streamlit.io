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
    
    fig, ax = plt.subplots(figsize=(8,5))
    region_sales.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Revenue by Region')
    ax.set_ylabel('Total Revenue')
    ax.set_xlabel('Region')
    plt.xticks(rotation=0)  # Rotate x labels 0 degrees (horizontal)
    st.pyplot(fig)

    # Visualization 2: Top 5 Products by Revenue
    st.subheader("Top 5 Products by Revenue")

    top_products = df.groupby('Product_ID')['Sales_Amount'].sum().sort_values(ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(8,5))
    top_products.plot(kind='barh', color='orange', ax=ax)
    ax.set_title('Top 5 Products by Revenue')
    ax.set_xlabel('Total Revenue')
    ax.set_ylabel('Product ID')
    ax.invert_yaxis()  # Put the best-selling product on top
    st.pyplot(fig)
    
    # Visualization 3: Revenue per Salesperson
    st.subheader("Revenue by Sales Representative")

    sales_rep_revenue = df.groupby('Sales_Rep')['Sales_Amount'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(8,5))
    sales_rep_revenue.plot(kind='bar', color='mediumseagreen', ax=ax)
    ax.set_title('Revenue by Sales Representative')
    ax.set_ylabel('Total Revenue')
    ax.set_xlabel('Sales Rep')
    plt.xticks(rotation=45)
    st.pyplot(fig)

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
