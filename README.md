# Online Currency Converter

A simple desktop currency converter built with **Python**, **Tkinter**, and the **Frankfurter Exchange Rates API**. Enter an amount in US dollars (USD), choose a country, and retrieve an exchange rate online to calculate the converted amount.

## Features

- Simple graphical user interface built with Tkinter.
- Fetches exchange rates online through the Frankfurter API.
- Converts USD into the selected currency.
- Supports these country selections:
  - Mexico — Mexican Peso (MXN)
  - Bangladesh — Bangladeshi Taka (BDT)
  - China — Chinese Yuan (CNY)
  - Japan — Japanese Yen (JPY)
  - France — Euro (EUR)
  - Germany — Euro (EUR)
  - Italy — Euro (EUR)
  - Pakistan — Pakistani Rupee (PKR)
  - Russia — Russian Ruble (RUB)
  - Saudi Arabia — Saudi Riyal (SAR)
- Displays results to two decimal places.
- Includes basic validation and handles unavailable rates or network errors.

## Requirements

- Python 3
- Internet connection
- `requests` package

Tkinter is included with many standard Python installations. On some Linux distributions, it may need to be installed separately.

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   cd YOUR-REPOSITORY
   ```

   Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub username and repository name.

2. **Install the dependency:**

   ```bash
   python -m pip install requests
   ```

3. **Run the application:**

   ```bash
   python online_currency_converter.py
   ```

   Depending on your Python installation, you may need to use `python3` instead of `python`.

## How to Use

1. Launch the application.
2. Enter the amount in USD.
3. Select a country from the dropdown menu.
4. Click **Convert Currency**.
5. Read the converted amount in the output area.

## API

The application uses the Frankfurter API to request a rate for a currency pair. For example:

```text
https://api.frankfurter.dev/v2/rate/USD/MXN
```

The response contains the exchange rate used by the application. The app multiplies the entered USD amount by that rate.

- API website: https://frankfurter.dev/
- API documentation: https://frankfurter.dev/

Rates depend on the data available from the API and are **not guaranteed to be live trading rates**. An internet connection is required for a successful conversion. If the request fails or the rate is unavailable, the application displays an error message.

## Project Structure

```text
.
├── online_currency_converter.py
└── README.md
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'requests'`

Install the dependency:

```bash
python -m pip install requests
```

### Exchange rate unavailable

- Check that your computer is connected to the internet.
- Try again later if the API is temporarily unavailable.
- Check the Frankfurter API documentation for supported currencies and endpoints.

### Tkinter is unavailable

Install the Tkinter package appropriate for your operating system or Python distribution.
