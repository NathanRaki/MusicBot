import os
import time
import random
import methods as nm
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class User():
    
    def __init__(self, cred, tracks):
        self.streams = 0
        self.incognito_ext = nm.incognito_ext()
        self.proxy_ext = nm.proxy_ext(cred)
        self.working_hours = nm.get_working_hours(13,17,18)
        self.starting_hour = nm.randrange_float(6, 8, 0.25)
        working = nm.working(self.working_hours, self.starting_hour)
        self.working_hours_str = working[0]
        self.working_pos = working[1]
        self.cred = cred
        self.account = self.cred[0].strip().split(':') # transforming account into a login,pwd array
        self.tracks = tracks
        self.logged = False
        self.displayed = False
        self.options = ChromeOptions()
        user_agent = nm.get_random_ua() # returns a random user agent
        self.options.add_argument(f'user-agent={user_agent}') # set webdriver user agent
        self.options.add_argument('start-maximized') # make the navigator to start maximized (avoid getting detected by letting basic dimension)
        self.options.add_extension(self.incognito_ext)
        self.options.add_extension(self.proxy_ext)
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.d = DesiredCapabilities.CHROME
        self.d['goog:loggingPrefs'] = {'browser':'ALL'} # to log all possible informations (for browser console log)
        print(os.getcwd())
        self.driver = webdriver.Chrome(executable_path='.\\chromedriver.exe', options=self.options, desired_capabilities=self.d) # creating a chrome webdriver with the modified chromedriver
        self.driver.set_page_load_timeout(60) # if the page takes more than 30 seconds to load, it raises an exception
        self.logs = []
    
    def close_browser(self):
        self.driver.quit()
        
    def get_random_track(self):
        return self.tracks[random.randint(0, len(self.tracks)-1)]
    
    def get_wh(self):
        return self.working_hours

    def get_streams(self):
        return self.streams

    def get_logs(self):
        logs = self.logs.copy()
        self.logs = []
        return logs

    def display(self):
        if self.is_working():
            status = 'At Work'
        else:
            status = 'Idle'
        self.logs.append('\n%s\n\tWorking Hours: %s\n\tStatus: %s' % (self.account[0], str(self.working_hours_str).strip('[]'), status))
        if status == 'Idle':
            self.logs.append('\n\tNext working period: %s\n' % self.working_hours_str[int(self.working_pos+1)])
        elif status == 'At Work':
            self.logs.append('\n\tListening to next song...\n')

    def is_working(self):
        work = nm.working(self.working_hours, self.starting_hour)
        self.working_pos = work[1]
        return work[2]

    def click_on_out_of_DOM(self, xpath, driverWait):
        stale = True
        while stale:
            try:
                driverWait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                stale = False
            except StaleElementReferenceException:
                stale = True
        time.sleep(5)
        
    def test_incognito(self):
        url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.driver.get(url)
        
    def test_ip(self):
        try:
            url = 'https://www.whatismyproxy.com/'
            self.driver.get(url)
        except Exception as e:
            print(type(e),' : ',e)
        
    def stream(self):
        driverWait = WebDriverWait(self.driver, 20)
        if not self.logged:
            url = nm.url_to_utf8(self.get_random_track())
            self.driver.get(url) # get a random track to play from the list
             # defines the time the bot will wait for a WebElement to be available
            actions = ActionChains(self.driver) # instantiates a chain of actions
            email = driverWait.until(EC.presence_of_element_located((By.ID, 'username'))) # find the email input on the page
            password = driverWait.until(EC.presence_of_element_located((By.ID, 'password'))) # find the password input on the page
            for char in self.account[0]: # for each character in the login
                email.send_keys(char) # send the corresponding key to the <input>
                time.sleep(random.random()/2.0) # wait a random time to seem human
            for char in self.account[1]: # for each character is the password
                password.send_keys(char) # send the corresponding key to the <input>
                time.sleep(random.random()/2.0) # wait a random time to seem human
            time.sleep(5) # wait x seconds
            submit = driverWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'signin'))) # find the submit element on the page
            actions.move_to_element(submit).click().perform() # stack actions and perform them
            self.logged = True
        else:
            url = self.get_random_track()
            self.driver.get(url)
        
        try:
            self.click_on_out_of_DOM('//a[@class="play-button icon-play-button"]', driverWait)
            #self.click_on_out_of_DOM('//div[contains(@class, "repeat-button")]', driverWait)
            #self.click_on_out_of_DOM('//div[contains(@class, "repeat-button")]', driverWait)
            songname = driverWait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="album-tracks"]//div[@class="name"]/a'))).text
            artistname = driverWait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="album-page-body"]//div[@class="album-page-header-small"]/a'))).text
            duration = driverWait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="duration-options-container"]/div[@class="duration"]'))).text
            self.logs.append('\n%s  //  %s - %s  =>  %s\n' % (self.account[0], songname, artistname, duration))
            infos = duration.strip().split(':')
            minutes = infos[0]
            seconds = infos[1]
            waitingTime = int(minutes)*60 + int(seconds)
            for i in range(waitingTime):
                time.sleep(1)
                if i > 45:
                    t = random.random()
                    if t < ((i-45)/2)/100:
                        break
            self.streams += 1
        except TimeoutException:
            print('{ %s } : Failed to access track page OR could not find play button.' % self.account[0])
            time.sleep(30)
            self.logged = False
            self.stream()