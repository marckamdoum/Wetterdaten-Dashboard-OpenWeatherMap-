# Wetterdaten-Dashboard-OpenWeatherMap-
Ein professionelles Dashboard zur Abfrage, Speicherung und Visualisierung aktueller Wetterdaten von OpenWeatherMap. Die Anwendung nutzt Streamlit zur Anzeige und SQLite zur Speicherung aller Wetterabfragen. CSV-Export und Diagramme sind integriert.

# Feature
🌍 API-Anbindung an OpenWeatherMap (via requests)

🧾 Speicherung aller Abrufe in SQLite-Datenbank

📊 Streamlit-Oberfläche mit interaktiver Stadtwahl

🔁 Anzeige aktueller Wetterdaten aus Datenbank

📈 Temperatur-Diagramm (aktueller Wert, Min/Max)

📥 Download als CSV

🧠 Logging aller API-Aufrufe und Fehler

#🛠️ Verwendete Technologien
Streamlit – für die Benutzeroberfläche

OpenWeatherMap API – für Wetterdaten

SQLite – zur Datenspeicherung

Pandas – zur Datenverarbeitung

Plotly – für interaktive Diagramme

Logging – zur Prozessüberwachung

# Start
pip install -r requirements.txt
streamlit run app.py

# Screenshot
<img width="972" height="756" alt="image_weather" src="https://github.com/user-attachments/assets/372e0561-f913-4cb0-abab-e29d63748454" />
<img width="1047" height="716" alt="image2_weather" src="https://github.com/user-attachments/assets/65eccf52-5f7b-4256-9505-2b267b7eb151" />
<img width="482" height="361" alt="image3_weather" src="https://github.com/user-attachments/assets/3042a5a8-9ca7-4f93-9304-d3ab717b092c" />




