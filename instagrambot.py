from os import system
import os
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
from time import sleep
from credentials import username,password

class InstagramBot:
    INSTAGRAM_ROOT_PAGE = 'https://www.instagram.com'
    ROOT_PAGE_WAIT = 0.7
    URL = INSTAGRAM_ROOT_PAGE

    #ch_options = Options()
    #ch_options.add_argument('--eager')
    #ch_options.page_load_strategy = 'eager'

    def __init__(self) -> None:
        self.driver = webdriver.Chrome('chromedriver/chromedriver')

    
    def login (self):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)

        sleep(self.ROOT_PAGE_WAIT)

        uname_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
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
        sleep(self.ROOT_PAGE_WAIT)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    

    def go_to_profile(self):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)
        sleep(self.ROOT_PAGE_WAIT)
        self.driver.find_element_by_xpath('//*[@id="f481cd16025e5"]/div/div/div').click()


    def go_to_someones_profile (self,who):
        self.driver.get(url='https://www.instagram.com/' + who)
        sleep(1)
        wait = WebDriverWait(self.driver,2)
        search = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys(who)
        res = wait.until(presence_of_element_located((By.CLASS_NAME,"Fy4o8")))
        res.click()
    

    def get_fst_photo (self,url):
        self.driver.get(url)
        sleep(0.5)
        try:
            last_ph = self.driver.find_element_by_class_name('_9AhH0')
            return last_ph
        except:
            print("Couldnt find photo")
            return None



    def comment (self,message,url,post):
        self.driver.get(url)
        sleep(1)
        post.click()
        sleep(0.7)
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.click()
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.send_keys(message)
        comment_area.send_keys(Keys.ENTER)


    def scroll_and_like(self):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)
        sleep(self.ROOT_PAGE_WAIT)
        for _ in range (50):
            likes = self.driver.find_elements(By.CLASS_NAME,"fr66n")
            for like in likes:
                if like.get_attribute('height') != 16:
                    like.click()

            for _ in range (50):
                webdriver.ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
    

    def autoscroll (self,time):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)
        sleep(self.ROOT_PAGE_WAIT)
        for i in range (time):
            if (i % 10 == 0):
                sleep(3)
            webdriver.ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
        

    def autocomment (self,shortlist,n,filename,url,post):
        from filename import followers
        message = ""
        for i in range (n):
            for _ in range (shortlist):
                message += '@' + followers[i]
            self.comment(message,url,post)
                
            
    def username_cleanse (self,uname):
        uname = uname.replace('https://www.instagram.com/','')
        uname = uname.replace('/','')
        return uname
    

    def write_to_file (self,listt : List[str],filename=None,username=None):
        fname = ""
        i = 1
        PY = '.py'
        if filename is None:
            if username is None:
                username = 'someone`s'

            fname = username + '_followers'
            while (os.path.isfile(fname+PY)):
                fname = username + '_followers' + str(i)
                i += 1

        else:
            fname = filename
            while (os.path.isfile(fname+PY)):
                fname = filename + i
                i += 1

        fname += PY
        f = open(fname,'x')
        
        f.write('followers = ')
        f.close()
        
        f = open(fname,'a')
        f.write(listt.__str__())
        f.close()



    def get_followers (self,who):
        self.driver.get(self.URL + "/" + who)
        sleep(1)
        n_of_followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
        N_OF_FOLLOWERS = int(n_of_followers.get_attribute('title'))
        followers_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers_btn.click()
        sleep(1)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        followers = []
        slider = self.driver.find_element_by_class_name('isgrP')
        exceptions = 0
        iterations = 0
        while(len(followers) != N_OF_FOLLOWERS and exceptions < 50):
            print(iterations)
            iterations += 1
            try:
                for user in followersList.find_elements_by_css_selector('li'):
                    userLink = user.find_element_by_css_selector('a').get_attribute('href')
                    clean_uname = self.username_cleanse(userLink)
                    if clean_uname not in followers:
                        print(clean_uname)
                        followers.append(clean_uname)

            
                #slider = self.driver.find_element_by_class_name('isgrP')
                slider.click()
                actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                sleep(0.2)
                #slider.send_keys(Keys.ARROW_DOWN)
    
            except:
                exceptions += 1
                print("Lol")
                actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                continue

        return followers


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

#bot.autoscroll(500)

#bot.get_followers('juliramoss1')