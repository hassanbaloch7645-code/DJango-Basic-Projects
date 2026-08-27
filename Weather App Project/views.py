import requests
from django.conf import settings
from django.shortcuts import render

DEFAULT_CITY = 'Lahore'
REQUEST_TIMEOUT = 10

WMO_DESCRIPTIONS = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    71: 'Slight snow',
    73: 'Moderate snow',
    75: 'Heavy snow',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail',
}

WMO_ICON_CODES = {
    0: '01d',
    1: '02d',
    2: '03d',
    3: '04d',
    45: '50d',
    48: '50d',
    51: '09d',
    53: '09d',
    55: '09d',
    61: '10d',
    63: '10d',
    65: '10d',
    71: '13d',
    73: '13d',
    75: '13d',
    80: '09d',
    81: '09d',
    82: '09d',
    95: '11d',
    96: '11d',
    99: '11d',
}


def fetch_openweather(city):
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        return None, None

    api_url = (
        'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&units=metric&appid={api_key}'
    )
    response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
    data = response.json()

    if response.status_code == 200:
        return {
            'city': data['name'],
            'country': data['sys'].get('country', ''),
            'temperature': round(data['main']['temp']),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_unit': 'm/s',
            'provider': 'OpenWeatherMap',
        }, None

    if response.status_code == 404:
        return None, f'City "{city}" not found. Please check the spelling and try again.'

    return None, data.get('message', 'Unable to fetch weather data from OpenWeatherMap.')


def fetch_open_meteo(city):
    geo_url = 'https://geocoding-api.open-meteo.com/v1/search'
    geo_response = requests.get(
        geo_url,
        params={'name': city, 'count': 1, 'language': 'en', 'format': 'json'},
        timeout=REQUEST_TIMEOUT,
    )
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    results = geo_data.get('results') or []
    if not results:
        return None, f'City "{city}" not found. Please check the spelling and try again.'

    location = results[0]
    weather_url = 'https://api.open-meteo.com/v1/forecast'
    weather_response = requests.get(
        weather_url,
        params={
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
        },
        timeout=REQUEST_TIMEOUT,
    )
    weather_response.raise_for_status()
    weather_data = weather_response.json()['current']

    weather_code = weather_data['weather_code']
    description = WMO_DESCRIPTIONS.get(weather_code, 'Unknown')

    return {
        'city': location['name'],
        'country': location.get('country_code', ''),
        'temperature': round(weather_data['temperature_2m']),
        'description': description,
        'icon': WMO_ICON_CODES.get(weather_code, '01d'),
        'humidity': weather_data['relative_humidity_2m'],
        'wind_speed': round(weather_data['wind_speed_10m'], 1),
        'wind_unit': 'km/h',
        'provider': 'Open-Meteo',
    }, None


def get_weather(city):
    try:
        if settings.OPENWEATHER_API_KEY:
            weather_data, error = fetch_openweather(city)
            if weather_data:
                return weather_data, None
            if error and 'not found' in error.lower():
                return None, error

        weather_data, error = fetch_open_meteo(city)
        if weather_data:
            return weather_data, None
        return None, error or 'Unable to fetch weather data. Please try again.'

    except requests.Timeout:
        return None, 'The weather service took too long to respond. Please try again.'
    except requests.RequestException:
        return None, 'Network error. Please check your connection and try again.'
    except (KeyError, TypeError, ValueError):
        return None, 'Received an invalid response from the weather service.'


def weather_view(request):
    city = request.GET.get('city', '').strip() or DEFAULT_CITY
    weather_data, error = get_weather(city)

    return render(request, 'weather.html', {
        'weather': weather_data,
        'error': error,
        'city': city,
        'default_city': DEFAULT_CITY,
    })
