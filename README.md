
# gismeteo_parse
Парсим сайт gismeteo.ru на предмет получения основных данных о погоде


## 0. Подготовка окружения
```bash
python -m venv venv

.\venv\Scripts\Activate.ps1

python.exe -m pip install --upgrade pip

pip install requests beautifulsoup4 python-dotenv

pip freeze > requirements.txt
```

Для установки зависимостей: pip install -r requirements.txt

В файле `.env` укзаать ссылку на url страницу c текущей погодой (в ссылке должно быть `now`, например `"https://www.gismeteo.ru/weather-kurgan-4569/now/"`)

## 1. Запуск скрипта и его вывод

```bash
python gismeteo.py
 ```

Вывод:
```bash
Данные о погоде:
Local_date: Ср, 3 сентября, 10:39
Temperature: 13
Pressure: 757
Humidity: 88
```