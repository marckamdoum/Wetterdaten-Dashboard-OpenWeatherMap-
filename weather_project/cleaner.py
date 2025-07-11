import os
import requests
import sqlite3
import csv
import logging
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Arbeitsverzeichnis setzen & .env laden
os.chdir(Path(__file__).parent)
load_dotenv()

# Logging einrichten
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "weather.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# API-Key aus .env laden
API_KEY = os.getenv("API_KEY")
COUNTRY = "de"

def get_cities(): # Beispielhafte Liste von Städten.

    return ["Stuttgart", "Aachen", "Berlin"]

def get_city_information(city: str): # Holt aktuelle Wetterdaten von OpenWeatherMap und speichert sie als CSV.

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city},{COUNTRY}"
            f"&appid={API_KEY}&units=metric&lang=de"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Relevante Infos extrahieren
        weather_info = {
            'city': city,
            'Description_EN': data['weather'][0]['description'],
            'Description_DE': data['weather'][0]['description'],
            'Temperature': data['main']['temp'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max']
        }

        # Speichern als CSV
        csv_dir = Path("data")
        csv_dir.mkdir(exist_ok=True)
        csv_file_path = csv_dir / f"{city.lower()}.csv"
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['City', 'Description EN', 'Description DE', 'Temperature', 'Temp Min', 'Temp Max'])
            writer.writerow([
                weather_info['city'],
                weather_info['Description_EN'],
                weather_info['Description_DE'],
                weather_info['Temperature'],
                weather_info['temp_min'],
                weather_info['temp_max']
            ])
        logging.info(f"Wetterdaten für {city} gespeichert in {csv_file_path}")
        return data

    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Wetterdaten für {city}: {e}")
        return None

def create_table_city_weather(db_path): # Erstellt die Tabellen 'city' und 'weather' falls sie nicht existieren.

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS city (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                cityname TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                FK_cityID INTEGER,
                Description_EN TEXT,
                Description_DE TEXT,
                Temperature_in_C REAL,
                temp_min REAL,
                temp_max REAL,
                FOREIGN KEY(FK_cityID) REFERENCES city(ID)
            )
        """)
        con.commit()
        con.close()
        logging.info("Tabellen 'city' und 'weather' erfolgreich erstellt.")
    except Exception as e:
        logging.error(f"Fehler beim Erstellen der Tabellen: {e}")

def insert_city(cur, cityname): # Fügt Stadtname in die Tabelle 'city' ein.

    try:
        cur.execute("INSERT INTO city (cityname) VALUES (?)", (cityname,))
        logging.info(f"Stadt '{cityname}' in Datenbank eingefügt.")
        return cur.lastrowid
    except Exception as e:
        logging.error(f"Fehler beim Einfügen der Stadt '{cityname}': {e}")
        return None

def insert_weather(cur, city_id, weather_data): # Fügt Wetterdaten in die Tabelle 'weather' ein.

    try:
        cur.execute("""
            INSERT INTO weather (FK_cityID, Description_EN, Description_DE, Temperature_in_C, temp_min, temp_max)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            city_id,
            weather_data['weather'][0]['description'],
            weather_data['weather'][0]['description'],
            weather_data['main']['temp'],
            weather_data['main']['temp_min'],
            weather_data['main']['temp_max']
        ))
        logging.info(f"Wetterdaten für Stadt-ID {city_id} gespeichert.")
    except Exception as e:
        logging.error(f"Fehler beim Speichern der Wetterdaten: {e}")

def get_weather_dataframe(db_path):# Lädt alle Wetterdaten aus der Datenbank als DataFrame.

    try:
        con = sqlite3.connect(db_path)
        df = pd.read_sql_query("""
            SELECT city.cityname, weather.Description_EN, weather.Temperature_in_C,
                   weather.temp_min, weather.temp_max
            FROM weather
            JOIN city ON weather.FK_cityID = city.ID
        """, con)
        con.close()
        return df
    except Exception as e:
        logging.error(f"Fehler beim Lesen der Datenbank: {e}")
        return pd.DataFrame()
