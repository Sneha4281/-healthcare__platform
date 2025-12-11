import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Function to get DB connection
def get_db():
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Create table if not exists
def create_tables():
    patients_table = """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id  varchar PRIMARY KEY,
        patient_name TEXT NOT NULL
    );
    """

    documents_table = """
    CREATE TABLE IF NOT EXISTS documents (
        document_id varchar PRIMARY KEY,
        patient_id varchar NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filesize BIGINT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    conn = get_db()
    cur = conn.cursor()
    cur.execute(patients_table)
    cur.execute(documents_table)
    conn.commit()
    cur.close()
    conn.close()

# Call the function once to create tables
if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")