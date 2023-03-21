# ------------------------------------------------
#    External imports
# ------------------------------------------------

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
from errors.v1.handlers import ApiError
from database.mysql.db_utils import db_connect


# ------------------------------------------------
#     Database TABLE CREATION functions
# ------------------------------------------------

def user_model():
    """
        Return the SQL statement to create the Users table

    :return: string containing POSTGRESQL user table creation statement
    """
    return "(id int NOT NULL AUTO_INCREMENT, email VARCHAR(255), password VARCHAR(255), refresh_token VARCHAR(1024), " \
           "access_role VARCHAR(10), created DATETIME default now(), disabled BOOLEAN, email_verified BOOLEAN, " \
           "logged_in BOOLEAN, " \
           "CONSTRAINT UC_user UNIQUE (id,email,password))"


def check_table_exists(db_connection):
    """
            Check if the user table for the database is already created
        :param db_connection: The active connection to our database
        :return:
        """
    try:
        with db_connection.cursor() as cur:
            cur.execute("""
        SELECT COUNT(*) as TotalNumberOfTablesInaerolab
        FROM information_schema.tables where table_schema='aerolab'
        and table_name = 'users'
        """)
            if cur.fetchone()[0] == 1:
                return True
    except Exception as e:
        raise ApiError("checking table error", 500)


def create_user_table(db_connection):
    """
        Create the user table for the database
    :param db_connection: The active connection to our database
    :return:
    """
    try:
        with db_connection.cursor() as cur:
            user = user_model()
            check_table = check_table_exists(db_connection)
            create_users = "CREATE TABLE users " + user
            if not check_table:
                cur.execute(create_users)
                db_connection.commit()
            else:
                pass
    except Exception as e:
        raise ApiError("User table creation error", 500)


# ------------------------------------------------
#     Setup the database
# ------------------------------------------------
connection = db_connect()
create_user_table(connection)
