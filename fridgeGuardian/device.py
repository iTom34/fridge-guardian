from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.email import Email
from fridgeGuardian.temperature import TemperatureRange
from rich.console import Console

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

    def _get_temperature_range(self) -> TemperatureRange:
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

    def _send_protect_envelopes(self, temperature_range: TemperatureRange):
        """
        Builds the envelopes to protect the device

        :return: List of Envelope containing the message to ask to protect the device.
        """
        console = Console()

        subject = f"""Protect your {self.name}"""

        message = f"""
        Temperatures are getting out of operational range.

        -> Protect your device

        Temperature range [{temperature_range.minimum}, {temperature_range.maximum}]
        Device range: [{self.operating_range.minimum}, {self.operating_range.maximum}]

        Fridge-guardian
        Keeps an eye on your devices ;)"""

        envelopes = []

        # Building the envelopes
        for contact in self.email_list:
            envelope = self.email.build_envelope(subject=subject,
                                                 message=message,
                                                 dest_addr=contact,
                                                 dest_name="")
            envelopes.append(envelope)

        # Sending the envelopes
        for envelope in envelopes:
            console.print(f":incoming_envelope: Sending protect your {self.name} to {envelope.to_addr}")
            self.email.send(envelope)

        return envelopes

    def _send_unprotect_envelopes(self, temperature_range: TemperatureRange):
        """
        Builds the envelopes to unprotect the device

        :return: List of Envelope containing the message to ask to unprotect the device.
        """

        console = Console()

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

        # Sending the envelopes
        for envelope in envelopes:
            self.email.send(envelope)
            console.print(f":incoming_envelope: Sending unprotect your {self.name} to {envelope.to_addr}")

        return envelopes

    def check_temperature(self):
        """
        Method that check the temperature, depending on the state of the device (protected / unprotected) it will send
        an email notification.
        """
        console = Console()

        # Check the weather forcast:
        console.print(f"Device: {self.name}")
        console.print(":satellite_antenna: Checking weather forcast")
        temperature_range = self._get_temperature_range()
        console.print(f":thermometer: Temperature range: [{temperature_range.minimum}, {temperature_range.maximum}]")

        # Check device state:
        console.print(":point_right: Checking device state")
        protected = self._get_protected()

        # Checking the device need to be unprotected
        if protected:
            console.print("Device is [green bold] protected")

            # Check if we don't need to protect the device anymore
            if self.operating_range.minimum < temperature_range.minimum < self.operating_range.maximum and \
                    self.operating_range.minimum < temperature_range.maximum < self.operating_range.maximum:
                self._send_unprotect_envelopes(temperature_range)
                self.database.clear_protected()

        # Checking if the device need to be protected
        else:
            console.print("Device is [red bold] unprotected")

            if not (self.operating_range.minimum < temperature_range.minimum < self.operating_range.maximum and \
                    self.operating_range.minimum < temperature_range.maximum < self.operating_range.maximum):
                self._send_protect_envelopes(temperature_range)
                self.database.set_protected()
        pass
