from selenium import webdriver
from selenium.webdriver.common.by import By

import re

class stsScrapper():
    def __init__(self):
        self.bets = []
        self.name_of_stakeholder = "STS"

        url = "https://www.sts.pl/pl/zaklady-bukmacherskie/pilka-nozna/rozgr-miedzynarodowe/mistrzostwa-swiata/184/30851/98982/"
        driver = webdriver.Chrome("/home/jerry/BETter/chromedriver")
        driver.get(url)

        bet_tabs = driver.find_element(By.ID, "prematch_1047000100184").find_elements(By.CLASS_NAME, "col3")
        for tab in bet_tabs:
            unparsed_string = tab.find_element(By.CLASS_NAME, "subTable").get_attribute("innerHTML")
            stakes = [float(re.sub(r'[^0-9.]', '', line)) for line in unparsed_string.split('\n') if "<span>" in line]
            names = [line for line in unparsed_string.split('\n') if "<" not in line]
            date = unparsed_string[unparsed_string.find("oppty_end_date") + 27 : unparsed_string.find("oppty_end_date") + 37] + " " + unparsed_string[unparsed_string.find("oppty_end_date") + 77 : unparsed_string.find("oppty_end_date") + 85]
            self.bets.append(({"date": date,
                               "a": (names[1], stakes[0]),
                               "b": (names[2], stakes[1]),
                               "c": (names[3], stakes[2])}))