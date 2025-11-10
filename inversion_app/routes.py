from inversion_app import app
from flask import render_template, request, session
from inversion_app.forms import TradeForm
from inversion_app.models.transactions import Transaction, TransactionError
from inversion_app.models.api_crypto import ApiCrypto, ApiCryptoError
from inversion_app.services import *

try:
    from config import CURRENCIES
except (ImportError, AttributeError):
    CURRENCIES = {
    "EUR": 2790,
    "BTC": 1,
    "ETH": 1027,
    "USDT": 825,
    "BNB": 1839,
    "XRP": 52,
    "USDC": 3408,
    "SOL": 5426,
    "TRON": 1958,
    "DOGE": 74
}
id_to_symbol = {v: k for k, v in CURRENCIES.items()}

@app.route("/")
def index():
    message = None
    try:
        user_transactions = Transaction(CURRENCIES)
        all_transactions = user_transactions.get_all()
        for transaction in all_transactions:
            transaction['currency_from'] = id_to_symbol.get(transaction['currency_from'])
            transaction['currency_to'] = id_to_symbol.get(transaction['currency_to'])
    except TransactionError as e:
        all_transactions = None
        message = f"No se ha podido conectar con la base de datos: {e}"

    return render_template("index.html", transactions=all_transactions, message=message)

@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    message = None
    conversion_value = None
    form = TradeForm()
    try:
        user_transactions = Transaction(CURRENCIES)  
        owned_currencies = user_transactions.get_owned_currencies()

        update_form_currencies(form, owned_currencies)

        if request.method == "POST":
            if form.validate_on_submit():
                if form.currency_from.data == form.currency_to.data:
                    message = "Error: La moneda de destino debe ser diferente a la moneda de origen."
                else:
                    action = request.form.get("action")
                    
                    if action == "calculate":
                        message, conversion_value = handle_calculation(form, session)

                    elif action == "save":
                        message = handle_save_transaction(user_transactions, form, session, owned_currencies)

    except TransactionError as e:
        message = f"Error en la base de datos: {e}"
    except KeyError:
        message = f"Error en la configuración de la app"

    return render_template("purchase.html", 
                         form=form, 
                         message=message,
                         calculated_amount=conversion_value)

@app.route("/status")
def status():
    message = None
    investment_status = None
    try:
        user_transactions = Transaction(CURRENCIES)
        transactions = user_transactions.get_all()
        if transactions:
            invested = user_transactions.get_total_investment()
            recovered = user_transactions.get_total_recovered()
            purchase_value = invested - recovered
            actual_value = user_transactions.calculate_actual_value()
            investment_status = {"invested": invested,
                                "recovered": recovered,
                                "purchase_value": purchase_value,
                                "actual_value": actual_value}
    except TransactionError as e:
        message = f"Error en la base de datos: {e}"

    return render_template("status.html", status_data=investment_status, message=message)