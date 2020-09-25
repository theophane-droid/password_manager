import sqlite3
import random
from des import DesKey
import hashlib
import argparse

def get_cursor_and_connexion():
    """
    A function which return the cursor of the pass database
    return: tuple (sqlite cursor, sqlite connexion) 
    """
    conn = sqlite3.connect('bdd/pass.db', check_same_thread=False)
    return conn.cursor(), conn

def create_database(cursor):
    """
    A function which create the needed database for application, warning if the database already exist, everything will be cleared
    param cursor: sqlite cursor
    """
    with open("bdd/create.sql", "r") as sql_file:
        content = sql_file.read()
        cursor.executescript(content)

def add_password(cursor, connexion, name, content, password, user_name):
    """
    A function a new password in the database
    param cursor: sqlite cursor
    param connexion: sql connexion
    param name: str
    param content: str
    """
    random.seed(password)
    passphrase = ""
    for i in range(24):
        passphrase += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ1234567890")
    key = DesKey(bytes(passphrase, "UTF-8"))
    content = key.encrypt(bytes(content,"UTF-8"), padding=True).hex()
    cursor.execute("INSERT INTO password VALUES (NULL, '{0}', '{1}', '{2}')".format(name, content, user_name))
    connexion.commit()

def add_user(cursor, connexion, name, password):
    name = name.replace(";","")
    hash_ = hashlib.sha3_512(bytes(password,"UTF-8")).hexdigest()
    cursor.execute("INSERT INTO user VALUES ('{0}', '{1}')".format(name, hash_))
    connexion.commit()

def get_user_password_hash(cursor, user_name):
    """
    A function to get the password hash of the user_name user
    param cursor: sqlite cursor
    username: str
    return: str
    """
    cursor.execute("SELECT passwd FROM user WHERE user.name=='{0}'".format(user_name))
    lines = cursor.fetchall()
    try:
        return list(lines[0])[0]
    except:
        return None
def get_passwords(cursor, password, user_name):
    """
    A function to get all stored passwords
    param cursor: sqlite cursor
    return: list; contains tuples of all stored passwords
    """
    cursor.execute("SELECT * FROM password WHERE password.user_name=='{0}'".format(user_name))
    lines = cursor.fetchall()
    result = list()
    for line in lines:
        line = list(line)
        content = line[2]
        random.seed(password)
        passphrase = ""
        for i in range(24):
            passphrase += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ1234567890")
        key = DesKey(bytes(passphrase, "UTF-8"))
        content = key.decrypt(bytes(bytearray.fromhex(content)), padding=True).decode("UTF-8")
        line[2]=content
        result.append(line)
    return result

def delete_password(cursor, connexion, id):
    """
    A function to delete a password
    param cursor: sqlite cursor
    param connexion: sqlite connexion
    param id: int
    """
    cursor.execute('DELETE FROM password WHERE id={}'.format(id))
    connexion.commit()

def test():
    """ A test function """
    cursor, connexion = get_cursor_and_connexion()
    create_database(cursor)
    add_user(cursor, connexion, "theo","mdp1")
    add_user(cursor, connexion, "theo2","mdp2")
    print(get_user_password_hash(cursor,"theo"))
    print(get_user_password_hash(cursor,"theod"))
    add_password(cursor, connexion, "name","content","coucou","theo")
    add_password(cursor, connexion, "name2","content2","coucou","theo")
    print(get_passwords(cursor, "coucou", "theo"))
    delete_password(cursor, connexion, 1)
    connexion.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action",help="should be reset, add or remove")
    parser.add_argument("username",help="should be reset, add or remove")