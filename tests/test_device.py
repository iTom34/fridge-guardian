from unittest.mock import Mock

from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.email import Email
from fridgeGuardian.temperature import TemperatureRange
from fridgeGuardian.device import Device

from pytest import fixture

DEVICE_NAME = "device_name"
EMAIL_LIST = ["test1@test.com", "test2@test.com"]

@fixture
def device():
    device = Device(name=DEVICE_NAME,
                    weather=Mock(name="weather"),
                    email=Mock(name="email"),
                    email_list=EMAIL_LIST,
                    database=Mock(name="database"),
                    operating_range=Mock(name="TemperatureRange"))
    return device


def test_get_protected(device):
    device.database.get_protected.return_value = True

    assert device._get_protected() is True
    device.database.get_protected.assert_called_with(DEVICE_NAME)


def test_set_protected(device):
    device._set_protected()
    device.database.set_protected.assert_called_with(DEVICE_NAME)


def test_clear_protected(device):
    device._set_protected()
    device.database.set_protected.assert_called_with(DEVICE_NAME)