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

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    select_device_query = f"""
                    SELECT name, protected
                    FROM {TABLE_NAME}
                    WHERE name = '{device_name}'"""

                    cursor.execute(select_device_query)
                    result = cursor.fetchall()

                    print(f"Number of entries: {len(result)}")

                    if len(result) == 0:
                        console.print(f':point_right: Adding {device_name} to database')

                        insert_device_query = f"""
                        INSERT INTO {TABLE_NAME} (name, protected)
                        VALUES
                        ("{device_name}", FALSE)"""

                        cursor.execute(insert_device_query)
                        connection.commit()

        except Error as e:
            console.print(":warning-emoji: MySQL error:")
            print(e)

    def set_protected(self, device_name: str):
        """
        Sets the device as protected.
        If the device doesn't exist in the database it will create it.

        :param device_name: Sets the device name
        """

        console = Console()
        self.create_device(device_name)

        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    set_protected_query = f"""
                    UPDATE
                        {TABLE_NAME}
                    SET
                        protected = TRUE
                    WHERE
                        name = '{device_name}'"""

                    cursor.execute(set_protected_query)
                    connection.commit()

        except Error as e:
            console.print(":warning-emoji: MySQL error:")
            print(e)

    def clear_protected(self, device_name: str):
        """
        Sets the device as NOT protected.
        If the device doesn't exist in the database it will create it.

        :param device_name: Sets the device name
        """

        console = Console()
        self.create_device(device_name)

        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    set_protected_query = f"""
                    UPDATE
                        {TABLE_NAME}
                    SET
                        protected = FALSE
                    WHERE
                        name = '{device_name}'"""

                    cursor.execute(set_protected_query)
                    connection.commit()

        except Error as e:
            console.print(":warning-emoji: MySQL error:")
            print(e)

    def get_protected(self, device_name):
        """
        Returns the status of the device (protected or not).
        :return:
        """

        console = Console()
        self.create_device(device_name)

        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    get_protected_query = f"""
                            SELECT name, protected
                            FROM {TABLE_NAME}
                            WHERE name = '{device_name}'"""

                    cursor.execute(get_protected_query)
                    result = cursor.fetchall()

                    if len(result) != 1:
                        console.print(":warning-emoji: Unexpected reply from database (got more than 1 result for a device name)=")
                        return False

                    if result[0][1] == 1:
                        return True

                    else:
                        return False

        except Error as e:
            console.print(":warning-emoji: MySQL error:")
            print(e)