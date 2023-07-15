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
        self.email_list: list[str]
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

    def _build_envelopes(self) -> list[Envelope]:
        pass

    def _send_emails(self):
        pass

    def check_temperature(self):
        pass
