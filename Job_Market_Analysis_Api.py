from flask import Flask
from flask import jsonify
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import urllib, requests, re, pandas as pd
import simplejson as json
import regex

app = Flask(__name__)

@app.route("/crimeData")
def crimeData():
    crimePage = requests.get("https://www.worldatlas.com/articles/most-dangerous-cities-in-canada.html")
    crimeData = BeautifulSoup(crimePage.text, 'html.parser')
    table = crimeData.find("table")
    output_row = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        for column in columns:
            output_row.append(column.text)
    # Initialize a Crime Data JSON
    return jsonify({'crimeData':output_row})

@app.route("/flaskJobs/<query>/<location>")
def jobDetails(query,location):
    """
    Parameters:
        query: Indeed query keyword such as 'Data Scientist'
        num_pages: Number of search results needed
        location: location to search for
    Returns:
        Json of Job Data
    """
    # Convert the queried title to Indeed format
    query = '+'.join(query.lower().split())
    jsonData = get_data(query, 3, location)
    return jsonData

def get_data(query, num_pages, location):
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
    crimePage = requests.get("https://www.worldatlas.com/articles/most-dangerous-cities-in-canada.html")
    crimeData = BeautifulSoup(crimePage.text, 'html.parser')
    table = crimeData.find("table")
    
    #output_rows = []
    output_row = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        
        for column in columns:
            output_row.append(column.text)
            print(column.text)
            print("*****************")
            #output_rows.append(output_row)
    dangerousCity = False
    if location in output_row:
        dangerousCity = True
        print("in City")
    
    print(dangerousCity)
    for page in range(1,3):
        page = (page-1) * 10  
        # get full url 
        url = "%s%s%s%d" % (base_url, sort_by, start_from, page) 
        # Open the Url
        source = urllib.request.urlopen(url).read()
        # Create Empty Json Object
        jobList = []
        soup1 = BeautifulSoup(source,'lxml')
        for div2 in soup1.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result'):
            job_title_div = div2.find(class_='title')
            job_location_div = div2.find(class_='location accessible-contrast-color-location')
            job_desc_div = div2.find(class_="summary")
            # Job Title
            job_title = job_title_div.find('a').text
            # Job Address
            job_location = job_location_div.text
            # Job Description
            job_desc = job_desc_div.text
            # Job Link
            job_link = job_title_div.find('a').get('href')
            geolocator = Nominatim(user_agent="your Google Key...")
            location = geolocator.geocode(job_location)
            lng = location.longitude
            lat = location.latitude
            print("Success!")
            # Returns False as x is False 
            x = False
            jobDetails = {'safeCity':dangerousCity,'lng':lng,'lat':lat,'jobs':job_title,'url':'https://ca.indeed.com/'+job_link,'desc':job_desc,'address':job_location,'crimeData':output_row,'open':bool(x) }
            jobList.append(jobDetails)
            # convert to json data
            jsonStr = json.dumps(jobList)
    return jsonify(Jobs=jsonStr)

# If script is run directly, we'll take input from the user
if __name__ == "__main__":
    app.run(port=5002)
