import pytz

from fridgeGuardian.device import Device
from fridgeGuardian.email import Email
from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.app_settings import YR_IDENTITY
from fridgeGuardian.temperature import TemperatureRange


class ConfigurationParser():
    """
    Class in charge to build a list of devices from the configuration provided
    """

    def __init__(self,
                 configuration: dict):
        """
        Constructor of the configuration parser

        :param configuration: Dictionary containing the configuration to parse
        """
        self.configuration: dict = configuration
        self.time_zone: pytz.timezone = pytz.timezone(self.configuration["time_zone"])
        self.email: Email | None = None
        self.database: Database | None = None

    def build_email(self) -> Email:
        """
        Based on the email confiburation it build the Email object

        :return: Email object
        """
        email = Email(smtp_address=self.configuration["email"]["smtp_address"],
                      smtp_port=self.configuration["email"]["smtp_port"],
                      login=self.configuration["email"]["login"],
                      password=self.configuration["email"]["password"],
                      tls=self.configuration["email"]["tls"],
                      from_email=self.configuration["email"]["from_email"],
                      from_name=self.configuration["email"]["from_name"])
        return email

    def build_database(self) -> Database:
        """
        Based on the database configuration it builds the Database object

        :return: A database interface
        """
        database = Database(host=self.configuration["host"],
                            user=self.configuration["user"],
                            password=self.configuration["password"],
                            database=self.configuration["database"])
        return database

    def build_yr(self, device_config: dict) -> Yr:
        """
        Builds the Yr configuration for a device
        
        :param device_config: Configuration of the device
        :return: Yr interface for the specified device
        """
        yr = Yr(longitude=device_config["longitude"],
                latitude=device_config["latitude"],
                identity=YR_IDENTITY,
                time_zone=self.time_zone)

        return yr

    def build_device(self, device_config) -> Device:
        """
        Builds a Device object

        :param device_config: Configuration of a device.
        :return: Device object
        """
        operating_range = TemperatureRange(minimum=device_config["temperature_min"],
                                           maximum=device_config["temperature_max"])
        weather = self.build_yr(device_config)

        device = Device(name=device_config["name"],
                        weather=weather,
                        email=self.email,
                        email_list=device_config["email_list"],
                        database=self.database,
                        operating_range=operating_range)

        return device
