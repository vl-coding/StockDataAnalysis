import pandas as pd
# import numpy as np

# def read_stock_data(ticker):
#     file_path = f"FinancialAnalysis\Stock Data\{ticker}.csv"
#     data = pd.read_csv(file_path)
#     return data

def calculate_rsi(data: pd.DataFrame, periods=14):
    # Calculate daily price changes
    delta = data['Close'].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate initial averages for the first 14 days
    avg_gains = gains.rolling(window=periods, min_periods=periods).mean()
    avg_losses = losses.rolling(window=periods, min_periods=periods).mean()
    
    # Initialize RSI series
    rsi = pd.Series(index=data.index, dtype=float)
    
    # Calculate RSI for each day
    for i in range(periods, len(data)):
        if i == periods:
            # First RSI using simple average
            avg_gain = avg_gains.iloc[i]
            avg_loss = avg_losses.iloc[i]
        else:
            # Smoothed averages for subsequent days
            current_gain = gains.iloc[i]
            current_loss = losses.iloc[i]
            avg_gain = ((avg_gains.iloc[i-1] * (periods - 1)) + current_gain) / periods
            avg_loss = ((avg_losses.iloc[i-1] * (periods - 1)) + current_loss) / periods
            avg_gains.iloc[i] = avg_gain
            avg_losses.iloc[i] = avg_loss
        
        # Calculate RS and RSI
        if avg_loss == 0:
            rsi.iloc[i] = 100
        elif avg_gain == 0:
            rsi.iloc[i] = 0
        else:
            rs = avg_gain / avg_loss
            rsi.iloc[i] = 100 - (100 / (1 + rs))
    
    return rsi

# # Load data
# data = read_stock_data('AAPL')
# # Add RSI_14 column to DataFrame
# data['RSI_14'] = calculate_rsi(data)
# # Display the last 16 rows for verification
# print(data.tail(16))