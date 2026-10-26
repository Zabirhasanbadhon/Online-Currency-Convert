import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import json
import os
from datetime import datetime


# ============================================================
# GLOBAL CURRENCY CONVERTER
# Country Selection | Favorites | History | Auto Refresh
# Primary API: Frankfurter
# Fallback API: ExchangeRate-API (open.er-api.com)
# ============================================================


# -------------------- THEME --------------------

CREAM = "#F8F5EE"
CARD = "#FFFEFA"
DARK = "#40352B"
MUTED = "#887E72"
GREEN = "#52765B"
GREEN_DARK = "#3D6046"
GREEN_LIGHT = "#E8F0E6"
BORDER = "#E7E0D5"
WHITE = "#FFFFFF"
RED = "#B94B43"
GOLD = "#C3923E"

PRIMARY_API = "https://api.frankfurter.dev/v2"
FALLBACK_API = "https://open.er-api.com/v6/latest"

HISTORY_FILE = "conversion_history.json"
FAVORITES_FILE = "favorite_countries.json"

AUTO_REFRESH_MS = 60_000


# ============================================================
# COUNTRY DATABASE
# Country: (ISO country code, currency code)
#
# Flags are generated from ISO country codes.
# Countries sharing a currency use the same currency code.
# ============================================================

COUNTRY_DATA = {
    "Afghanistan": ("AF", "AFN"),
    "Albania": ("AL", "ALL"),
    "Algeria": ("DZ", "DZD"),
    "Andorra": ("AD", "EUR"),
    "Angola": ("AO", "AOA"),
    "Antigua and Barbuda": ("AG", "XCD"),
    "Argentina": ("AR", "ARS"),
    "Armenia": ("AM", "AMD"),
    "Australia": ("AU", "AUD"),
    "Austria": ("AT", "EUR"),
    "Azerbaijan": ("AZ", "AZN"),
    "Bahamas": ("BS", "BSD"),
    "Bahrain": ("BH", "BHD"),
    "Bangladesh": ("BD", "BDT"),
    "Barbados": ("BB", "BBD"),
    "Belarus": ("BY", "BYN"),
    "Belgium": ("BE", "EUR"),
    "Belize": ("BZ", "BZD"),
    "Benin": ("BJ", "XOF"),
    "Bhutan": ("BT", "BTN"),
    "Bolivia": ("BO", "BOB"),
    "Bosnia and Herzegovina": ("BA", "BAM"),
    "Botswana": ("BW", "BWP"),
    "Brazil": ("BR", "BRL"),
    "Brunei": ("BN", "BND"),
    "Bulgaria": ("BG", "EUR"),
    "Burkina Faso": ("BF", "XOF"),
    "Burundi": ("BI", "BIF"),
    "Cabo Verde": ("CV", "CVE"),
    "Cambodia": ("KH", "KHR"),
    "Cameroon": ("CM", "XAF"),
    "Canada": ("CA", "CAD"),
    "Central African Republic": ("CF", "XAF"),
    "Chad": ("TD", "XAF"),
    "Chile": ("CL", "CLP"),
    "China": ("CN", "CNY"),
    "Colombia": ("CO", "COP"),
    "Comoros": ("KM", "KMF"),
    "Costa Rica": ("CR", "CRC"),
    "Croatia": ("HR", "EUR"),
    "Cuba": ("CU", "CUP"),
    "Cyprus": ("CY", "EUR"),
    "Czechia": ("CZ", "CZK"),
    "Democratic Republic of the Congo": ("CD", "CDF"),
    "Denmark": ("DK", "DKK"),
    "Djibouti": ("DJ", "DJF"),
    "Dominica": ("DM", "XCD"),
    "Dominican Republic": ("DO", "DOP"),
    "Ecuador": ("EC", "USD"),
    "Egypt": ("EG", "EGP"),
    "El Salvador": ("SV", "USD"),
    "Equatorial Guinea": ("GQ", "XAF"),
    "Eritrea": ("ER", "ERN"),
    "Estonia": ("EE", "EUR"),
    "Eswatini": ("SZ", "SZL"),
    "Ethiopia": ("ET", "ETB"),
    "Fiji": ("FJ", "FJD"),
    "Finland": ("FI", "EUR"),
    "France": ("FR", "EUR"),
    "Gabon": ("GA", "XAF"),
    "Gambia": ("GM", "GMD"),
    "Georgia": ("GE", "GEL"),
    "Germany": ("DE", "EUR"),
    "Ghana": ("GH", "GHS"),
    "Greece": ("GR", "EUR"),
    "Grenada": ("GD", "XCD"),
    "Guatemala": ("GT", "GTQ"),
    "Guinea": ("GN", "GNF"),
    "Guinea-Bissau": ("GW", "XOF"),
    "Guyana": ("GY", "GYD"),
    "Haiti": ("HT", "HTG"),
    "Honduras": ("HN", "HNL"),
    "Hungary": ("HU", "HUF"),
    "Iceland": ("IS", "ISK"),
    "India": ("IN", "INR"),
    "Indonesia": ("ID", "IDR"),
    "Iran": ("IR", "IRR"),
    "Iraq": ("IQ", "IQD"),
    "Ireland": ("IE", "EUR"),
    "Israel": ("IL", "ILS"),
    "Italy": ("IT", "EUR"),
    "Jamaica": ("JM", "JMD"),
    "Japan": ("JP", "JPY"),
    "Jordan": ("JO", "JOD"),
    "Kazakhstan": ("KZ", "KZT"),
    "Kenya": ("KE", "KES"),
    "Kiribati": ("KI", "AUD"),
    "Kosovo": ("XK", "EUR"),
    "Kuwait": ("KW", "KWD"),
    "Kyrgyzstan": ("KG", "KGS"),
    "Laos": ("LA", "LAK"),
    "Latvia": ("LV", "EUR"),
    "Lebanon": ("LB", "LBP"),
    "Lesotho": ("LS", "LSL"),
    "Liberia": ("LR", "LRD"),
    "Libya": ("LY", "LYD"),
    "Liechtenstein": ("LI", "CHF"),
    "Lithuania": ("LT", "EUR"),
    "Luxembourg": ("LU", "EUR"),
    "Madagascar": ("MG", "MGA"),
    "Malawi": ("MW", "MWK"),
    "Malaysia": ("MY", "MYR"),
    "Maldives": ("MV", "MVR"),
    "Mali": ("ML", "XOF"),
    "Malta": ("MT", "EUR"),
    "Marshall Islands": ("MH", "USD"),
    "Mauritania": ("MR", "MRU"),
    "Mauritius": ("MU", "MUR"),
    "Mexico": ("MX", "MXN"),
    "Micronesia": ("FM", "USD"),
    "Moldova": ("MD", "MDL"),
    "Monaco": ("MC", "EUR"),
    "Mongolia": ("MN", "MNT"),
    "Montenegro": ("ME", "EUR"),
    "Morocco": ("MA", "MAD"),
    "Mozambique": ("MZ", "MZN"),
    "Myanmar": ("MM", "MMK"),
    "Namibia": ("NA", "NAD"),
    "Nauru": ("NR", "AUD"),
    "Nepal": ("NP", "NPR"),
    "Netherlands": ("NL", "EUR"),
    "New Zealand": ("NZ", "NZD"),
    "Nicaragua": ("NI", "NIO"),
    "Niger": ("NE", "XOF"),
    "Nigeria": ("NG", "NGN"),
    "North Korea": ("KP", "KPW"),
    "North Macedonia": ("MK", "MKD"),
    "Norway": ("NO", "NOK"),
    "Oman": ("OM", "OMR"),
    "Pakistan": ("PK", "PKR"),
    "Palau": ("PW", "USD"),
    "Palestine": ("PS", "ILS"),
    "Panama": ("PA", "PAB"),
    "Papua New Guinea": ("PG", "PGK"),
    "Paraguay": ("PY", "PYG"),
    "Peru": ("PE", "PEN"),
    "Philippines": ("PH", "PHP"),
    "Poland": ("PL", "PLN"),
    "Portugal": ("PT", "EUR"),
    "Qatar": ("QA", "QAR"),
    "Republic of the Congo": ("CG", "XAF"),
    "Romania": ("RO", "RON"),
    "Russia": ("RU", "RUB"),
    "Rwanda": ("RW", "RWF"),
    "Saint Kitts and Nevis": ("KN", "XCD"),
    "Saint Lucia": ("LC", "XCD"),
    "Saint Vincent and the Grenadines": ("VC", "XCD"),
    "Samoa": ("WS", "WST"),
    "San Marino": ("SM", "EUR"),
    "Sao Tome and Principe": ("ST", "STN"),
    "Saudi Arabia": ("SA", "SAR"),
    "Senegal": ("SN", "XOF"),
    "Serbia": ("RS", "RSD"),
    "Seychelles": ("SC", "SCR"),
    "Sierra Leone": ("SL", "SLE"),
    "Singapore": ("SG", "SGD"),
    "Slovakia": ("SK", "EUR"),
    "Slovenia": ("SI", "EUR"),
    "Solomon Islands": ("SB", "SBD"),
    "Somalia": ("SO", "SOS"),
    "South Africa": ("ZA", "ZAR"),
    "South Korea": ("KR", "KRW"),
    "South Sudan": ("SS", "SSP"),
    "Spain": ("ES", "EUR"),
    "Sri Lanka": ("LK", "LKR"),
    "Sudan": ("SD", "SDG"),
    "Suriname": ("SR", "SRD"),
    "Sweden": ("SE", "SEK"),
    "Switzerland": ("CH", "CHF"),
    "Syria": ("SY", "SYP"),
    "Taiwan": ("TW", "TWD"),
    "Tajikistan": ("TJ", "TJS"),
    "Tanzania": ("TZ", "TZS"),
    "Thailand": ("TH", "THB"),
    "Timor-Leste": ("TL", "USD"),
    "Togo": ("TG", "XOF"),
    "Tonga": ("TO", "TOP"),
    "Trinidad and Tobago": ("TT", "TTD"),
    "Tunisia": ("TN", "TND"),
    "Turkey": ("TR", "TRY"),
    "Turkmenistan": ("TM", "TMT"),
    "Tuvalu": ("TV", "AUD"),
    "Uganda": ("UG", "UGX"),
    "Ukraine": ("UA", "UAH"),
    "United Arab Emirates": ("AE", "AED"),
    "United Kingdom": ("GB", "GBP"),
    "United States": ("US", "USD"),
    "Uruguay": ("UY", "UYU"),
    "Uzbekistan": ("UZ", "UZS"),
    "Vanuatu": ("VU", "VUV"),
    "Vatican City": ("VA", "EUR"),
    "Venezuela": ("VE", "VES"),
    "Vietnam": ("VN", "VND"),
    "Yemen": ("YE", "YER"),
    "Zambia": ("ZM", "ZMW"),
    "Zimbabwe": ("ZW", "ZWG"),
}


