from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import mysql.connector
from mysql.connector import errorcode

url="http://psleci.nic.in/"

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome Beta\\Application\\chrome.exe"
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)
except:
    print("ChromeDriver Error")
x=Select(driver.find_element_by_id("ddlState"))

print(len(x.options))
state=x.options
st=[]
for i in x.options:
    st.append(i.text)

print(st)

try:
    cnx = mysql.connector.connect(user='root', password="", database='aap')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    

for i in range(1,len(x.options)):
    district=[]
    x=Select(driver.find_element_by_id("ddlState"))
    x.options[i].click()
    y=Select(driver.find_element_by_id("ddlDistrict"))
    for a in y.options:
        district.append(a.text)
    district=district[1:]
    for j in range(1,len(y.options)):
        y=Select(driver.find_element_by_id("ddlDistrict"))
        y.options[j].click()
        z=Select(driver.find_element_by_id("ddlAC"))
        ac=[]
        for a in z.options:
            ac.append(a.text)
        ac=ac[1:]
        for k in range(1,len(z.options)):
            z=Select(driver.find_element_by_id("ddlAC"))
            z.options[k].click()
            l=Select(driver.find_element_by_id("ddlPS"))
            pollst=[]
            for a in l.options:
                pollst.append(a.text)
            pollst=pollst[1:]
            for m in pollst:
                print(str(st[i]),str(district[j]),str(ac[k]),str(m))
                try:
                    cursor.execute("""insert into aap.pollst values(%s,%s,%s,%s)""", (str(st[i]),str(district[j]),str(ac[k]),str(m)))
                    cnx.commit()
                except mysql.connector.Error as err:
                    print(err)
                except:
                    print("Unknown Error")
cnx.close()



