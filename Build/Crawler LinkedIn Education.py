from linkedin_scraper import Person, actions, Education
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import mysql.connector 
import os
import time

driver = webdriver.Chrome()

# must type your own linkedin email and password
email= 'capstonespring21@gmail.com'
password = 'techclass2021'
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

#connect to mysql database 
mydb = mysql.connector.connect (
    host="127.0.0.1",
    user="root",
    password="dataspider",
    database="linkedin"
)

mycursor = mydb.cursor()

personURLs = ["https://www.linkedin.com/in/svetlana-kurilova-275ba219/"]
             
for url in personURLs:
    person = Person(linkedin_url=url, name=True, about=None, experiences= None, educations= [], interests=None, accomplishments=None, company= None, job_title=True, driver=driver, scrape= False)

    #Need Chrome to wait 8 second for linkedin to load before scrape
    time.sleep(10)

    #scrape without log in over and over to avoid Linkedin locks our account
    person.scrape(close_on_complete=False)

# write instatement first
for education in person.educations:
    insertStatement = ("insert into l_education (name, degree, from_date, to_date, current_position, url) values (%s, %s, %s, %s, %s, %s)")
    insertValues = (person.name, education.degree, education.from_date, education.to_date,
                    person.job_title, url)

    mycursor.execute(insertStatement, insertValues)

    mydb.commit()
    print (mycursor.rowcount, " record inserted")
    #Add break so wont scrape past information. Only scrape latest degree
    break
   
    # sleep 8 seconds again before scrape new profile
time.sleep(10)


driver.quit()



