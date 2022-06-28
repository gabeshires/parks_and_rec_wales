"""
Created on Fri Jun 24 10:50:25 2022

@author: gabeshires
"""
   
from JobScraper import job_scraper

scraper = job_scraper('Data scientist')

scraper.scrape()

scraper.send()

