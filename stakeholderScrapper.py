from selenium import webdriver
from selenium.webdriver.common.by import By

from playerNameUnifier import PlayerNameUnifier

import re
import time

class stakeholderScrapper():
    def __init__(self, name_of_stakeholder, url):
        self.bets = []
        self.name_of_stakeholder = name_of_stakeholder
        self.url = url
        self.driver = webdriver.Chrome("/home/jerry/BETter/chromedriver")

        if self.name_of_stakeholder == "STS":
            self.driver.get(self.url)
            self.sts()
        elif self.name_of_stakeholder == "Betcris":
            self.driver.get(self.url)
            self.betcris()
        else:
            print(self.name_of_stakeholder + " stakeholder not found!")
            self.bets.append("Not implemented yet!")

        playerNameUnifier = PlayerNameUnifier(self.bets)
        
    def sts(self):
        bet_tabs = self.driver.find_element(By.ID, "prematch_1047000100184").find_elements(By.CLASS_NAME, "col3")
        for tab in bet_tabs:
            unparsed_string = tab.find_element(By.CLASS_NAME, "subTable").get_attribute("innerHTML")
            stakes = [float(re.sub(r'[^0-9.]', '', line)) for line in unparsed_string.split('\n') if "<span>" in line]
            names = [line for line in unparsed_string.split('\n') if "<" not in line]
            date = unparsed_string[unparsed_string.find("oppty_end_date") + 27 : unparsed_string.find("oppty_end_date") + 37] + " " + unparsed_string[unparsed_string.find("oppty_end_date") + 77 : unparsed_string.find("oppty_end_date") + 82]
            self.bets.append(({"date": date,
                               "a": [names[1], stakes[0], False],
                               "b": [names[2], stakes[1], False],
                               "c": [names[3], stakes[2], False]}))
    
    def which_month(self, polish_month_name):
        if polish_month_name == "Styczeń":
            return "01"
        elif polish_month_name == "Luty":
            return "02"
        elif polish_month_name == "Marzec":
            return "03"
        elif polish_month_name == "Kwiecień":
            return "04"
        elif polish_month_name == "Maj":
            return "05"
        elif polish_month_name == "Czerwiec":
            return "06"
        elif polish_month_name == "Lipiec":
            return "07"
        elif polish_month_name == "Sierpień":
            return "08"
        elif polish_month_name == "Wrzesień":
            return "09"
        elif polish_month_name == "Październik":
            return "10"
        elif polish_month_name == "Listopad":
            return "11"
        elif polish_month_name == "Grudzień":
            return "12"

    def betcris(self):
        time.sleep(2)
        unparsed_list = self.driver.find_element(By.ID, "eventListBody").text.split('\n')
        bets_list = []
        for line in unparsed_list:
            if "Dzisiaj" in line or "Jutro" in line or "Poniedziałek" in line or "Wtorek" in line or "Środa" in line or "Czwartek" in line or "Piątek" in line or "Sobota" in line or "Niedziela" in line:
                sub_list = []
                sub_list.append(line)
                bets_list.append(sub_list)
                continue
            elif line == "":
                continue
            sub_list.append(line)
        dates = []
        names_a = []
        names_b = []
        stakes_a = []
        stakes_b = []
        stakes_draw = []
        for day in bets_list:
            day_split = day[0].split(' ')
            year = day_split[3]
            day_number = day_split[1]
            month = self.which_month(day_split[2])
            matches = day[4:]
            for match_hour in matches[1::7]:
                dates.append(year + "-" + month + "-" + day_number + " " + match_hour)
            for match_name_a in matches[::7]:
                names_a.append(match_name_a)
            for match_name_b in matches[2::7]:
                names_b.append(match_name_b)
            for match_stake_a in matches[4::7]:
                stakes_a.append(match_stake_a)
            for match_stake_b in matches[6::7]:
                stakes_b.append(match_stake_b)
            for match_stake_draw in matches[5::7]:
                stakes_draw.append(match_stake_draw)
            
        count = 0
        for _ in dates, names_a, names_b, stakes_a, stakes_b, stakes_draw:
            self.bets.append(({"date": dates[count],
            "a": [names_a[count], float(stakes_a[count]), False],
            "b": ["X", float(stakes_draw[count]), False],
            "c": [names_b[count], float(stakes_b[count]), False]}))
            count += 1
            
                
            
            

