import sqlite3

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            op_type TEXT,
            description TEXT,
            date TEXT,
            user TEXT
        )
    ''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT
                   )
                    ''')
    conn.commit()
    conn.close()


def add_operation(amount, op_type, description, date, user):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO operations (amount, op_type, description, date, user)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, op_type, description, date, user))

    conn.commit()
    conn.close()




def get_operations():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM operations")

    operations = cursor.fetchall()
    conn.close()

    return operations

def get_report():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT op_type, SUM(amount) 
                   FROM operations
                   GROUP BY op_type
                   """)

    sum_operations = cursor.fetchall()
    
    conn.close()
    return sum_operations

def delete_item(operation_id):
    conn =sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    DELETE FROM operations
                    WHERE id = ?

                   """ ,(operation_id,))
    print(operation_id)
    conn.commit()
    conn.close()

def get_for_edit(edit_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT * FROM operations
                    where id =?
                   
                    """, (edit_id,))
    data_for_edit = cursor.fetchone()

    conn.commit()
    conn.close()
    return(data_for_edit)
    

def update_operation(edit_id, amount, op_type, description, date, user):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    UPDATE operations
                   SET amount = ?, op_type = ?, description = ?, date = ?, user = ?
                   WHERE id = ?
                   """, ( amount, op_type, description, date, user, edit_id))
    conn.commit()
    conn.close()

def get_fitered_operations(data_before, data_after):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT * FROM operations
                   WHERE date BETWEEN ? AND ?
                   """, (data_before, data_after))
    filtered_data = cursor.fetchall()
   
    conn.close()
    return(filtered_data)

def find_user(user_login):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT * FROM users
                   WHERE username = ?
                    """, (user_login,))
    user_data = cursor.fetchone()

    conn.close()
    return(user_data)

def add_column():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""
                    ALTER TABLE users
                   ADD users_name TEXT """)
    conn.commit()
    conn.close()
    