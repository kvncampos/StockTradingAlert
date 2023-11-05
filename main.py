import json
import yfinance as yahooFinance
from datetime import datetime
from smtplib import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from creds import GMAIL_SERVER, FROM_ADDRESS, TO_ADDRESS, PASSWORD
import logging

# ----------------- TICKER TO MONITOR -----------------------
TICKER = '^TNX'

def ticker_info(ticker=TICKER):
    return yahooFinance.Ticker(ticker)


# ----------------- LOGGING SETUP -----------------------
# set up logging to file
logging.basicConfig(
    filename='logs_for_ticker.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    filemode='a'
)

# ----------------- FETCH TICKET INFO -----------------------
logging.info(f"Starting StockTrackerApp for: {TICKER}")
ticker_data = ticker_info()

last_3_months = '3mo'
last_week = '1wk'
end_date = datetime.now().strftime('%Y-%m-%d')

# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y and ytd.
current_week = ticker_data.history(period=last_week, interval='1d')
last_6_months_data = ticker_data.history(period=last_3_months, interval='1wk')

# ----------------- TICKER INFO TODAY -----------------------
try:
    current_week.index = current_week.index.strftime('%Y-%m-%d')
except AttributeError:
    print('No data found, symbol may be delisted')
    logging.info(f"No data found, symbol may be delisted. Verify {TICKER}")

# Tap into the current day ticker info.
current_closing = current_week['Close'].tail(1)
current_closing_price = format(current_closing._get_value(0, 'Close'), '.3f')
today_date = current_week.index[-1]

# ----------------- TICKER INFO YESTERDAY -----------------------
# Tap into yesterday's ticker info.
previous_day = current_week['Close'].tail(2)
previous_day_closing_price = format(previous_day._get_value(0, 'Close'), '.3f')
yesterday_date = current_week.index[-2]

# ----------------- TICKER INFO PRICE TODAY VS YESTERDAY -----------------------
price_diff_today_vs_yesterday = format(float(current_closing_price) - float(previous_day_closing_price), '.4f')

percentage_change = format((float(current_closing_price) - float(previous_day_closing_price)) /
                           float(previous_day_closing_price) * 100, '.2f')

# ----------------- TICKER INFO OUTPUT FOR CONSOLE -----------------------
print(f'TICKER: 10 Year Treasury Yield')

print(
    f"------------------------------\n"
    f"--- Today's Closing Price: {today_date} -> \N{Dollar Sign}{current_closing_price}\n"
    f"--- Yesterday's Closing Price: {yesterday_date} -> \N{Dollar Sign}{previous_day_closing_price}"
)

good_vs_bad_day = None
if float(price_diff_today_vs_yesterday) < 0:
    good_vs_bad_day = "Price Has Gone Down! \N{down-pointing red triangle} \N{White Smiling Face}"
    print(f"Price Has Gone Down! \N{down-pointing red triangle} \N{White Smiling Face}")

    print(f"----------------------")
else:
    good_vs_bad_day = "Price Has Gone Up! \N{Chart with Upwards Trend} \N{White Frowning Face}"
    print(f"Price Has Gone Up! \N{Chart with Upwards Trend} \N{White Frowning Face}")
    print(f"----------------------")
print(f"--- Difference in Price Movement (Today vs Yesterday): \N{Dollar Sign}{price_diff_today_vs_yesterday}")
print(f"--- Percentage Change: {percentage_change}%")
print(f"---------------------------------------------------------------\n")

# ----------------- Last Weeks Data -----------------------
print('Last Weeks Data:\n')
print(current_week[['Open', 'High', 'Low', 'Close']])

# ----------------- Last 6 Month Data -----------------------
print('\n\nLast 6 Month Data:\n')
last_6_months_data.index = last_6_months_data.index.strftime('%Y-%m-%d')
print(last_6_months_data[['Open', 'Close']])

# ----------------- Latest 3 News Articles -----------------------
latest_3_news = ticker_data.get_news()[:3]
news_dict = {}
print("\n\nLatest 3 News Articles About the 10 Year Treasury Yield.")
for num, each_dict in enumerate(latest_3_news, start=1):
    for key, value in each_dict.items():
        if key == 'title':
            name_of_article = value
            print(f"  {num}) Title of Article: {value}")
        if key == 'link':
            news_dict[f'{name_of_article}'] = value
            print(f"  LinkURL: {value}")
    print()

logging.info("Script Ran Succesfully.")
# --------------------------- SNMP VARIABLES -----------------------------------

GMAIL_SERVER = GMAIL_SERVER
FROM_ADDRESS = FROM_ADDRESS
TO_ADDRESS = TO_ADDRESS
PASSWORD = PASSWORD
SUBJECT = f'10 Year Treasury Yield : {good_vs_bad_day}'
CURRENT_TIME = datetime.now()
NEWS = json.dumps(news_dict, indent=4)
NEWS_ARTICLES = list(news_dict.items())

# --------------------------- SNMP MESSAGE SETUP -----------------------------------
# EMAIL MESSAGE STRUCTURE IN HTML
MESSAGE = f"""
<div>
<h2>
10 Year Treasury Yield : {good_vs_bad_day}<br> ---------------------------------------------------------------------
</h2>
</div>
<div>
<h3>({today_date}) Today's Closing Price:</h3>
<h3 style="color:blue;" </h3>\N{Dollar Sign}{current_closing_price}</h3>
<p>----------------------------------------------------<br>
<h3>({yesterday_date}) Yesterday's Closing Price:</h3>
<h3 style="color:blue;" </h3>\N{Dollar Sign}{previous_day_closing_price}</h3>
<p>----------------------------------------------------<br>
<div>
<p>Difference in Price Movement (Today vs Yesterday):</p>
<h4 style="color:blue;">\N{Dollar Sign}{price_diff_today_vs_yesterday}</h4>
Percentage Change:
<h4 style="color:blue;">{percentage_change}%</h4>
<p>---------------------------------------------------------------
<h4>Latest 3 News Articles About the 10 Year Treasury Yield.</h4>
<p>
1) {NEWS_ARTICLES[0][0]}<br> URL: {NEWS_ARTICLES[0][1]}<br> 
2) {NEWS_ARTICLES[1][0]}<br> URL: {NEWS_ARTICLES[1][1]}<br> 
3) {NEWS_ARTICLES[2][0]}<br> URL: {NEWS_ARTICLES[2][1]}<br>
</p>
<br>
<b>Powered by www.pythonanywhere.com!</b><br>
<b>Ran on {CURRENT_TIME} </b
"""

# --------------------------- SNMP CONNECTION SETUP -----------------------------------
# Send Email with TICKER Information for the Day
with SMTP(GMAIL_SERVER, port=587) as connection:
    connection.starttls()
    connection.login(FROM_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Subject'] = SUBJECT

    # add in the message body
    msg.attach(MIMEText(MESSAGE, 'html'))
    connection.send_message(msg)

    print(msg)
    connection.quit()

