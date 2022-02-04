
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import os
import pathlib

# Reading logins
# passphrase read from file given as sys arg
decrypt = "gpg --batch --no-tty --passphrase-file '" + sys.argv[1] + "' " + os.path.join(os.path.dirname(__file__),'login.txt.gpg')
os.system(decrypt)

# Reading logins
logins = []
with open(os.path.join(os.path.dirname(__file__),'login.txt'), 'r') as flux:
    for line in flux.readlines():
        logins.append(line.split(':')[-1].replace('\n',''))


# Removing decrypted logins
os.system('rm ' + os.path.join(os.path.dirname(__file__),'login.txt'))
  
options = Options()
  
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
prefs = {"download.default_directory":os.path.dirname(__file__)}
options.add_experimental_option("prefs", prefs)
  
driver = webdriver.Chrome(options=options)
  
driver.get('https://vtmob.uphf.fr/esup-vtclient-up4/stylesheets/desktop/welcome.xhtml')

identifiant = '//*[@id="username"]'
mdp = '//*[@id="password"]'
connexion = '//*[@id="login"]/div[3]/input[6]'
calendrier = '//*[@id="j_id12"]/a[3]/img'

driver.find_element_by_xpath(identifiant).send_keys(logins[0])
driver.find_element_by_xpath(mdp).send_keys(logins[1])
driver.find_element_by_xpath(connexion).click()
driver.find_element_by_xpath(calendrier).click()
  
# close driver after our manipulations
driver.close()

path = str(os.path.join(os.path.dirname(__file__)))
for file in os.listdir(path):
    if file.endswith('.ics') or file.endswith('.ics.crdownload'):
        os.system('mv ' + os.path.join(path, file) + ' /var/www/clarenceclaux.fr/public_html/calendar.ics')