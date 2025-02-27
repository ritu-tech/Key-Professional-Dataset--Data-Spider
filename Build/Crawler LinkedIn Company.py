from linkedin_scraper import Company, actions
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import mysql.connector 
import time

# let Python know we using Chrome Driver
driver = webdriver.Chrome()

# must type your own linkedin email and password
email= 'capstonespring21@gmail.com'
password = 'techclass2021'

# login use the info you provide above
actions.login(driver, email, password) 

# Scrapping company
url = "https://www.linkedin.com/company/nylinvestments?trk=public_profile_topcard-current-company"
company = Company( linkedin_url=url, driver=driver, scrape=True, get_employees=False)

# connect to mysql database 
mydb = mysql.connector.connect (
  host="127.0.0.1",
    user="root",
    password="dataspider",
    database="linkedin"

)

# run insert statement 
mycursor = mydb.cursor()
# write instatement first
insertStatement = ("insert into l_company (companyAbbreviation, companyName, industry, companysize, url) values (%s, %s, %s, %s, %s)")
insertValues = (company.name, company.name, company.specialties, company.company_size,url)
mycursor.execute(insertStatement, insertValues)

mydb.commit()
print (mycursor.rowcount, " record inserted")

driver.quit()