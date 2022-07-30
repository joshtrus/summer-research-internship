#Josh Morris
#07/29/22
#test.01
#First the program scrapes all tickers names from the website. Then the program scrapes the ticker name in the article, date and time 
#the article was published, the summary of the article and the full article. Currently the program is not scraping the links of the 
#documents for the full article. I found that scraping the href should solve the problem


import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sqlite3
import string

#-----------------------------------------------------------------------------------------------------------------#
#SETTING UP DATABASE STUFF
#Connection and cursor
conn = sqlite3.connect('jseScrape.db')
cursor = conn.cursor()

#Create Table
createTable = """CREATE TABLE IF NOT EXISTS
jse_main(id INTEGER PRIMARY KEY autoincrement, tickerName TEXT, newsDate TEXT, newsTime TEXT, newsSummary TEXT, fullArticle TEXT)"""
cursor.execute(createTable)

createTable = """CREATE TABLE IF NOT EXISTS
jse_select(id INTEGER PRIMARY KEY autoincrement, tickerName TEXT, newsDate TEXT, newsTime TEXT, newsSummary TEXT, fullArticle TEXT)"""
cursor.execute(createTable)
#-----------------------------------------------------------------------------------------------------------------#
os.environ["PATH"] += os.pathsep + r'/Users/joshparchment/Documents/GitHub/summer-research-internship/chromedriver'
chrome_options = Options()
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome()
#-----------------------------------------------------------------------------------------------------------------#
def ticker(ticker_name):
    thing = ticker_name.translate(str.maketrans('', '', string.punctuation))
    strings = thing.split()
    n = len(strings) 
    for x in range(0,n):
        if strings[x].isupper():
            if strings[x] in main or strings[x] in select:
                ticker_name = strings[x]
    return ticker_name
#-----------------------------------------------------------------------------------------------------------------#
#setting up the list of desired ticker names 
main = []
browser.get("https://www.jamstockex.com/trading/indices/index-composition/?indexCode=jse-index")
for x in range(1,55):
    try:
        main_ticker_name = browser.find_element("xpath", 
            f"""//*[@id="main"]/div/section[2]/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div/div[1]/div/div/table/tbody/tr[{x}]/td[1]""")
        main_ticker_name = main_ticker_name.text
        main.append(main_ticker_name)
    except:
        pass

select = []
browser.get("https://www.jamstockex.com/trading/indices/index-composition/?indexCode=jse-select")
for x in range(1,20):
    try:
        select_ticker_name = browser.find_element("xpath", 
            f"""//*[@id="main"]/div/section[2]/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div/div[1]/div/div/table/tbody/tr[{x}]/td[1]""")
        select_ticker_name = select_ticker_name.text
        select.append(select_ticker_name)
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------#
#defining the empty lists for all the data to be placed into
main_ticker_names = []
main_dates = []
main_times = []
main_summaries = []
main_full_summary = []

select_ticker_names = []
select_dates = []
select_times = []
select_summaries = []
select_full_summary = []
p = 0

#pre-setting the while loop to true
runUserCode = True
while runUserCode:
    #for loop which cycles through the pages of the website
    for x in range(1,4000):
        browser.get(f"https://www.jamstockex.com/news/page/{x}/")
        p += 1
        #there are 10 articles on each page therfore the range is 1,11
        for x in range(1,11): 
            
        #scraping the ticker names
            ticker_name = browser.find_element("xpath",
                f"""//*[@id="content"]/div/div/section[2]/div/div[1]/div/div/div/div[1]/article[{x}]/div/h3""")
            ticker_name = ticker_name.text
            
            #scraping the date of each article
            date = browser.find_element("xpath",
                f"""//*[@id="content"]/div/div/section[2]/div/div[1]/div/div/div/div[1]/article[{x}]/div/div[1]/span[1]""")
            date = date.text
            
            #scraping the times
            time = browser.find_element("xpath",
                f"""//*[@id="content"]/div/div/section[2]/div/div[1]/div/div/div/div[1]/article[{x}]/div/div[1]/span[2]""")
            time = time.text
            
            #scraping the summary 
            try:
                article_summary = browser.find_element("xpath",
                f"""//*[@id="content"]/div/div/section[2]/div/div[1]/div/div/div/div[1]/article[{x}]/div/div[2]/p""")
                article_summary = article_summary.text
            #in the case that no summary exists for that article, an empty space is entered into the list
            except:
                article_summary = ' '
            
            #clicking the article to scrape the full summary 
            full_summary_page = browser.find_element("xpath",
                f"""//*[@id="content"]/div/div/section[2]/div/div[1]/div/div/div/div[1]/article[{x}]/div/h3/a""")
            full_summary_page.click()

            full_summary = browser.find_element_by_xpath('''//*[@id="main"]/div/section[2]/div/div[1]/div''')
            full_summary = full_summary.text

            if "Click here to open document" in full_summary:
                elems = browser.find_elements_by_xpath('//*[@id="main"]/div/section[2]/div/div[1]/div/div[2]/div/p/a')
                for elem in elems:
                    full_article = elem.get_attribute("href")
                    
            elif "Click here to open document" not in full_summary:
                full_article = full_summary 
            
            else:
                full_summary = ''

            browser.get(f"https://www.jamstockex.com/news/page/{p}/")  
            runUserCode = False               

                
            temporary_dates = []
            temporary_dates = date.split()
            year = int(temporary_dates[2])
            ticker_name = ticker(ticker_name)
                        
            if ticker_name in select and year >= 2010:
                select_ticker_names.append(ticker_name)
                select_dates.append(date)
                select_times.append(time)
                select_summaries.append(article_summary)
                select_full_summary.append(full_article)
                cursor.execute(f"INSERT INTO jse_select (tickerName, newsDate, newsTime, newsSummary, fullArticle) VALUES ('{ticker_name}', '{date}', '{time}', '{article_summary}', '{full_article}')")
                conn.commit()

                main_ticker_names.append(ticker_name)
                main_dates.append(date)
                main_times.append(time)
                main_summaries.append(article_summary)
                main_full_summary.append(full_article)
                cursor.execute(f"INSERT INTO jse_main (tickerName, newsDate, newsTime, newsSummary, fullArticle) VALUES ('{ticker_name}', '{date}', '{time}', '{article_summary}', '{full_article}')")
                conn.commit()
                
            elif ticker_name in main and year >= 2010:
                main_ticker_names.append(ticker_name)
                main_dates.append(date)
                main_times.append(time)
                main_summaries.append(article_summary)
                main_full_summary.append(full_article)
                cursor.execute(f"INSERT INTO jse_main (tickerName, newsDate, newsTime, newsSummary, fullArticle) VALUES ('{ticker_name}', '{date}', '{time}', '{article_summary}', '{full_article}')")
                conn.commit()
                
            elif year < 2010:
                runUserCode = False     
    runUserCode = False



fullJseMain = cursor.execute("SELECT * FROM jse_main")
fullJseMain = cursor.fetchall()

fullJseSelect = cursor.execute("SELECT * FROM jse_select")
fullJseSelect = cursor.fetchall()


print(fullJseMain)
print(fullJseSelect)

