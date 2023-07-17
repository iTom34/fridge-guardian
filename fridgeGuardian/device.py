from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.email import Email
from fridgeGuardian.temperature import TemperatureRange

from envelopes import Envelope


class Device:
    def __init__(self,
                 name: str,
                 weather: Yr,
                 email: Email,
                 email_list: list[str],
                 database: Database,
                 operating_range: TemperatureRange):
        """
        Constructor of a device

        :param name: Name of the device.
        :param weather: Yr API mapped to the location of the device.
        :param email: Email object to send email.
        :param email_list: Email list of contact person.
        :param database: Database link storing the state of the device (protected or not).
        :param operating_range: Operational temperature range of the device.
        """
        self.name: str = name
        self.weather: Yr = weather
        self.email: Email = email
        self.email_list: list[str] = email_list
        self.database: Database = database
        self.operating_range: TemperatureRange = operating_range

    def _get_protected(self) -> bool:
        """
        Returns the status of the device (protected or not)

        :return: True, the device is protected, False, the device is not protected
        """
        return self.database.get_protected(self.name)

    def _set_protected(self):
        """
        Sets the device as protected
        """
        self.database.set_protected(self.name)

    def _clear_protected(self):
        """
        set the device as UNprotected
        """
        self.database.clear_protected(self.name)

    def _forcast_find_temperature_range(self) -> TemperatureRange:
        """
        Ask the Yr API and return the temperature range of the weather forcast

        :return: Temperature range of the weather forcast
        """
        weather_forcast = self.weather.get_weather_forcast()
        temperature_list = list()

        for time_entry in weather_forcast['properties']['timeseries']:
            temperature_list.append(time_entry['data']['instant']['details']['air_temperature'])

        print(temperature_list)

        temperature_range = TemperatureRange(minimum=min(temperature_list),
                                             maximum=max(temperature_list))

        return temperature_range

    def _build_protect_envelopes(self, temperature_range: TemperatureRange) -> list[Envelope]:
        """
        Builds the envelopes to protect the device

        :return: List of Envelope containing the message to ask to protect the device.
        """

        subject = f"""Protect your {self.name}"""

        message = f"""
        Temperatures are getting out of operational range.

        -> Protect your device

        Temperature range [{temperature_range.minimum}, {temperature_range.maximum}]
        Device range: [{self.operating_range.minimum}, {self.operating_range.maximum}]

        Fridge-guardian
        Keeps an eye on your devices ;)"""

        envelopes = []

        for contact in self.email_list:
            envelope = self.email.build_envelope(subject=subject,
                                                 message=message,
                                                 dest_addr=contact,
                                                 dest_name="")
            envelopes.append(envelope)

        return envelopes

    def _build_unprotect_envelopes(self, temperature_range: TemperatureRange) -> list[Envelope]:
        """
        Builds the envelopes to unprotect the device

        :return: List of Envelope containing the message to ask to unprotect the device.
        """

        subject = f"""Your {self.name} don't need protection anymore"""

        message = f"""
        Temperatures are getting in the operational range.

        -> Your {self.name} don't need to be protected anymore

        Temperature range [{temperature_range.minimum}, {temperature_range.maximum}]
        Device range: [{self.operating_range.minimum}, {self.operating_range.maximum}]

        Fridge-guardian
        Keeps an eye on your devices ;)"""

        envelopes = []

        for contact in self.email_list:
            envelope = self.email.build_envelope(subject=subject,
                                                 message=message,
                                                 dest_addr=contact,
                                                 dest_name="")
            envelopes.append(envelope)

        return envelopes

    def _send_emails(self):
        pass

    def check_temperature(self):
        pass
