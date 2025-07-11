import streamlit as st
import pandas as pd
from cleaner import (
    get_cities,
    get_city_information,
    create_table_city_weather,
    insert_city,
    insert_weather,
    get_weather_dataframe
)
import sqlite3

# Pfad zur Datenbank
DB_PATH = "weather.db"

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title=" Wetter Dashboard", layout="centered")
st.title(" Wetter Dashboard")
st.markdown("Lade aktuelle Wetterdaten herunter, speichere sie in der Datenbank und visualisiere sie interaktiv.")

# Datenbank initialisieren (Tabellen erstellen)
create_table_city_weather(DB_PATH)

# Abschnitt 1: Stadt auswählen
st.subheader("1. Stadt auswählen und Wetter abrufen")
cities = get_cities()
selected_city = st.selectbox("Wähle eine Stadt", cities)

if st.button(" Wetterdaten abrufen und speichern"):
    data = get_city_information(selected_city)
    if data:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        city_id = insert_city(cur, selected_city)
        insert_weather(cur, city_id, data)
        con.commit()
        con.close()
        st.success(f"Wetterdaten für {selected_city} erfolgreich gespeichert.")
    else:
        st.error("Fehler beim Abrufen der Wetterdaten.")

# Abschnitt 2: Wetterdaten-Vorschau aus DB
st.subheader("2. Wetterdaten Vorschau")
df = get_weather_dataframe(DB_PATH)

if not df.empty:
    st.dataframe(df)

    # Abschnitt 3: Diagramm
    st.subheader("3. Temperaturdiagramm")
    st.line_chart(df[['Temperature_in_C', 'temp_min', 'temp_max']])
else:
    st.info("Noch keine Wetterdaten vorhanden.")

# Abschnitt 4: CSV-Export
if not df.empty:
    st.subheader(" CSV-Datei herunterladen")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(" CSV herunterladen", csv, file_name="wetterdaten.csv", mime="text/csv")