# ============================================================
# CURRENCY NAMES AND SYMBOLS
# ============================================================

CURRENCY_NAMES = {
    "USD": ("US Dollar", "$"),
    "EUR": ("Euro", "€"),
    "GBP": ("British Pound", "£"),
    "BDT": ("Bangladeshi Taka", "৳"),
    "INR": ("Indian Rupee", "₹"),
    "PKR": ("Pakistani Rupee", "₨"),
    "NPR": ("Nepalese Rupee", "रु"),
    "LKR": ("Sri Lankan Rupee", "Rs"),
    "JPY": ("Japanese Yen", "¥"),
    "CNY": ("Chinese Yuan", "¥"),
    "KRW": ("South Korean Won", "₩"),
    "RUB": ("Russian Ruble", "₽"),
    "SAR": ("Saudi Riyal", "﷼"),
    "AED": ("UAE Dirham", "د.إ"),
    "QAR": ("Qatari Riyal", "﷼"),
    "KWD": ("Kuwaiti Dinar", "د.ك"),
    "BHD": ("Bahraini Dinar", "د.ب"),
    "OMR": ("Omani Rial", "ر.ع."),
    "JOD": ("Jordanian Dinar", "د.ا"),
    "ILS": ("Israeli New Shekel", "₪"),
    "TRY": ("Turkish Lira", "₺"),
    "IRR": ("Iranian Rial", "﷼"),
    "IQD": ("Iraqi Dinar", "ع.د"),
    "EGP": ("Egyptian Pound", "E£"),
    "MAD": ("Moroccan Dirham", "د.م."),
    "CHF": ("Swiss Franc", "CHF"),
    "CAD": ("Canadian Dollar", "C$"),
    "AUD": ("Australian Dollar", "A$"),
    "NZD": ("New Zealand Dollar", "NZ$"),
    "SGD": ("Singapore Dollar", "S$"),
    "MYR": ("Malaysian Ringgit", "RM"),
    "IDR": ("Indonesian Rupiah", "Rp"),
    "THB": ("Thai Baht", "฿"),
    "PHP": ("Philippine Peso", "₱"),
    "VND": ("Vietnamese Dong", "₫"),
    "BRL": ("Brazilian Real", "R$"),
    "MXN": ("Mexican Peso", "$"),
    "ZAR": ("South African Rand", "R"),
    "NGN": ("Nigerian Naira", "₦"),
    "KES": ("Kenyan Shilling", "KSh"),
    "GHS": ("Ghanaian Cedi", "₵"),
    "SEK": ("Swedish Krona", "kr"),
    "NOK": ("Norwegian Krone", "kr"),
    "DKK": ("Danish Krone", "kr"),
    "PLN": ("Polish Zloty", "zł"),
    "CZK": ("Czech Koruna", "Kč"),
    "HUF": ("Hungarian Forint", "Ft"),
    "UAH": ("Ukrainian Hryvnia", "₴"),
    "PKR": ("Pakistani Rupee", "₨"),
    "AFN": ("Afghan Afghani", "؋"),
    "IRR": ("Iranian Rial", "﷼"),
    "ARS": ("Argentine Peso", "$"),
    "CLP": ("Chilean Peso", "$"),
    "COP": ("Colombian Peso", "$"),
    "PEN": ("Peruvian Sol", "S/"),
    "CRC": ("Costa Rican Colon", "₡"),
    "UYU": ("Uruguayan Peso", "$U"),
    "XOF": ("West African CFA Franc", "CFA"),
    "XAF": ("Central African CFA Franc", "FCFA"),
    "XCD": ("East Caribbean Dollar", "EC$"),
}


