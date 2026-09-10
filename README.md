# Flask Application with PostgreSQL Connection

This is a simple Flask application configured to connect to a PostgreSQL database hosted on Aiven Cloud.

## Database Connection Details

- **Host**: devops-joaodan-b63e.f.aivencloud.com
- **Port**: 27506
- **Database**: defaultdb
- **User**: avnadmin
- **Password**: AVNS_ZifEsm9Mt4zdl4Wt6bU
- **SSL Mode**: require

## GitHub Repository

This application is connected to the GitHub repository: https://github.com/Basquat/Devops.git

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the application:
   - Home page: http://localhost:5000/
   - Database test endpoint: http://localhost:5000/db-test

## Application Endpoints

- `GET /`: Returns basic information about the database configuration
- `GET /db-test`: Tests the database connection and returns PostgreSQL version

## Notes

- The database connection uses SSL as required by the Aiven cloud service
- The application uses psycopg2-binary for PostgreSQL connectivity
- RealDictCursor is used to return results as dictionaries for easier handling