from mysql.connector import connect, Error
from rich.console import Console

DB_NAME = "fridge_guardian"
TABLE_NAME = "device_states"
CREATE_DB_QUERY = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
SELECT_DB_QUERY = f"USE {DB_NAME}"
CREATE_DEVICE_STATES_DB_QUERY = f"""
create table IF NOT EXISTS
  `{TABLE_NAME}` (
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

    def create_device(self, device_name: str):
        """
        Creates the device only if it doesn't exist in the database.
        If created the unprotected state is set.
        If the device exists it doesn't do anything.

        :param device_name: Name of the device
        """
        console = Console()
        select_device_query = f"""
        SELECT name, protected
        FROM {TABLE_NAME}
        WHERE name = '{device_name}'"""
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(select_device_query)
                    result = cursor.fetchall()

                    print(f"Number of entries: {len(result)}")

        except Error as e:
            console.print(":warning-emoji: MySQL error:")
            print(e)
