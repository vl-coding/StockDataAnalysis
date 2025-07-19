import yfinance as yf
import csv
import pandas as pd

tickers = ["AAPL", "NOBL", "MSFT", "META", "TSLA", "NVDA", "GOOGL", "GOOG", 
           "RIOT", "WULF", "BITF"]

def write_to_csv(tick: str, data: pd.DataFrame) -> None:
    file_path = "FinancialAnalysis\\Stock Data\\" + tick + ".csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ["Date Time"]
        headers.extend(i for i in data)
        writer.writerow(headers)
        for index, row in data.iterrows():
            input = []
            input.append(pd.to_datetime(index).strftime("%Y-%m-%d %H:%M:%S"))
            input.extend([row[i] for i in data])
            writer.writerow(input)
    # print(f"Data written to {ticker}.csv")

# for i in tickers:
#     stock = yf.Ticker(i)
#     # Fetch historical data for the last 5 years with daily intervals
#     data = pd.DataFrame(stock.history(period="5y", interval="1d"))
#     # data['Day_Delta'] = data['Close'] - data['Open']
#     # chg = data["Close"] - data["Open"]
#     # data["Status"] = chg.apply(lambda x: "Gain" if x > 0 else "Loss")
#     write_to_csv(i, data)
# # print("Data fetching and writing completed for all tickers.")

def read_stock_data(tick: str, period: str, interval: str) -> pd.DataFrame:
    stock = yf.Ticker(tick)
    data = pd.DataFrame(stock.history(period, interval))
    write_to_csv(tick, data)
    file_path = "FinancialAnalysis\\Stock Data\\" + tick + ".csv"
    data = pd.read_csv(file_path)
    return data

# data = read_stock_data(tickers[0], "5y", "1d")
# print(data.head())