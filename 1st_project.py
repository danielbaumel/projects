{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMro+79q+O085+HgbNHQTSh",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/danielbaumel/projects/blob/main/1st_project.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 90,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "46G4dUj4lNtU",
        "outputId": "2d2dc28e-94f7-4afe-f4d9-fea16b324beb"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Hello, place a city name to recieve it's weather conditions, write fav to choose from a list of favorite locations or press enter for the default city's weather conditionsfav\n",
            "write add to add cities to your favorite cities list or press enter to show the list\n",
            "Your favorite locations are:\n",
            "['lima', 'los angeles', 'london', '']\n",
            "Which of your favorite cities would like to know the weather conditionslos angeles\n",
            "\n",
            "Press c for Celsius or f for Fahrenheit otherwise standard kelvin will be presented\n",
            "\n",
            "Your current date and time: Saturday, November 25, 2023, 04:18 PM\n",
            "Date and time in America/Los_Angeles: Saturday, November 25, 2023, 07:18 AM\n",
            "\n",
            "The weather conditions in Los Angeles are: \n",
            "Temperature : 285.08°K \n",
            "feels like  : 284.34°K \n",
            "Description : Clouds \n",
            "Humidity    : 77% \n",
            "Wind speed  : 2.06 \n",
            "Sun rise    : 2023-11-25 06:35:03 \n",
            "Sun set     : 2023-11-25 16:45:13 \n"
          ]
        }
      ],
      "source": [
        "import requests\n",
        "import json\n",
        "from datetime import datetime\n",
        "import pytz\n",
        "from timezonefinder import TimezoneFinder\n",
        "import geocoder\n",
        "from pathlib import Path\n",
        "\n",
        "def default_location():\n",
        "    #changing the default city\n",
        "    insert_default_location = input(f\"Which default city would you like to choose?\")\n",
        "    with open(\"default.json\", \"w\") as f:\n",
        "        json.dump(insert_default_location, f)\n",
        "\n",
        "def fav_locations():\n",
        "    #inserting several favorite places\n",
        "    favorite_locations_list = []\n",
        "    while True:\n",
        "        default_location = input('insert favorite weather locations')\n",
        "        favorite_locations_list.append(default_location)\n",
        "        if not default_location:\n",
        "            break\n",
        "    with open(\"fav.json\", \"a\") as f:\n",
        "        fav_write = json.dump(favorite_locations_list, f)\n",
        "    return fav_write\n",
        "\n",
        "def reading_fav_file():\n",
        "    #reading the fav locations json file\n",
        "    with open(\"fav.json\", \"r\") as f:\n",
        "        fav_read = json.load(f)\n",
        "    print(fav_read)\n",
        "\n",
        "def request_weather(city_name = default_location, units = \"standard\"):\n",
        "    # returning the weather conditions of specific place\n",
        "    weather = requests.get(\n",
        "        \"http://api.openweathermap.org/data/2.5/weather\",\n",
        "        params = {\"q\" : city_name, \"units\" : units, \"appid\" : \"b1746ddcb0f77f6278e62c3050e97269\"},\n",
        "    ).json()\n",
        "    return weather\n",
        "\n",
        "def current_geographical_coordinations():\n",
        "    #returning current location geographical coordinations\n",
        "    location = geocoder.ip('me')\n",
        "    return location.latlng\n",
        "\n",
        "def finding_timezone(lon, lat):\n",
        "    #returning timezone region using geographical coordination\n",
        "    obj = TimezoneFinder()\n",
        "    location_timezone = obj.timezone_at(lng=lon, lat=lat)\n",
        "    return location_timezone\n",
        "\n",
        "def display_date_time(user_timezone, location_timezone=None):\n",
        "    # Fetch current date and time in user's timezone\n",
        "    user_time = datetime.now(pytz.timezone(user_timezone))\n",
        "    formatted_user_time = user_time.strftime(\"%A, %B %d, %Y, %I:%M %p\")\n",
        "    print(f\"\\nYour current date and time: {formatted_user_time}\")\n",
        "\n",
        "    # Optional: Convert and display the date and time for the specified location\n",
        "    if location_timezone:\n",
        "        location_time = user_time.astimezone(pytz.timezone(location_timezone))\n",
        "        formatted_location_time = location_time.strftime(\"%A, %B %d, %Y, %I:%M %p\")\n",
        "        print(f\"Date and time in {location_timezone}: {formatted_location_time}\")\n",
        "\n",
        "\n",
        "\n",
        "welcome = input(\"Hello, place a city name to recieve it's weather conditions, write fav to choose from a list of favorite locations or press enter for the default city's weather conditions\")\n",
        "if welcome:\n",
        "    if welcome == \"fav\":\n",
        "        adding_fav_locations = input(\"write add to add cities to your favorite cities list or press enter to show the list\")\n",
        "        if adding_fav_locations:\n",
        "            fav_locations()\n",
        "            print(\"Your favorite locations are:\")\n",
        "            reading_fav_file()\n",
        "            city_name = input(\"Which of your favorite cities would like to know the weather conditions\")\n",
        "        else:\n",
        "          print(\"Your favorite locations are:\")\n",
        "          reading_fav_file()\n",
        "          city_name = input(\"Which of your favorite cities would like to know the weather conditions\")\n",
        "    else:\n",
        "        city_name = welcome\n",
        "else:\n",
        "    changing_default_location = input(f\"insert yes if you would like to change the default city or enter for it's weather conditions\")\n",
        "    if changing_default_location:\n",
        "        default_location()\n",
        "        with open(\"default.json\", \"r\") as f:\n",
        "            city_name =  json.load(f)\n",
        "    else:\n",
        "        with open(\"default.json\", \"r\") as f:\n",
        "            city_name =  json.load(f)\n",
        "\n",
        "temp_units = input(\"\\nPress c for Celsius or f for Fahrenheit otherwise standard kelvin will be presented\")\n",
        "if temp_units == \"c\":\n",
        "    temp_u = \"°C\"\n",
        "    units = \"metric\"\n",
        "elif temp_units == \"f\":\n",
        "    temp_u = \"°F\"\n",
        "    units = \"imperial\"\n",
        "else:\n",
        "    temp_u = \"°K\"\n",
        "    units = \"standard\"\n",
        "weather_condotion = request_weather(city_name, units)\n",
        "\n",
        "\n",
        "\n",
        "temperature = weather_condotion[\"main\"][\"temp\"]\n",
        "feels_like = weather_condotion[\"main\"][\"feels_like\"]\n",
        "weather_parameters = weather_condotion[\"weather\"][0][\"main\"]\n",
        "humidity = weather_condotion[\"main\"][\"humidity\"]\n",
        "wind_speed = weather_condotion[\"wind\"][\"speed\"]\n",
        "sun_rise = datetime.utcfromtimestamp(weather_condotion[\"sys\"][\"sunrise\"] + weather_condotion[\"timezone\"])\n",
        "sun_set = datetime.utcfromtimestamp(weather_condotion[\"sys\"][\"sunset\"] + weather_condotion[\"timezone\"])\n",
        "city_lon = weather_condotion[\"coord\"][\"lon\"]\n",
        "city_lat = weather_condotion[\"coord\"][\"lat\"]\n",
        "place_name = weather_condotion[\"name\"]\n",
        "\n",
        "\n",
        "current_lat_lon = current_geographical_coordinations()\n",
        "current_lat = current_lat_lon[0]\n",
        "current_lon = current_lat_lon[1]\n",
        "\n",
        "\n",
        "current_timezone_region = finding_timezone(current_lon, current_lat)\n",
        "city_timezone_region = finding_timezone(city_lon, city_lat)\n",
        "\n",
        "\n",
        "display_date_time(current_timezone_region, city_timezone_region)\n",
        "\n",
        "\n",
        "print(f\"\\nThe weather conditions in {place_name} are: \")\n",
        "print(f\"Temperature : {temperature}{temp_u} \")\n",
        "print(f\"feels like  : {feels_like}{temp_u} \")\n",
        "print(f\"Description : {weather_parameters} \")\n",
        "print(f\"Humidity    : {humidity}% \")\n",
        "print(f\"Wind speed  : {wind_speed} \")\n",
        "print(f\"Sun rise    : {sun_rise} \")\n",
        "print(f\"Sun set     : {sun_set} \")"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "Mf1HkyggrYRn"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}