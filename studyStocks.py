## use from PersonalProjects.FinancialAnalysis.predict_stocks
# from datetime import datetime
# from readStocks import read_stock_data
import pandas as pd
from RSI import calculate_rsi
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, r2_score
import matplotlib.pyplot as plt

# loading data
tick = "AAPL"

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    ## make new features
    # get rsi_14 from previous days
    data["RSI_14"] = calculate_rsi(data, 14)

    # get previous day's data
    data2 = data.shift(1)
    data['Prev_RSI_14'] = data2['RSI_14']
    data['Prev_Close'] = data2['Close']

    # convert date and time to numerical features
    data['Date Time'] = pd.to_datetime(data['Date Time'])
    data['Year'] = data['Date Time'].dt.year
    data['Month'] = data['Date Time'].dt.month
    data['Day'] = data['Date Time'].dt.day
    data['Weekday'] = data['Date Time'].dt.day_of_week
    if((data['Date Time'].dt.hour.sum()) + (data['Date Time'].dt.minute.sum()) != 0):
        data['Hour'] = data['Date Time'].dt.hour
        data['Minute'] = data['Date Time'].dt.minute
    
    # select features
    data = data.drop(['Date Time', 'Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits']
                      , axis=1)
    
    # eliminate missing values
    data=data.dropna(axis=0, how='any') 
    
    return data    

# data = clean_data(read_stock_data(tick, "8d", "1m"))
# print(data.head())

def pred_model(data: pd.DataFrame, evaluate: bool = False) -> RandomForestRegressor:
    # data = read_stock_data(tick, periods, intervals)
    # if("d" not in intervals):
    #     data = clean_data(data, True)
    # else:
    #     data = clean_data(data)
    
    # split data into training and testing sets
    X = data.drop(columns=['Close'], axis=1)
    y = data['Close']

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=89)
    except:
        print("Period and interval do not make for enough data points to train a random forest model on")
        return None

    # initialize the random forest objects
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=89)

    # train the model
    rf_reg.fit(X_train, y_train)

    # make predictions
    y_pred = rf_reg.predict(X_test)

    ## Evaulate model (optional)
    if(evaluate):
        results = pd.DataFrame(X_test, columns=X.columns)  # Test features

        results[f'Act_Close'] = y_test 
        results[f'Regr_Close'] = y_pred

        # # filter data
        # results = results[results['Year'] == 2020]
        
        drops = ['Year', 'Month', 'Day']
        renames = {'Year': 'year', 'Month': 'month', 'Day': 'day'}
        if("Hour" in  results.columns or "Minute" in results.columns):
            drops.extend(['Hour', 'Minute'])
            renames['Hour'] = 'hour'
            renames['Minute'] = 'minute'
        results['Date Time'] = pd.to_datetime(results[drops].rename(renames))
        results = results.set_index('Date Time').sort_index(axis=0, ascending=True).drop(drops, axis=1).drop('Weekday', 
                                                                                                             axis = 1)

        # see preview of results
        print(results.head())

        # Plot actual vs predicted
        plt.figure(figsize=(10, 6))
        plt.plot(results.index, results['Act_Close'], label='Actual Close', color='blue', linewidth=2)
        plt.plot(results.index, results['Regr_Close'], label='Predicted Close', color='red', linestyle='--', linewidth=2)
        
        ## Customize the plot
        plt.title(f'Actual vs Predicted Closes ({tick})', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close', fontsize=12)
        plt.legend()
        plt.grid(True)
       
        # Rotate x-axis labels for better readability
        plt.gcf().autofmt_xdate()
       
        # show plot
        plt.show()

        # Evaluation metrics
        print(f'Root Mean Squared Error: {root_mean_squared_error(y_test, y_pred)}') # lower wanted
        print(f"R^2: {r2_score(y_test, y_pred)}") # higher wanted
    
    return rf_reg

# # model test
# model = pred_model(data, True)