from flask import Flask
from flask_jsonpify import jsonify
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import urllib, requests, re, pandas as pd
import simplejson as json

app = Flask(__name__)


@app.route("/")
def hello():
    queries = ["software engineer","data scientist", "machine learning engineer", "data engineer"]
    while True: 
        query = input("Please enter the title to scrape data for: \n").lower()
        if query in queries:
            break
        else:
            print("Invalid title! Please try again.")

    while True:
        num_pages = input("Please enter the number of pages needed (integer only): \n")
        try:
            num_pages = int(num_pages)
            break
        except:
            print("Invalid number of pages! Please try again.")

    jsonData = get_data(query, num_pages, location='Canada')
    return jsonData


def get_urls(query, num_pages, location):
    #Author Rajwinder
    """
    Get all the job posting URLs resulted from a specific search.
    Parameters:
        query: job title to query
        num_pages: number of pages needed
        location: city to search in
    Returns:
        Job details in Json format
    """
    # We always need the first page
    base_url = 'https://ca.indeed.com/jobs?q={}&l={}&sort='.format(query, location)
    print(base_url)
    sort_by = 'date'          # sort by data
    start_from = '&start='    # start page number  

    for page in range(1,10):
        page = (page-1) * 10  
        # get full url 
        url = "%s%s%s%d" % (base_url, sort_by, start_from, page) 
        # Open the Url
        source = urllib.request.urlopen(url).read()
        # Create Empty Json Object
        jobList = []
        soup1 = BeautifulSoup(source,'lxml')
        for div2 in soup1.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result'):
            #job_div = div2.find(class_='sjcl')
            job_title_div = div2.find(class_='title')
            job_location_div = div2.find(class_='location accessible-contrast-color-location')
            job_title = job_title_div.find('a').text
            #company_name = job_div.find('div').text
            job_location = job_location_div.text
            geolocator = Nominatim(user_agent="your Google Key...")
            location = geolocator.geocode(job_location)
            lng = location.longitude
            lat = location.latitude
            print("Success!")
            jobDetails = {'lng':lng,'lat':lat,'jobs':job_title,'open':'false' }
            jobList.append(jobDetails)
            # convert to json data
            jsonStr = json.dumps(jobList)
    return jsonify(Jobs=jsonStr)

def get_data(query, num_pages, location='Windsor'):
    """
    Parameters:
        query: Indeed query keyword such as 'Data Scientist'
        num_pages: Number of search results needed
        location: location to search for
    Returns:
        postings_dict: Python dict including all posting data
    """
    # Convert the queried title to Indeed format
    query = '+'.join(query.lower().split())
    urls = get_urls(query, num_pages, location)
    return urls

# If script is run directly, we'll take input from the user
if __name__ == "__main__":
    app.run(port=5002)
