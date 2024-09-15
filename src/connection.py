import mysql.connector
from mysql.connector import errorcode
from logger import logger

def connect_to_mysql():
    try:
        return mysql.connector.connect(user='root', password='secretrootpass', host='db', database='abw', port=3306)
    except (mysql.connector.Error, IOError) as err:
        logger.info("Failure to connect, exiting without a connection: %s", err)
        return None

    return None

def execute_sql(statement, fill):
    # TODO: connection pool
    # TODO: SECURITY!!!!

    cnx = connect_to_mysql()
    if not cnx or not cnx.is_connected():
        logger.info("Failed to connect to mysql")
        raise ConnectionError("Couldn't connect to mysql") 

    with cnx.cursor() as cursor:
        try:
            cursor.execute(statement, fill)         
        except mysql.connector.Error as err: 
            logger.error(f"Syntax error in request ({statement}, {fill}): {err}")
            raise SyntaxError(f"Error parsing SQL: {err}")

        cnx.commit()

    cnx.close()
