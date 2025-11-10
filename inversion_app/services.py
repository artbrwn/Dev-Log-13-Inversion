from inversion_app.models.api_crypto import ApiCrypto, ApiCryptoError
from datetime import datetime
from inversion_app.models.transactions import TransactionError
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

def handle_calculation(form, session):
    """
    Recieves a form with amount_from, currency_from and currency_to and returns its conversion_value and status message.
    Also recieves a session and saves data recieved in session.
    """
    conversion_value = None
    try:
        api_connection = ApiCrypto()
        conversion_value = api_connection.get_conversion_price(form.amount_from.data, 
                                                            form.currency_from.data,
                                                            form.currency_to.data)
        
        # Save result in session to proof in case user wants to save
        session['last_calculation'] = {
            'currency_from': form.currency_from.data,
            'currency_to': form.currency_to.data,
            'amount_from': float(form.amount_from.data),
            'amount_to': float(conversion_value)
        }
        message = "Cálculo realizado"
    except ApiCryptoError as e:
        message = f"Error al obtener información de criptomonedas: {str(e)}"
        
    return message, conversion_value
                            

def handle_save_transaction(user_transactions, form, session, owned_currencies):
    last_calc = session.get('last_calculation')
    
    if not last_calc:
        message = "Error: Debes calcular antes de guardar"

    elif is_form_unchanged(last_calc, form):
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
    
    return message

def is_form_unchanged(last_calc, form):
    return last_calc['currency_from'] != form.currency_from.data or last_calc['currency_to'] != form.currency_to.data or last_calc['amount_from'] != float(form.amount_from.data)

def update_form_currencies(form, owned_currencies):
    """
    Recieves a form and actual owned currencies and updates its property currency_from and currency_to
    """
    form.currency_from.choices = [(currency_id, id_to_symbol[currency_id]) 
                                for currency_id in owned_currencies.keys()]
        
    form.currency_to.choices = [(id, symbol) for symbol, id in CURRENCIES.items()]