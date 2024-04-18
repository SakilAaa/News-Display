from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os, pymysql
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'admin'
DBNAME = 'sys'
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
Options().add_argument("log-level=3")

db = pymysql.connect(host=DBHOST,user=DBUSER, password=DBPASS, database=DBNAME)
cur = db.cursor()
sqlQuery = 'SELECT * FROM sheet'
col = cur.execute(sqlQuery)
results = cur.fetchall()
driver = webdriver.Chrome()
for row in results:
    url = row[1]
    driver.get(url)
    try:
        keywords = driver.find_element(By.ID, 'keywords').get_attribute('data-wbkey')
        cur.execute("UPDATE sheet\nSET keyword = \"%s\"\nWHERE url = \"%s\"" % (keywords, url))
    except:
        pass
    try:
        src = driver.find_element(By.XPATH, '//*[@id="top_bar"]/div/div[2]').find_element(By.CSS_SELECTOR, "[target = '_blank']").text
        cur.execute("UPDATE sheet\nSET source = \"%s\"\nWHERE url = \"%s\"" % (src, url))
    except:
        pass
    body = driver.find_element(By.ID, 'artibody')
    query = "UPDATE sheet\nSET body = \"\"%s\"\"\nWHERE url = \"%s\"" % (body.text, url)
    cur.execute(query)
    try:
        pics_raw = body.find_elements(By.CLASS_NAME, 'img_wrapper')
        pics = [i.find_element(By.XPATH, './img').get_attribute('src') for i in pics_raw]
        cur.execute("UPDATE sheet\nSET pic = \"%s\"\nWHERE url = \"%s\"" % (str(pics), url))
    except:
        pass
    db.commit()

driver.close()
cur.close()
db.close()