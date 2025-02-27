from selenium import webdriver
from selenium.webdriver import Chrome 
from instascrape import *
import mysql.connector 

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"cookie":f'sessionid= 46417601215%3A0ThcWyoptnwSle%3A27;'
}
instaposts = []
driver = webdriver.Chrome()

url = 'https://www.instagram.com/guggenheim/?hl=en'

company = Profile(url)

company.scrape(headers=headers)

# Connect to the database
mydb = mysql.connector.connect (host="127.0.0.1",
                                      user="root",
                                      password="capstone",
                                      database="instagram")

cursor = mydb.cursor()
use_query = "USE instagram"
cursor.execute(use_query)

# run insert statement 
mycursor = mydb.cursor()
# write instatement first
insertStatement = ("insert into i_company (user, followers, following, posts, url) values (%s, %s, %s, %s, %s)")
insertValues = (company.username, company.followers, company.following, company.posts, url)
mycursor.execute(insertStatement, insertValues)

mydb.commit()
print (mycursor.rowcount, " record inserted")

driver.quit()
