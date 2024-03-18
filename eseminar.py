from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyodbc


# Create a new instance of the WebDriver

driver = webdriver.Chrome(executable_path=r"E:\Chrome Driver\chromedriver.exe")

driver.maximize_window()

driver.get("https://eseminar.tv/webinars?refresh=1")


WB = []

L  = True

while L:

    time.sleep(4)
        
    webinarSection = driver.find_element(By.CSS_SELECTOR,".row-webinar-list")

    webinarsTitle = webinarSection.find_elements(By.CSS_SELECTOR,".webinarCard-title")

    webinarsCover = webinarSection.find_elements(By.CSS_SELECTOR,".webinarCard-title")


    for i in range(len(webinarsTitle)):
        

        try: 


            try:
                webinarsTitle[i].click()
            except:
                webinarsCover[i].click()

            time.sleep(2)

            driver.switch_to.window(driver.window_handles[1])

            T = []

            try:
                T.append(driver.find_element(By.CSS_SELECTOR, ".es__webinarContent-hd-item h3").text)
            except:
                T.append('')    
                
            try:
                T.append(driver.find_element(By.CSS_SELECTOR, ".es__webinarDetail-holder").text)
            except:
                T.append('')

            try:
                T.append(driver.find_element(By.CSS_SELECTOR, "td.es__webinarContent-meetingDate").text)
            except:
                T.append('')

            try:
                T.append(driver.find_element(By.CSS_SELECTOR,".es__webinarContent-cover img").get_attribute('src'))
            except:
                T.append('')

            try:
                T.append(driver.find_element(By.CSS_SELECTOR,".es__webinarContent-teacher h6").text)
            except:
                T.append('')

            try:
                T.append(driver.find_element(By.CSS_SELECTOR,".es__webinarContent-teacher img").get_attribute('src'))
            except:
                T.append('')

            WB.append(T)

            driver.close()

            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
    
    
    try:
        nextPage = driver.find_element(By.CSS_SELECTOR, ".es__icon-back")
        nextPage.click()
    except:
        break

    


# print(WB)


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=localhost;'
                        'DATABASE=Eseminar_1;'
                        'Trusted_Connection=yes;')

cur = conn.cursor()

for i in range(len(WB)):

    cur.execute("""INSERT INTO dbo.Webinars VALUES (?, ?, ?, ?, ?, ?);""", (WB[i][0],WB[i][1],WB[i][2],WB[i][3],WB[i][4],WB[i][5]))


conn.commit()

cur.close()