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
                            client_id SERIAL PRIMARY KEY,
                            first_name VARCHAR(60) NOT NULL
                            last_name VARCHAR(60) NOT NULL
                            e_mail VARCHAR NOT NULL UNIQUE CHECK (e_mail LIKE '%@%.%' AND "e-mail" NOT LIKE '%@%@%')
                        );
                        """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS telephone(
                            telephone_id SERIAL PRIMARY KEY,
                            client_id INTEGER REFERENCES clients(client_id),
                            number char(10) UNIQUE CHECK (number SIMILAR TO '[0-9]{10}'),
                        );
                        """)
        conn.commit()
        print('Таблицы созданы успешно.')
    except psycopg2.OperationalError as error:
        print(f"Произошла ошибка '{error}'")

def add_client(client_id, first_name, last_name, e_mail):
    cur.execute("""
            INSERT INTO clients(first_name, last_name, e_mail, number) VALUES (%s, %s, %s, %s);
            """, (client_id, first_name, last_name, e_mail,))
    conn.commit()
    cur.execute("""SELECT * FROM clients;""")
    print(cur.fetchall())

def add_namber(telephone_id, number):
    cur.execute("""
                INSERT INTO telephone(telephone_id, number) VALUES (%s, %s);
                """, (telephone_id, number,))
    conn.commit()
    cur.execute("""SELECT * FROM telephone;""")
    print(cur.fetchall())





def main():
    create_table()
    first_name = input('Имя клиента: ')
    last_name = input("Фамилия клиента: ")
    e_mail = input("Email клиента: ")
    add_client(first_name=first_name, last_name=last_name, e_mail=e_mail)
    number = input('Телефон клиента: ')
    add_namber(number)

if __name__ == "__main__":
    main()