def currency_name(code):
    """Return a readable currency name."""

    return CURRENCY_NAMES.get(
        code,
        (code, code)
    )[0]


def currency_symbol(code):
    """Return a currency symbol or the currency code."""

    return CURRENCY_NAMES.get(
        code,
        (code, code)
    )[1]


def country_flag(country_code):
    """Convert a two-letter ISO country code into a flag emoji."""

    if not country_code or len(country_code) != 2:
        return "🌐"

    return "".join(
        chr(127397 + ord(char))
        for char in country_code.upper()
    )


def country_display(country):
    """Format a country name with its flag and currency."""

    iso_code, currency_code = COUNTRY_DATA[country]

    return (
        f"{country_flag(iso_code)}  {country}  "
        f"({currency_code})"
    )


# ============================================================
# LOCAL STORAGE
# ============================================================

def read_json(filename, default):
    """Read a JSON file safely."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def write_json(filename, data):
    """Save application data locally."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except OSError as error:
        print(f"Could not save {filename}: {error}")


history = read_json(HISTORY_FILE, [])
favorites = read_json(FAVORITES_FILE, [])

if not isinstance(history, list):
    history = []

if not isinstance(favorites, list):
    favorites = []

favorites = [
    country for country in favorites
    if country in COUNTRY_DATA
]


