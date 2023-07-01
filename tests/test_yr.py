from fridgeGuardian.yr import Yr
from pytest import fixture

GREENWICH_LONGITUDE = -0.00143
GREENWICH_LATITUDE = 51.47782
YR_IDENTITY = "fridge-guardian github.com/iTom34/fridge-guardian"

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

def test_request(greenwich_weather):
    assert greenwich_weather._request() == []

