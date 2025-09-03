#! python
# -*- coding: utf-8 -*-

"""Парсим сайт gismeteo.ru на предмет получения основных данных о погоде:
 - текущая дата с сайта;
 - температура в градусах;
 - давление в мм.рт.ст.;
 - относительная влажность в %.

Настройки работы скрипта хранятся в переменных окружения.
"""

import requests
import os
from bs4 import BeautifulSoup
from typing import Dict, Optional

# Импорт переменных окружения
from dotenv import load_dotenv

load_dotenv(verbose=True)

# Адрес страницы с погодой берем из переменной окружения
GISMETEO_URL = os.getenv("GISMETEO_URL")

# Конфигурационные константы
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_weather_data() -> Optional[Dict[str, str]]:
    """Получает и парсит данные о погоде с Gismeteo."""
    try:
        response = requests.get(GISMETEO_URL, headers=HEADERS)
        response.raise_for_status()
        return parse_weather_data(response.text)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def parse_weather_data(html_content: str) -> Dict[str, str]:
    """Парсит HTML-контент и извлекает данные о погоде."""
    soup = BeautifulSoup(html_content, "html.parser")
    weather_widget = get_weather_widget(soup)

    result = {
        "local_date": extract_local_date(weather_widget),
        "temperature": extract_temperature(weather_widget),
        **extract_weather_metrics(weather_widget),
    }

    return {k: v for k, v in result.items() if v is not None}


def get_weather_widget(soup: BeautifulSoup) -> BeautifulSoup:
    """Находит и возвращает основной виджет погоды."""
    widget = soup.find("div", class_="widget now", attrs={"data-widget": "weather-now"})
    if not widget:
        raise ValueError("Виджет погоды не найден на странице")
    return widget


def extract_local_date(widget: BeautifulSoup) -> Optional[str]:
    """Извлекает локальную дату и время."""
    date_element = widget.find("div", class_="now-localdate")
    return date_element.text.strip() if date_element else None


def extract_temperature(widget: BeautifulSoup) -> Optional[str]:
    """Извлекает значение температуры."""
    temp_element = widget.find("div", class_="now-weather").find("temperature-value")
    return temp_element["value"] if temp_element else None


def extract_weather_metrics(widget: BeautifulSoup) -> Dict[str, str]:
    """Извлекает дополнительные метрики погоды (давление, влажность и т.д.)."""
    metrics = {}
    info_items = widget.find_all("div", class_="now-info-item")

    for item in info_items:
        title_element = item.find("div", class_="item-title")
        if not title_element:
            continue

        title = title_element.text.strip()
        value = extract_metric_value(item, title)

        if value:
            metrics[get_metric_key(title)] = value

    return metrics


def extract_metric_value(item: BeautifulSoup, title: str) -> Optional[str]:
    """Извлекает значение метрики в зависимости от её типа."""
    if title == "Давление":
        pressure_element = item.find("pressure-value")
        return pressure_element["value"] if pressure_element else None
    elif title == "Влажность":
        humidity_element = item.find("div", class_="item-value")
        return humidity_element.text.strip() if humidity_element else None
    return None


def get_metric_key(title: str) -> str:
    """Преобразует название метрики в ключ для словаря."""
    metric_map = {"Давление": "pressure", "Влажность": "humidity"}
    return metric_map.get(title, title.lower())


if __name__ == "__main__":
    """Выводим информацию в консоль для примера"""
    weather_data = fetch_weather_data()
    if weather_data:
        print("Данные о погоде:")
        for key, value in weather_data.items():
            print(f"{key.capitalize()}: {value}")