# ============================================================
# EXCHANGE RATE PROVIDERS
# ============================================================

def fetch_frankfurter_rate(base, target):
    """Try the primary exchange-rate provider."""

    if base == target:
        return 1.0, datetime.now().strftime("%Y-%m-%d"), "Same currency"

    response = requests.get(
        f"{PRIMARY_API}/rate/{base}/{target}",
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    rate = float(data["rate"])

    if rate <= 0:
        raise ValueError("Invalid exchange rate.")

    return rate, data.get("date", ""), "Frankfurter"


def fetch_fallback_rate(base, target):
    """
    Use a second provider if the primary provider fails.

    The fallback returns rates relative to a requested base
    currency, allowing direct conversion between supported pairs.
    """

    if base == target:
        return 1.0, datetime.now().strftime("%Y-%m-%d"), "Same currency"

    response = requests.get(
        f"{FALLBACK_API}/{base}",
        timeout=12,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Fallback provider returned an error.")

    rates = data.get("rates", {})

    if target not in rates:
        raise ValueError(f"{target} is not supported by the fallback provider.")

    rate = float(rates[target])

    if rate <= 0:
        raise ValueError("Invalid fallback exchange rate.")

    return rate, data.get("time_last_update_utc", ""), "ExchangeRate-API"


def get_exchange_rate(base, target):
    """Try the primary provider, then the fallback."""

    errors = []

    for provider in (fetch_frankfurter_rate, fetch_fallback_rate):
        try:
            return provider(base, target)

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            errors.append(str(error))

    return None, None, "Unavailable"


# ============================================================
# APPLICATION STATE
# ============================================================

current_conversion = None
conversion_in_progress = False
auto_refresh_enabled = True
last_successful_rate = None
refresh_job = None


# ============================================================
# COUNTRY SELECTORS
# ============================================================

def selected_country(variable):
    """Find the country represented by a dropdown selection."""

    display = variable.get()

    for country in COUNTRY_DATA:
        if country_display(country) == display:
            return country

    return None


def on_country_changed(*args):
    """Update the currency labels when countries change."""

    source = selected_country(from_var)
    target = selected_country(to_var)

    if source:
        from_currency_label.config(
            text=COUNTRY_DATA[source][1]
        )

    if target:
        to_currency_label.config(
            text=COUNTRY_DATA[target][1]
        )


def select_country(country, target=True):
    """Select a country programmatically."""

    if country not in COUNTRY_DATA:
        return

    if target:
        to_var.set(country_display(country))
    else:
        from_var.set(country_display(country))

    on_country_changed()


def swap_countries():
    """Swap the selected countries."""

    old_from = from_var.get()
    old_to = to_var.get()

    from_var.set(old_to)
    to_var.set(old_from)

    on_country_changed()


# ============================================================
# FAVORITES
# ============================================================

def save_favorites():
    write_json(FAVORITES_FILE, favorites)


def toggle_favorite():
    """Add or remove the selected target country from favorites."""

    country = selected_country(to_var)

    if not country:
        return

    if country in favorites:
        favorites.remove(country)
        status_var.set(f"Removed {country} from favorites.")

    else:
        favorites.append(country)
        status_var.set(f"Added {country} to favorites.")

    save_favorites()
    refresh_favorites_view()
    update_favorite_button()


def update_favorite_button():
    country = selected_country(to_var)

    if country and country in favorites:
        favorite_button.config(text="★  Remove Favorite")
    else:
        favorite_button.config(text="☆  Add Favorite")


def refresh_favorites_view():
    favorites_list.delete(0, tk.END)

    for country in sorted(favorites):
        favorites_list.insert(tk.END, country_display(country))


def use_favorite(event=None):
    selection = favorites_list.curselection()

    if not selection:
        return

    display = favorites_list.get(selection[0])

    for country in COUNTRY_DATA:
        if country_display(country) == display:
            select_country(country, target=True)
            notebook.select(converter_tab)
            update_favorite_button()
            return


# ============================================================
# CONVERSION HISTORY
# ============================================================

def save_history():
    write_json(HISTORY_FILE, history)


def refresh_history_view():
    history_tree.delete(*history_tree.get_children())

    for item in history:
        history_tree.insert(
            "",
            tk.END,
            values=(
                item.get("time", ""),
                item.get("amount", ""),
                item.get("from", ""),
                item.get("to", ""),
                item.get("result", ""),
                item.get("provider", ""),
            ),
        )


def clear_history():
    if not history:
        return

    if not messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all conversion history?",
    ):
        return

    history.clear()
    save_history()
    refresh_history_view()
    status_var.set("Conversion history cleared.")


def add_history(amount, source, target, result, rate, provider):
    """Store a conversion and refresh the history screen."""

    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": round(amount, 8),
        "from": source,
        "to": target,
        "result": round(result, 8),
        "rate": rate,
        "provider": provider,
    }

    history.insert(0, entry)

    # Keep the most recent 500 conversions.
    del history[500:]

    save_history()
    refresh_history_view()


