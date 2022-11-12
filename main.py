import psycopg2
from config import database
from config import user
from config import password
from config import password2

with psycopg2.connect(database=database, user=user, password=password, password2=password2) as conn:
    with conn.cursor() as cur:
        cur = cur

def create_table():
    cur.conn




def main():
    pass

if __name__ == "__main__":
    main()