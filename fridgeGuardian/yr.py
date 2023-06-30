from datetime import datetime


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
        self.last_report: dict = dict()         # Last report
        self.expire: datetime = datetime.now()  # Expiration date of the last report

    def _build_url(self) -> str:
        """
        Generates the URL for the request

        :return: The URL to make the API request
        """
        return f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={self.latitude:.4f}&lon={self.longitude:.4f}"

    def _request_yr(self):
        """
        Sends a request to the Yr API and returns the result

        :return:
        """

    