# ============================================================
# CONVERSION LOGIC
# ============================================================

def convert_currency():
    """Validate the input and start conversion in a background thread."""

    global conversion_in_progress, current_conversion

    if conversion_in_progress:
        return

    amount_text = amount_entry.get().strip()

    try:
        amount = float(amount_text)

        if not amount_text or amount < 0:
            raise ValueError

        if amount != amount or amount == float("inf"):
            raise ValueError

    except ValueError:
        result_var.set("Please enter a valid amount.")
        return

    source = selected_country(from_var)
    target = selected_country(to_var)

    if not source or not target:
        result_var.set("Please select both countries.")
        return

    base = COUNTRY_DATA[source][1]
    quote = COUNTRY_DATA[target][1]

    current_conversion = {
        "amount": amount,
        "source": source,
        "target": target,
        "base": base,
        "quote": quote,
    }

    start_conversion(
        amount,
        source,
        target,
        base,
        quote,
        record_history=True,
    )


def start_conversion(
    amount,
    source,
    target,
    base,
    quote,
    record_history,
):
    """Run the network request without freezing the GUI."""

    global conversion_in_progress

    if conversion_in_progress:
        return

    conversion_in_progress = True
    convert_button.config(state="disabled")
    refresh_button.config(state="disabled")

    result_var.set("Fetching exchange rate...")
    rate_var.set("")
    date_var.set("")

    def worker():
        rate, rate_date, provider = get_exchange_rate(base, quote)

        root.after(
            0,
            lambda: finish_conversion(
                amount,
                source,
                target,
                base,
                quote,
                rate,
                rate_date,
                provider,
                record_history,
            ),
        )

    threading.Thread(target=worker, daemon=True).start()


def finish_conversion(
    amount,
    source,
    target,
    base,
    quote,
    rate,
    rate_date,
    provider,
    record_history,
):
    """Update the interface after the network request completes."""

    global conversion_in_progress, last_successful_rate

    conversion_in_progress = False

    convert_button.config(state="normal")
    refresh_button.config(state="normal")

    if rate is None:
        result_var.set("Unable to retrieve exchange rate.")
        rate_var.set(
            "Both providers failed or this currency pair is unsupported."
        )
        date_var.set("Check your internet connection and try again.")

        status_var.set("Conversion failed.")
        return

    converted = amount * rate
    last_successful_rate = rate

    source_symbol = currency_symbol(base)
    target_symbol = currency_symbol(quote)

    result_var.set(
        f"{target_symbol} {converted:,.4f}"
    )

    rate_var.set(
        f"{source_symbol} {amount:,.2f}  {base}"
        f"  =  {target_symbol} {converted:,.4f}  {quote}"
    )

    if rate_date:
        date_var.set(
            f"Rate information: {rate_date}  •  Provider: {provider}"
        )
    else:
        date_var.set(f"Provider: {provider}")

    status_var.set(
        f"{source} → {target} | 1 {base} = {rate:.6f} {quote}"
    )

    if record_history:
        add_history(
            amount,
            source,
            target,
            converted,
            rate,
            provider,
        )

    update_favorite_button()


