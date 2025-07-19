## use from PersonalProjects.FinancialAnalysis.predict_stocks
# from datetime import datetime
import pandas as pd
from readStocks import read_stock_data
from studyStocks import pred_model, clean_data
from RSI import calculate_rsi
import matplotlib.pyplot as plt

def pred_future(tick: str, period: str, interval: str, future: str) -> pd.DataFrame:
    future = pd.to_datetime(future)
    if(future < pd.to_datetime(pd.Timestamp.now().date())):
        print("Not in the future")
        return None
    elif(future == pd.to_datetime(pd.Timestamp.now().date())):
        if(future.time() < pd.to_datetime(pd.Timestamp.now()).time()):
            print("Not in the future")
            return None
    if(future.day_of_week in [5, 6]):
        print("Future date falls on weekend.")
        return None
    

    original = read_stock_data(tick, period, interval)
    pred_data = clean_data(original)
    model = pred_model(pred_data)
    time = ("Hour" in pred_data.columns or "Minute" in pred_data.columns)
    delta = ""
    delta_period = ""
    for i in interval:
        if(i.isdigit()):
            delta = delta + str(i)
        elif(i.isalpha()):
            delta_period = delta_period + i
    delta = int(delta)

    next_stock = pd.to_datetime(original['Date Time'].iloc[-1])
    futures = 0
    while(next_stock <= future):
        # if(next_stock.day_of_week == 4):
        #     delta = delta + 2
        gap = pd.to_timedelta(delta, delta_period)
        next_stock = next_stock + gap
        new_data = pd.DataFrame({
            # 'Close' : {0: None},
            'RSI_14' : {0: calculate_rsi( pred_data.shift(-1).tail(15) , 14).iloc[-1]},
            'Prev_RSI_14' : {0: pred_data['RSI_14'].iloc[-1]},
            'Prev_Close' : {0: pred_data['Close'].iloc[-1]},
            'Year' : {0: float(next_stock.year)},
            'Month': {0: float(next_stock.month)},
            'Day' : {0: float(next_stock.day)},
            'Weekday': {0: float(next_stock.day_of_week)}
        })
        if(time):
            new_data['Hour'] = float(next_stock.hour),
            new_data['Minute'] = float(next_stock.minute)
        # print(new_input)

        # model = pred_model(pred_data)
        new_data['Close'] = model.predict(new_data)
        # print(new_data)

        pred_data = pd.concat([pred_data, new_data], axis=0, ignore_index=True)
        # print(data.tail(5))
        futures = futures + 1
        # print(next_stock)
    
    pred_data = pred_data.tail(30 + futures)

    date_and_time = ['Year', 'Month', 'Day']
    renames = {'Year': 'year', 'Month': 'month', 'Day': 'day'}
    if(time):
        date_and_time.extend(['Hour', 'Minute'])
        renames['Hour'] = 'hour'
        renames['Minute'] = 'minute'
    pred_data = pred_data.set_index(pd.to_datetime(pred_data[date_and_time].rename(renames)))
    date_and_time.append('Weekday')
    pred_data = pred_data.sort_index(axis=0, ascending=True).drop(date_and_time, axis=1)
    # print(pred_data)
    
    # visualize
    # Plot actual and predicted
    plt.figure(figsize=(10, 6))
    plt.plot(pred_data.head(30).index, pred_data.head(30)['Close'], label='Actual Close', color='blue', linewidth=2)
    plt.plot(pred_data.tail(1+futures).index, pred_data.tail(1+futures)['Close'], label='Predicted Close', color='red', linestyle='--', linewidth=2)
    ## Customize the plot
    plt.title(f'Actual and Predicted Closes ({tick})', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Close', fontsize=12)
    plt.legend()
    plt.grid(True)
    # Rotate x-axis labels for better readability
    plt.gcf().autofmt_xdate()
    # show plot
    plt.show()

    return pred_data.tail(futures+1)

tick = "RIOT"
future_date = pd.to_datetime('06-23-2025 00:00:00')

the_future = pred_future(tick, "7d", "5m", future_date)
print(the_future)

# next_stock = pd.to_datetime('06-02-2025 05:00:00')
# while(next_stock < future_date):
#     gap = pd.to_timedelta(1, "hr")
#     next_stock = next_stock + gap
#     print(next_stock)
