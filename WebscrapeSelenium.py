from bs4 import BeautifulSoup
import time, json, shutil
from selenium import webdriver
from selenium.webdriver import Chrome

url = "https://www.fdic.gov/bank-failures/failed-bank-list"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.page_load_strategy = "none"

driver = Chrome(options=options)
driver.implicitly_wait(5)

pages = 58
page_delay = 5

store = []
keys = ["Bank Name","City","State","Cert","Acquiring Institution","Closing Date","Fund"]

for page in range(pages):

    driver.get(url+f"?page={page}")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    html_source = driver.page_source
    soup = BeautifulSoup(html_source,"html.parser")
    table_data = soup.find_all("table",class_="usa-table cols-7 sticky-enabled")
    tbody = table_data[0].find("tbody")
    tr = tbody.find_all("tr")
   
    for i in tr:

        i = i.find_all("td")
        data = [j.text.strip() for j in i]
        store.append(dict(zip(keys,data)))
   
else:

    driver.close()
    
    file = json.dumps(store,indent=7)
    filetxt = "Data.txt"
    filejson = "Data.json"
    
    with open(filetxt,"wt") as handler:
        handler.write(file)
        print("done")

    shutil.copyfile(filetxt,filejson)
    print("done")