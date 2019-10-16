import re
import json
import time
from bs4 import BeautifulSoup
import requests

url_template = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={}&start={}"
max_results_per_city = 1000
#Initialize empty lists to scrape results into
location=[]
company=[]
job_title=[]
salary=[]
city=[]
for city in set(['New+York', 'Chicago', 'San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh','Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+City']):
    for start in range(0, max_results_per_city, 10):
        #to keep track of progress
        URL=url_template.format(city, start)
        html=requests.get(URL)
        soup=BeautifulSoup(html.text, 'lxml')
        # Grab the results from the request (as above)
        # Append to the full set of results
        results=[]
        for _ in soup.find_all(class_='result'):
            results.append(_)
        for result in results:
            company.append(getcompany(result).encode('ascii', 'replace'))
            location.append(getlocation(result).encode('ascii', 'replace'))
            job_title.append(getjob(result).encode('ascii', 'replace'))
            salary.append(getsalary(result.prettify().encode('utf-8')))
            cit.append(city)
