import json
import os

from datetime import datetime

from stakeholderScrapper import stakeholderScrapper

now = str(datetime.now())
data_json_path = "Bets/" + now + "/data.json"

def create_json_file_and_add_metadata():
    os.mkdir("Bets/" + now)
    with open(data_json_path, "w") as json_data_file:
        sport_name = input("What sport is it?: ")
        metadata_json = {"metadata": 
                                        { 
                                        "sport_type": sport_name
                                        }, 
                        "bets": {}}
        json.dump(metadata_json, json_data_file)

def get_avaiable_stakeholders():
    available_stakeholders = []
    with open("available_stakeholders.json", "r") as json_file:
        json_data = json.load(json_file)
        for stakeholder in json_data.items():
            available_stakeholders.append(stakeholderScrapper(stakeholder[0], stakeholder[1]))
        return available_stakeholders

def create_stakeholders():
    stakeholders = get_avaiable_stakeholders()
    with open(data_json_path) as json_data_file:
        json_data = json.load(json_data_file)
        for stakeholder in stakeholders:
            json_data["bets"][stakeholder.name_of_stakeholder] = stakeholder.bets
    with open(data_json_path, "w") as json_data_file:
        json.dump(json_data, json_data_file)

def print_json_file():
    with open(data_json_path, "r") as json_data_file:
        json_data = json.load(json_data_file)
        print(json_data)

create_json_file_and_add_metadata()
create_stakeholders()