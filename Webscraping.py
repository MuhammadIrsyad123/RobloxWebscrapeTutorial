import requests
import json
import shutil
from bs4 import BeautifulSoup

pages = 58
store = []
keys = ["Bank Name","City","State","Cert","Acquiring Institution","Closing Date","Fund"]

for page in range(pages):

    url = f"https://www.fdic.gov/bank-failures/failed-bank-list?page={page}"
    response = requests.get(url)
    html_source = response.text
    soup = BeautifulSoup(html_source,"html.parser")

    table = soup.find("table", class_ = "usa-table cols-7 sticky-enabled")
    tbody = table.find("tbody")
    tr = tbody.find_all("tr") 

    for row in tr:

        td = row.find_all("td")
        data = [i.text.strip() for i in td]
        store.append(dict(zip(keys,data)))
    
else:

    file = json.dumps(store,indent = 7)
    filetxt = "data.txt"
    filejson = "data.json"

    with open(filetxt,"wt") as handler:
        handler.write(file)

    shutil.copyfile(filetxt,filejson)
