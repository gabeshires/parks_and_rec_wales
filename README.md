# parks_and_rec_wales
Simple scraper to get jobs from South Wales local governments. Currently to run it's a manual .py file with a search term specified at the start. I have a few things in mind to improve it. I've scheduled so it sends an email weekly to myself with job updates. To run this there needs to be an email and password txt file in same file as .py.
- [ ] Changing it to a class so it can be imported and ran in seperate script
- [ ] Adding in more South Wales local governments 
- [ ] Generalising the output all sites can be seen in one place (csv or other)
- [ ] Add in functionality to search through multiple pages


```python
from JobScraper import job_scraper

scraper = job_scraper('Analyst')

scraper.scrape()

scraper.send()
```
