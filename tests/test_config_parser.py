from pytest import fixture
from fridgeGuardian.database import Database
from fridgeGuardian.config_parser import ConfigurationParser
from fridgeGuardian.app_settings import YR_IDENTITY


CONFIGURATION = {'time_zone': "Europe/Oslo",
                     'database': {
                         'host': "127.0.0.1",
                         'user': 'root',
                         'password': 'root',
                         'database': 'fridge_guardian'},
                     'email': {
                         "smtp_address": "smtp.email.com",
                         "smtp_port": 487,
                         "login": "login",
                         "password": "password",
                         "tls": True,
                         "from_email": "test@email.com",
                         "from_name": "Fridge Guardian"},
                     "devices": [
                         {"name": "Ourdoor fridge",
                          "longitude": 33.631839,
                          "latitude": 27.380583,
                          "email_list": ['email_1@email.com',
                                         'email_2@email.com'],
                          "temperature_min": 10,
                          "temperature_max": 60},
                         {"name": "Karsher",
                          "longitude": 30.000000,
                          "latitude": 27.000000,
                          "email_list": ['email_1@email.com',
                                         'email_2@email.com'],
                          "temperature_min": 0,
                          "temperature_max": 60}
                     ]}

@fixture
def configuration():
    config_parser = ConfigurationParser(CONFIGURATION)
    return config_parser


def test_build_email(configuration):
    email = configuration.build_email()

    assert email.smtp._host == CONFIGURATION['email']["smtp_address"]
    assert email.smtp._port == CONFIGURATION['email']["smtp_port"]
    assert email.smtp._login == CONFIGURATION['email']["login"]
    assert email.smtp._password == CONFIGURATION['email']["password"]
    assert email.smtp._tls == CONFIGURATION['email']["tls"]
    assert email.from_email == CONFIGURATION['email']["from_email"]
    assert email.from_name == CONFIGURATION['email']["from_name"]


def test_build_yr(configuration):
    yr_config = {"longitude": 33.631839,
                 "latitude": 27.380583}
    time_zone = "Europe/Oslo"

    yr = configuration.build_yr(yr_config)

    assert yr.longitude == yr_config["longitude"]
    assert yr.latitude == yr_config["latitude"]
    assert yr.identity == YR_IDENTITY
    assert str(yr._time_zone) == CONFIGURATION['time_zone']


def test_build_device(configuration):
    pass