def refresh_conversion():
    """Refresh the last conversion without creating duplicate history."""

    if not current_conversion or conversion_in_progress:
        return

    data = current_conversion

    start_conversion(
        data["amount"],
        data["source"],
        data["target"],
        data["base"],
        data["quote"],
        record_history=False,
    )


def toggle_auto_refresh():
    """Enable or disable automatic refresh."""

    global auto_refresh_enabled

    auto_refresh_enabled = auto_refresh_var.get()

    if auto_refresh_enabled:
        status_var.set("Automatic refresh enabled.")
        schedule_auto_refresh()
    else:
        status_var.set("Automatic refresh disabled.")


def schedule_auto_refresh():
    """Schedule periodic updates while the application is open."""

    global refresh_job

    if refresh_job is not None:
        root.after_cancel(refresh_job)
        refresh_job = None

    if auto_refresh_enabled:
        refresh_job = root.after(
            AUTO_REFRESH_MS,
            auto_refresh_tick,
        )


def auto_refresh_tick():
    """Refresh the last conversion every 60 seconds."""

    global refresh_job

    refresh_job = None

    if auto_refresh_enabled and current_conversion:
        refresh_conversion()

    schedule_auto_refresh()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("ZaBir | Currency Converter")
root.geometry("1100x850")
root.minsize(900, 720)
root.configure(bg=CREAM)


# ============================================================
# STYLES
# ============================================================

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "TNotebook",
    background=CREAM,
    borderwidth=0,
)

style.configure(
    "TNotebook.Tab",
    background="#EEE8DC",
    foreground=DARK,
    padding=(20, 12),
    font=("Segoe UI", 10, "bold"),
)

style.map(
    "TNotebook.Tab",
    background=[("selected", CARD)],
    foreground=[("selected", GREEN)],
)

style.configure(
    "TCombobox",
    padding=9,
    fieldbackground=WHITE,
    background=WHITE,
    foreground=DARK,
    arrowcolor=GREEN,
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", WHITE)],
    selectbackground=[("readonly", WHITE)],
    selectforeground=[("readonly", DARK)],
)

style.configure(
    "Primary.TButton",
    background=GREEN,
    foreground=WHITE,
    padding=(14, 12),
    font=("Segoe UI", 11, "bold"),
    borderwidth=0,
)

style.map(
    "Primary.TButton",
    background=[("active", GREEN_DARK)],
)

style.configure(
    "Secondary.TButton",
    background=GREEN_LIGHT,
    foreground=DARK,
    padding=(12, 9),
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
)

style.map(
    "Secondary.TButton",
    background=[("active", "#DCE7D9")],
)

style.configure(
    "Treeview",
    background=CARD,
    fieldbackground=CARD,
    foreground=DARK,
    rowheight=32,
    font=("Segoe UI", 9),
)

style.configure(
    "Treeview.Heading",
    background="#EEE8DC",
    foreground=DARK,
    font=("Segoe UI", 9, "bold"),
    padding=8,
)

style.map(
    "Treeview",
    background=[("selected", GREEN_LIGHT)],
    foreground=[("selected", DARK)],
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root, bg=CREAM)
header.pack(fill="x", padx=30, pady=(24, 16))

header_top = tk.Frame(header, bg=CREAM)
header_top.pack(fill="x")

tk.Label(
    header_top,
    text="🌍 ZaBir GlobeX",
    font=("Segoe UI", 20, "bold"),
    bg=CREAM,
    fg=GREEN,
).pack(side="left")

tk.Label(
    header,
    text="Currency Converter",
    font=("Segoe UI", 27, "bold"),
    bg=CREAM,
    fg=DARK,
).pack(anchor="w", pady=(8, 3))

tk.Label(
    header,
    text="Convert currencies from countries around the world.",
    font=("Segoe UI", 11),
    bg=CREAM,
    fg=MUTED,
).pack(anchor="w")


# ============================================================
# NOTEBOOK
# ============================================================

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=30, pady=(0, 12))

converter_tab = tk.Frame(notebook, bg=CREAM)
history_tab = tk.Frame(notebook, bg=CREAM)
favorites_tab = tk.Frame(notebook, bg=CREAM)

notebook.add(converter_tab, text="  Converter  ")
notebook.add(history_tab, text="  History  ")
notebook.add(favorites_tab, text="  Favorites  ")


# ============================================================
# CONVERTER CARD
# ============================================================

main_card = tk.Frame(
    converter_tab,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
)

main_card.pack(fill="x", padx=10, pady=12)

content = tk.Frame(main_card, bg=CARD)
content.pack(fill="x", padx=24, pady=22)


# ============================================================
# AMOUNT ENTRY
# ============================================================

tk.Label(
    content,
    text="AMOUNT TO CONVERT",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=MUTED,
).pack(anchor="w", pady=(0, 8))

amount_entry = tk.Entry(
    content,
    font=("Segoe UI", 19),
    bg=WHITE,
    fg=DARK,
    insertbackground=DARK,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=GREEN,
)

