# Stock Analysis Tool

This Python script retrieves and analyzes the 10 Year Treasury Yield data using the Yahoo Finance API.

## Prerequisites

- [yfinance](https://pypi.org/project/yfinance/): A Python library that provides an interface to Yahoo Finance.

You can install it using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Create a creds.py with your Email Credentials. You will need App Password from your SNMP Server.

        GMAIL_SERVER = "smtp.email_provier.com"
        FROM_ADDRESS = 'email@email.com'
        TO_ADDRESS = 'email@email.com'
        PASSWORD = "SNMP_APP_PASSWORD"

- GMAIL APP PASSWORD HELP: https://support.google.com/mail/answer/185833?hl=en

2. Change the Ticker in the 'TICKER' Variable to what you want to monitor.

       line10: TICKER = '^TNX'

       line13: def ticker_info(ticker=TICKER):
                  return yahooFinance.Ticker(ticker)
