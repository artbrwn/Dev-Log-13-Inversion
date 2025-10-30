from inversion_app import app
from flask import render_template, request, session
from inversion_app.forms import TradeForm
from inversion_app.models.transactions import Transaction, TransactionError
from inversion_app.models.api_crypto import ApiCrypto, ApiCryptoError
from datetime import datetime
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

        form.currency_from.choices = [(currency_id, id_to_symbol[currency_id]) 
                                for currency_id in owned_currencies.keys()]
        
        form.currency_to.choices = [(id, symbol) for symbol, id in CURRENCIES.items()]

        if request.method == "POST":
            if form.validate_on_submit():  
                action = request.form.get("action")
                
                if action == "calculate":
                    try:
                        api_connection = ApiCrypto()
                        conversion_value = api_connection.get_conversion_price(form.amount_from.data, 
                                                                               form.currency_from.data,
                                                                               form.currency_to.data)
                        
                        # Save result in session to proof if user wants to save
                        session['last_calculation'] = {
                            'currency_from': form.currency_from.data,
                            'currency_to': form.currency_to.data,
                            'amount_from': float(form.amount_from.data),
                            'amount_to': float(conversion_value)
                        }
                        message = "Cálculo realizado"
                    except ApiCryptoError as e:
                        message = f"Error al obtener información de criptomonedas: {str(e)}"
                        

                elif action == "save":

                    last_calc = session.get('last_calculation')
                    
                    if not last_calc:
                        message = "Error: Debes calcular antes de guardar"

                    elif (last_calc['currency_from'] != form.currency_from.data or
                        last_calc['currency_to'] != form.currency_to.data or
                        last_calc['amount_from'] != float(form.amount_from.data)):

                        message = "Error: Los datos han sido modificados. Vuelve a calcular"

                    else:
                        currency_from_id = int(form.currency_from.data)  
                        amount_from = float(form.amount_from.data)
                        
                        if amount_from > owned_currencies[currency_from_id]:
                            balance = owned_currencies[currency_from_id]
                            symbol = id_to_symbol[currency_from_id]
                            message = f"Error: tan solo tienes {balance} de {symbol}"
                        else:
                        
                            now = datetime.now()
                            
                            data_form = (
                                now.strftime('%Y-%m-%d'),           
                                now.strftime('%H:%M:%S'),           
                                last_calc['currency_from'],         
                                last_calc['amount_from'],           
                                last_calc['currency_to'],           
                                last_calc['amount_to']              
                            )
                            
                            try:
                                user_transactions.insert(data_form)
                                message = "Transacción guardada exitosamente"
                            except TransactionError as e:
                                message = f"Error al guardar: {str(e)}"
                            
                            # Remove session after saving
                            session.pop('last_calculation', None)
    except TransactionError as e:
        message = f"Error en la base de datos: {e}"

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