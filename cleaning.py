import pandas as pd
def jag_bank_clean(data):
    for i in data.index:
        for j in data.iloc[i]:
            if j =='Date':
                data.columns=[k for k in data.iloc[i]]
                continue
    data['Date']=pd.to_datetime(data['Date'],errors='coerce')
    data['Value Date']=pd.to_datetime(data['Value Date'],errors='coerce')
    data.dropna(subset=['Particulars','Value Date'],inplace=True)
    data.reset_index(drop=True,inplace=True)
    data['Month']=data['Date'].dt.month
    data['Year']=data['Date'].dt.year
    return data

def mani_bank_clean(data):
    for i in data.index:
        for j in data.iloc[i]:
            if j =='Date':
                data.columns=[k for k in data.iloc[i]]
                continue
    data['Date']=pd.to_datetime(data['Date'],errors='coerce')
    data['Value Date']=pd.to_datetime(data['Value Dt'],errors='coerce')
    data.dropna(subset=['Narration','Value Date'],inplace=True)
    data.reset_index(drop=True,inplace=True)
    data['Month']=data['Date'].dt.month
    data['Year']=data['Date'].dt.year
    
    return data
def mop(col):
    if 'UPI IN' in str(col):
        return 'UPI IN'
    elif 'UPIOUT' in str(col):
        return 'UPI OUT'
    elif 'IMPS' in str(col):
        return 'IMPS'
    else:
        return 'Others'

def loadfile(path):
    data=pd.read_excel(path)
    return data
def mani_process_query(llm, df, query):
    if df.columns==['Date', 'Narration', 'Chq./Ref.No.', 'Value Dt', 'Withdrawal Amt.','Deposit Amt.', 'Closing Balance', 'Value Date', 'Month', 'Year']:
        monthly_summary = df.groupby('Month')[['Withdrawal Amt.', 'Deposit Amt.']].sum()
    
    # Convert summary to a string with Rupee symbol
    summary_text = monthly_summary.to_string(formatters={'Withdrawal Amt.': '₹{:,.2f}'.format, 'Deposit Amt.': '₹{:,.2f}'.format})