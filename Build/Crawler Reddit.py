import praw
from psaw import PushshiftAPI
import mysql.connector 
import pandas as pd
from praw.models import MoreComments


api = PushshiftAPI()

# Connect to the database
connection = mysql.connector.connect(host="127.0.0.1",
    user="root",
    password="dataspider",
    database="reddit")

posts = []
    
submissions = api.search_submissions(q= 'La Banque Postale Asset Management',
                                    subreddit= 'finance',
                                    filter=['url','author', 'title', 'num_comments' , 'score', 'subreddit'],
                                    limit = 5)
                   
for post in submissions:
        posts.append([post.url, post.author, post.title, post.num_comments, post.score, post.subreddit])
posts = pd.DataFrame(posts,columns=['url','author', 'title','num_comments', 'score', 'subreddit'])
print(posts)

# create cursor
cursor=connection.cursor()

for i,row in posts.iterrows():
    sql = ("INSERT INTO r_scrap ( url, author, title, num_comments, score, subreddit, company, country) VALUES ( %s, %s, %s, %s, %s, %s, 'Baillie Gifford & Co.', 'UK')")
    cursor.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    connection.commit()
    print (cursor.rowcount, " record inserted")