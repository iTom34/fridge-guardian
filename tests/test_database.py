from fridgeGuardian.database import Database

def test_database():
    database = Database(host='localhost',
                        user='root',
                        password='example',
                        database='fridge_guardian_db')

