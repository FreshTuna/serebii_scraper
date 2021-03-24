import csv 
import time 
import re

from bs4                      import BeautifulSoup
from selenium                 import webdriver
from webdriver_manager.chrome import ChromeDriverManager

csv_filename = "serebii.csv"
csv_open     = open(csv_filename, "w+", encoding='utf-8')
csv_writer   = csv.writer(csv_open)

csv_writer.writerow( ('name','image_url','type') )

driver = webdriver.Chrome(ChromeDriverManager().install())
URL    = "https://www.serebii.net/swordshield/pokemon.shtml"

driver.get(URL)

full_html = driver.page_source
soup      = BeautifulSoup(full_html, 'html.parser')

driver.implicitly_wait(3)   

table = soup.select("#content > main > table > tbody")
print(len(table))
for p in range(3,99):
    reg     = re.compile('[a-zA-Z]')
    name_td = soup.select(f"#content > main > table > tbody > tr:nth-child({p}) > td:nth-child(3)")[0].text
    name    = ''.join(reg.findall(name_td))

    image_url_td = soup.select(f"#content > main > table > tbody > tr:nth-child({p}) > td:nth-child(2) > table > tbody > tr > td > a > img")
    image_url    = image_url_td[0]['src']

    Type_td     = soup.select(f"#content > main > table > tbody > tr:nth-child({p}) > td:nth-child(4) > a")
    Type_sliced = ''.join(re.findall(r"\/(.*?)\.",Type_td[0]['href']))
    Type        = Type_sliced[ Type_sliced.find("/")+1: ]

    csv_writer.writerow( (name, image_url, Type) )
    

