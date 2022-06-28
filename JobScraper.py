"""
Created on Thu Jun 16 08:57:20 2022

@author: gabeshires
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib, ssl
from email.message import EmailMessage
import pandas as pd 
import io

class job_scraper:
    
    def __init__(self, search_term):
        self.search_term = search_term
        self.url_search = search_term.replace(' ', '%20')
        self.email_address = open("email.txt", "r").readline()
        self.email_password = open("password.txt", "r").readline()
        self.path_to_driver = open("path_to_driver.txt", "r").readline()
        self.simple_df = pd.DataFrame(columns=['location', 'jobs'])
        
    def scrape(self):
        """
        scrape jobs from local government websites and return as df
        """
        driver = webdriver.Chrome(self.path_to_driver)        
        urls = {
            'Cardiff': ["https://www.jobscardiffcouncil.co.uk/vacancies/?date=all&keywords={}&sort=recent&lang=en_GB".format(self.url_search),
                        '//div[@class="cs-post-title"]'],
            'VoG': ["https://www.valeofglamorgan.gov.uk/en/our_council/jobs/index.aspx?searchCriteria[0][key]=keywords&searchCriteria[0][values][]={}&searchCriteria[1][key]=JobAdlg&searchCriteria[1][values][]=UKEN&searchCriteria[2][key]=Resultsperpage&searchCriteria[2][values][]=48".format(self.url_search),
                    '//div[@class="jlist-tile-wrapper"]']
            }
        all_jobs = []
        for u in urls:
            driver.implicitly_wait(10)
            driver.get(urls[u][0])
            jobs = driver.find_elements_by_xpath(urls[u][1])
            jobs_list = [jobs[j].text.split('\n')[0] for j in range(len(jobs))]
            if len(jobs_list) > 0:
                region_df = pd.DataFrame(data=jobs_list, columns=['jobs'])
                region_df['location'] = u
            else:
                pass
            all_jobs.append(region_df)
        self.simple_df = pd.concat(all_jobs).reset_index(drop=True)
        driver.close()
        return self.simple_df
    
    def email_build(self):
        """
        gets subject and body parameters for email message
        """
        if len(self.simple_df) > 0:
            subject = "{} jobs available in {}".format\
                (self.search_term,', '.\
                 join(self.simple_df['location'].unique()))
            text = """\
            <b>Your job alert has found {} openings</b>
            """.format(len(self.simple_df))
            table = self.simple_df
        else:
            subject = "No {} jobs found this week".format(self.search_term)
            text = "Your job alert has found no openings. Consider changing \
                search term or decreasing frequency of alert"
            table = ""
        return subject, text, table
             
    
    def send(self):
        """
        sets email parameters, formats message and sends 
        """
        subject, text, table = self.email_build()
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = self.email_address
        
        if len(table) > 0:
            str_io = io.StringIO()
            table.to_html(buf=str_io)
            table_html = str_io.getvalue()

            html = """\
            <html>
                <body>
                    <p>{table_html}</p>
                </body>
            </html>
            """.format(table_html=table_html)
       
            msg.set_content(text + html, subtype='html')
        else: 
            msg.set_content(text, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.email_address, self.email_password)
            server.sendmail(
                self.email_address, self.email_address, msg.as_string()
                )
     

"""
def get_cardiff_jobs(term):

    url = "https://www.jobscardiffcouncil.co.uk/vacancies/?date=all&keywords={}&sort=recent&lang=en_GB".format(term)
    driver.implicitly_wait(10)
    driver.get(url)
    
    jobs = driver.find_elements_by_xpath('//div[@class="cs-post-title"]')
    #job_information = driver.find_elements_by_xpath('//div[@class="cs-text"]/ul')
    
    return jobs

def cardiff_response(jobs):

    job_list = [jobs[j].text for j in range(len(jobs))]
    
    if len(job_list) == 0:
        cardiff_response = "No {} jobs available in Cardiff".format(search_term)
    else:
        cardiff_response = "There are {} jobs available in Cardiff".format(search_term),\
            job_list

    return cardiff_response

def get_vog_jobs(term):

    url = "https://www.valeofglamorgan.gov.uk/en/our_council/jobs/index.aspx?searchCriteria[0][key]=keywords&searchCriteria[0][values][]={}&searchCriteria[1][key]=JobAdlg&searchCriteria[1][values][]=UKEN&searchCriteria[2][key]=Resultsperpage&searchCriteria[2][values][]=48".format(term)
    driver.implicitly_wait(10)

    driver.get(url)

    jobs = driver.find_elements_by_xpath('//div[@class="jlist-tile-wrapper"]')
    job_list = [jobs[j].text for j in range(len(jobs))]
    return job_list

def vog_response(jobs):

    job_names = [jobs[j].text.split('\n')[0] for j in range(len(jobs))]
    salaries = [jobs[j].text.split('\n')[4] for j in range(len(jobs))]
    if len(jobs) == 0:
        vog_response = "No {} jobs available in VoG".format(search_term)
    else:
        vog_response = "There are {} jobs available in VoG".format(search_term), \
            list(zip(job_names, salaries))

    return vog_response

def responses(term=search_term):

    cardiff = cardiff_response(get_cardiff_jobs(term))
    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 20)
    vog = vog_response(get_vog_jobs(term))
    return cardiff, vog

#cardiff, vog = responses()

driver.close()

def get_email():

    email = open("email.txt", "r")
    email_address = email.readline()
    return email_address

def get_password():

    password = open("password.txt", "r")
    email_password = password.readline()
    return email_password

email_address = get_email()

def email_message(subject, body):

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
        
        
        
        
str_io = io.StringIO()
scrape_output.to_html(buf=str_io)
table_html = str_io.getvalue()
print(table_html)



email_address = get_email()


msg = EmailMessage()
msg["Subject"] = "Subject: Your Title"
msg["From"] = email_address
msg["To"] = email_address

msg.set_content(text + html, subtype='html')


context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_address, get_password())
    server.sendmail(
        email_address, email_address, msg.as_string()
    )

"""
"""
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
"""




