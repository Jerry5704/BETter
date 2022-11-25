import json
import os

print(os.listdir("/home/jerry/BETter/Bets")[0])
with open("/home/jerry/BETter/Bets/" + os.listdir("/home/jerry/BETter/Bets")[0] + "/data.json", "r") as json_file:
    json_data = json.load(json_file)
    with open("available_stakeholders.json", "r") as json_second_file:
        json_second_data = json.load(json_second_file)
        stakeholders = [(stakeholder_key, {}) for stakeholder_key, stakeholder_value in json_second_data.items()]
    best_bets = {}
    for stakeholder_name, stakeholder_dict in stakeholders:
        for day in json_data["bets"][stakeholder_name]:
            stakeholder_dict[day["date"] + " " + day["a"][0] + " - " + day["c"][0]] = ((day["a"][1], stakeholder_name), (day["b"][1], stakeholder_name), (day["c"][1], stakeholder_name))
            best_bets[day["date"] + " " + day["a"][0] + " - " + day["c"][0]] = [[day["a"][1], stakeholder_name], [day["b"][1], stakeholder_name], [day["c"][1], stakeholder_name]]
    for name, best_tuples in best_bets.items():
        for stakeholder_name, stakeholder_dict in stakeholders:
            try:                
                if float(stakeholder_dict[name][0][0]) > best_tuples[0][0]:
                    best_tuples[0][0] = float(stakeholder_dict[name][0][0])
                    best_tuples[0][1] = stakeholder_name
                if float(stakeholder_dict[name][1][0]) > best_tuples[1][0]:
                    best_tuples[1][0] = float(stakeholder_dict[name][1][0])
                    best_tuples[1][1] = stakeholder_name
                if float(stakeholder_dict[name][2][0]) > best_tuples[2][0]:
                    best_tuples[2][0] = float(stakeholder_dict[name][2][0])
                    best_tuples[2][1] = stakeholder_name
            except Exception as e:
                continue
    best_yet = float(2)
    for date, best_odds in best_bets.items():
        print(date)
        print(best_odds)
        implied_win_probability = float()
        for odd in best_odds:
            implied_win_probability += 1/odd[0]
        if best_yet > implied_win_probability:
            best_yet = implied_win_probability
        if implied_win_probability < 1:
            print(f"##############################################")
            print(f"O KURWA MAMY TO - {implied_win_probability}")
            print(f"##############################################")
        else:
            print(implied_win_probability)
    print("#########")
    print(best_yet)
    print("#########")
        
