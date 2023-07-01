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
                 identity: str):
        """
        Constructor for the Yr API

        :param longitude: Longitude position (degrees)
        :param latitude: Latitude position (degrees)
        :param identity: Identity used on the Yr API
        """
        self.longitude: float = longitude       # Longitude coordinate of the position
        self.latitude: float = latitude         # Latitude coordinate of the position
        self.identity: str = identity           # Identity used on the Yr API
        self.weather_forcast: dict = dict()     # Last weather forcast
        self.expire: datetime = datetime.now()  # Expiration date of the last report
        self.expire_raw: str = ""               # Expiration date from the header response

    def _build_url(self) -> str:
        """
        Generates the URL for the request

        :return: The URL to make the API request
        """
        return f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={self.latitude:.4f}&lon={self.longitude:.4f}"

    def _request(self):
        """
        Sends a request to the Yr API and returns the result

        :return:
        """

        console = Console()
        url = self._build_url()


        # First request
        if self.weather_forcast == dict():
            headers = {'user-agent': self.identity}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise YrRequestFailed

            self.expire_raw = response.headers['Expires']
            self.expire = parse(response.headers['Expires'])
            self.now = datetime.now(tz=pytz.timezone("Europe/Oslo"))

            self.weather_forcast = response.json()
            return self.weather_forcast

        # Weather forcast expired
        elif self.expire < datetime.now():
            headers = {'user-agent': self.identity,
                       'If-Modified-Since': self.expire_raw}
            response = requests.get(url, headers=headers)

            # Model not updated
            if response.status_code == 304:
                console.log(":info: Model not updated")
                return self.weather_forcast

            elif

        # Weather forcast didn't expire
        else:
            return




        if response.status_code == 200:
            self.expire = parse(response.headers['Expires'])
            self.now = datetime.now(tz=pytz.timezone("Europe/Oslo"))

            if self.expire < self.now:
                print("It expired")

            else:
                print("It didn't expire")

            delta = self.expire - self.now
            print(response.headers)
            #console.print_json(data=result.json())
            console.print(f"{datetime.hour}:{datetime.minute}:{datetime.second}")
            self.weather_forcast = response.json()
            return response.json()

        else:
            console.log(f":warning: Yr API replied {response.status_code}")
    