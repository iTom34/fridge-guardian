import pytz

from fridgeGuardian.device import Device
from fridgeGuardian.email import Email
from fridgeGuardian.yr import Yr
from fridgeGuardian.database import Database
from fridgeGuardian.app_settings import YR_IDENTITY


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
        self.configuartion: dict = configuration
        self.time_zone: pytz.timezone = pytz.timezone(self.configuration["time_zone"])
        self.email: Email = build_email()
        self.database: Database = build_database()

    def build_email(self) -> Email:
        """
        Based on the email confiburation it build the Email object

        :return: Email object
        """
        email = Email(smtp_address=self.config["email"]["smtp_address"],
                      smtp_port=self.config["email"]["smtp_port"],
                      login=self.config["email"]["login"],
                      password=self.config["email"]["password"],
                      tls=self.config["email"]["tls"],
                      from_email=self.config["email"]["from_email"],
                      from_name=self.config["email"]["from_name"])
        return email

    def build_database(self) -> Database:
        """
        Based on the database configuration it build the Database object
        :return:
        """
        database = Database(host=config["host"],
                            user=config["user"],
                            password=config["password"],
                            database=config["database"])
        return database

    def build_yr(self) -> Yr:
        yr = Yr(longitude=config["longitude"],
                latitude=config["latitude"],
                identity=YR_IDENTITY,
                time_zone=self.time_zone)

        return yr

    def build_device(self, device_config) -> Device:
        """
        Builds a Device object

        :param device_config: Configuration of an device
        :return: Device object
        """
        operating_range = TemperatureRange(minimum=device_config["temperature_min"],
                                           maximum=device_config["temperature_max"])
        weather = build_yr(config)

        device = Device(name=device_config["name"],
                        weather=weather,
                        email=self.email,
                        email_list=device_config["email_list"],
                        database=self.database,
                        operating_range=operating_range)

        return device
