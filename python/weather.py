#!/usr/bin/python
import argparse
import os
import sys
from typing import Tuple

import requests


API_KEY = os.getenv('OW_API')

class Weather:

  def __init__(self, args) -> None:
      self.args = args
      self.api_key = API_KEY
      self.session = self._session()

      # Retrieve latitute and longitude
      latitude, longitude = self._get_coord()
      self.latitude = latitude
      self.longitude = longitude

      units = self._get_units()
      self.units = units

  def _session(self) -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

  def _get(self, url: str) -> requests.Response:
        response = self.session.get(url)
        response.raise_for_status()
        return response

  def _get_coord(self) -> Tuple[str,str]:
      latitude = ""
      longitude = ""
      coordinates_url= f"http://api.openweathermap.org/geo/1.0/zip?zip={self.args.zip},{self.args.country}&appid={self.api_key}"
      print(coordinates_url) 
      response = self._get(coordinates_url)
      coordinates = response.json()

      latitude = coordinates['lat']
      longitude = coordinates['lon']
      return latitude, longitude

  def _get_units(self):
      units = "standard"
      return units

  def get_weather_details(self) -> str:
      weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units={self.args.units}&appid={self.api_key}"
      response = self._get(weather_url)

      weather_details = ""
      weather_deets = response.json()
      my_dict = {"Temperature": weather_deets['main']['temp'], "Temperature Min": weather_deets['main']['temp_min'],
                 "Temperature Max": weather_deets['main']['temp_max'], "Wind Speed": weather_deets['wind']['speed']}

      for key, value in my_dict.items():
          weather_details += key + ": " + str(value) + "\n"

      my_array = weather_deets['weather']

      for element in my_array:
          weather_details += "Description: " + element['description'] + "\n"

      return weather_details

  def get_daily_weather(self):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units={self.args.units}&appid={self.api_key}"
    self._get(weather_url)


if __name__ == "__main__":

  if not API_KEY:
    print("API key does not exist for open weather")
    sys.exit(1)

  parser = argparse.ArgumentParser(description= 'Generates current weather data')
  parser.add_argument('--zip', type=str, help="enter zipcode for weather data", required=True)
  parser.add_argument('--country', '-c', type=str, default='US', help="enter country abbreviation")
  parser.add_argument('--units', '-u', type=str, help="enter a measurement standard: standard, metric or imperial")
  args = parser.parse_args()

  weather = Weather(args)
  weather.get_daily_weather()
  print (weather.get_weather_details())
