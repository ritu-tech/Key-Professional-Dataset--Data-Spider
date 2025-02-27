import praw
from psaw import PushshiftAPI
import mysql.connector 
import pandas as pd
from praw.models import MoreComments
import time
from datetime import datetime
import MySQLdb

api = PushshiftAPI()

# Connect to the database
connection = MySQLdb.connect(host="127.0.0.1",
    user="root",
    password="dataspider",
    database="reddit")

# create cursor
cursor=connection.cursor()

# Read the excel sheet
redditExcel = pd.read_excel (r'reddit2.xls')

# get the list of company name, and country
companyList = redditExcel.Name.to_list()
countryList = redditExcel.Country.to_list()

for i in range(len(companyList)):
        posts = []
        
        submissions = api.search_submissions(q= companyList[i],
                                        subreddit= 'investing',
                                        filter=['url','author', 'title', 'num_comments' , 'score', 'subreddit', 'country','created_utc'],
                                        limit = 2)
                        
        for post in submissions:
                posts.append([post.url, post.author, post.title, post.num_comments, post.score, post.subreddit,companyList[i],countryList[i], datetime.utcfromtimestamp(post.created_utc)])
        posts = pd.DataFrame(posts,columns=['url','author', 'title','num_comments', 'score', 'subreddit', 'company', 'country', 'created_utc'])

        for i,row in posts.iterrows():
                sql = ("INSERT IGNORE INTO reddit.r_scrap ( url, author, title, num_comments, score, subreddit, company, country, createdtime ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(sql, tuple(row))

                # the connection is not autocommitted by default, so we must commit to save our changes
                connection.commit()
                print (cursor.rowcount, " record inserted")