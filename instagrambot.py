from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from credentials import username,password
#from juliramoss1_followers import followers
from example_users import followers
from filewrite import write_to_file
#from dontsleep import *
import time

class InstagramBot:
    INSTAGRAM_ROOT_PAGE = 'https://www.instagram.com/'
    ROOT_PAGE_WAIT = 0.7

    def __init__(self) -> None:
        self.driver = webdriver.Chrome('chromedriver/chromedriver')

    
    def login (self):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)

        sleep(self.ROOT_PAGE_WAIT)

        uname_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        uname_btn.send_keys(username)
        pwd_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        pwd_btn.send_keys(password)
        login_btn2 = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login_btn2.click()

        try:
            #Avoid pop-up 1
            sleep(3.5)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        except:
            pass
        try:
            #Avoid pop-up 2 (notifications enabling)
            sleep(self.ROOT_PAGE_WAIT)
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except:
            pass
    
    
    def get_fst_photo (self,who):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE + who)
        sleep(self.ROOT_PAGE_WAIT)
        try:
            self.driver.find_element_by_class_name('_9AhH0').click()
            return self.driver.current_url
        except:
            print("Couldnt find photo")
            return None


    def comment (self,message,url,post,option=False):
        if option:
            if post != self.driver.current_url:
                self.driver.get(post)
                sleep(1)
        else:
            self.driver.get(url)
            sleep(1)
            post.click()

        sleep(self.ROOT_PAGE_WAIT)

        #comment area
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.click()
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.send_keys(message)
        comment_area = self.driver.find_element_by_class_name('Ypffh')
        comment_area.send_keys(Keys.ENTER)


    def autocomment (self,shortlist,n,url,post,filename=None):
        #TODO investigate how can i make an import from a variable
        #from filename import followers
        self.driver.get(post)
        message = ""
        user = 0
        for _ in range (n):
            message = ""
            for j in range (shortlist):
                message += '@' + followers[user+j] + ' '
            user += 3
            try:
                self.comment(message,url,post,True)
                #3 bc otherwise instagram blocks u
                sleep(3)
            except:
                continue
            

    #TODO after 10 times aprox stops liking, just scrolls
    def scroll_and_like(self,wh):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)
        sleep(self.ROOT_PAGE_WAIT)
        action_chain = webdriver.ActionChains(self.driver)
        liked = []
        for _ in range (wh):
            try:
                for like in self.driver.find_elements(By.CLASS_NAME,"fr66n"):
                    if (like.get_attribute('height') != 16 and like not in liked
                        and like.get_attribute('type') != 'button'):
                        like.click()
                        liked.append(like)
                action_chain.key_down(Keys.ARROW_DOWN).perform()
            except:
                action_chain.key_down(Keys.ARROW_DOWN).perform()
    

    def autoscroll (self,time):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE)
        sleep(self.ROOT_PAGE_WAIT)
        actions = webdriver.ActionChains(self.driver)
        for i in range (time):
            if (i % 10 == 0):
                sleep(3)
            actions.key_down(Keys.ARROW_DOWN).perform()
                
            
    def username_cleanse (self,uname):
        uname = uname.replace(self.INSTAGRAM_ROOT_PAGE,'')
        uname = uname.replace('/','')
        return uname


    def get_followers (self,who,dontsleep=True):
        self.driver.get(self.INSTAGRAM_ROOT_PAGE + who)
        sleep(self.ROOT_PAGE_WAIT)
        #if dontsleep:
         #   dont()
        n_of_followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
        try:
            N_OF_FOLLOWERS = int(n_of_followers.get_attribute('title'))
        #If the profile has > 1000 followers, the number becomes '1,xxx', and
        #this is not a float for python
        except ValueError:
            N_OF_FOLLOWERS = int(n_of_followers.get_attribute('title').replace(',',''))

        print(N_OF_FOLLOWERS)
        followers_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers_btn.click()
        sleep(1)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        followers = []
        slider = self.driver.find_element_by_class_name('isgrP')
        exceptions = 0
        i = 0
        #                       This is because this tool is imprecise so 
        #                       it would never end
        while(len(followers) <= N_OF_FOLLOWERS-5 and i < N_OF_FOLLOWERS/2):
            i += 1
            print(len(followers))
            try:
                for user in followersList.find_elements_by_css_selector('li'):
                    userLink = user.find_element_by_css_selector('a').get_attribute('href')
                    clean_uname = self.username_cleanse(userLink)
                    if clean_uname not in followers:
                        followers.append(clean_uname)

                slider.click()
                actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                sleep(0.2)
    
            except:
                exceptions += 1
                actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

        #if dontsleep:
         #   do()

        return followers


    def clean (self):
        self.driver.close()



def main ():
    bot = InstagramBot()

    bot.login()

    #bot.comment('xd',bot.INSTAGRAM_ROOT_PAGE+'echeketere',bot.get_fst_photo('echeketere'),True)

    #bot.scroll_and_like(50)

    #bot.autoscroll(500)

    start = time.time()
    uname = 'facu_percerra'
    res = bot.get_followers(uname)
    end = time.time()
    write_to_file(res,username=uname)
    print(f"Got {len(res)} followers in {end-start} seconds")

    #bot.autocomment(3,10,'',bot.get_fst_photo('echeketere'))

    sleep(2)
    bot.clean()


if __name__ == '__main__':
    main()
