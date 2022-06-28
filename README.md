# parks_and_rec_wales (currently work in progress)
Web scraper to get jobs from South Wales local governments based off a user specified search term. The output csv can also be sent by email user the send() function. To run, this needs 3 txt files in folder, email.txt, password.txt and path_to_driver.txt. The email and password files should be the email account details and the path_to_driver should contain a path to your selenium webdriver. Example of how to use can be seen in main.py and below:

```python
from JobScraper import job_scraper

scraper = job_scraper('Analyst')

scraper.scrape()

scraper.send()
```

I've set the main.py file to be ran weekly using crontab.


I have a few things in mind to improve it:

- [ ] add in ability to search for > 1 search term at the same time ('data scientist' insead of just 'data')
- [ ] adding in more South Wales local governments 
- [ ] adding in a second function scrape_detailed() that returns most information like salary and specific location
- [ ] add in functionality to search through multiple pages if the search returns multiply pages
- [ ] add in requirements.txt
