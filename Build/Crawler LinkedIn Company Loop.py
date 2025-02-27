from linkedin_scraper import Company, actions
from selenium import webdriver
import mysql.connector 
import pandas as pd


# Read the excel sheet
linkedinExcel = pd.read_excel (r'linkedin.xls')

# get the url column only from the excel list
urlList = linkedinExcel.url.to_list()


# connect to mysql database 
mydb = mysql.connector.connect (
    host="127.0.0.1",
    user="root",
    password="dataspider",
    database="linkedin"
)

for url in urlList:

    # let Python know we using Chrome Driver
    driver = webdriver.Chrome()

    # must type your own linkedin email and password
    email= 'capstonespring21@gmail.com'
    password = 'techclass2021'

    # login use the info you provide above
    actions.login(driver, email, password) 

    # start scraping
    company = Company(linkedin_url=url, driver=driver, scrape=True, get_employees=False)
    if company.specialties is None:
        industry = ''
    else:
        industry = company.specialties[0:254]

    # insert data to database
    mycursor = mydb.cursor()
    insertStatement = ("insert into l_company (companyAbbreviation, companyName, companySize, industry, url) values (%s, %s, %s, %s, %s)")
    insertValues = (company.name, company.name, company.company_size, industry, url)
    mycursor.execute(insertStatement, insertValues)
    mydb.commit()
    print (mycursor.rowcount, " record inserted")


