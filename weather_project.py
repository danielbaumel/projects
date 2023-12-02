import requests
import json
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import geocoder
from pathlib import Path


def default_location():
    # changing the default city
    insert_default_location = input(f"Which default city would you like to choose?")
    with open(p / "default.json", "w") as default_file:
        json.dump(insert_default_location, default_file)


def fav_locations():
    # inserting several favorite places
    favorite_locations_list = []
    while True:
        favorite_location = input('insert favorite weather locations')
        favorite_locations_list.append(favorite_location)
        if not favorite_location:
            break
    with open(p / "fav.json", "a") as fav_file:
        json.dump(favorite_locations_list, fav_file, indent=4)


def reading_fav_file():
    # reading the fav locations json file
    with open(p / "fav.json", "r") as fav_r:
        fav_read = json.load(fav_r)
    print(fav_read)


def request_weather(location=default_location):
    # returning the weather conditions of specific place
    weather = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={"q": city_name, "units": units, "appid": "b1746ddcb0f77f6278e62c3050e97269"},
    ).json()
    return weather


def current_geographical_coordination():
    # returning current location geographical coordination
    location = geocoder.ip('me')
    return location.latlng


def finding_timezone(lon, lat):
    # returning timezone region using geographical coordination
    obj = TimezoneFinder()
    location_timezone = obj.timezone_at(lng=lon, lat=lat)
    return location_timezone


def display_date_time(user_timezone, location_timezone=None):
    # Fetch current date and time in user's timezone
    user_time = datetime.now(pytz.timezone(user_timezone))
    formatted_user_time = user_time.strftime("%A, %B %d, %Y, %I:%M %p")
    print(f"\nYour current date and time: {formatted_user_time}")

    # Optional: Convert and display the date and time for the specified location
    if location_timezone:
        location_time = user_time.astimezone(pytz.timezone(location_timezone))
        formatted_location_time = location_time.strftime("%A, %B %d, %Y, %I:%M %p")
        print(f"Date and time in {location_timezone}: {formatted_location_time}")


p = Path("c:/users/user")

default_path = p / "default.json"
if not default_path.exists():
    with open(default_path, "w") as f:
        json.dump("tel aviv", f)

fav_path = p / "fav.json"
if not fav_path.exists():
    with open(fav_path, "w") as f:
        json.dump("tel aviv", f)

welcome = input("Hello, place a city name to receive it's weather conditions, write fav to choose from a list of "
                "favorite locations or press enter for the default city's weather conditions")
if welcome:
    if welcome == "fav":
        adding_fav_locations = input("write add to add cities to your favorite cities list or press enter to show the "
                                     "list")
        if adding_fav_locations:
            fav_locations()
            print("Your favorite locations are:")
            reading_fav_file()
            city_name = input("Which of your favorite cities would like to know the weather conditions")
        else:
            print("Your favorite locations are:")
            reading_fav_file()
            city_name = input("Which of your favorite cities would like to know the weather conditions")
    else:
        city_name = welcome
else:
    changing_default_location = input(f"insert yes if you would like to change the default city or enter for it's "
                                      f"weather conditions")
    if changing_default_location:
        default_location()
        with open(p / "default.json", "r") as f:
            city_name = json.load(f)
    else:
        with open(p / "default.json", "r") as f:
            city_name = json.load(f)

temp_units = input("\nPress c for Celsius or f for Fahrenheit otherwise standard kelvin will be presented")
if temp_units == "c":
    temp_u = "°C"
    units = "metric"
elif temp_units == "f":
    temp_u = "°F"
    units = "imperial"
else:
    temp_u = "°K"
    units = "standard"
weather_condition = request_weather(city_name)

temperature = weather_condition["main"]["temp"]
feels_like = weather_condition["main"]["feels_like"]
weather_parameters = weather_condition["weather"][0]["main"]
humidity = weather_condition["main"]["humidity"]
wind_speed = weather_condition["wind"]["speed"]
sun_rise = datetime.utcfromtimestamp(weather_condition["sys"]["sunrise"] + weather_condition["timezone"])
sun_set = datetime.utcfromtimestamp(weather_condition["sys"]["sunset"] + weather_condition["timezone"])
city_lon = weather_condition["coord"]["lon"]
city_lat = weather_condition["coord"]["lat"]
place_name = weather_condition["name"]

current_lat_lon = current_geographical_coordination()
current_lat = current_lat_lon[1]
current_lon = current_lat_lon[0]

current_timezone_region = finding_timezone(current_lon, current_lat)
city_timezone_region = finding_timezone(city_lon, city_lat)

display_date_time(current_timezone_region, city_timezone_region)

print(f"\nThe weather conditions in {place_name} are: ")
print(f"Temperature : {temperature}{temp_u} ")
print(f"feels like  : {feels_like}{temp_u} ")
print(f"Description : {weather_parameters} ")
print(f"Humidity    : {humidity}% ")
print(f"Wind speed  : {wind_speed} ")
print(f"Sun rise    : {sun_rise} ")
print(f"Sun set     : {sun_set} ")
