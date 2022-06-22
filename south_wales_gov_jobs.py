"""
Created on Thu Jun 16 08:57:20 2022

@author: gabeshires
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib
from email.message import EmailMessage

# open browser
path_to_driver = '/Users/gabeshires/Documents/Training/web_scraping_training/chromedriver'
driver = webdriver.Chrome(path_to_driver)

# define search time used throughout and urls that are used to if any jobs are found
search_term = 'analyst'
cardiff_jobs = 'https://www.jobscardiffcouncil.co.uk/vacancies/?date=all&keywords=&sort=recent&lang=en_GB'
vog_jobs = 'https://www.valeofglamorgan.gov.uk/en/our_council/jobs/index.aspx?searchCriteria[0][key]=JobAdlg&searchCriteria[0][values][]=UKEN&searchCriteria[1][key]=Resultsperpage&searchCriteria[1][values][]=48'

def get_cardiff_jobs(term):
    """
    get jobs that contain search term from cardiff council
    """
    url = "https://www.jobscardiffcouncil.co.uk/vacancies/?date=all&keywords={}&sort=recent&lang=en_GB".format(term)
    driver.implicitly_wait(10)
    driver.get(url)
    
    jobs = driver.find_elements_by_xpath('//div[@class="cs-post-title"]')
    #job_information = driver.find_elements_by_xpath('//div[@class="cs-text"]/ul')
    
    return jobs

def cardiff_response(jobs):
    """
    generate response from job info
    """
    job_list = [jobs[j].text for j in range(len(jobs))]
    
    if len(job_list) == 0:
        cardiff_response = "No {} jobs available in Cardiff".format(search_term)
    else:
        cardiff_response = "There are {} jobs available in Cardiff".format(search_term),\
            job_list

    return cardiff_response

def get_vog_jobs(term):
    """
    get jobs that contain search term from vog council
    """
    url = "https://www.valeofglamorgan.gov.uk/en/our_council/jobs/index.aspx?searchCriteria[0][key]=keywords&searchCriteria[0][values][]={}&searchCriteria[1][key]=JobAdlg&searchCriteria[1][values][]=UKEN&searchCriteria[2][key]=Resultsperpage&searchCriteria[2][values][]=48".format(term)
    driver.get(url)

    jobs = driver.find_elements_by_xpath('//div[@class="jlist-tile-wrapper"]')
    return jobs

def vog_response(jobs):
    """
    generate response from job info 
    """
    job_names = [jobs[j].text.split('\n')[0] for j in range(len(jobs))]
    salaries = [jobs[j].text.split('\n')[4] for j in range(len(jobs))]
    if len(jobs) == 0:
        vog_response = "No {} jobs available in VoG".format(search_term)
    else:
        vog_response = "There are {} jobs available in VoG".format(search_term), \
            list(zip(job_names, salaries))

    return vog_response

def responses(term=search_term):
    """
    calls above functions to generate responses
    """
    cardiff = cardiff_response(get_cardiff_jobs(term))
    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 20)
    vog = vog_response(get_vog_jobs(term))
    return cardiff, vog

cardiff, vog = responses()

driver.close()

def get_email():
    """
    get email address from saved txt file
    """
    email = open("email.txt", "r")
    email_address = email.readline()
    return email_address

def get_password():
    """
    get password from saved txt file
    """
    password = open("password.txt", "r")
    email_password = password.readline()
    return email_password

email_address = get_email()

def email_message(subject, body):
    """
    sets email message parameters
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = email_address
    string = body
    msg.set_content(string, subtype='html')
    return msg

def send_email(msg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, get_password()) 
        smtp.send_message(msg)
        
### if statement that sounds out information depending on what's been scraped 
if type(cardiff) is str and type(vog) is str:
    send_email(email_message(cardiff + " or VoG", 'Will search again next week'))
elif type(cardiff) is not str and type(vog) is str:
    send_email(email_message(cardiff[0], "{} More information at {}"\
                             .format(cardiff[1], cardiff_jobs)))
elif type(cardiff) is str and type(vog) is not str:
    send_email(email_message(vog[0], "{} More information at {}"\
                             .format(vog[1], vog_jobs)))
elif type(cardiff) is not str and type(vog) is not str:
    send_email(email_message("{} and VoG".format(cardiff[0]), \
                             "{} More information at {} {} More information at {}"\
                                 .format(cardiff[1], cardiff_jobs,
                                         vog[1], vog_jobs)))
else:
    send_email(email_message('Types broken - come back to fix'), "")
    




