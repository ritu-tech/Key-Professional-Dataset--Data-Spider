from linkedin_scraper import Person, actions, Experience
from selenium import webdriver
import mysql.connector 
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

# run insert statement 
mycursor = mydb.cursor()

personURLs = ["https://www.linkedin.com/in/leo-lam-b1228014/","https://www.linkedin.com/in/keisuke-kamiura-50a73716a/"]

for url in personURLs:
    person = Person(linkedin_url=url, name=True, about=None, experiences=[], educations=None, interests=None, accomplishments=None, company=True, job_title=True, driver=driver, scrape=False)

    #Need Chrome to wait 8 second for linkedin to load before scrape
    time.sleep(8)

    #scrape without log in over and over to avoid Linkedin locks our account
    person.scrape(close_on_complete=False)

    for experience in person.experiences:
        insertStatement = ("insert into l_person (name, position, from_date, to_date, duration, location, current_position, url, company) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        insertValues = (person.name, experience.position_title, experience.from_date, experience.to_date,
                    experience.duration, experience.location, person.job_title, url, person.company)

        mycursor.execute(insertStatement, insertValues)

        mydb.commit()
        print (mycursor.rowcount, " record inserted")

         #Add break so wont scrape past information. Only scrape current company work experience
        break

    # sleep 8 seconds again before scrape new profile
    time.sleep(8)


driver.quit()

