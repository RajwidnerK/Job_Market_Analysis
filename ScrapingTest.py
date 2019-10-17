import requests
from bs4 import BeautifulSoup as Soup
from geopy.geocoders import Nominatim
import urllib, requests, re, pandas as pd

# indeed.com url
base_url = 'http://www.indeed.com/jobs?q=data+scientist&jt=fulltime&sort='
sort_by = 'date'          # sort by data
start_from = '&start='    # start page number

pd.set_option('max_colwidth',500)    # to remove column limit (Otherwise, we'll lose some info)
df = pd.DataFrame()   # create a new data frame

#artist_name_list = soup.find(class_='summary')
#job_div = soup.find(class_='sjcl')
#job_title_div = soup.find(class_='title')
#job_location_div = soup.find(class_='location accessible-contrast-color-location')

for page in range(1,10): # page from 1 to 100 (last page we can scrape is 100)
    print('hii')
    page = (page-1) * 10  
    url = "%s%s%s%d" % (base_url, sort_by, start_from, page) # get full url 
    target = Soup(urllib.request.urlopen(url), "lxml") 
    targetElements = target.findAll('div', attrs={'class' : 'jobsearch-SerpJobCard unifiedRow row result'}) 
    # we're interested in each row (= each job)
    print('there')
    # trying to get each specific job information (such as company name, job title, urls, ...)
    for elem in targetElements: 
        print('yo')
       
        comp_name = elem.find('a', attrs={'class':'turnstileLink'}).text
        print(comp_name)
        job_title = elem.find('a', attrs={'class':'jobtitle'}).attrs['title']
        print(job_title)
        home_url = "http://www.indeed.com"
        job_link = "%s%s" % (home_url,elem.find('a').get('href'))
        job_addr = elem.find('span', attrs={'class':'location accessible-contrast-color-location'}).getText()
        job_posted = elem.find('span', attrs={'class': 'date'}).getText()

        comp_link_overall = elem.find('span', attrs={'itemprop':'name'}).find('a')
        if comp_link_overall != None: # if company link exists, access it. Otherwise, skip.
            comp_link_overall = "%s%s" % (home_url, comp_link_overall.attrs['href'])
        else: comp_link_overall = None

				# add a job info to our data frame
        df = df.append({'comp_name': comp_name, 'job_title': job_title, 
                        'job_link': job_link, 'job_posted': job_posted,
                        'overall_link': comp_link_overall, 'job_location': job_addr,
                        'overall_rating': None, 'wl_bal_rating': None, 
                        'benefit_rating': None, 'jsecurity_rating': None, 
                        'mgmt_rating': None, 'culture_rating': None
                       }, ignore_index=True)

df

