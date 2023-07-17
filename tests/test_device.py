from unittest.mock import Mock, call

from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.email import Email
from fridgeGuardian.temperature import TemperatureRange
from fridgeGuardian.device import Device
from tests.ressources import WEATHER_FORCAST
from envelopes import Envelope

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
    device._clear_protected()
    device.database.clear_protected.assert_called_with(DEVICE_NAME)


def test_find_temperature_range(device):
    device.weather.get_weather_forcast.return_value = WEATHER_FORCAST

    result = device._forcast_find_temperature_range()
    assert result.minimum == 10.9
    assert result.maximum == 28.3


def test_build_protect_envelopes(device):
    envelope_1 = Envelope(to_addr="to_addr_1")
    envelope_2 = Envelope(to_addr="to_addr_2")

    device.email.build_envelope = Mock(side_effect=[envelope_1, envelope_2])
    device.email.send = Mock()

    device._send_protect_envelopes(TemperatureRange(minimum=10.0, maximum=20.0))

    device.email.send.assert_called()


def test_build_unprotect_envelopes(device):
    envelope_1 = Envelope(to_addr="to_addr_1")
    envelope_2 = Envelope(to_addr="to_addr_2")

    device.email.build_envelope = Mock(side_effect=[envelope_1, envelope_2])
    device.email.send = Mock()

    device._send_unprotect_envelopes(TemperatureRange(minimum=10.0, maximum=20.0))

    device.email.send.assert_called()
