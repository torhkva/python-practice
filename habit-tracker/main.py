import os
import requests
from datetime import datetime

# Se definen los valores de usuario y contraseña
USERNAME = os.environ.get("USERNAME")
TOKEN = os.environ.get("TOKEN")
GRAPH_ID = os.environ.get("GRAPH_ID")
# Para crear una cuenta podemos utilizar el siguiente endpoint
pixela_endpoint = "https://www.pixe.la/v1/users"
# Asi como los parametros de usuario siguientes:
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",

}
# Para ejecutar la creacion de cuenta vamos a usar la siguiente petición
# response = requests.post(pixela_endpoint, json=user_params)

# Con este comando se puede ver el status de la respuesta
# print(response.text)

# Para generar la grafica usamos el siguiente endpoint
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
# Esta vez enviamos el token como header
headers = {
    "X-USER-TOKEN": TOKEN
}
# Asignamos los parametros necesarios para generar la grafica
graph_config = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "sora",

}

# Nuevamente mandamos la post request con los datos
# graph_response = requests.post(graph_endpoint, json=graph_config, headers=headers)
# print(graph_response.text)

# Para mandar algun dato en la grafica utilizamos el siguiente endpoint
pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_config = {
    "date": "20231221",
    "quantity": "10.7",
}


# pixel_response = requests.post(pixel_endpoint, json=pixel_config, headers=headers)
# print(pixel_response.text)

# Para editar alguna fecha vamos a utilizar el siguiente endpoint esta vez usamos datetime para formatear la fecha
date_edited_raw = datetime(year=2023, month=12, day=21)
date_edited = date_edited_raw.strftime("%Y%m%d")

edit_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date_edited}"

# Y utilzamos el siguiente cuerpo
edit_config = {
    "quantity": "4.8"
}
edit_response = requests.put(edit_endpoint, json=edit_config, headers=headers)
print(edit_response.text)

