from mysql.connector import connect, Error
from rich.console import Console

DB_NAME = "fridge_guardian"
SHOW_DB_QUERY = "SHOW DATABASES LIKE \'fridge_guardian\'"
CREATE_DB_QUERY = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
SELECT_DB_QUERY = f"USE {DB_NAME}"
CREATE_DEVICE_STATES_DB_QUERY = """
create table IF NOT EXISTS
  `device_states` (
    `id` int unsigned not null auto_increment primary key,
    `name` VARCHAR(100) not null,
    `protected` BOOLEAN not null
  )
"""

class Database:
    def __init__(self,
                 host: str,
                 user: str,
                 password: str,
                 database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        console = Console()

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_DB_QUERY)
                    cursor.execute(SELECT_DB_QUERY)
                    cursor.execute(CREATE_DEVICE_STATES_DB_QUERY)
                    connection.commit()

        except Error as e:
            print(e)

