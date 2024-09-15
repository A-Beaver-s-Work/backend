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

def execute_sql(statement, fill, callback=None, commit=True):
    # TODO: connection pool
    # TODO: SECURITY!!!!
    ret = None

    cnx = connect_to_mysql()
    if not cnx or not cnx.is_connected():
        logger.info("Failed to connect to mysql")
        raise ConnectionError("Couldn't connect to mysql") 

    with cnx.cursor(buffered=True) as cursor:
        try:
            cursor.execute(statement, fill)         

            if callback:
                ret = callback(cursor)
        except mysql.connector.Error as err: 
            logger.error(f"Syntax error in request ({statement}, {fill}): {err}")
            raise SyntaxError(f"Error parsing SQL: {err}")

        if commit:
            cnx.commit()

    cnx.close()

    return ret

def count_results(cursor):
    return len(cursor.fetchall()) 
