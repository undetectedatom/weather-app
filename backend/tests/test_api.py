from __future__ import annotations

from itertools import count
from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database.engine import get_session
from app.main import app
from app.schemas.location import LocationResult
from app.schemas.weather import CurrentWeather, ForecastDay, RangeSummary, WeatherResponse
from app.services.location_service import location_service
from app.services.weather_service import weather_service

DB_PATH = Path('/tmp/weather-app-test.db')
if DB_PATH.exists():
    DB_PATH.unlink()
engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)
email_counter = count(1)


async def fake_search(query: str):
    return [LocationResult(name=query, region='CA', country='USA', latitude=37.7749, longitude=-122.4194, display_label=f'{query}, CA, USA')]


async def fake_resolve(query: str):
    return (await fake_search(query))[0]


async def fake_reverse(lat: float, lon: float):
    return LocationResult(name='Current Location', region='CA', country='USA', latitude=lat, longitude=lon, display_label='Current Location, CA, USA')


async def fake_reverse_name(lat: float, lon: float):
    return LocationResult(name='Fremont', region='California', country='USA', latitude=lat, longitude=lon, display_label='Fremont, California, USA')


async def fake_current_weather(query: str):
    location = await fake_resolve(query)
    return WeatherResponse(location=location, current=CurrentWeather(temperature_c=21.5, feels_like_c=21.0, condition='Clear sky', humidity=61, wind_speed=10, temp_max_c=24, temp_min_c=16, icon_code='clear'))


async def fake_current_by_coordinates(lat: float, lon: float, resolved_location=None):
    location = resolved_location or await fake_reverse(lat, lon)
    return WeatherResponse(location=location, current=CurrentWeather(temperature_c=19.0, feels_like_c=18.5, condition='Partly cloudy', humidity=55, wind_speed=8, temp_max_c=22, temp_min_c=14, icon_code='partly-cloudy'))


async def fake_forecast(query: str, days: int):
    location = await fake_resolve(query)
    forecast = [ForecastDay(date=f'2026-07-0{i+1}', temp_max_c=25 + i, temp_min_c=16 + i, condition='Clear sky', icon_code='clear') for i in range(days)]
    return WeatherResponse(location=location, forecast_days=forecast)


async def fake_range(query: str, start_date: str, end_date: str):
    location = await fake_resolve(query)
    forecast = [ForecastDay(date=start_date, temp_max_c=25, temp_min_c=16, condition='Clear sky', icon_code='clear')]
    return WeatherResponse(location=location, forecast_days=forecast, range_summary=RangeSummary(start_date=start_date, end_date=end_date, average_temp_c=20.5, max_temp_c=25, min_temp_c=16))


location_service.search = fake_search
location_service.resolve = fake_resolve
location_service.reverse = fake_reverse
location_service.reverse_name = fake_reverse_name
weather_service.get_current_weather = fake_current_weather
weather_service.get_current_weather_by_coordinates = fake_current_by_coordinates
weather_service.get_forecast = fake_forecast
weather_service.get_range_weather = fake_range


def register_and_authenticate():
    email = f'user{next(email_counter)}@example.com'
    response = client.post('/api/auth/register', json={'email': email, 'password': 'secret123'})
    assert response.status_code == 201
    return response.cookies, email


def test_auth_flow_and_me():
    cookies, email = register_and_authenticate()
    response = client.get('/api/auth/me', cookies=cookies)
    assert response.status_code == 200
    assert response.json()['user']['email'] == email


def test_current_weather_by_location():
    response = client.get('/api/weather/current', params={'location': 'San Francisco'})
    assert response.status_code == 200
    assert response.json()['location']['name'] == 'San Francisco'


def test_current_weather_by_coordinates():
    response = client.get('/api/weather/current-location', params={'lat': 37.77, 'lon': -122.41})
    assert response.status_code == 200
    assert response.json()['location']['latitude'] == 37.77
    assert response.json()['current']['temp_max_c'] == 22


def test_reverse_location_name():
    response = client.get('/api/locations/reverse', params={'lat': 37.55, 'lon': -121.98})
    assert response.status_code == 200
    assert response.json()['display_label'] == 'Fremont, California, USA'


def test_forecast_endpoint():
    response = client.get('/api/weather/forecast', params={'location': 'San Francisco', 'days': 5})
    assert response.status_code == 200
    assert len(response.json()['forecast_days']) == 5


def test_location_ranking_prefers_country_context():
    results = [
        LocationResult(name='Georgetown', region='Demerara-Mahaica', country='Guyana', country_code='GY', latitude=6.8013, longitude=-58.1551, display_label='Georgetown, Demerara-Mahaica, Guyana'),
        LocationResult(name='Georgetown', region='South Carolina', country='United States', country_code='US', latitude=33.3768, longitude=-79.2945, display_label='Georgetown, South Carolina, United States'),
    ]

    ranked = location_service._rank_results('Georgetown, South Carolina, United States', results)

    assert ranked[0].country == 'United States'
    assert ranked[0].region == 'South Carolina'


def test_history_crud_and_export():
    cookies, _ = register_and_authenticate()
    create_response = client.post('/api/weather/history', json={'location': 'San Francisco', 'start_date': '2026-06-01', 'end_date': '2026-06-03'}, cookies=cookies)
    assert create_response.status_code == 201
    record_id = create_response.json()['id']

    list_response = client.get('/api/weather/history', cookies=cookies)
    assert list_response.status_code == 200
    assert len(list_response.json()['records']) >= 1

    update_response = client.patch(f'/api/weather/history/{record_id}', json={'status': 'Active', 'notes': 'Refreshed'}, cookies=cookies)
    assert update_response.status_code == 200
    assert update_response.json()['status'] == 'Active'

    export_response = client.get('/api/weather/export', params={'format': 'csv'}, cookies=cookies)
    assert export_response.status_code == 200
    assert export_response.headers['content-type'].startswith('text/csv')
    assert 'range_average_temp_c' in export_response.text
    assert 'forecast_days_json' in export_response.text
    assert 'Clear sky' in export_response.text

    json_export_response = client.get('/api/weather/export', params={'format': 'json'}, cookies=cookies)
    assert json_export_response.status_code == 200
    exported_records = json_export_response.json()
    assert exported_records[0]['range_average_temp_c'] == 20.5
    assert exported_records[0]['forecast_days'][0]['condition'] == 'Clear sky'

    delete_response = client.delete(f'/api/weather/history/{record_id}', cookies=cookies)
    assert delete_response.status_code == 200


def test_recent_locations_endpoint():
    response = client.get('/api/locations/recent')
    assert response.status_code == 200
