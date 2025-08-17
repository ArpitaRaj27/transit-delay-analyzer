
import os
import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB","transit"),
        user=os.getenv("POSTGRES_USER","transit"),
        password=os.getenv("POSTGRES_PASSWORD","transit"),
        host=os.getenv("POSTGRES_HOST","localhost"),
        port=int(os.getenv("POSTGRES_PORT","5432"))
    )
