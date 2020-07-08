import random
import string
import base64
import pymysql
from passlib.hash import bcrypt

from app.helpers.database import get_connection


def get_activation_code(email):
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            cur.execute('SELECT valid_account FROM user WHERE username=%s', (email,))
            try:
                valid_account = cur.fetchone()['valid_account']
            except TypeError:
                return "No account found with given email.", 404
            if valid_account == 1:
                activation_code = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
                cur.execute('UPDATE user SET activation_code=%s WHERE username=%s', (activation_code, email,))
                conn.commit()
                conn.close()
                return activation_code, 200
            else:
                conn.close()
                return "Account is not eligible for activation", 403
        except TypeError as e:
            print(e.with_traceback())
            conn.close()
            return "Something went wrong with the query.", 500


def activate_account(request):
    print(request)
    email = request[0]['username']
    password = bcrypt.encrypt(base64.b64decode(request[0]['password']).decode("utf-8"))
    activation_code = request[0]['activation_code']
    if activation_code:
        conn = get_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            try:
                affected_rows = cur.execute("UPDATE user SET password=%s, is_active=1 WHERE username=%s AND activation_code=%s AND is_active!=1",
                            (password, email, activation_code,))
                if affected_rows == 1:
                    conn.commit()
                    conn.close()
                    return "Account successfully activated and password set.", 200
                else:
                    conn.close()
                    return "Either the email or the activation code is wrong.", 400
            except TypeError as e:
                print(e.with_traceback())
                conn.close()
                return "Something went wrong with the query.", 500
