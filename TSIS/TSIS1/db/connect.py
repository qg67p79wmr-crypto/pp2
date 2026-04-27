import psycopg2
from db.config import load_config 

def get_connection():
   
    conn = psycopg2.connect(
        host="localhost",
        database="phonebook",
        user="postgres",
        password="your_password"
    )
    return conn