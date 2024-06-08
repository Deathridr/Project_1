import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome()


base_url = 'https://pib.gov.in/Allrel.aspx'


def scrape_articles(start_date, end_date):
    driver.get(base_url)
    
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    all_articles = []
    
    
    for single_date in pd.date_range(start=start_date, end=end_date):
        day = single_date.day
        month = single_date.month
        year = single_date.year
        
        
        Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlday')).select_by_value(str(day))
        Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlMonth')).select_by_value(str(month))
        Select(driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlYear')).select_by_value(str(year))
        
        
        time.sleep(2)  
        
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            
            for article in soup.select('.content-area ul li'):
                headline_tag = article.select_one('h3.font104')
                link_tag = article.select_one('a')
                date_text = single_date.strftime('%d/%m/%Y')  
                
                if headline_tag and link_tag:
                    headline = headline_tag.text.strip()
                    link = link_tag['href']
                    content = link_tag['title']
                    
                    all_articles.append({
                        'Date': date_text,
                        'Headline': headline,
                        'Content': content,
                        'Link': link,
                    })
            
            
            next_page = driver.find_elements(By.LINK_TEXT, 'Next')
            if next_page:
                next_page[0].click()
                time.sleep(2)  
            else:
                break
    
    return all_articles


start_date = '2024-01-01'
end_date = '2024-03-31'


articles = scrape_articles(start_date, end_date)

df = pd.DataFrame(articles)
df.to_excel('articles_jan_mar_2024.xlsx', index=False)
print("Articles saved to articles_jan_mar_2024.xlsx")


driver.quit()
