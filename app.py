from flask import Flask, render_template
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from datetime import datetime

app = Flask(__name__)

# Banco Central SGS API configuration
BCB_API_BASE = "https://api.bcb.gov.br/dados/serie"

# Common economic indicators series IDs
SERIES = {
    'usd_brl': {'id': '1', 'name': 'USD/BRL Exchange Rate', 'format': 'currency'},
    'selic': {'id': '432', 'name': 'Selic Rate', 'format': 'percent'},
    'ipca': {'id': '433', 'name': 'IPCA Inflation', 'format': 'percent'},
    'cdi': {'id': '12', 'name': 'CDI Rate', 'format': 'percent'}
}

def fetch_bcb_data(series_id, last_n=30):
    """Fetch data from Banco Central SGS API"""
    try:
        url = f"{BCB_API_BASE}/bcdata.sgs.{series_id}/dados/ultimos/{last_n}?formato=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Convert to format suitable for charts
        labels = []
        values = []
        for item in reversed(data):  # Reverse to show oldest first
            labels.append(item['data'])
            values.append(float(item['valor']))

        return {'labels': labels, 'values': values, 'error': None}
    except Exception as e:
        return {'labels': [], 'values': [], 'error': str(e)}

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 27506)),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'sslmode': os.environ.get('DB_SSLMODE', 'require')
}

def get_db_connection():
    """Establish database connection"""
    required_settings = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing = [setting for setting in required_settings if not os.environ.get(setting)]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def dashboard():
    # Fetch data for all series
    series_data = {}
    for key, info in SERIES.items():
        series_data[key] = fetch_bcb_data(info['id'], last_n=30)
        series_data[key]['info'] = info

    return render_template('dashboard.html', series_data=series_data, now=datetime.now())

@app.route('/db-test')
def db_test():
    """Test database connection endpoint"""
    try:
        conn = get_db_connection()
        if conn is None:
            return "<h1>Database Connection Failed</h1><p>Check server logs for details.</p>", 500

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            return f'<h1>Database Connection Successful</h1><p>PostgreSQL version: {version["version"]}</p>'
        except Exception as e:
            conn.close()
            return f'<h1>Database Query Failed</h1><p>Error: {str(e)}</p>', 500
    except ValueError as e:
        return f'<h1>Configuration Error</h1><p>{str(e)}</p>', 500
    except Exception as e:
        return f'<h1>Unexpected Error</h1><p>{str(e)}</p>', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)