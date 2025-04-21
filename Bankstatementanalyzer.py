import streamlit as st
import pandas as pd
import ollama
from cleaning import jag_bank_clean, mop
# Load, clean, and preprocess bank statement data
path = r"C:\Users\zineb\Downloads\AccountStatement_2023_2024.xlsx"
df=pd.read_excel(path)
jag_bank_clean(df)
mop(df['Particulars'])
df['Date'] = pd.to_datetime(df['Date'],format='%d-%m-%Y', errors='coerce')
df['Month'] = df['Date'].dt.strftime('%m-%Y')
df.to_csv('cleaned_bank_statement.csv', index=False)  # Save cleaned data

# Initialize chatbot model
def initialize_chatbot():
    return "llama3"

# Filter data by name in 'Particulars'
def filter_by_name(df, name):
    df1 = df[df['Particulars'].str.contains(name, case=False, na=False)].loc[:,['Date','Particulars','Withdrawals','Deposits','Year']]
    df2=df1.describe().iloc[[0,1,3,-1],[0,1]]
    sumdf = df1.groupby('Year')[['Withdrawals','Deposits']].sum()
    mindf = df1.groupby('Year')[['Withdrawals','Deposits']].min()
    maxdf = df1.groupby('Year')[['Withdrawals','Deposits']].max()
    wtot = df1['Withdrawals'].sum()
    # wmin['Withdrawals'].min()
    min = df1['Withdrawals'].max()
    max = df1['Deposits'].sum()
    df1['Deposits'].min()
    df1['Deposits'].max()
    return df1,df2

# Process user queries with Llama 3 via Ollama
def process_query(llm, df, query):
    # monthly_summary = df.groupby('Month').agg({
    #     'Withdrawals': 'sum',
    #     'Deposits': 'sum'
    # }).reset_index()
    monthly_summary = df.groupby('Month')[['Withdrawals','Deposits']].sum().reset_index()
    yearly_summary = df.groupby('Year')[['Withdrawals','Deposits']].sum().reset_index()
    
    if 'month' in query.lower():
        summary_text = monthly_summary.to_string(index=False, formatters={
            'Withdrawals': lambda x: f'₹{x:,.2f}',
            'Deposits': lambda x: f'₹{x:,.2f}'
    })
    else:
        summary_text = yearly_summary.to_string(index=False, formatters={
            'Withdrawals': lambda x: f'₹{x:,.2f}',
            'Deposits': lambda x: f'₹{x:,.2f}'
    })

    
    response = ollama.chat(model=llm, messages=[
        {"role": "system", "content": "You are a financial assistant analyzing bank statements. All amounts are in Indian Rupees (₹ INR)."},
        {"role": "user", "content": f"Here is my monthly financial summary in INR:\n\n"
                                      f"Month-wise Total Income (Deposits) and Expenses (Withdrawals):\n{summary_text}\n\n"
                                      f"Question: {query}"}
    ])
    return response["message"]["content"]

# Streamlit UI
def main():
    st.title("Bank Statement Analyzer Chatbot 💰")
    st.write("Upload your cleaned bank statement CSV and ask financial questions.")
    
    uploaded_file = st.file_uploader("Upload Cleaned CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)  # Load already cleaned data
        # df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        # df['Month'] = df['Date'].dt.strftime('%m-%Y')
        
        llm = initialize_chatbot()
        st.write("### Bank Statement Preview:")
        st.dataframe(df.head())
        
        # Display Monthly Summary Table
        st.write("### Monthly Income & Expense Summary:")
        monthly_summary = df.groupby('Month')[['Withdrawals','Deposits']].sum().reset_index()
        st.dataframe(monthly_summary)
        
        # Name filter
        name_filter = st.text_input("Filter transactions by name in 'Particulars':")
        if name_filter:
            filtered_df,df2 = filter_by_name(df, name_filter)
            if not filtered_df.empty:
                st.write(f"### Transactions containing '{name_filter}':")
                st.dataframe(filtered_df)
                st.write(df2)
                # st.dataframe(min)
                # st.dataframe(max)
            else:
                st.warning("No transactions found with the specified name.")
        
        query = st.text_input("Ask a financial question:")
        if st.button("Submit") and query:
            response = process_query(llm, df, query)
            st.write("### Chatbot Response:")
            st.write(response)
        elif not query:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
