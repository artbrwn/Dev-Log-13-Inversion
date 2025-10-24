from inversion_app import app
from flask import render_template, request, session
from inversion_app.forms import TradeForm
from inversion_app.models.transactions import Transaction, TransactionError
from config import CURRENCIES
from inversion_app.models.api_crypto import ApiCrypto, ApiCryptoError
from datetime import datetime

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    form = TradeForm()
    user_transactions = Transaction()  
    owned_currencies = user_transactions.get_owned_currencies()
    id_to_symbol = {v: k for k, v in CURRENCIES.items()}

    form.currency_from.choices = [(currency_id, id_to_symbol[currency_id]) 
                              for currency_id in owned_currencies.keys()]
    
    form.currency_to.choices = [(id, symbol) for symbol, id in CURRENCIES.items()]

    message = None
    conversion_value = None

    if request.method == "POST":
        if form.validate_on_submit():  
            action = request.form.get("action")
            
            if action == "calculate":
                try:
                    api_connection = ApiCrypto()
                    conversion_value = api_connection.get_conversion_price(form)
                    
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
                    currency_from_id = int(form.currency_from.data)  # Convertir a int
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

    return render_template("purchase.html", 
                         form=form, 
                         message=message,
                         calculated_amount=conversion_value)
