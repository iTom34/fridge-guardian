from unittest.mock import Mock, call

import pytest

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
OUT_OF_SPEC = [TemperatureRange(minimum=10, maximum=15),
               TemperatureRange(minimum=10, maximum=25),
               TemperatureRange(minimum=10, maximum=40),
               TemperatureRange(minimum=25, maximum=40),
               TemperatureRange(minimum=40, maximum=50)]
IN_SPEC = TemperatureRange(minimum=25, maximum=30)

@fixture
def device():
    device = Device(name=DEVICE_NAME,
                    weather=Mock(name="weather"),
                    email=Mock(name="email"),
                    email_list=EMAIL_LIST,
                    database=Mock(name="database"),
                    operating_range=TemperatureRange(minimum=20, maximum=35))
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

    result = device._get_temperature_range()
    assert result.minimum == 10.9
    assert result.maximum == 28.3


class TestCheckTemperature:
    @pytest.mark.parametrize('temperature_range', OUT_OF_SPEC)
    def test_unprotected_out_of_range(self, temperature_range, device):
        """
        Testing an unprotected device with a tempearture out of range
        """
        device._get_temperature_range = Mock(return_value=temperature_range)
        device._get_protected = Mock(return_value=False)
        device._send_protect_envelopes = Mock()
        device.database.set_protected = Mock()

        device.check_temperature()

        device._get_temperature_range.assert_called_once()
        device._get_protected.assert_called_once()
        device._send_protect_envelopes.assert_called_once_with(temperature_range)
        device.database.set_protected.assert_called_once()

    def test_unprotected_in_range(self, device):
        """
        Testing an unprotected device with a tempearture in range
        """
        device._get_temperature_range = Mock(return_value=IN_SPEC)
        device._get_protected = Mock(return_value=False)
        device._send_protect_envelopes = Mock()
        device.database.set_protected = Mock()

        device.check_temperature()

        device._get_temperature_range.assert_called_once()
        device._get_protected.assert_called_once()
        device._send_protect_envelopes.assert_not_called()
        device.database.set_protected.assert_not_called()

    @pytest.mark.parametrize('temperature_range', OUT_OF_SPEC)
    def test_protected_out_of_range(self, temperature_range, device):
        """
        Testing a protected device with a tempearture out of range
        """
        device._get_temperature_range = Mock(return_value=temperature_range)
        device._get_protected = Mock(return_value=True)
        device._send_unprotect_envelopes = Mock()
        device.database.clear_protected = Mock()

        device.check_temperature()

        device._get_temperature_range.assert_called_once()
        device._get_protected.assert_called_once()
        device._send_unprotect_envelopes.assert_not_called()
        device.database.clear_protected.assert_not_called()

    def test_protected_in_range(self, device):
        """
        Testing a protected device with a tempearture in range
        """
        device._get_temperature_range = Mock(return_value=IN_SPEC)
        device._get_protected = Mock(return_value=True)
        device._send_unprotect_envelopes = Mock()
        device.database.clear_protected = Mock()

        device.check_temperature()

        device._get_temperature_range.assert_called_once()
        device._get_protected.assert_called_once()
        device._send_unprotect_envelopes.assert_called_once_with(IN_SPEC)
        device.database.clear_protected.assert_called_once()


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
