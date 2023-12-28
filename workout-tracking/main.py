import os
from datetime import datetime

import requests

# Primeramente asignamos todas las variables constantes
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
AUTH_URL = os.environ.get("AUTH_URL")
GENDER = os.environ.get("GENDER")
WEIGHT_KG = os.environ.get("WEIGHT_KG")
HEIGHT_CM = os.environ.get("HEIGHT_CM")
AGE = os.environ.get("AGE")
API_SHEETS = os.environ.get("API_SHEETS")

# Declaramos la url del API del calculo de calorias e interpretacion de texto
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
# Se declara las fechas a tomar
today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
today_time = today.strftime("%I:%M:%S %p")
# Se asignan los headers
headers = {
    "Content-Type": "application/json",
    "x-app-key": APP_KEY,
    "x-app-id": APP_ID,
}

# Es necesario que se requiera un input
query = input("Tell me wich exercises you did: ")

# Asignamos los parametros de la consulta
parameters = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

#######################################################################
# Definimos la url del API
sheety_endpoint = F"https://api.sheety.co/{API_SHEETS}/myWorkouts/workouts"
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": AUTH_URL
}


# Esta funcion manda la lista de diccionarios a Google Sheets
def post_request_sheets(exercises):
    for item in exercises:
        print(item)
        try:
            response = requests.post(sheety_endpoint, headers=sheety_headers, json=item)
            if response.status_code == 200:
                print("Request successful")

            else:
                print(f'Error: {response.status_code}')
                print(response.text)
        except Exception as e:
            print(f'Error: {e}')


# Se comprueba que la data del input no sea None
if query:
    exercises = []
    try:
        response = requests.post(exercise_endpoint, headers=headers, json=parameters)
        if response.status_code == 200:
            response_json = response.json()
            for item in response_json["exercises"]:
                workout = {
                    "workout": {
                        "date": today_date,
                        "time": today_time,
                        "exercise": item["name"],
                        "duration": item["duration_min"],
                        "calories": item["nf_calories"]
                    }
                }
                exercises.append(workout)
            post_request_sheets(exercises)

        else:
            print(f'Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error: {e}')
