from fridgeGuardian.database import Database
from pytest import fixture

@fixture
def database():
    database = Database(host='localhost',
                        user='root',
                        password='example',
                        database='fridge_guardian_db')
    return database


def test_create_device(database):

    database.create_device("fridge")
