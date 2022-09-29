from selenium import webdriver
from selenium.webdriver.common.by import By

import re

class stakeholderScrapper():
    def __init__(self, name_of_stakeholder, url):
        self.bets = []
        self.name_of_stakeholder = name_of_stakeholder
        self.url = url
        self.driver = webdriver.Chrome("/home/jerry/BETter/chromedriver")

        if self.name_of_stakeholder == "STS":
            self.driver.get(self.url)
            self.sts()
        else:
            print(self.name_of_stakeholder + " stakeholder not found!")
            self.bets.append("Not implemented yet!")


    def sts(self):
        bet_tabs = self.driver.find_element(By.ID, "prematch_1047000100184").find_elements(By.CLASS_NAME, "col3")
        for tab in bet_tabs:
            unparsed_string = tab.find_element(By.CLASS_NAME, "subTable").get_attribute("innerHTML")
            stakes = [float(re.sub(r'[^0-9.]', '', line)) for line in unparsed_string.split('\n') if "<span>" in line]
            names = [line for line in unparsed_string.split('\n') if "<" not in line]
            date = unparsed_string[unparsed_string.find("oppty_end_date") + 27 : unparsed_string.find("oppty_end_date") + 37] + " " + unparsed_string[unparsed_string.find("oppty_end_date") + 77 : unparsed_string.find("oppty_end_date") + 82]
            self.bets.append(({"date": date,
                               "a": (names[1], stakes[0], False),
                               "b": (names[2], stakes[1], False),
                               "c": (names[3], stakes[2], False)}))