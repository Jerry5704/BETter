import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


from playerNameUnifier import PlayerNameUnifier

import re
import time
import itertools
import datetime
import json

class stakeholderScrapper():
    def __init__(self, name_of_stakeholder, list_of_urls):
        self.bets = []
        self.name_of_stakeholder = name_of_stakeholder
        self.list_of_urls = list_of_urls
        self.driver = uc.Chrome()


        if self.name_of_stakeholder == "STS":
            for url in self.list_of_urls:
                print(url)
                self.driver.get(url)
                self.sts()
        elif self.name_of_stakeholder == "Betcris":
            for url in self.list_of_urls:
                print(url)
                self.driver.get(url)
                self.betcris()
        elif self.name_of_stakeholder == "Fuksiarz":
            for url in self.list_of_urls:
                print(url)
                self.driver.get(url)
                self.fuksiarz()
        else:
            print(self.name_of_stakeholder + " stakeholder not found!")
            self.bets.append("Not implemented yet!")

        self.playerNameUnifier = PlayerNameUnifier(self.bets)
        
    def sts(self):
        bet_tabs = self.driver.find_element(By.CLASS_NAME, "bet_tab").find_elements(By.CLASS_NAME, "col3")
        for tab in bet_tabs:
            unparsed_string = tab.find_element(By.CLASS_NAME, "subTable").get_attribute("innerHTML")
            stakes = [float(re.sub(r'[^0-9.]', '', line)) for line in unparsed_string.split('\n') if "<span>" in line]
            names = [line for line in unparsed_string.split('\n') if "<" not in line]
            
            # ToDo: move somewhere else, eg. another function
            for name in names:
                if name in names:
                    pass
                else:
                    with open("available_players.json") as fp:
                        dictObj = json.load(fp)
                    dictObj.update({name: [name]})
                    with open("available_players.json", "w") as json_million_file:
                        json.dump(dictObj, json_million_file)
                    
            
            date = unparsed_string[unparsed_string.find("oppty_end_date") + 27 : unparsed_string.find("oppty_end_date") + 37] + " " + unparsed_string[unparsed_string.find("oppty_end_date") + 77 : unparsed_string.find("oppty_end_date") + 82]
            self.bets.append(({"date": date,
                               "a": [names[1], stakes[0], False],
                               "b": [names[2], stakes[1], False],
                               "c": [names[3], stakes[2], False]}))
    
    def betcris(self):
        time.sleep(5)
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
            if count == len(dates):
                return
            self.bets.append(({"date": dates[count],
            "a": [names_a[count], float(stakes_a[count]), False],
            "b": ["X", float(stakes_draw[count]), False],
            "c": [names_b[count], float(stakes_b[count]), False]}))
            count += 1

    def fuksiarz(self):
        time.sleep(5)
        bet_tabs = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[1]/div[2]/div[3]/div/div/div[3]/partial[4]/div/div/div/div[2]/div[2]/div[3]").text.split('\n')
        if "Idź do wydarzenia" in bet_tabs:
            self.delete_idz_do_wydarzenia_in_fuksiarz(bet_tabs)

        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        times = len(bet_tabs)/7
        
        # dates set
        dates = [date.strftime("%Y")] * int(times)
        months = [date[3:] for date in bet_tabs[1::7]]
        days = [date[:2] for date in bet_tabs[1::7]]
        hours = bet_tabs[::7]
        for i in range(len(dates)):
            dates[i] += "-" + months[i] + "-" + days[i] + " " + hours[i]

        # player names set
        # for x in bet_tabs[2::7]:
        #     print(x.split("-")[1].lstrip(" "))
        names_a = [matchup.split("-")[0].strip(" ") for matchup in bet_tabs[2::7]] 
        names_c = [matchup.split("-")[1].lstrip(" ") for matchup in bet_tabs[2::7]] 
        names_b = ["X"] * int(times)

        # player odds set
        odds_a = bet_tabs[3::7]
        odds_b = bet_tabs[4::7]
        odds_c = bet_tabs[5::7]

        # insert into data.json 
        for i in range(int(times)):
            self.bets.append(({"date": dates[i],
                    "a": [names_a[i], float(odds_a[i]), False],
                    "b": [names_b[i], float(odds_b[i]), False],
                    "c": [names_c[i], float(odds_c[i]), False]}))

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

    def delete_idz_do_wydarzenia_in_fuksiarz(self, bet_tabs):
            counter = 0
            for line in range(len(bet_tabs)):
                if bet_tabs[counter] == "Idź do wydarzenia":
                    del bet_tabs[counter + 1]
                    del bet_tabs[counter]
                    del bet_tabs[counter - 1]
                    del bet_tabs[counter - 2]
                    del bet_tabs[counter - 3]
                    counter -= 5
                counter += 1


            



            
                
            
            

