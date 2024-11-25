import psycopg2



def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        lastname VARCHAR(30),
        email VARCHAR(254)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        number VARCHAR(16) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    # conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO client(client_name, client_surname, client_email, client_phones) VALUES (%s, %s, %s) 
           RETURNING client_id;""", (name, surname, email))
        client_id = cur.fetchone()[0]
        print('Client has been added successfully')

def add_phone(conn, client_id, *phones):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones(client_id, phones) VALUES (%s, %s);
        """, (client_id, phones))

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, email=%s
        WHERE client_id=%s;
        """, (first_name, last_name, email, client_id))


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phones WHERE client_id=%s AND phone_number=%s;
                """, (client_id, phone))
        # conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phones WHERE client_id=%s AND phone_number=%s;
                """, (client_id, phone))
        # conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client_info WHERE client_id=%s;
                """, (client_id,))
        # conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT ci.first_name, ci.last_name, ci.email, p.phone_number FROM client_info ci
                LEFT JOIN phones p ON ci.client_id = p.client_id OR ci.client_id IS NULL
                WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
                AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
                AND (email = %(email)s OR %(email)s IS NULL)
                AND (phone_number = %(phone_number)s or %(phone_number)s IS NULL)
                ORDER BY ci.last_name, ci.first_name;
        """)

with psycopg2.connect(database="clients_db", user="postgres", password="Jaguar2427") as conn:
    # Создаем таблицы БД
    create_db(conn)

    # Добавляем клиентов
    add_client(conn, "Ника", "Иванова", "iva@ya.ru", ("7999546411", "198741263", "+22222222"))
    add_client(conn, "Петр", "Пименов", "petya@mail.com")
    add_client(conn, "Костя", "Александров", "abcв@mail.com", 123456)
    add_client(conn, "Иван", "Попов", "zaq@gmail.com", 123451641)
    add_client(conn, "Инна", "Серова", "irina.s@gmail.ru")

    # Добавляем телефонные номера
    add_phone(conn, 2, "22222")
    add_phone(conn, 3, "77777")

    # Вносим изменения в информацию о клиенте
    change_client(conn, 2, "Петр", "Сидоров", "petya@gmail.com")

    # Удаляем номер телефона
    delete_phone(conn, 1, "7999546411")

    # Удаляем колиента из БД (в том числе все записи с его номерами телефонов из таблицы phones)
    delete_client(conn, 1)

    # Ищем клиентов по параметрам
    find_client(conn)
    find_client(conn, first_name="Петр", phone="00000")
    find_client(conn, first_name="Костя", last_name="Александров", phone="123456")
    find_client(conn, email="petya@mail.com")
    find_client(conn, last_name="Попов")
    find_client(conn, first_name="Инна")

    conn.close()