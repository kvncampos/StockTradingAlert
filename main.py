import yfinance as yahooFinance
from datetime import datetime

get_10_year_treasury_yield_data = yahooFinance.Ticker("^TNX")

last_3_months = '3mo'
last_week = '1wk'
end_date = datetime.now().strftime('%Y-%m-%d')

# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y and ytd.
last_week_data = get_10_year_treasury_yield_data.history(period=last_week, interval='1d')
last_6_months_data = get_10_year_treasury_yield_data.history(period=last_3_months, interval='1wk')

# ----------------- TICKER INFO -----------------------
print(f'TICKER: 10 Year Treasury Yield')

# ----------------- TICKER INFO TODAY -----------------------
close_price = last_week_data
close_price.index = close_price.index.strftime('%Y-%m-%d')


current_closing = close_price['Close'].tail(1)
current_closing_price = format(current_closing._get_value(0, 'Close'), '.3f')
today_date = close_price.index[-1]

# ----------------- TICKER INFO YESTERDAY -----------------------
yesterday_price = last_week_data
previous_day = close_price['Close'].tail(2)
previous_day_closing_price = format(previous_day._get_value(0, 'Close'), '.3f')
yesterday_date = yesterday_price.index[-2]

# ----------------- TICKER INFO PRICE TODAY VS YESTERDAY -----------------------
price_diff_today_vs_yesterday = format(float(current_closing_price) - float(previous_day_closing_price), '.4f')

percentage_change = format((float(current_closing_price) - float(previous_day_closing_price)) /
                           float(previous_day_closing_price) * 100, '.4f')

# ----------------- TICKER INFO OUTPUT -----------------------
print(
    f"------------------------------\n"
    f"--- Today's Closing Price: {today_date} -> \N{Dollar Sign}{current_closing_price}\n"
    f"--- Yesterday's Closing Price: {yesterday_date} -> \N{Dollar Sign}{previous_day_closing_price}"
)
if float(price_diff_today_vs_yesterday) < 0:
    print(f"Price Has Gone Down! \N{White Smiling Face}")
    print(f"----------------------")
else:
    print(f"Price Has Gone Up! \N{White Frowning Face}")
    print(f"----------------------")
print(f"--- Difference in Price Movement (Today vs Yesterday): \N{Dollar Sign}{price_diff_today_vs_yesterday}")
print(f"--- Percentage Change: {percentage_change}%")
print(f"---------------------------------------------------------------\n")

# ----------------- Last Weeks Data -----------------------
print('Last Weeks Data:\n')
print(last_week_data[['Open', 'High', 'Low', 'Close']])


# ----------------- Last 6 Month Data -----------------------
print('\n\nLast 6 Month Data:\n')
last_6_months_data.index = last_6_months_data.index.strftime('%Y-%m-%d')
print(last_6_months_data[['Open', 'Close']])

# ----------------- Latest 3 News Articles -----------------------
latest_3_news = get_10_year_treasury_yield_data.get_news()[:3]
print("\n\nLatest 3 News Articles About the 10 Year Treasury Yield.")
for num, each_dict in enumerate(latest_3_news, start=1):
    for key, value in each_dict.items():
        if key == 'title':
            print(f"  {num}) Title of Article: {value}")
        if key == 'link':
            print(f"  LinkURL: {value}")
    print()