amount_entry.pack(fill="x", ipady=9)
amount_entry.insert(0, "1")


# ============================================================
# COUNTRY SELECTORS
# ============================================================

selectors = tk.Frame(content, bg=CARD)
selectors.pack(fill="x", pady=(22, 10))

selectors.columnconfigure(0, weight=1)
selectors.columnconfigure(1, weight=1)


tk.Label(
    selectors,
    text="FROM COUNTRY",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=MUTED,
).grid(row=0, column=0, sticky="w", pady=(0, 8))

tk.Label(
    selectors,
    text="TO COUNTRY",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=MUTED,
).grid(row=0, column=1, sticky="w", padx=(14, 0), pady=(0, 8))


from_var = tk.StringVar()
to_var = tk.StringVar()

from_box = ttk.Combobox(
    selectors,
    textvariable=from_var,
    values=[
        country_display(c)
        for c in sorted(COUNTRY_DATA)
    ],
    state="readonly",
    font=("Segoe UI", 10),
)

from_box.grid(row=1, column=0, sticky="ew")

to_box = ttk.Combobox(
    selectors,
    textvariable=to_var,
    values=[
        country_display(c)
        for c in sorted(COUNTRY_DATA)
    ],
    state="readonly",
    font=("Segoe UI", 10),
)

to_box.grid(row=1, column=1, sticky="ew", padx=(14, 0))


# ============================================================
# CURRENCY DETAILS
# ============================================================

details = tk.Frame(content, bg=CARD)
details.pack(fill="x", pady=(10, 0))

from_currency_label = tk.Label(
    details,
    text="USD",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=GREEN,
)

from_currency_label.pack(side="left")

to_currency_label = tk.Label(
    details,
    text="BDT",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=GREEN,
)

to_currency_label.pack(side="right")


# ============================================================
# ACTION BUTTONS
# ============================================================

action_row = tk.Frame(content, bg=CARD)
action_row.pack(fill="x", pady=(18, 0))

action_row.columnconfigure(0, weight=1)
action_row.columnconfigure(1, weight=1)

ttk.Button(
    action_row,
    text="⇄  Swap Countries",
    command=swap_countries,
    style="Secondary.TButton",
).grid(row=0, column=0, sticky="ew", padx=(0, 6))

favorite_button = ttk.Button(
    action_row,
    text="☆  Add Favorite",
    command=toggle_favorite,
    style="Secondary.TButton",
)

favorite_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))


# ============================================================
# CONVERT AND REFRESH
# ============================================================

button_row = tk.Frame(content, bg=CARD)
button_row.pack(fill="x", pady=(14, 0))

button_row.columnconfigure(0, weight=3)
button_row.columnconfigure(1, weight=1)

convert_button = ttk.Button(
    button_row,
    text="Convert Currency",
    command=convert_currency,
    style="Primary.TButton",
)

convert_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

refresh_button = ttk.Button(
    button_row,
    text="↻  Refresh",
    command=refresh_conversion,
    style="Secondary.TButton",
)

refresh_button.grid(row=0, column=1, sticky="ew")


# ============================================================
# AUTO REFRESH CONTROL
# ============================================================

refresh_options = tk.Frame(content, bg=CARD)
refresh_options.pack(fill="x", pady=(14, 0))

auto_refresh_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    refresh_options,
    text="Automatically refresh every 60 seconds",
    variable=auto_refresh_var,
    command=toggle_auto_refresh,
    font=("Segoe UI", 10),
    bg=CARD,
    fg=DARK,
    activebackground=CARD,
    selectcolor=GREEN_LIGHT,
).pack(side="left")


# ============================================================
# RESULT CARD
# ============================================================

result_card = tk.Frame(
    converter_tab,
    bg=GREEN_LIGHT,
    highlightbackground="#D8E3D5",
    highlightthickness=1,
)

result_card.pack(fill="x", padx=10, pady=(4, 12))

result_content = tk.Frame(result_card, bg=GREEN_LIGHT)
result_content.pack(fill="x", padx=24, pady=22)

tk.Label(
    result_content,
    text="CONVERSION RESULT",
    font=("Segoe UI", 10, "bold"),
    bg=GREEN_LIGHT,
    fg=GREEN,
).pack(anchor="w")

result_var = tk.StringVar(value="Your result will appear here.")

tk.Label(
    result_content,
    textvariable=result_var,
    font=("Segoe UI", 25, "bold"),
    bg=GREEN_LIGHT,
    fg=DARK,
    wraplength=850,
    justify="left",
).pack(anchor="w", pady=(10, 8))

rate_var = tk.StringVar(value="")

tk.Label(
    result_content,
    textvariable=rate_var,
    font=("Segoe UI", 11),
    bg=GREEN_LIGHT,
    fg=DARK,
    wraplength=850,
    justify="left",
).pack(anchor="w")

