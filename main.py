import sys
import time
import names
import string
import random
import requests
from selenium import webdriver
from twocaptcha import TwoCaptcha
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options
from random_user_agent.params import SoftwareName, OperatingSystem

sitekey = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'
api = ''#2captcha apikey
uri = 'https://old.reddit.com/register'

#generates username and password
def generateuser(useragent):
    uri = 'https://old.reddit.com/api/v1/generate_username.json?'

    hdr = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer':'https://old.reddit.com/signup',
        'user-agent': useragent
        }
    res = requests.get(uri, headers=hdr)

    if res.status_code == 429:
        username = names.get_first_name()
        username += ''.join(str(random.randint(0,9))for i in range(random.randint(5,15)))
    
    else:
        b = res.json()
        username = random.choice(b['usernames'])
    
    passwd = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(random.randint(10,15)))

    return username, passwd

#solves captcha using 2cpatcha
def captcha(uri, sitekey, api):
    solver = TwoCaptcha(api)
    result = solver.recaptcha(sitekey=sitekey,
    url=uri)
    return result

#initializes the webdriver
def make_driver():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    useragent = user_agent_rotator.get_random_user_agent()

    options = Options()
    #options.binary_location = 'C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave.exe'
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    stealth(driver,
        languages=["en-US", "en"],
        user_agent=useragent,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver, useragent

#verify the email address
def verify_email(driver):
    driver.switch_to.window('tab2')
    time.sleep(25)

    k = 0
    while True:
        if k==5:
            print("Cannot verify email")
            driver.close()
            sys.exit()

        try:
            driver.find_element(By.XPATH, "//a[contains(text(), 'Verify your Reddit email address')]").click()
            print('got email')
            break

        except:
            time.sleep(10)
            k = k+1

    time.sleep(17)
    print("Getting links")
    iframe = driver.find_element(By.ID, 'the_message_iframe')
    driver.switch_to.frame(iframe)
    time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/a').click()

    time.sleep(15)
    driver.close()

#make account
def make_account():
    driver, useragent = make_driver()
    username, passwd = generateuser(useragent)

    driver.get("https://old.reddit.com/register")
    time.sleep(random.randint(1, 5))

    print('Entering username...')
    time.sleep(random.randint(1,5))
    driver.find_element(By.ID, 'user_reg').click()
    driver.find_element(By.ID, 'user_reg').send_keys(username)
    print(f'Using username {username}')

    print('Entering password...')
    time.sleep(random.randint(1,5))
    driver.find_element(By.ID, 'passwd_reg').click()
    driver.find_element(By.ID, 'passwd_reg').send_keys(passwd)
    print(f'Using password {passwd}')

    print('Entering 2nd password...')
    time.sleep(random.randint(2,5))
    driver.find_element(By.ID, 'passwd2_reg').click()
    driver.find_element(By.ID, 'passwd2_reg').send_keys(passwd)
    time.sleep(2)

    print("Getting email")
    driver.execute_script("window.open('about:blank', 'tab2');")
    driver.switch_to.window('tab2')
    driver.get('https://getnada.com')
    time.sleep(2)
    email = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/nav/div/div/ul[2]/li/span').text

    print(f'Got email: {email}')
    print("Entering email")
    
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(random.randint(1, 5))
    driver.find_element(By.ID, 'email_reg').send_keys(email)
    time.sleep(2)

    k = 0
    while True:
        if k ==5:
            print("Error captcha not found")
            return
        try:
            time.sleep(3)
            captchaInput = driver.find_element(By.ID, 'g-recaptcha-response')
            print("captcha found")
            driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');", captchaInput)
            break

        except:
            k += 1
            driver.find_element(By.CLASS_NAME, 'c-pull-right').click()
            time.sleep(10)
        
    print("Solving captcha")
    time.sleep(random.randint(10, 15))
    resp = captcha(uri, sitekey, api)
    print("Solved the captcha")
    captchaInput.send_keys(resp['code'])

    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'c-pull-right').click()
    print("Waiting for email")
    time.sleep(10)

    k = 0
    while True:
        if k==5:
            print("Failed to created account")
            driver.close()
            sys.exit()

        try:
            driver.find_element(By.ID, 'evb-resend-btn')
            with open('accounts.txt', 'a+') as f:
                f.write(f'{username} {passwd}\n')
            break

        except:
            time.sleep(5)
            k = k+1

    verify_email(driver)

make_account()