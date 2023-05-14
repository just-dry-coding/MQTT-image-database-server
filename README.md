# MQTT-image-database-server
Receives images from a MQTT broker and stores them in a MongoDB database

## Setup
1. install python (v3.9.13)
2. setup venv
   1. `python -m venv venv`
   2. `./venv/Scripts/activate`
   3. `pip install -r requirements.txt`

## Tests
1. run `pytest`

## Run
1. run `python ./src/image_management_server.py <mongo_connection_string> <database> <collection>