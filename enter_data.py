import json
import os

from datetime import datetime

from stsScrapper import stsScrapper

data_json_path = "data.json"

def create_json_file_and_add_metadata():
# os.mkdir("Bets/" + str(datetime.now()))
    with open(data_json_path, "w") as json_data_file:
        stakeholder_count = input("How much stakeholders?: ")
        sport_name = input("What sport is it?: ")
        metadata_json = {"metadata": 
                                        {"stakeholders_count": stakeholder_count, 
                                        "sport_type": sport_name
                                        }, 
                        "bets": {}}
        json.dump(metadata_json, json_data_file)
        return stakeholder_count

def create_stakeholder(count):
    scrapper = stsScrapper()
    name_of_stakeholder = scrapper.name_of_stakeholder
    with open(data_json_path) as json_data_file:
        json_data = json.load(json_data_file)
    json_data["bets"][name_of_stakeholder] = scrapper.bets
    with open(data_json_path, "w") as json_data_file:
        json.dump(json_data, json_data_file)

def print_json_file():
    with open(data_json_path, "r") as json_data_file:
        json_data = json.load(json_data_file)
        print(json_data)

count = create_json_file_and_add_metadata()
create_stakeholder(count)
print_json_file()