import psycopg2
from config import database
from config import user
from config import password
from config import password2

with psycopg2.connect(database=database, user=user, password=password, password2=password2) as conn:
    with conn.cursor() as cur:
        cur = cur

def create_table():
    try:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                            clients_id SERIAL PRIMARY KEY,
                            first_name VARCHAR(60) NOT NULL
                            last_name VARCHAR(60) NOT NULL
                            "e-mail" varchar NOT NULL UNIQUE CHECK ("e-mail" ILIKE '%@%.%' AND "e-mail" NOT LIKE '%@%@%')
                            tel integer REFERENCES telephone(telephone_id)
                        );
                        """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS telephone(
                            telephone_id SERIAL PRIMARY KEY,
                            number char(10) UNIQUE CHECK (number SIMILAR TO '[0-9]{10}'),
                        );
                        """)
        conn.commit()
        print('Таблицы созданы успешно.')
    except Exception as error:
        print(f"Произошла ошибка '{error}'")






def main():
    pass

if __name__ == "__main__":
    main()