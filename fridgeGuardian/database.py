from mysql.connector import connect, Error

SHOW_DB_QUERY = "SHOW DATABASES"


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

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(SHOW_DB_QUERY)
                    for db in cursor:
                        print(db)
        except Error as e:
            print(e)

