from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
from time import sleep
from credentials import username,password

class InstagramBot:
    URL = 'https://www.instagram.com'

    ch_options = Options()
    #ch_options.add_argument('--eager')
    ch_options.page_load_strategy = 'eager'

    def __init__(self) -> None:
        self.driver = webdriver.Chrome('chromedriver/chromedriver',options=self.ch_options)

    
    def login (self):
        self.driver.get(url=self.URL)

        sleep(1)

        uname_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        #uname_btn.click()
        uname_btn.send_keys(username)
        pwd_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        pwd_btn.click()
        pwd_btn.send_keys(password)
        login_btn2 = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login_btn2.click()

        #Avoid pop-up 1
        sleep(3.5)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()

        #Avoid pop-up 2 (notifications enabling)
        sleep(0.6)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    

    def go_to_profile(self):
        self.driver.get(url='https://www.instagram.com')
        sleep(1)
        #self.driver.find_element_by_xpath('//*[@id="f28a898725cda34"]/div/div/a').click()
        self.driver.find_element_by_xpath('//*[@id="f481cd16025e5"]/div/div/div').click()


    def go_to_someones_profile (self,who):
        self.driver.get(url='https://www.instagram.com')
        sleep(1)
        wait = WebDriverWait(self.driver,2)
        search = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys(who)
        res = wait.until(presence_of_element_located((By.CLASS_NAME,"Fy4o8")))
        res.click()
    

    def comment_fst_ph (self,message,url):
        self.driver.get(url)
        sleep(1)
        #last_ph = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[4]/article/div[1]/div/div[1]/div[2]/a')
        last_ph = self.driver.find_element_by_class_name('_9AhH0')
        last_ph.click()
        sleep(0.7)
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.click()
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.send_keys(message)
        comment_area.send_keys(Keys.ENTER)


    def scroll_and_like(self):
        self.driver.get(self.URL)
        sleep(1)
        for _ in range (50):
            likes = self.driver.find_elements(By.CLASS_NAME,"fr66n")
            for like in likes:
                if like.get_attribute('height') != 16:
                    like.click()

            for _ in range (50):
                webdriver.ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
    

    def autoscroll (self,time):
        self.driver.get(self.URL)
        sleep(0.5)
        for i in range (time):
            if (i % 10 == 0):
                sleep(1)
            webdriver.ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
        


bot = InstagramBot()

browser = bot.driver

browser.get(bot.URL)

sleep(1)

bot.login()

sleep(0.5)

#bot.go_to_profile()
#bot.go_to_someones_profile('joacoto')

#sleep(1)

#bot.comment_fst_ph('Dragon blanco de ojos azules',"https://www.instagram.com/joaco_torres1/")

#bot.scroll_and_like()

bot.autoscroll(500)