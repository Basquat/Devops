from flask import Flask
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database configuration from environment variables
# ALL of these MUST be set in your environment - no defaults provided for security
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 27506)),  # Port can have default as it's not secret
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),  # MUST be set - no default for security
    'sslmode': os.environ.get('DB_SSLMODE', 'require')
}

def get_db_connection():
    """Establish database connection"""
    # Check that required settings are present
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
def hello():
    # Only show non-sensitive config info
    safe_config = {
        'host': DB_CONFIG['host'] or 'Not set',
        'port': DB_CONFIG['port'],
        'database': DB_CONFIG['database'] or 'Not set',
        'user': DB_CONFIG['user'] or 'Not set'
    }

    return '''
    <h1>Flask App PostgreSQL Configuration</h1>
    <p>This application connects to PostgreSQL using environment variables:</p>
    <ul>
        <li>Host: {host}</li>
        <li>Port: {port}</li>
        <li>Database: {database}</li>
        <li>User: {user}</li>
    </ul>
    <p><em>Password and SSL mode are set from environment variables (not shown for security)</em></p>
    <p><em>Note: Make sure to set DB_HOST, DB_NAME, DB_USER, and DB_PASSWORD environment variables.</em></p>
    '''.format(**safe_config)

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
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Debug off for production safety