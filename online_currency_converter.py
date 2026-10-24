import tkinter as tk
from tkinter import ttk
import requests


def get_exchange_rate(base_currency, target_currency):
    """Fetch an exchange rate from the Frankfurter API."""
    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{base_currency}/{target_currency}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["rate"])

    except (requests.RequestException, KeyError, TypeError, ValueError):
        return None


def convert_currency():
    """Convert the entered USD amount into the selected currency."""
    amount_text = amount_entry.get().strip()

    try:
        amount = float(amount_text)
        if amount < 0:
            raise ValueError
    except ValueError:
        output_var.set("Please enter a valid positive amount.")
        return

    target_currency = currency_var.get()

    # Currency code and display name for each country.
    currencies = {
        "Mexico": ("MXN", "Mexican Peso"),
        "Bangladesh": ("BDT", "Bangladeshi Taka"),
        "China": ("CNY", "Chinese Yuan"),
        "Japan": ("JPY", "Japanese Yen"),
        "France": ("EUR", "Euro"),
        "Germany": ("EUR", "Euro"),
        "Italy": ("EUR", "Euro"),
        "Pakistan": ("PKR", "Pakistani Rupee"),
        "Russia": ("RUB", "Russian Ruble"),
        "Saudi Arabia": ("SAR", "Saudi Riyal"),
    }

    currency_code, currency_name = currencies[target_currency]
    output_var.set("Getting exchange rate online...")

    rate = get_exchange_rate("USD", currency_code)

    if rate is None:
        output_var.set(
            "Exchange rate unavailable. Check your internet connection "
            "or try again later."
        )
        return

    converted_amount = amount * rate
    output_var.set(
        f"{amount:,.2f} USD = {converted_amount:,.2f} {currency_name}"
    )


root = tk.Tk()
root.title("Online Currency Converter")
root.geometry("520x300")
root.configure(bg="white")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Online Currency Converter",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="black",
)
title_label.pack(pady=(20, 15))

amount_label = tk.Label(
    root,
    text="Amount in US Dollars (USD):",
    font=("Arial", 11),
    bg="white",
)
amount_label.pack()

amount_entry = ttk.Entry(root, font=("Arial", 12), justify="center", width=25)
amount_entry.pack(pady=6)
amount_entry.insert(0, "100")

currency_label = tk.Label(
    root,
    text="Choose a country:",
    font=("Arial", 11),
    bg="white",
)
currency_label.pack(pady=(5, 0))

currency_var = tk.StringVar(value="Mexico")
currency_box = ttk.Combobox(
    root,
    textvariable=currency_var,
    values=[
        "Mexico",
        "Bangladesh",
        "China",
        "Japan",
        "France",
        "Germany",
        "Italy",
        "Pakistan",
        "Russia",
        "Saudi Arabia",
    ],
    state="readonly",
    font=("Arial", 11),
    width=22,
)
currency_box.pack(pady=6)

convert_button = ttk.Button(
    root,
    text="Convert Currency",
    command=convert_currency,
)
convert_button.pack(pady=8)

output_var = tk.StringVar(value="Enter an amount and click Convert.")
output_label = tk.Label(
    root,
    textvariable=output_var,
    font=("Arial", 11, "bold"),
    bg="white",
    fg="blue",
    wraplength=480,
)
output_label.pack(pady=8)

root.mainloop()
