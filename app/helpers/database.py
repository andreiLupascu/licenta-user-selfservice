import pymysql
from flask import current_app


def get_connection():
    port = int(current_app.config['DB_PORT'])
    return pymysql.connect(host=current_app.config['DB_HOST'],
                           port=port,
                           user=current_app.config['DB_USER'],
                           passwd=current_app.config['DB_PASS'],
                           db=current_app.config['DB_NAME'])
