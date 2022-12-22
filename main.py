from pprint import pprint
from typing import Union, Dict, Type, Any
import datetime

import requests
from urllib.request import urlopen
import json

from config import open_weather_token


def get_ip_data() -> dict:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)


def get_coordinates() -> Dict[str, str]:
    """Returns current coordinates using IP address"""
    data = get_ip_data()
    coordinate = dict()
    coordinate["latitude"] = data['loc'].split(',')[0]
    coordinate["longitude"] = data['loc'].split(',')[1]
    return coordinate


def parse_data_from_request(data: Dict[str, Dict[str, Union[float, str]]]) -> None:
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, не пойму что там за погода!"
    city = data['name']
    cur_weather = data['main']['temp']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])

    print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
          f"Погода в населиному пункті: {city}\nТемпература: {cur_weather}C° {wd}\n"
          f"Вологість: {humidity}%\nВітер: {wind} м/с\n"
          f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
          f"Гарного дня!"
          )


def get_weather(city: str, open_weather_token: str) -> None:
    try:
        location = get_coordinates()
        r = requests.get(
            #f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            f"https://api.openweathermap.org/data/2.5/weather?lat={location['latitude']}&lon={location['longitude']}"
            f"&appid={open_weather_token}"
        )

        data = r.json()
        parse_data_from_request(data)
    except Exception as ex:
        print(ex)
        print("Wrong town!")


def main():
    city = input("Input your city(or vilage) ")

    get_weather(city, open_weather_token)


if __name__ == "__main__":
    main()

