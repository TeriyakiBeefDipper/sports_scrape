#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 00:20:42 2023

@author: tbd
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv


driver = webdriver.Chrome()
driver.implicitly_wait(5)
url = "https://nsb88.com/index.html?"
driver.get(url)

# Find the frame based on the src
frame_element = driver.find_element('css selector','frame[src="./html/frm/index.html"]') 
# Switch to the frame 
driver.switch_to.frame(frame_element)

# Find the CAPCHA code
soup = BeautifulSoup(driver.page_source,'html.parser')
verifiCode = soup.find('img',id="verifi").get("src")
verifiCode = verifiCode[-4:]
print("CAPCHA code found")

# Find the username input field and enter the username
username_field = driver.find_element(By.NAME, 'username')
username_field.send_keys('demo0207')

# Find the password input field and enter the password
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('demo0207')

# Find the CAPCHA input field and enter verifiCode
auth_field = driver.find_element(By.NAME, 'code')
auth_field.send_keys(verifiCode)

time.sleep(2)

# Click the Login button
submit_button = driver.find_element(By.ID,'login')
submit_button.click()
print("Logged in")

time.sleep(5)

# Click on the sports catagory tab btn
sports_catagory_btn = driver.find_element('css selector','a[href="../sport/sportsbook.html"]')
sports_catagory_btn.click()
print("Clicked Sports tab")

# Move to CPSPORTS
actions = ActionChains(driver)
xoffset = 500
yoffset = 340
actions.move_by_offset(xoffset, yoffset)

time.sleep(5)

actions.click()
actions.perform()
print("Clicked 皇冠體育")

time.sleep(20)

# Change tab window to game
window_handles = driver.window_handles
new_tab = len(window_handles) - 1
driver.switch_to.window(window_handles[new_tab])
print("driver switched tabs")

time.sleep(10)

# print("finding today tab")
today_tab = driver.find_element(By.ID,'today_page')
today_tab.click()
print('Clicked today tab')

time.sleep(10)

# Find 波膽
try:
    # print("finding field")
    field = driver.find_element('css selector', 'span[class="ft_txt"]')
    field.click()
    print("Clicked Middle Field")
except:
    print("cannot find field")

# # click on spot
# actions = ActionChains(driver)
# xoffset = 100
# yoffset = 100
# actions.move_by_offset(xoffset, yoffset)

# print("moved cursor")
# actions.click()
# actions.perform()
# print("clicked cursor")

time.sleep(5)

# now = datetime.datetime.now().strftime("%m-%d-%H:%M")

# Scrape and Parse data
with open('soup.html','w')as file:
    file.write(driver.page_source)

soup = BeautifulSoup(driver.page_source,'html.parser')
contents = soup.find(id="div_show")
league_name = contents.find_all("div",class_="btn_title_le")
host_team = contents.find_all(id="game_team_h")
guest_team = contents.find_all(id="game_team_c")
match_time = contents.find_all("tt",class_="text_time")
numbers = contents.find_all('div',class_='box_rpdbet')

csvdata = [['League','Host_Team','Guest_Team','Date_Time','Score_to_Payrate']]

list_of_times = []
today = datetime.date.today()
now = datetime.datetime.now()
year = datetime.datetime.now().year
for i in match_time:
    text = i.text
    text = re.sub("今日", today.strftime("%Y-%m-%d "), text)
    dateTime = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M")
    list_of_times.append(dateTime)

list_of_scores = []
for i in numbers:
    scores = i.find_all("tt",class_='text_ballou')
    payrate = i.find_all("span",class_='text_odds')
    score_to_payrate = {}
    for i in range(len(scores)):
        score_to_payrate[scores[i].text] = payrate[i].text
    list_of_scores.append(score_to_payrate)

for i in range(len(league_name)):
    csvdata.append([league_name[i].text,host_team[i].text,guest_team[i].text,list_of_times[i],list_of_scores[i]])

with open('fulldata-{}.csv'.format(now.strftime("%m-%d-t%H%M")), mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csvdata)
    print("Full data saved")

for row in csvdata[1:]:
    target = row[3]
    if target < now:
        csvdata.remove(row)

with open("data-{}.csv".format(now.strftime("%m-%d-t%H%M")), mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csvdata)
    print("Timed data saved")

driver.quit()
print("scrape complete at {}".format(now))


