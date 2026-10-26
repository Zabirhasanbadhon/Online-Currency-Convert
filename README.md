# 🌍 ZaBir GlobeX

A modern, desktop-based **Currency Converter** built with Python and Tkinter. It features a beautiful cream-white interface and retrieves supported currencies and exchange rates online using the [Frankfurter API](https://frankfurter.dev/).

Convert between supported currencies from around the world with a clean, simple, and user-friendly interface.

## ✨ Features

- 🌎 **Global Currency Support:** Dynamically loads available currencies from the Frankfurter API.
- 💱 **Live Exchange Rates:** Retrieves the latest available reference exchange rates online.
- 🎨 **Modern UI:** Features a cream-white background, elegant typography, and a soft green color palette.
- 🔄 **Currency Swap:** Quickly switch the source and target currencies.
- ⚡ **Background Processing:** Fetches exchange rates in a separate thread to keep the interface responsive.
- ✅ **Input Validation:** Handles invalid amounts and prevents negative values.
- 📊 **Conversion Details:** Displays the converted amount, exchange rate, and rate date when available.
- 🌐 **Internet Connectivity Handling:** Displays an error message when the API is unavailable.
- 🖥️ **Desktop Application:** Built with Python's Tkinter GUI toolkit.

## 🛠️ Technologies Used

- **Python** — Core programming language.
- **Tkinter** — Graphical user interface.
- **Requests** — HTTP requests to retrieve currencies and exchange rates.
- **Threading** — Background processing for network requests.
- **Frankfurter API** — Currency information and exchange rates.

## 📋 Requirements

Before running this project, make sure you have:

- Python 3.8 or later.
- An active internet connection.
- The `requests` Python library.

## 💡 How to Use

1. Launch the application.
2. Enter the amount you want to convert.
3. Select the source currency from the **From Currency** dropdown.
4. Select the target currency from the **To Currency** dropdown.
5. Click **Convert Currency**.
6. View the converted amount, exchange rate, and rate date when available.
7. Use **Swap Currencies** to reverse the selected currencies.

### Example

Suppose you want to convert 100 US Dollars (USD) into Bangladeshi Taka (BDT).

- **Amount:** 1
- **From Currency:** USD — US Dollar
- **To Currency:** BDT — Bangladeshi Taka

The application retrieves the available exchange rate and calculates the converted amount.

*The actual result depends on the exchange rate returned by the API.*

## 🔌 API Information

This project uses the **Frankfurter API** to retrieve currency information and exchange rates.

- **Official Website:** https://frankfurter.dev/
- **Currency Catalogue:** `/v2/currencies`
- **Exchange Rate Endpoint:** `/v2/rate/{base}/{quote}`

Example endpoint:

```text
https://api.frankfurter.dev/v2/rate/USD/BDT
```

The API provides reference exchange rates. These rates may differ from those offered by banks, money exchangers, or payment services.

**Note:** The available currency catalogue does not necessarily include every national currency worldwide.

## ⚠️ Limitations

- An internet connection is required to retrieve currency data and exchange rates.
- Only currencies supported by the API can be used successfully.
- Exchange rates are reference rates and may not match real-time commercial rates.
- The application does not execute actual currency exchanges or financial transactions.
- Currency availability and the dates of available rates depend on the API.

## 👨‍💻 Author

**ZaBir HaSan**

**Built with Python, Tkinter, and the Frankfurter API.**
