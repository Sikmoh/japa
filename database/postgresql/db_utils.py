# -*- coding: utf-8 -*-

# ------------------------------------------------
#    External imports
# ------------------------------------------------
import psycopg2

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
from errors.v1.handlers import ApiError
from config.app_config import POSTGRESQL


# ------------------------------------------------
#     Database Connection
# ------------------------------------------------

def db_connect() -> tuple:
    """
        Connects to our database

    :return:
    """

    try:
        return psycopg2.connect(
            database=POSTGRESQL["database"],
            user=POSTGRESQL["user"],
            password=POSTGRESQL["password"],
            host=POSTGRESQL["host"],
            port=POSTGRESQL["port"],
        )

    except Exception as e:
        # We could use an HTTP error status code of 500 or 503
        raise ApiError(message="Database Connection Error", status_code=503)


def db_insert_update(sql: str, values=None):
    """
        Calls sql on the database and
        returns the result.

    :param sql: The SQL INSERT statement
    :param values: The values to be inserted
    :return: The row ID
    """
    try:
        db = db_connect()
        with db.cursor() as cur:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
        db.commit()
        # If it's an INSERT Return the ID of the last row inserted
        if "INSERT" in sql:
            rid = cur.lastrowid
            db.close()
            return rid

    except psycopg2.OperationalError as e:
        # Integrity Error normally evoked when a duplicate entry is attempted - i.e. same email address, password, etc.
        # Check Unique columns for the database
        raise ApiError(message=e.args[1], status_code=503)
    except Exception as e:
        if e == "Database Connection Error":
            message = "service unavailable"
        else:
            message = e

        raise ApiError(message=message, status_code=503)


def db_query(sql: str, values: str):
    """
        Calls sql on the database and
        returns the result.
    :param sql: The SQL statement
    :param values: The values to be substituted in the SQL query
    :return:
    """

    try:
        db = db_connect()
        with db.cursor() as cur:
            # Extract row headers
            cur.execute(sql, values)
            # Collect the column names, i.e. headers
            headers = [x[0] for x in cur.description]
            return db_json_result(cur.fetchall(), headers)
    except Exception as e:
        if e.message == "Database Connection Error":
            message = "service unavailable"
        else:
            message = e.message
        raise ApiError(message=message, status_code=503)


def db_json_result(data, headers) -> list[dict]:
    json_data = []
    for result in data:
        try:
            json_data.append(dict(zip(headers, result)))
        except TypeError:
            json_data.append(dict(zip(headers, str(result))))
    return json_data