date_var = tk.StringVar(value="")

tk.Label(
    result_content,
    textvariable=date_var,
    font=("Segoe UI", 9),
    bg=GREEN_LIGHT,
    fg=MUTED,
    wraplength=850,
    justify="left",
).pack(anchor="w", pady=(8, 0))


# ============================================================
# FAVORITES TAB
# ============================================================

fav_card = tk.Frame(
    favorites_tab,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
)

fav_card.pack(fill="both", expand=True, padx=10, pady=12)

tk.Label(
    fav_card,
    text="Your Favorite Countries",
    font=("Segoe UI", 18, "bold"),
    bg=CARD,
    fg=DARK,
).pack(anchor="w", padx=20, pady=(20, 5))

tk.Label(
    fav_card,
    text="Double-click a country to select it as the target.",
    font=("Segoe UI", 10),
    bg=CARD,
    fg=MUTED,
).pack(anchor="w", padx=20, pady=(0, 12))

favorites_list = tk.Listbox(
    fav_card,
    font=("Segoe UI", 11),
    bg=WHITE,
    fg=DARK,
    selectbackground=GREEN_LIGHT,
    selectforeground=DARK,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    activestyle="none",
)

favorites_list.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 14),
)

favorites_list.bind("<Double-Button-1>", use_favorite)

ttk.Button(
    fav_card,
    text="Remove Selected Favorite",
    command=toggle_favorite,
    style="Secondary.TButton",
).pack(anchor="e", padx=20, pady=(0, 20))


# ============================================================
# HISTORY TAB
# ============================================================

history_card = tk.Frame(
    history_tab,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
)

history_card.pack(fill="both", expand=True, padx=10, pady=12)

history_header = tk.Frame(history_card, bg=CARD)
history_header.pack(fill="x", padx=16, pady=16)

tk.Label(
    history_header,
    text="Conversion History",
    font=("Segoe UI", 18, "bold"),
    bg=CARD,
    fg=DARK,
).pack(side="left")

ttk.Button(
    history_header,
    text="Clear History",
    command=clear_history,
    style="Secondary.TButton",
).pack(side="right")


columns = (
    "time",
    "amount",
    "from",
    "to",
    "result",
    "provider",
)

history_tree = ttk.Treeview(
    history_card,
    columns=columns,
    show="headings",
)

headings = {
    "time": "Date / Time",
    "amount": "Amount",
    "from": "From",
    "to": "To",
    "result": "Result",
    "provider": "Provider",
}

widths = {
    "time": 150,
    "amount": 90,
    "from": 70,
    "to": 70,
    "result": 120,
    "provider": 120,
}

for column in columns:
    history_tree.heading(column, text=headings[column])
    history_tree.column(
        column,
        width=widths[column],
        anchor="center",
    )

history_scrollbar = ttk.Scrollbar(
    history_card,
    orient="vertical",
    command=history_tree.yview,
)

history_tree.configure(
    yscrollcommand=history_scrollbar.set
)

history_tree.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(16, 0),
    pady=(0, 16),
)

history_scrollbar.pack(
    side="right",
    fill="y",
    padx=(0, 16),
    pady=(0, 16),
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Frame(root, bg=CREAM)
footer.pack(fill="x", padx=30, pady=(0, 16))

status_var = tk.StringVar(
    value="Ready to convert currencies."
)

tk.Label(
    footer,
    textvariable=status_var,
    font=("Segoe UI", 9),
    bg=CREAM,
    fg=MUTED,
    wraplength=1000,
    justify="left",
).pack(anchor="w")

tk.Label(
    footer,
    text=(
        "Reference rates only. Rates may differ from banks and "
        "money-exchange services."
    ),
    font=("Segoe UI", 9),
    bg=CREAM,
    fg=MUTED,
).pack(anchor="w", pady=(4, 0))


# ============================================================
# EVENT BINDINGS
# ============================================================

from_var.trace_add("write", on_country_changed)
to_var.trace_add("write", on_country_changed)

from_box.bind(
    "<<ComboboxSelected>>",
    lambda event: on_country_changed(),
)

to_box.bind(
    "<<ComboboxSelected>>",
    lambda event: (
        on_country_changed(),
        update_favorite_button(),
    ),
)

amount_entry.bind(
    "<Return>",
    lambda event: convert_currency(),
)

root.bind(
    "<Control-Return>",
    lambda event: convert_currency(),
)


# ============================================================
# INITIALIZATION
# ============================================================

select_country("United States", target=False)
select_country("Bangladesh", target=True)

refresh_history_view()
refresh_favorites_view()
update_favorite_button()
schedule_auto_refresh()


# ============================================================
# CLEAN EXIT
# ============================================================

def on_close():
    global refresh_job

    if refresh_job is not None:
        try:
            root.after_cancel(refresh_job)
        except tk.TclError:
            pass

    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()