import psycopg2
from config import database
from config import user
from config import password
from config import password2
import pprint


def create_table(conn, cur):
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

def add_client(conn, cur, client_id, first_name, last_name, e_mail):
    cur.execute("""
            INSERT INTO clients(first_name, last_name, e_mail, number) VALUES (%s, %s, %s, %s);
            """, (client_id, first_name, last_name, e_mail,))
    conn.commit()
    cur.execute("""SELECT * FROM clients;""")
    print(cur.fetchall())

def add_namber(conn, cur, client_id, number):
    cur.execute("""
                INSERT INTO telephone(telephone_id, number) VALUES (%s, %s);
                """, (client_id, number,))
    conn.commit()
    cur.execute("""SELECT * FROM telephone;""")
    print(cur.fetchall())

def change_client(conn, cur):
    print("Для изменения информации о клиенте, пожалуйста, введите нужную Вам команду.\n "
        "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")

    while True:
        command_symbol = int(input())
        if command_symbol == 1:
            input_id_for_changing_name = input("Введите id клиента имя которого хотите изменить: ")
            input_name_for_changing = input("Введите имя для изменения: ")
            cur.execute("""
            UPDATE clients SET first_name=%s WHERE client_id=%s;
            """, (input_name_for_changing, input_id_for_changing_name))
            conn.commit()
            break
        elif command_symbol == 2:
            input_id_for_changing_surname = input("Введите id клиента фамилию которого хотите изменить: ")
            input_surname_for_changing = input("Введите фамилию для изменения: ")
            cur.execute("""
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            """, (input_surname_for_changing, input_id_for_changing_surname))
            conn.commit()
            break
        elif command_symbol == 3:
            input_id_for_changing_email = input("Введите id клиента e-mail которого хотите изменить: ")
            input_email_for_changing = input("Введите e-mail для изменения: ")
            cur.execute("""
            UPDATE clients SET e_mail=%s WHERE client_id=%s;
            """, (input_email_for_changing, input_id_for_changing_email))
            conn.commit()
            break
        elif command_symbol == 4:
            input_number_change = input("Введите номер телефона который Вы хотите изменить: ")
            input_number_for_changing = input("Введите новый номер телефона, который заменит собой старый: ")
            cur.execute("""
            UPDATE telephone SET number=%s WHERE number=%s;
            """, (input_number_for_changing, input_number_change))
            conn.commit()
            break
        else:
            print("Вы ввели неправильную команду, повторите ввод!")


def delete_client_number(conn):
    input_id_for_deleting_number = input("Введите id клиента номер телефона которого хотите удалить: ")
    input_number_for_deleting = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s AND number=%s
        """, (input_id_for_deleting_number, input_number_for_deleting))
    conn.commit()


def delete_client(conn):
    id_for_deleting_client = input("Введите id клиента которого хотите удалить: ")
    client_surname_for_deleting = input("Введите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s
        """, (id_for_deleting_client,))
        cur.execute("""
        DELETE FROM clients WHERE client_id=%s AND last_name=%s
        """, (id_for_deleting_client, client_surname_for_deleting))
    conn.commit()

def find_client(cur):
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
    while True:
        command_for_finding = int(input("Введите команду для поиска информации о клиенте: "))
        if command_for_finding == 1:
            name_for_finding = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
            SELECT client_id, first_name, last_name, e_mail, number
            FROM clients AS c
            LEFT JOIN numbers AS n ON n.telephone_id = c.client_id
            WHERE first_name=%s
            """, (name_for_finding,))
            print(cur.fetchall())
        elif command_for_finding == 2:
            last_name_for_finding = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
            SELECT client_id, first_name, last_name, e_mail, number
            FROM clients AS c
            LEFT JOIN numbers AS n ON n.telephone_id = c.client_id
            WHERE last_name=%s
            """, (last_name_for_finding,))
            print(cur.fetchall())
        elif command_for_finding == 3:
            email_for_finding = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
            SELECT client_id, first_name, last_name, e_mail, number
            FROM clients AS c
            LEFT JOIN numbers AS n ON n.telephone_id = c.client_id
            WHERE e_mail=%s
            """, (email_for_finding,))
            print(cur.fetchall())
        elif command_for_finding == 4:
            number_for_finding = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT client_id, first_name, last_name, e_mail, number
            FROM clients AS c
            LEFT JOIN numbers AS n ON n.telephone_id = c.client_id
            WHERE number=%s
            """, (number_for_finding,))
            print(cur.fetchall())
        else:
            print("Вы ввели неправильную команду, повторите ввод!")


#проверяем таблицы
def check_function(cur):
    cur.execute("""
    SELECT * FROM clients;
    """)
    pprint(cur.fetchall())
    cur.execute("""
    SELECT * FROM telephone;
    """)
    pprint(cur.fetchall())



def main():
    with psycopg2.connect(database=database, user=user, password=password, password2=password2) as conn:
        with conn.cursor() as cur:
            create_table(cur)
            client_id = input('Имя ID клиента: ')
            first_name = input('Имя клиента: ')
            last_name = input("Фамилия клиента: ")
            e_mail = input("Email клиента: ")
            add_client(client_id=client_id, first_name=first_name, last_name=last_name, e_mail=e_mail)
            client_id = input('Имя ID клиента которому будет добавлен номер телефона: ')
            number = input('Телефон клиента: ')
            add_namber(client_id=client_id, number=number)
            change_client(conn, cur)
            delete_client_number(conn)
            find_client(cur)

if __name__ == "__main__":
    main()