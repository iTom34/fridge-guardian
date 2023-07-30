
from fridgeGuardian.database import Database
from fridgeGuardian.config_parser import build_email, build_yr
from fridgeGuardian.app_settings import YR_IDENTITY


def test_build_email():
    email_config = {"smtp_address": "smtp.email.com",
                    "smtp_port": 487,
                    "login": "login",
                    "password": "password",
                    "tls": True,
                    "from_email": "test@email.com",
                    "from_name": "Fridge Guardian"}

    email = build_email(email_config)

    assert email.smtp._host == email_config["smtp_address"]
    assert email.smtp._port == email_config["smtp_port"]
    assert email.smtp._login == email_config["login"]
    assert email.smtp._password == email_config["password"]
    assert email.smtp._tls == email_config["tls"]
    assert email.from_email == email_config["from_email"]
    assert email.from_name == email_config["from_name"]

def test_build_yr():
    yr_config = {"longitude": 33.631839,
                 "latitude": 27.380583}
    time_zone = "Europe/Oslo"

    yr = build_yr(yr_config, time_zone)

    assert yr.longitude == yr_config["longitude"]
    assert yr.latitude == yr_config["latitude"]
    assert yr.identity == YR_IDENTITY
    assert str(yr._time_zone) == time_zone

def test_build_device():
    device_config = {"name": "Ourdoor fridge",
                     "longitude"}
