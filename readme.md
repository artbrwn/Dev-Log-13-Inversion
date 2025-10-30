# 💰 Inversión App - Gestor de Criptomonedas

Aplicación web para gestionar inversiones en criptomonedas. Permite realizar conversiones entre diferentes criptomonedas, registrar transacciones y visualizar el estado actual de tu cartera de inversión.


## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/artbrwn/Dev-Log-13-Inversion.git
cd inversion_app
```

### 2. Crear entorno virtual y activarlo

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la aplicación

Copia el archivo de configuración de ejemplo `config_template.py` y edítalo con tus datos:


```python
# API Key de CoinMarketCap (obtener en https://coinmarketcap.com/api/)
API_KEY = "tu-api-key-aqui"

# Ruta a la base de datos SQLite
ORIGIN_DATA = "data/transactions.db"

# Clave secreta para sesiones de Flask (genera una aleatoria)
SECRET_KEY = "tu-clave-secreta"

# Diccionario de criptomonedas disponibles (símbolo: id de CoinMarketCap)
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
```
**IMPORTANTE:** Es importante mantener el diccionario CURRENCIES con los valores que se aparecen en el archivo de ejemplo, o con unos valores donde el símbolo de la moneda coincida con el índice asociado en CoinMarketCap. 
El índice de las criptomonedas se puede obtener en el siguiente endpoint:
https://pro-api.coinmarketcap.com/v1/cryptocurrency/map

y el de las monedas fiat en el siguiente:
https://pro-api.coinmarketcap.com//v1/fiat/map

### 5. Crear la base de datos

Crea la tabla sqlite3 usando el archivo que encontrarás en `data/create.sql`.

### 6. Ejecutar la aplicación

Con el entorno virtual activado, ejecuta:

```bash
flask run
```

La aplicación estará disponible en: `http://127.0.0.1:5002` por compatibilidad con mac, puedes cambiar el puerto en el archivo `.env`.


## 🎯 Funcionalidades

- **Vista de transacciones:** Listado completo de todas las operaciones realizadas
- **Compra/Venta:** Calculadora de conversiones entre criptomonedas con guardado de transacciones
- **Estado de inversión:** 
  - Total invertido en EUR
  - Total recuperado en EUR
  - Valor de compra de la cartera
  - Valor actual de la cartera (en tiempo real)

## ⚙️ Uso

1. Accede a la página principal para ver tu historial de transacciones
2. Ve a "Compra" para realizar una nueva operación:
   - Selecciona la moneda de origen y destino
   - Ingresa la cantidad
   - Haz clic en "Calcular" para ver la conversión
   - Si estás conforme, haz clic en "Guardar" para registrar la transacción^*^
3. Consulta "Status" para ver el estado actual de tu inversión

**^*^Nota:** Si deseas realizar un cambio debes volver a darle a calcular antes de guardar la transacción.

## 📝 Notas del Desarrollador

Este proyecto es la práctica final de un bootcamp de programación desde cero. Incluye:

- Flask como framework web
- SQLite para persistencia de datos
- Integración con API REST de CoinMarketCap
- Validación de formularios con Flask-WTF
- Manejo de errores y excepciones custom
- Sistema de sesiones para validación de transacciones