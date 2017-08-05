import requests
import base64
import json


def upload(imagen):
    with open(imagen, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    url = "https://api.imgur.com/3/image"
    payload = {'image': encoded_string}
    headers = {'authorization': 'Client-ID 914d09e98a60acb'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return(response.json()["data"]["link"])
