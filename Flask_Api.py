from flask import Flask
from flask_jsonpify import jsonify
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import simplejson as json
import regex
app = Flask(__name__)


@app.route("/crimeData")
def crimeData():
    crimePage = requests.get("https://www.worldatlas.com/articles/most-dangerous-cities-in-canada.html")
    crimeData = BeautifulSoup(crimePage.text, 'html.parser')
    table = crimeData.find("table")
    
    #output_rows = []
    output_row = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        
        for column in columns:
            output_row.append(column.text)
            #print(column.text)
            
            #print("*****************")
            #output_rows.append(output_row)
    # Initialize a employee list JSON
    return jsonify({'crimeData':output_row})


@app.route("/")
def jobDetails():
    #Author Rajwinder
    # Collect and parse first page
    page = requests.get('https://ca.indeed.com/jobs?q=software&l=Windsor%2C+ON')
    crimePage = requests.get("https://www.worldatlas.com/articles/most-dangerous-cities-in-canada.html")
    crimeData = BeautifulSoup(crimePage.text, 'html.parser')
    table = crimeData.find("table")
    
    #output_rows = []
    output_row = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        
        for column in columns:
            output_row.append(column.text)
            #print(column.text)
            
            #print("*****************")
            #output_rows.append(output_row)

    dangerousCity = False
    if "Windsor" in output_row:
        dangerousCity = True
        print("in City")
    
    print(dangerousCity)
    soup = BeautifulSoup(page.text, 'html.parser')

    #Author Rajwinder# Pull all text from the BodyText div
    job_div = soup.find(class_='sjcl')
    job_title_div = soup.find(class_='title')
    job_desc_div = soup.find(class_="summary")
    job_desc = job_desc_div.text
    job_location_div = soup.find(class_='location accessible-contrast-color-location')
    job_title = job_title_div.find('a').text
    job_link = job_title_div.find('a').get('href')
    company_name = job_div.find('div').text
    job_location = job_location_div.text
    geolocator = Nominatim(user_agent="your Google Key...")
    location = geolocator.geocode(job_location)
    lng = location.longitude
    lat = location.latitude

    # print job details
    print(output_row)
    print('JOB TITLE --- '+job_title)
    print('COMPANY NAME --- '+company_name)
    print('JOB LOCATION--- '+job_location)
    print(lng)
    print(lat)
    print('JOB LINK --- '+job_link)
    print('JOB DESC --- '+job_desc)
    print("Success!")
    # Returns False as x is False 
    x = False
    
    # Initialize a employee list JSON
    return jsonify({'safeCity':dangerousCity,'lng':lng,'lat':lat,'jobs':job_title,'url':'https://ca.indeed.com/'+job_link,'desc':job_desc,'address':job_location,'crimeData':output_row,'open':bool(x)})



if __name__ == '__main__':
     app.run(port=5002)