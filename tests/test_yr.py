import fridgeGuardian.yr

from fridgeGuardian.yr import Yr
from pytest import fixture
from mock import patch, Mock
from dateutil.parser import parse
from requests import Response
from tests.ressources import WEATHER_FORCAST, WEATHER_FORCAST_2

GREENWICH_LONGITUDE = -0.00143
GREENWICH_LATITUDE = 51.47782
YR_IDENTITY = "fridge-guardian github.com/iTom34/fridge-guardian"
HEADERS = {'Expires': 'Mon, 03 Jul 2023 07:30:00 GMT'}

@fixture
def greenwich_weather():
    greenwich_weather = Yr(GREENWICH_LONGITUDE, GREENWICH_LATITUDE, YR_IDENTITY)
    return greenwich_weather


def test_constructor(greenwich_weather):
    assert greenwich_weather.longitude == GREENWICH_LONGITUDE
    assert greenwich_weather.latitude == GREENWICH_LATITUDE
    assert greenwich_weather.identity == YR_IDENTITY


def test_build_url(greenwich_weather):
    assert greenwich_weather._build_url() == \
           f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=51.4778&lon=-0.0014"


@patch('fridgeGuardian.yr.datetime', name='mock_datetime')
def test_get_weather_forcast_first_request(mock_datetime, greenwich_weather):

    # Mocking
    mock_datetime.now.return_value = parse('Mon, 03 Jul 2023 07:00:00 GMT')
    response = Response()
    response.status_code = 200
    response.headers = HEADERS
    response.json = Mock(return_value=WEATHER_FORCAST)
    greenwich_weather._request = Mock(return_value=response)

    # Assertion
    assert greenwich_weather.get_weather_forcast() == WEATHER_FORCAST
    assert greenwich_weather.weather_forcast == WEATHER_FORCAST
    assert greenwich_weather.expire_raw == HEADERS['Expires']
    assert greenwich_weather.expire == parse(HEADERS['Expires'])
    greenwich_weather._request.assert_called_once()



@patch('fridgeGuardian.yr.datetime', name='mock_datetime')
def test_get_weather_forcast_expired_and_not_updated(mock_datetime, greenwich_weather):
    """
    Testing get_weather_forcast() the branch when the forcast stored in the Yr object has expired and the Yr model
    has NOT been updated
    """
    # Mocking
    mock_datetime.now.return_value = parse('Mon, 03 Jul 2023 07:31:00 GMT')
    greenwich_weather.weather_forcast = WEATHER_FORCAST
    greenwich_weather.expire = parse('Mon, 03 Jul 2023 07:30:00 GMT')
    greenwich_weather.expire_raw = 'Mon, 03 Jul 2023 07:30:00 GMT'
    response = Response()
    response.status_code = 304
    response.headers = {'Expires': 'Mon, 03 Jul 2023 08:00:00 GMT'}
    response.json = Mock(return_value={})
    greenwich_weather._request = Mock(return_value=response)

    assert greenwich_weather.get_weather_forcast() == WEATHER_FORCAST
    assert greenwich_weather.weather_forcast == WEATHER_FORCAST
    assert greenwich_weather.expire_raw == 'Mon, 03 Jul 2023 07:30:00 GMT'
    assert greenwich_weather.expire == parse('Mon, 03 Jul 2023 07:30:00 GMT')
    greenwich_weather._request.assert_called_once()


@patch('fridgeGuardian.yr.datetime', name='mock_datetime')
def test_get_weather_forcast_expired_and_updated(mock_datetime, greenwich_weather):
    """
    Testing get_weather_forcast() the branch when the forcast stored in the Yr object has expired and the Yr model
    has been updated
    """
    # Mocking
    mock_datetime.now.return_value = parse('Mon, 03 Jul 2023 07:31:00 GMT')
    greenwich_weather.weather_forcast = WEATHER_FORCAST
    greenwich_weather.expire = parse('Mon, 03 Jul 2023 07:30:00 GMT')
    greenwich_weather.expire_raw = 'Mon, 03 Jul 2023 07:30:00 GMT'
    response = Response()
    response.status_code = 200
    response.headers = {'Expires': 'Mon, 03 Jul 2023 08:00:00 GMT'}
    response.json = Mock(return_value=WEATHER_FORCAST_2)
    greenwich_weather._request = Mock(return_value=response)

    assert greenwich_weather.get_weather_forcast() == WEATHER_FORCAST_2
    assert greenwich_weather.weather_forcast == WEATHER_FORCAST_2
    assert greenwich_weather.expire_raw == 'Mon, 03 Jul 2023 08:00:00 GMT'
    assert greenwich_weather.expire == parse('Mon, 03 Jul 2023 08:00:00 GMT')
    greenwich_weather._request.assert_called_once()


@patch('fridgeGuardian.yr.datetime', name='mock_datetime')
def test_get_weather_forcast_not_expired(mock_datetime, greenwich_weather):
    """
    Testing get_weather_forcast() the branch when the forcast stored in the Yr object has expired and the Yr model
    has been updated
    """
    # Mocking
    mock_datetime.now.return_value = parse('Mon, 03 Jul 2023 07:29:00 GMT')
    greenwich_weather.weather_forcast = WEATHER_FORCAST
    greenwich_weather.expire = parse('Mon, 03 Jul 2023 07:30:00 GMT')
    greenwich_weather.expire_raw = 'Mon, 03 Jul 2023 07:30:00 GMT'
    greenwich_weather._request = Mock()

    assert greenwich_weather.get_weather_forcast() == WEATHER_FORCAST
    assert greenwich_weather.weather_forcast == WEATHER_FORCAST
    assert greenwich_weather.expire_raw == 'Mon, 03 Jul 2023 07:30:00 GMT'
    assert greenwich_weather.expire == parse('Mon, 03 Jul 2023 07:30:00 GMT')
    greenwich_weather._request.assert_not_called()


@patch('fridgeGuardian.yr.requests.get', name='mock_get')
def test_request(mock_get, greenwich_weather):
    url = "test_URL"

    # if_modified_since = False
    greenwich_weather._build_url = Mock(name='mock_build_url', return_value=url)
    mock_get.return_value = "mocked_response"

    assert greenwich_weather._request(if_modified_since=False) == "mocked_response"
    assert mock_get.assert_called_with(url, {'user-agent': greenwich_weather.identity})

