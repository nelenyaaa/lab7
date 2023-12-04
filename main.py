import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def select_table_from_query(sql_split, query_type):
    if query_type == 'insert':
        query_table = sql_split.index('into') + 1
    elif query_type == 'update':
        query_table = sql_split.index('update') + 1
    else:
        query_table = sql_split.index('from') + 1

    table_name = sql_split[query_table]
    sql = 'SELECT * FROM ' + table_name

    return sql


def execute(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)

        print('Запит: ' + sql)

        sql_split = sql.lower().split()

        if sql_split[0] == 'select':
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print()

        elif sql_split[0] == 'insert':
            print('Запис додано')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

        elif sql_split[0] == 'update' or sql_split[0] == 'delete':
            conn.commit()
            print('Запис змінено / видалено')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

    except Error as e:
        print(e)


def main():
    database = r"agenda.db"

    conn = create_connection(database)

    with conn:
        print("1. Вивести всі записи з таблиці records")
        execute(conn, "SELECT * FROM records")

        print("2. Зміна часу в записі з id = 2")
        execute(conn, "UPDATE records SET remind = '2023-12-04 16:30' WHERE id = 2")

        print("3. Видалення запису з записів планувальника")
        execute(conn, "DELETE FROM records WHERE id = 1")

        print("4. Додати новий запис про подію")
        execute(conn, """
                INSERT INTO
                records (id, name, remind, content)
                VALUES (4, 'Прибрати у кімнаті', '2023-12-04 22:00', 'Який безлад у мене в кімнаті...');
            """)


if __name__ == '__main__':
    main()
