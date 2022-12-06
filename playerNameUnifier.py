import json

class PlayerNameUnifier ():
    def __init__(self, bets):
        self.bets = bets
        self.available_players_dict = self.get_available_players_dict()
        self.convert_players_names()

    def get_available_players_dict(self):
        with open("available_players.json", "r") as json_file:
            json_data = json.load(json_file)
            return json_data
    
    def convert_name(self, unconverted_name):
        for good_name, bad_names_list in self.available_players_dict.items():
            if unconverted_name in bad_names_list:
                return good_name
        self.available_players_dict.update({unconverted_name: [unconverted_name]})
        return f"Official name not found. Add official name for {unconverted_name}"

    def convert_players_names(self):
        for bet in self.bets:
            bet["a"][0] = self.convert_name(bet["a"][0])
            bet["c"][0] = self.convert_name(bet["c"][0])