import psycopg2


def drop_tables(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS phones;")
        cur.execute("DROP TABLE IF EXISTS client;")

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(20) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                number VARCHAR(40) UNIQUE,
                client_id INTEGER REFERENCES client(id)
            );
            """)

# Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO client(first_name, last_name, email) 
           VALUES (%s, %s, %s)
           RETURNING id; 
           """, (first_name, last_name, email))
        cur.fetchall()
    print('Client has been added successfully')

# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, number) VALUES (%s, %s);
            """, (client_id, number,))
        cur.execute("""
            SELECT * FROM phones;
            """)
    print('Номер телефона добавлен')

# Функция, позволяющая изменить данные о клиенте.
def change_client(conn, id: int, first_name: str = None,
                  last_name: str = None, email: str = None,
                  old_phone: str = None, new_phone: str = None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE client SET first_name = %s
                WHERE id = %s;
                """, (first_name, id))
            conn.commit()
        if last_name:
            cur.execute("""
            UPDATE client SET last_name = %s
            WHERE id = %s;
            """, (last_name, id))
            conn.commit()
        if email:
            cur.execute("""
            UPDATE client SET email = %s
            WHERE id = %s;
            """, (email, id))
            conn.commit()
        if old_phone and new_phone:
            cur.execute("""
            UPDATE phones SET number = %s 
            WHERE client_id = %s AND numbere = %s;
            """, (new_phone, client_id, old_phone))
            conn.commit()
        print('Изменения внесены в таблицу')

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s AND number=%s;
            """, (client_id, number))

# Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id: int):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = %s;
        """, (client_id,))
        cur.execute("""
        DELETE FROM client
        WHERE id = %s;
        """, (id,))
    print('Client has been removed successfully')

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM client
            WHERE first_name = %s;
            """, (first_name,))
        return cur.fetchall()
        cur.execute("""
            SELECT * FROM client
            WHERE email = %s;
            """, (email,))
        return cur.fetchall()
        cur.execute("""
            SELECT * FROM client
            WHERE last_name = %s;
            """, (last_name))
        return cur.fetchall()


if __name__ == '__main__':

    with psycopg2.connect(database="netology", user="postgres", password="Jaguar2427") as conn:
        drop_tables(conn)
        create_db(conn)

    # Добавляем клиентов
    add_client(conn, first_name="Петр", last_name="Пименов", email="petya@mail.com")
    add_client(conn, "Костя", "Александров", "abcв@mail.com", 123456)
    add_client(conn, "Иван", "Попов", "zaq@gmail.com", 123451641)
    add_client(conn, "Инна", "Серова", "irina.s@gmail.ru")

    # Добавляем телефонные номера
    add_phone(conn, 2, "22222")
    add_phone(conn, 3, "77777")

    # Вносим изменения в информацию о клиенте
    change_client(conn, 2, "Максим", "Сидоров", "petya@gmail.com")

    # Удаляем номер телефона
    delete_phone(conn, 1, "7999546411")

    # Удаляем колиента из БД (в том числе все записи с его номерами телефонов из таблицы phones)
    delete_client(conn, 1)

    # Ищем клиентов по параметрам
    find_client(conn, first_name = "Петр", last_name = "Пименов", email = "petya@mail.com")
    find_client(conn, last_name="Попов")
    find_client(conn, email = "petya@mail.com")


    conn.close()