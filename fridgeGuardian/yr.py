import pytz
import requests
from datetime import datetime
from rich.console import Console
from dateutil.parser import parse


class YrRequestFailed(Exception):
    pass


class Yr:
    """
    Yr API to get weather report
    """
    def __init__(self,
                 longitude:float,
                 latitude: float,
                 identity: str,
                 time_zone: str = "Europe/Oslo"):
        """
        Constructor for the Yr API

        :param longitude: Longitude position (degrees)
        :param latitude: Latitude position (degrees)
        :param identity: Identity used on the Yr API
        :param time_zone: Time zone of the computer clock (Ex: "Europe/Oslo")
        """
        self.longitude: float = longitude           # Longitude coordinate of the position
        self.latitude: float = latitude             # Latitude coordinate of the position
        self.identity: str = identity               # Identity used on the Yr API
        self.weather_forcast: dict = dict()         # Last weather forcast
        self.expire: datetime = datetime.now()      # Expiration date of the last report
        self.expire_raw: str = ""                   # Expiration date from the header response
        self._time_zone = pytz.timezone(time_zone)  # Time zone

    def _build_url(self) -> str:
        """
        Generates the URL for the request

        :return: The URL to make the API request
        """
        return f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={self.latitude:.4f}&lon={self.longitude:.4f}"

    def get_weather_forcast(self):
        """
        Sends a request to the Yr API and returns the result

        :return:
        """

        console = Console()
        date_now = datetime.now(tz=self._time_zone)

        # First request
        if self.weather_forcast == dict():
            response = self._request(if_modified_since=False)

            if response.status_code != 200:
                raise YrRequestFailed(f":warning: Yr API replied {response.status_code}")

            self.expire_raw = response.headers['Expires']
            self.expire = parse(response.headers['Expires'])
            self.weather_forcast = response.json()

            console.log(":info: First weather forcast received")
            return self.weather_forcast

        # Weather forcast expired
        elif self.expire < date_now:
            response = self._request(if_modified_since=True)

            # Model not updated
            if response.status_code == 304:
                console.log(":info: Model not updated")
                return self.weather_forcast

            elif response.status_code == 200:
                self.expire_raw = response.headers['Expires']
                self.expire = parse(response.headers['Expires'])
                self.weather_forcast = response.json()

                console.log(":info: Model updated")
                return self.weather_forcast

            else:
                console.log(f":warning: Yr API replied {response.status_code}")
                raise YrRequestFailed(f":warning: Yr API replied {response.status_code}")

        # Weather forcast didn't expire
        else:
            expires_in = (self.expire - date_now).seconds
            console.log(f":info: Weather forcast didn't expire (expires in {expires_in} s)")
            return self.weather_forcast

    def _request(self, if_modified_since: bool) -> requests.Response:
        """
        Sends a request to the API

        :param if_modified_since: Adds the header to ask if the weather model have been updated since the last request
        :return: The response of the API
        """

        url = self._build_url()
        headers = {'user-agent': self.identity}

        if if_modified_since:
            headers.update({'If-Modified-Since': self.expire_raw})

        return requests.get(url, headers=headers)
